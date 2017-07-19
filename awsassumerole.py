#!/usr/bin/python

"""Create a set of AWS temporary STS assume role credenials.

Usage:
  awsassumerole (-h | --help)
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
  -h, --help                Show this help message and exit.

"""


import os
import boto3
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser


DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG_FILE = '~/.aws/config'
DEFAULT_CONFIG_DIR = '~/.aws/config.d'


def get_session(aws_profile):
    """
    Return boto3 session object for a given profile.  Try to 
    obtain client credentials from shell environment.  This should
    capture MFA credential if present in user's shell env.
    """
    session_args = dict(
            profile_name=aws_profile,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN', ''))
    return boto3.Session(**session_args)


def assume_role(session, role_arn, role_session_name):
    """
    Get temporary sts assume_role credentials for account.
    """
    sts_client = session.client('sts')
    credentials = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
            )['Credentials']
    return dict(
            aws_access_key_id = credentials['AccessKeyId'],
            aws_secret_access_key = credentials['SecretAccessKey'],
            aws_session_token = credentials['SessionToken'])


def get_profile(args):
    if args['--profile']:
        return args['--profile']
    if os.environ.get('AWS_PROFILE'):
        return os.environ.get('AWS_PROFILE')
    return DEFAULT_PROFILE


def load_aws_config(args):
    if args['--config']:
        aws_config_file = args['--config']
    elif os.environ.get('AWS_CONFIG_FILE'):
        aws_config_file = os.environ.get('AWS_CONFIG_FILE')
    else:
        aws_config_file = DEFAULT_CONFIG_FILE
    aws_config_file = os.path.expanduser(aws_config_file)
        
    if args['--config-dir']:
        aws_config_dir = args['--config-dir']
    elif os.environ.get('AWS_CONFIG_DIR'):
        aws_config_dir = os.environ.get('AWS_CONFIG_DIR')
    else:
        aws_config_dir = DEFAULT_CONFIG_DIR
    aws_config_dir = os.path.expanduser(aws_config_dir)

    config_files = []
    if os.path.isfile(aws_config_file):
        config_files.append(aws_config_file)
    if os.path.isdir(aws_config_dir):
        config_files += [os.path.join(aws_config_dir, f)
                for f in os.listdir(aws_config_dir)]

    config = configparser.SafeConfigParser()
    config.read(config_files)
    return config


def main():
    args = docopt(__doc__)
    aws_profile = get_profile(args)
    session = get_session(aws_profile)
    config = load_aws_config(args)
    #print config.sections()

    section = "profile %s" % args['--role-name']
    if config.has_section(section):
        role_arn = config.get(section, 'role_arn')
        role_session_name = config.get(section, 'role_session_name')
    token = assume_role(session, role_arn, role_session_name)
    print token

if __name__ == "__main__":
    main()


# ashely@horus:~/aws/aws-shelltools> ./awsassumerole.py -r goeruio
# Traceback (most recent call last):
#   File "./awsassumerole.py", line 120, in <module>
#     main()
#   File "./awsassumerole.py", line 116, in main
#     token = assume_role(session, role_arn, role_session_name)
# UnboundLocalError: local variable 'role_arn' referenced before assignment







#org_client = session.client('organizations', **credentials)

