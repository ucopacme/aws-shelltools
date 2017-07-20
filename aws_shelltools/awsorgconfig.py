#!/usr/bin/python

"""Generate aws client config file by traversing account in an Organization

Usage:
  awsorgconfig (-h | --help)
  awsorgconfig --version
  awsorgconfig [--mfa-token <token>] [--profile <profile>]
  awsassumerole --role-name <profile> [--profile <profile>] [--config <path>]
                [--config-dir <path>]

Options:
  -r, --role-name <profile>  The config profile title identifying the
                            role to assume.  Required.
  -p, --profile <profile>   AWS credentials profile to use.  Defaults to
                            $AWS_PROFILE env var, then to 'default'.
  -f, --config <path>       Path of the aws config file.  Defaults to
                            $AWS_CONFIG_FILE, then to '~/.aws/config'.
  -d, --config-dir <path>   Directory where to look for additional aws
                            config files.  Defaults to
                            $AWS_CONFIG_DIR, then to '~/.aws/config.d/'.

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -m, --mfa-token <token>    6 digit tokencode provided by MFA device.

"""


import os
import boto3
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser



def make_org_config():
    """
    create aws config file with a profile for all accounts in org
    if no args, use [master] profile in ~/.aws/config
    if no args and no [master] profile in ~/.aws/config,
     ask for master account_id, 
     role_name for scanning accounts in master, 
     and default role_name to set in org config file.
    if one arg , use this as 'master' profile
    if 2 arg, first is 'master' profile, second is default role_name to set
    """
    return None


def get_profile(args):
    if args['--profile']:
        return args['--profile']
    if os.environ.get('AWS_PROFILE'):
        return os.environ.get('AWS_PROFILE')
    return DEFAULT_PROFILE

def main:
    args = docopt(__doc__)
    print args
    aws_profile = get_profile(args)
