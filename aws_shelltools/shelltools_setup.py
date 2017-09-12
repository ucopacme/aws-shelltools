#!/usr/bin/env python

""" Edit user shell profile to source shell_functions at login.


Usage:
  aws-shelltools-setup [-h | --help]

Options:
  -h, --help                Show this help message and exit.

Supported shells:
  bash


"""

import os
import pkg_resources
from docopt import docopt


def main():
    args = docopt(__doc__)
    homedir = os.environ.get('HOME')
    shell = os.path.basename(os.environ.get('SHELL'))
    filename =  os.path.abspath(pkg_resources.resource_filename(__name__,
            'shell_functions/shell_functions.%s' % shell))

    if os.name == 'posix':
        snippet = """
# aws-shelltools functions
export AWS_CONFIG_FILE='~/.aws/config'
export AWS_CONFIG_DIR='~/.aws/config.d'
[ -f %s ] && . %s
""" % (filename, filename)

        if shell == 'bash':
            profile = '/'.join([homedir, '.bashrc'])
        else:
            profile = None

        if profile and os.path.exists(profile):
            with open(profile, 'a+') as f:
                if snippet not in f.read():
                    f.write(snippet)
                

if __name__ == "__main__":
    main()
