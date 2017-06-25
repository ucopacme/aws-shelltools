#!/usr/bin/python

"""Tools for basic AWS session setup.

Usage:
  awstools.py (-h | --help)
  awstools.py --version
  awstools.py --mfa-token <token> [--profile <profile>]

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -m, --mfa-token <token>    6 digit tokencode provided by MFA device.

"""
# The TokenCode is the time-based one-time password (TOTP) that the MFA devices produces.

import boto3
from docopt import docopt


def get_mfa_sn(session):
    """
    Return serial number (ARN) for the MFA device accociated with
    the user's session profile.
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
    sts_client = session.client('sts')
    response = sts_client.get_session_token(
        SerialNumber=get_mfa_sn(session),
        TokenCode=token_code
    )
    return response.get('Credentials', None)






if __name__ == "__main__":
    args = docopt(__doc__, version='awstools 0.0.0')
    session = boto3.Session(profile_name=args['--profile'])

     
    creds = get_sts_credentials(session, args['--mfa-token'])
    if creds:
        print "export AWS_ACCESS_KEY_ID=%s" % creds['AccessKeyId']
        print "export AWS_SECRET_ACCESS_KEY=%s" % creds['SecretAccessKey']
        print "export AWS_SECURITY_TOKEN=%s" % creds['SessionToken']
        print "export AWS_SECURITY_TOKEN_EXPIRATION='%s'" % creds['Expiration']

