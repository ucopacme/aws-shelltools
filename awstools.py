#!/usr/bin/python

"""Manage recources in an AWS Organization.

Usage:
  awstools.py (-h | --help)
  awstools.py --version
  awstools.py --otp <otp> [--profile <profile>] [--verbose]

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -v, --verbose              Log to STDOUT as well as log-target.
  --otp <otp>                 MFA one time password.

"""

import boto3
from docopt import docopt


def mfasn(session):
    """
    returns arn of mfa_serial you set in specified profile
    """
    iam_client = session.client('iam')
    #return iam_client.list_mfa_devices()['MFADevices'][0]['SerialNumber']
    response = iam_client.list_mfa_devices()
    if response.get('MFADevices', []):
        return response['MFADevices'][0]['SerialNumber']
    return None


def mfacli(args, session, duration = 43200):
    """
    generate temporary aws security token environment variables for your shell
    """
    sts_client = session.client('sts')
    token_code = args['--otp']
    response = sts_client.get_session_token(
        DurationSeconds=duration,
        SerialNumber=mfasn(session),
        TokenCode=token_code
    )
    creds = response.get('Credentials', None)
    if creds:
        print "export AWS_ACCESS_KEY_ID=%s" % creds['AccessKeyId']
        print "export AWS_SECRET_ACCESS_KEY_=%s" % creds['SecretAccessKey']
        print "export AWS_SECURITY_TOKEN_=%s" % creds['SessionToken']
        return creds['Expiration']
    return None

if __name__ == "__main__":
    args = docopt(__doc__, version='awstools 0.0.0')
    session = boto3.Session(profile_name=args['--profile'])
    mfacli(args, session)







## # List all your queues
## response = sqs.list_queues()
## for url in response.get('QueueUrls', []):
##     print(url)
