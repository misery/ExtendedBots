"""Review Bot tool to run typos for spell checking."""

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


class TyposExtTool(BaseTool):
    """Review Bot tool to check spelling using typos."""

    name = 'TyposExt'
    version = '1.0'
    description = (
        'Checks code and documentation for typos using the typos CLI. '
        'Fast and accurate spell checker written in Rust.'
    )
    timeout = 30
    exe_dependencies = ['typos']

    options = [
        {
            'name': 'config',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'label': 'Configuration',
                'help_text': (
                    'Complete content of a typos configuration file.'
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
    ]

    def build_base_command(self, **kwargs):
        """Build the base command line used to review files.

        Args:
            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            list of str:
            The base command line.
        """
        return ['typos', '--format', 'json', '--force-exclude', '--isolated']

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
        # Add all file paths
        file_map = {}
        for f in files:
            path = f.get_patched_file_path()
            if not path:
                continue

            file_map[path] = f

        if not file_map:
            return

        settings = self.settings
        config_content = settings.get('config', '').strip()

        # Build the command
        cmdline = self.build_base_command()
        config_file = make_tempfile(config_content.encode('utf-8'))
        cmdline.extend(['--config', config_file])
        cmdline.extend(file_map.keys())

        # Execute typos
        output = execute(
            cmdline,
            ignore_errors=True,
        )

        if not output:
            return

        # Parse JSON output
        for line in output.splitlines():
            if not line.strip():
                continue

            try:
                result = json.loads(line)
            except json.JSONDecodeError:
                logger.error('Failed to parse typos output: %s', line)
                continue

            # typos JSON format:
            # {
            #   "type": "typo",
            #   "path": "file.py",
            #   "line_num": 10,
            #   "byte_offset": 123,
            #   "typo": "teh",
            #   "corrections": ["the"]
            # }

            filename = result.get('path', '')
            typo = result.get('typo', '')
            corrections = result.get('corrections', [])

            # Build comment
            comment = f'Typo: `{typo}`'

            if corrections:
                clist = ', '.join(f'`{c}`' for c in corrections)
                comment += f'\n\nSuggested correction(s): {clist}'

            file_map.get(filename).comment(
                text=comment,
                first_line=result.get('line_num', 1),
                error_code=result.get('type'),
            )
