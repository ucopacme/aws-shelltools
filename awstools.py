#!/usr/bin/python

"""Manage recources in an AWS Organization.

Usage:
  awstools.py (-h | --help)
  awstools.py --version
  awstools.py [--profile <profile>] [--verbose]

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -v, --verbose              Log to STDOUT as well as log-target.

"""

import boto3
from docopt import docopt


def mfasn(session):
    """
    returns arn of mfa_serial you set in specified profile
    """
    iam_client = session.client('iam')
    return iam_client.list_mfa_devices()['MFADevices'][0]['SerialNumber']


def mfacli(session):
    """
    generate temporary aws security token environment variables for your shell
    """
    sts_client = session.client('sts')
    token_code = raw_input("please enter 6 digit one-time-password: ")
    return sts_client.get_session_token(
            SerialNumber=mfasn(session), TokenCode=token_code)


if __name__ == "__main__":
    args = docopt(__doc__, version='awstools 0.0.0')
    print args
    print
    session = boto3.Session(profile_name=args['--profile'])

    
    print mfasn(session)
    print mfacli(session)
