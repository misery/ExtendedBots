from __future__ import unicode_literals

from setuptools import setup

PACKAGE = "rbExtendedBots"
VERSION = "0.0.1"

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
            'regex = extended_bots.regex:RegexTool',
        ],
    },
    install_requires=[
        'reviewbot-worker>=1.0',
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
