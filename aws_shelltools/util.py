"""
Common functions for aws_shelltools modules
"""

import os
import boto3

def get_profile(profile_name=None):
    """Determine and return the AWS profile.  Check in order:
      the value of 'profile_name',
      the user's shell environment,
      the 'default'.
    """
    if profile_name:
        aws_profile = profile_name
    elif os.environ.get('AWS_PROFILE'):
        aws_profile = os.environ.get('AWS_PROFILE')
    else:
        aws_profile = 'default'
    return aws_profile


def get_session(profile_name):
    """
    Return boto3 session object for a given profile.  Try to 
    obtain client credentials from shell environment.  This should
    capture MFA credential if present in user's shell env.
    """
    return boto3.Session(
            profile_name=profile_name,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN', ''))


