#!/usr/bin/env python
"""Installs all the git tooling"""

import os
from os import getcwd, makedirs, name  # pylint: disable=no-name-in-module
from os.path import dirname, exists, isdir, join, normpath
from shutil import copyfile
from subprocess import CalledProcessError, check_output
import sys

import argparse


# import pygit2  # pylint: disable=no-name-in-module

__location__ = join(getcwd(), dirname(__file__))

HOOKS_LIBRARY = join(__location__, 'hooks')
print HOOKS_LIBRARY
HOOKS_DIR = join(__location__, '.git', 'hooks')

AVAILABLE_HOOKS = ['pre-push']


def install_via_symlink(src, dest):
    """Creates a symlink uses native commands where possible"""
    if 'nt' == name:
        # Totally backwards in the docs
        # https://docs.microsoft.com/en-us/powershell/wmf/5.0/feedback_symbolic
        linker = check_output([
            'powershell',
            'New-Item',
            '-ItemType',
            'SymbolicLink',
            '-Target',
            src,
            '-Path',
            dest
        ])
        print linker
    else:
        os.symlink(src, dest)  # pylint: disable=no-member


def install_file(src, dest, force=False):
    """Selects an installation strategy and runs with it"""
    if exists(dest):
        if force:
            os.remove(dest)
        else:
            # File exists
            raise OSError('File exists')
    try:
        install_via_symlink(src, dest)
    except (CalledProcessError, AttributeError):
        copyfile(src, dest)


def install_available_hooks(hooks_dir=HOOKS_DIR, force=False):
    """Installs all the available hooks"""
    if not isdir(hooks_dir):
        makedirs(hooks_dir)
    for hook in AVAILABLE_HOOKS:
        src = normpath(join(HOOKS_LIBRARY, hook))
        dest = normpath(join(HOOKS_DIR, hook))
        install_file(src, dest, force)


def main(*args):
    """Runs the script"""
    print 'Running main'
    parser = argparse.ArgumentParser(
        description='Python tool to install and manage local git tooling'
    )
    parser.add_argument(
        '-d', '--hooks-dir',
        dest='hooks_dir',
        default=join('.git', 'hooks', 'wotw-hooks'),
        help="Use a different hook installation location"
    )
    # Might not be the best names, but it is fun to read aloud
    parsed_args = parser.parse_args(*args)
    install_available_hooks(parsed_args.hooks_dir)


if '__main__' == __name__:
    sys.exit(main(*sys.argv[1:]))
