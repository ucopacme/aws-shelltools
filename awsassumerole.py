#!/usr/bin/python

"""Create a set of AWS temporary STS assume role credenials.

Usage:
  awsassumerole (-h | --help)
  awsassumerole [--profile <profile>]

Options:
  -h, --help                Show this help message and exit.
  -p, --profile <profile>   AWS credentials profile to use [default: default].
                            $AWS_PROFILE env var, then to 'default'.

"""



import os
import boto3
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser



def get_session(args):
    """
    Return boto3 session object for a given profile.  Try to 
    obtain client credentials from shell environment.  This should
    capture MFA credential if present in user's shell env.
    """
    if os.environ.get('AWS_PROFILE'):
        aws_profile = os.environ.get('AWS_PROFILE')
    else:
        aws_profile = args['--profile']
    session_args = dict(
            profile_name=aws_profile,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN', ''))
    return boto3.Session(**session_args)


def assume_role(session, role_profile):
    """
    Get temporary sts assume_role credentials for account.
    """
    #role_arn = 'arn:aws:iam::' + account_id + ':role/' + role_name
    #role_session_name = account_id + '-' + role_name
    sts_client = session.client('sts')
    credentials = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
            )['Credentials']
    return dict(
            aws_access_key_id = credentials['AccessKeyId'],
            aws_secret_access_key = credentials['SecretAccessKey'],
            aws_session_token = credentials['SessionToken'])



credentials = assume_role(session, role_profile)
org_client = session.client('organizations', **credentials)


# https://github.com/boto/boto3/pull/69
#>>> mgmt = boto3.session.Session(profile_name='Managment')
#>>> iam_client = mgmt.client('iam')
#>>> iam_client.list_users()

#>>> client = session.client('sts')
#>>> client.get_caller_identity


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

