from __future__ import print_function, unicode_literals

import getpass
import os
import subprocess
import sys

from distutils.util import strtobool
from six.moves import input

from rbtools.utils.filesystem import make_tempfile


def get_input(prompt):
    """Ask the user for input.

    Args:
        prompt (unicode):
            The text to prompt the user with.

    Returns:
        unicode:
        The entered user data.
    """
    # `input`'s usual prompt gets written to stdout, which results in really
    # crummy behavior if stdout is redirected to a file. Because this is often
    # paired with getpass (entering a username/password combination), we mimic
    # the behavior there, writing the prompt to stderr.
    sys.stderr.write(prompt)
    return input()


def get_pass(prompt):
    """Ask the user for a password.

    Args:
        prompt (unicode):
            The text to prompt the user with.

    Returns:
        bytes:
        The entered password.
    """
    return getpass.getpass(str(prompt))


def confirm(question):
    """Interactively prompt for a Yes/No answer.

    Accepted values (case-insensitive) depend on distutils.util.strtobool():
    'Yes' values: y, yes, t, true, on, 1
    'No' values: n, no , f, false, off, 0
    """
    while True:
        full_question = '%s [Yes/No]: ' % question
        answer = get_input(full_question).lower()
        try:
            return strtobool(answer)
        except ValueError:
            print('%s is not a valid answer.' % answer)


def edit_text(content):
    """Allows a user to edit a block of text and returns the saved result.

    The environment's default text editor is used if available, otherwise
    vi is used.
    """
    tempfile = make_tempfile(content.encode('utf8'))
    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'vi'
    try:
        subprocess.call(editor.split() + [tempfile])
    except OSError:
        print('No editor found. Set EDITOR environment variable or install '
              'vi.')
        raise

    f = open(tempfile)
    result = f.read()
    f.close()

    return result.decode('utf8')
