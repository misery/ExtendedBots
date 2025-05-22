from __future__ import unicode_literals

import chardet
from os.path import splitext

from reviewbot.tools import BaseTool


class ChardetectorTool(BaseTool):
    """Review Bot tool to run chardet."""

    name = 'chardetector'
    version = '1.0'
    description = ('Checks file encoding')
    timeout = 30
    options = [
        {
            'name': 'file_ext',
            'field_type': 'django.forms.CharField',
            'default': 'java,c,h,cpp,cxx,groovy,mm,js,cmake',
            'field_options': {
                'label': 'Check files',
                'help_text': 'Comma-separated list of file extensions'
                             ' to scan.',
                'required': True,
            },
        },
        {
            'name': 'encodings',
            'field_type': 'django.forms.CharField',
            'default': 'ascii',
            'field_options': {
                'label': 'Allowed file encoding',
                'help_text': 'Comma-separated list of allowed file'
                             ' encoding.',
                'required': True,
            },
        },
    ]

    def handle_file(self, f, settings, **kwargs):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        ext = splitext(f.dest_file)[1][1:]
        if not ext.lower() in settings['file_ext'].split(','):
            # Ignore the file.
            return

        path = f.get_patched_file_path()
        if not path:
            return

        allowed = settings['encodings'].split(',')

        with open(path, 'rb') as content:
            line_num = 0
            for line in content:
                line_num += 1
                parsed = chardet.detect(line)
                encoding = parsed.get('encoding')
                confidence = parsed.get('confidence')

                if encoding not in allowed:
                    f.comment('Encoding "%s" not allowed (confidence: %s)' %
                              (encoding, confidence), line_num)
