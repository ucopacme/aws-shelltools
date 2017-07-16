#!/usr/bin/python

"""Tools for basic AWS session setup.

Usage:
  awstools.py (-h | --help)
  awstools.py --version
  awstools.py token [--mfa-token <token>] [--profile <profile>]
  awstools.py config [--mfa-token <token>] [--profile <profile>]

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -m, --mfa-token <token>    6 digit tokencode provided by MFA device.
  token                      Return a set of temporary STS credenials.
  config                     Create AWS config file with a profile for all accounts in org.

"""
# The TokenCode is the time-based one-time password (TOTP) that the MFA devices produces.

import os
import boto3
from docopt import docopt


def get_mfa_sn(session):
    """
    Return serial number (ARN) for the MFA device accociated with
    the user's session profile.

    ISSUE: assumes only one device per user.
    """
    iam_client = session.client('iam')
    response = iam_client.list_mfa_devices()
    if response.get('MFADevices', []):
        return response['MFADevices'][0]['SerialNumber']
    return None


def get_sts_credentials(session, token_code):
    """
    Return temporary security credentials from AWS Simple Token Service.
    """
    mfa_sn = get_mfa_sn(session)
    if token_code and mfa_sn:
        kwargs = dict(SerialNumber=mfa_sn, TokenCode=token_code)
    else:
        kwargs = {}

    sts_client = session.client('sts')
    response = sts_client.get_session_token(**kwargs)
    return response.get('Credentials', None)

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


if __name__ == "__main__":
    args = docopt(__doc__, version='awstools 0.0.0')
    if os.environ.get('AWS_PROFILE'):
        aws_profile = os.environ.get('AWS_PROFILE')
    else:
        aws_profile = args['--profile']
    session = boto3.Session(profile_name=aws_profile)
     
    if args['token']:
        creds = get_sts_credentials(session, args['--mfa-token'])
        if creds:
            print "export AWS_ACCESS_KEY_ID=%s" % creds['AccessKeyId']
            print "export AWS_SECRET_ACCESS_KEY=%s" % creds['SecretAccessKey']
            print "export AWS_SECURITY_TOKEN=%s" % creds['SessionToken']
            print "export AWS_SECURITY_TOKEN_EXPIRATION='%s'" % creds['Expiration']

