from __future__ import unicode_literals

from setuptools import setup

PACKAGE = "rbExtendedBots"
VERSION = "0.0.3"

setup(
    name=PACKAGE,
    version=VERSION,
    license='MIT',
    description='Just another Review Bots',
    long_description='Additional tools and checker for Review Bot',
    author='Andre Klitzing',
    author_email='aklitzing@gmail.com',
    url='https://github.com/misery/ExtendedBots',
    packages=[str('extended_bots')],
    entry_points={
        'reviewbot.tools': [
            'chardetector = extended_bots.chardetector:ChardetectorTool',
            'regex = extended_bots.regex:RegexTool',
            'uncrustify = extended_bots.uncrustify:UncrustifyTool',
        ],
    },
    install_requires=[
        'chardet>=2.3.0',
        'reviewbot-worker>=3.0',
        'RBTools>=1.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Review Board',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
