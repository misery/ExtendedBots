from __future__ import unicode_literals

import os
from os.path import splitext

from reviewbot.tools import Tool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute, is_exe_in_path


class UncrustifyTool(Tool):
    """Review Bot tool to run formatting tool uncrustify."""

    name = 'uncrustify'
    version = '1.0'
    description = 'Checks formatting of source file.'
    timeout = 30
    options = [
        {
            'name': 'config',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'label': 'Configuration',
                'help_text': 'Content of configuration.',
                'required': True,
            },
            'widget': {
                'type': 'django.forms.Textarea',
                'attrs': {
                    'cols': 80,
                    'rows': 10,
                },
            }
        },
        {
            'name': 'max_diff_length',
            'field_type': 'django.forms.IntegerField',
            'default': 10,
            'field_options': {
                'label': 'Maximum diff length',
                'help_text': 'The maximum line length of diff output.',
                'required': True,
            },
        },
        {
            'name': 'file_ext',
            'field_type': 'django.forms.CharField',
            'default': 'java,cpp,h,c',
            'field_options': {
                'label': 'Scan files',
                'help_text': 'Comma-separated list of file extensions '
                             'to scan. Leave it empty to check any file.',
                'required': False,
            },
        },
    ]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path('uncrustify') and is_exe_in_path('diff')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        file_ext = settings['file_ext'].strip()

        if file_ext:
            ext = splitext(f.dest_file)[1][1:]

            if not ext.lower() in file_ext.split(','):
                # Ignore the file.
                return

        path = f.get_patched_file_path()

        if not path:
            return

        cfg = make_tempfile(settings['config'])
        formatted = make_tempfile()

        execute(
            [
                'uncrustify',
                '--if-changed',
                '-c', cfg,
                '-f', path,
                '-o', formatted,
            ])

        if os.path.getsize(formatted) > 0:
            diff = execute(
                [
                    'diff', '--unified=0',
                    path, formatted,
                ],
                ignore_errors=True)

            message = []
            start = None
            num = None
            max_line = int(settings['max_diff_length'])
            for line in diff.splitlines():
                if line.startswith('---') or line.startswith('+++'):
                    continue
                elif line.startswith('@@'):
                    self._comment(f, message, start, num, settings)
                    message = []
                    hunk = line.split(' ')[1].split(',')
                    start = hunk[0]
                    num = hunk[1] if len(hunk) > 1 else 1
                elif len(message) < max_line:
                    message.append(line)

            self._comment(f, message, start, num, settings)

    def _comment(self, f, message, start_line, num_lines, settings):
        if start_line and num_lines:
            msg = 'Formatting is incorrect. Run uncrustify and use:'
            if len(message) > 0:
                msg += '\n```diff\n' + '\n'.join(message) + '\n```'

            f.comment(msg, abs(int(start_line)), int(num_lines),
                      rich_text=True)
