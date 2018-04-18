#!/usr/bin/env python

"""Generate aws client config file by listing group assume role policies.

Usage:
  aws-make-config (-h | --help)
  aws-make-config [--profile <profile>] [--config <path>] [--config-dir <path>]

Options:
  -p, --profile <profile>   AWS credentials profile to use.  Defaults to
                            $AWS_PROFILE env var, then to 'default'.
  -f, --config <path>       Path of the aws config file to create.  Defaults
                            to $AWS_CONFIG_FILE, then to '~/.aws/config'.
  -d, --config-dir <path>   Directory where to create aws
                            config files.  Defaults to
                            $AWS_CONFIG_DIR, then to '~/.aws/config.d/'.
  -h, --help                Show this help message and exit.

"""


import os
import boto3
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from aws_shelltools import util


DEFAULT_CONFIG_FILE = '~/.aws/config'
DEFAULT_CONFIG_DIR = '~/.aws/config.d'



#def get_profile(args):
#    if args['--profile']:
#        return args['--profile']
#    if os.environ.get('AWS_PROFILE'):
#        return os.environ.get('AWS_PROFILE')
#    return DEFAULT_PROFILE


def get_user_name():
    """
    Returns the IAM user_name of the calling identidy (i.e. you)
    """
    sts = boto3.client('sts')
    return sts.get_caller_identity()['Arn'].split('/')[-1]


def get_assume_role_policies(user_name):
    """
    returns a list of IAM policy objects
    """
    iam = boto3.resource('iam')
    user = iam.User(user_name)
    groups = list(user.groups.all())
    assume_role_policies = []
    for group in user.groups.all():
        assume_role_policies += [p for p in list(group.policies.all()) if
                p.policy_document['Statement'][0]['Action'] == 'sts:AssumeRole']
    return assume_role_policies 


def get_config_dir(args):
    if args['--config-dir']:
        config_dir = args['--config-dir']
    elif os.environ.get('AWS_CONFIG_DIR'):
        config_dir = os.environ.get('AWS_CONFIG_DIR')
    else:
        config_dir = DEFAULT_CONFIG_DIR
    return os.path.expanduser(config_dir)


def create_config(args, user_name, assume_role_policies):
    """
    Write the config file into aws config dir.
    """
    aws_profile = util.get_profile(args['--profile'])
    aws_config_dir = get_config_dir(args)
    try: 
        os.makedirs(aws_config_dir)
    except OSError:
        if not os.path.isdir(aws_config_dir):
            raise
    config_file = os.path.join(aws_config_dir, 'config.aws_shelltools')
    config = configparser.SafeConfigParser()
    for policy in assume_role_policies:
        title = "profile %s" % policy.name
        config.add_section(title)
        config.set(title, 'role_arn',
                 policy.policy_document['Statement'][0]['Resource'])
        config.set(title, 'role_session_name', user_name+ '@' + policy.name)
        config.set(title, 'source_profile', aws_profile)
    with open(config_file, 'w') as cf:
        config.write(cf)




def main():
    args = docopt(__doc__)
    user_name = get_user_name()
    assume_role_policies = get_assume_role_policies(user_name)
    create_config(args, user_name, assume_role_policies)



if __name__ == "__main__":
    main()
