"""Review Bot tool to run ruff."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from reviewbot.tools.base import BaseTool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute

if TYPE_CHECKING:
    from reviewbot.processing.review import File


logger = logging.getLogger(__name__)


class RuffExtTool(BaseTool):
    """Review Bot tool to run ruff."""

    name = 'ruffExt'
    version = '1.0'
    description = 'Checks Python code for style and programming errors.'
    timeout = 30
    exe_dependencies = ['ruff']
    file_patterns = ['*.py']

    options = [
        {
            'name': 'config',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'label': 'Configuration',
                'help_text': (
                    'Complete content of a ruff.toml configuration file.'
                ),
                'required': True,
            },
            'widget': {
                'type': 'django.forms.Textarea',
                'attrs': {
                    'cols': 80,
                    'rows': 20,
                },
            },
        },
        {
            'name': 'formatting',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Check formatting',
                'help_text': (
                    'Checks if the file is formatted correctly.'
                ),
                'required': False,
            },
        },
    ]

    def handle_files(
        self,
        files: list[File],
        **kwargs,
    ) -> None:
        """Perform a review of all files.

        Args:
            files (list of reviewbot.processing.review.File):
                The files to process.

            **kwargs (dict):
                Additional keyword arguments.
        """
        file_map = {}
        for f in files:
            if not self.get_can_handle_file(f):
                continue

            path = f.get_patched_file_path()
            if not path:
                continue

            file_map[path] = f

        if not file_map:
            return

        settings = self.settings
        config_content = settings.get('config', '').strip()
        config_file = make_tempfile(config_content.encode('utf-8'))

        # Build the command
        cmdline = ['ruff', 'check', '--output-format=json']
        cmdline.extend(['--config', config_file])
        cmdline.extend(file_map.keys())

        # Execute ruff using the process utility
        output = execute(
            cmdline,
            ignore_errors=True,
        )

        # Parse JSON output
        try:
            results = json.loads(output)
        except json.JSONDecodeError:
            logger.error('Failed to parse ruff output as JSON: %s',
                         output)
            return

        # Process each result
        for result in results:
            filename = result.get('filename')
            file_obj = file_map.get(filename)

            if not file_obj:
                logger.warning(
                    'ruff reported issue for unknown file: %s',
                    filename
                )
                continue

            location = result.get('location', {})
            endlocation = result.get('end_location', {})

            line = location.get('row', 1)
            endline = endlocation.get('row', 1)

            message = result.get('message', '')
            fix = result.get('fix')
            if fix:
                fix = fix.get('message', '')
                message += f'\n\nSuggested fix available: {fix}'

            file_obj.comment(
                text=message,
                first_line=line,
                num_lines=endline - line + 1,
                start_column=location.get('column'),
                error_code=result.get('code', ''),
            )

        # Build the command for formatting
        if settings.get('formatting'):
            cmdline = ['ruff', 'format', '--check']
            cmdline.extend(file_map.keys())

            output = execute(
                cmdline,
                ignore_errors=True,
            )

            for line in output.splitlines():
                if line.startswith('Would reformat:'):
                    filename = line.split(":", 1)[1].strip()
                    file_obj = file_map.get(filename)
                    file_obj.comment(
                        first_line=0,
                        text=f'File "{file_obj.dest_file}" is not formatted.',
                        error_code='formatting',
                    )
