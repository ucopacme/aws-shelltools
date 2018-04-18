#!/usr/bin/env python

"""Create a set of AWS temporary STS assume role credenials.

Usage:
  awsassumerole (-h | --help)
  awsassumerole --profile <profile> [--config <path>] [--config-dir <path>]
  awsassumerole --list-profiles

Options:
  -p, --profile <profile>   Required. The config profile title identifying
                            the role to assume.  
  -f, --config <path>       Path of the aws config file.  Defaults to
                            $AWS_CONFIG_FILE, then to '~/.aws/config'.
  -d, --config-dir <path>   Directory where to look for additional aws
                            config files.  Defaults to
                            $AWS_CONFIG_DIR, then to '~/.aws/config.d/'.
  -l, --list-profiles       Display a list of configured aws assume
                            role profiles.
  -h, --help                Show this help message and exit.

"""


import sys
import os

import boto3
import botocore.exceptions
from botocore.exceptions import ClientError
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from aws_shelltools import util


DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG_FILE = '~/.aws/config'
DEFAULT_CONFIG_DIR = '~/.aws/config.d'


#def get_session(aws_profile):
#    """
#    Return boto3 session object for a given profile.  Try to 
#    obtain client credentials from shell environment.  This should
#    capture MFA credential if present in user's shell env.
#    """
#    return boto3.Session(
#            profile_name=aws_profile,
#            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
#            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
#            aws_session_token=os.environ.get('AWS_SESSION_TOKEN', ''))


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
    for f in config_files:
        try:
            config.read(f)
        except configparser.Error as e:
            print('Can not parse config file "{}".\n{}'.format(f, e))
            sys.exit(1)
    return config


def list_config_profiles(config):
    if os.environ.get('AWS_PROFILE'):
        aws_profile = os.environ.get('AWS_PROFILE')
    else:
        aws_profile = DEFAULT_PROFILE
    return [p for p in sorted(config.sections())
            if (config.has_option(p, 'source_profile')
            and config.get(p, 'source_profile') == aws_profile)]


def parse_assume_role_profile(args, config):
    profiles = list_config_profiles(config)
    candidates = [p for p in profiles if args['--profile'] in p]        
    if not candidates:
        print("\nProfile '%s' not found.\nSelect a profile from the list below and "
                "try again:\n\n%s" % (args['--profile'], "\n".join(profiles)))
        sys.exit(1)
    elif len(candidates) == 1:
        section = candidates[0]
    elif "profile %s" % args['--profile'] in candidates:
        section = "profile %s" % args['--profile']
    else:
        print("\nYour specified profile '%s' matches multiple configured "
        	"profiles.\nSelect one the list below and try again:\n\n%s" %
                (args['--profile'],
                "\n".join([p.split()[1] for p in candidates])))
        sys.exit(1)
    try:
        role_arn = config.get(section, 'role_arn')
    except (configparser.NoOptionError, configparser.NoSectionError) as e:
        print("AWS config Error: %s" % e)
        sys.exit(1)
    try:
        source_profile = config.get(section, 'source_profile')
    except (configparser.NoOptionError, configparser.NoSectionError) as e:
        print("AWS config Error: %s" % e)
        sys.exit(1)
    try:
        role_session_name = config.get(section, 'role_session_name')
    except (configparser.NoOptionError, configparser.NoSectionError) as e:
        print("AWS config Error: %s" % e)
        sys.exit(1)
    return (role_arn, source_profile, role_session_name)


def assume_role_from_profile(args):
    config = load_aws_config(args)
    (role_arn, source_profile, role_session_name) = parse_assume_role_profile(
            args, config)
    session = util.get_session(source_profile)
    sts_client = session.client('sts')
    try:
        response = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=role_session_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(e.response['Error']['Message'])
            sys.exit(1)
        else:
            raise e
    return response


def main():
    args = docopt(__doc__)
    if args['--list-profiles']:
        config = load_aws_config(args)
        profiles = list_config_profiles(config)
        print("\n".join(profiles))
    else:
        res = assume_role_from_profile(args)
        print("export AWS_ACCESS_KEY_ID=%s" % res['Credentials']['AccessKeyId'])
        print("export AWS_SECRET_ACCESS_KEY=%s" % res['Credentials']['SecretAccessKey'])
        print("export AWS_SESSION_TOKEN=%s" % res['Credentials']['SessionToken'])
        print("export AWS_SESSION_TOKEN_EXPIRATION='%s'" %
		res['Credentials']['Expiration'])
        print("export AWS_ASSUMED_ROLE_ARN=%s" % res['AssumedRoleUser']['Arn'])
        print("export AWS_ASSUMED_ROLE_PROFILE=%s" % args['--profile'])


if __name__ == "__main__":
    main()
