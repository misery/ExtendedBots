from __future__ import unicode_literals

from os.path import splitext
import re

from reviewbot.tools import Tool


class RegexTool(Tool):
    """Review Bot tool to run regex."""

    name = 'regex'
    version = '1.0'
    description = 'Runs pre-defined regex on text files.'
    timeout = 30
    options = [
        {
            'name': 'regex',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'label': 'regex',
                'help_text': 'A regex per line separated optionally '
                             'by a : for a comment. '
                             'Example: TODO|FIXME:Do that!',
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
            'name': 'file_ext',
            'field_type': 'django.forms.CharField',
            'default': 'java,cpp,h,cxx,groovy,mm,m',
            'field_options': {
                'label': 'Scan files',
                'help_text': 'Comma-separated list of file extensions '
                             'to scan. Leave it empty to check any file.',
                'required': False,
            },
        },
    ]

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

        list = []
        for entry in settings['regex'].splitlines():
            s = entry.rsplit(':', 1)
            regex = s[0]
            comment = 'Forbidden token'
            if len(s) > 1:
                comment = s[1]
            list.append((re.compile(regex, re.I), comment.strip()))

        with open(path, 'r') as content:
            line_num = 0
            for line in content:
                line_num += 1
                for entry in list:
                    if entry[0].search(line):
                        f.comment('%s (used pattern "%s")' %
                                  (entry[1], entry[0].pattern), line_num)
