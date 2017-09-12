#!/usr/bin/env python

"""Create a set of AWS temporary STS credenials.

Generate temporary security credentials and session token from AWS
Simple Token Service and display them as shell 'export' statements.  The
user will then apply these to her current shell environment, typically
using 'eval' as in:

  eval `aws awstoken --mfa-token 123456`


Usage:
  awstoken (-h | --help)
  awstoken [--mfa-token <token>] [--profile <profile>]

Options:
  -h, --help                Show this help message and exit.
  -p, --profile <profile>   AWS credentials profile to use.  Defaults to
                            $AWS_PROFILE env var, then to 'default'.
  -m, --mfa-token <token>   6 digit tokencode (time-based one-time password)
                            provided by MFA device.

"""



import os
import boto3
from docopt import docopt


def _get_mfa_sn(session):
    """
    Return serial number (ARN) for the MFA device accociated with
    the user's session profile if one exists.
    ISSUE: assumes only one device per user.
    """
    iam_client = session.client('iam')
    response = iam_client.list_mfa_devices()
    if response.get('MFADevices', []):
        return response['MFADevices'][0]['SerialNumber']
    return None


def _get_sts_credentials(session, token_code):
    """
    Return a set of STS session credentials.
    """
    mfa_sn = _get_mfa_sn(session)
    if token_code and mfa_sn:
        kwargs = dict(SerialNumber=mfa_sn, TokenCode=token_code)
    else:
        kwargs = {}
    sts_client = session.client('sts')
    response = sts_client.get_session_token(**kwargs)
    return response.get('Credentials', None)


def main():
    args = docopt(__doc__)

    if os.environ.get('AWS_PROFILE'):
        aws_profile = os.environ.get('AWS_PROFILE')
    elif args['--profile']:
        aws_profile = args['--profile']
    else:
        aws_profile = 'default'

    session = boto3.Session(profile_name=aws_profile)
     
    creds = _get_sts_credentials(session, args['--mfa-token'])
    if creds:
        print("export AWS_ACCESS_KEY_ID=%s" % creds['AccessKeyId'])
        print("export AWS_SECRET_ACCESS_KEY=%s" % creds['SecretAccessKey'])
        print("export AWS_SESSION_TOKEN=%s" % creds['SessionToken'])
        print("export AWS_SESSION_TOKEN_EXPIRATION='%s'" % creds['Expiration'])
        print("export AWS_MFA_ACCESS_KEY_ID=%s" % creds['AccessKeyId'])
        print("export AWS_MFA_SECRET_ACCESS_KEY=%s" % creds['SecretAccessKey'])
        print("export AWS_MFA_SESSION_TOKEN=%s" % creds['SessionToken'])
        print("export AWS_MFA_SESSION_TOKEN_EXPIRATION='%s'" % creds['Expiration'])


if __name__ == "__main__":
    main()
