#!/usr/bin/python

"""Generate aws client config file by traversing account in an Organization

Usage:
  awsorgconfig (-h | --help)
  awsorgconfig --version
  awsorgconfig [--mfa-token <token>] [--profile <profile>]

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


args = docopt(__doc__)
print args

config = configparser.SafeConfigParser()
config.read(os.path.expanduser('~/.aws/config'))
#print config.sections()
#for s in config.sections():
#    print s
#    print config.items(s)
#    print

if not args['--profile'] == 'default':
    try:
        print config.get("profile %s" % args['--profile'],'role_arn')
    except:
        raise
