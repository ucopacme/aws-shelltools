"""
Common functions for aws_shelltools modules
"""

import os
import boto3

DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG_FILE = '~/.aws/config'
DEFAULT_CONFIG_DIR = '~/.aws/config.d'


def get_profile(aws_profile=None):
    """Determine the AWS profile"""
    if not aws_profile:
        if os.environ.get('AWS_PROFILE'):
            aws_profile = os.environ.get('AWS_PROFILE')
        else:
            aws_profile = DEFAULT_PROFILE
    return aws_profile


def get_config_file(config_file=None):
    if not config_file:
        if os.environ.get('AWS_CONFIG_FILE'):
            config_file = os.environ.get('AWS_CONFIG_FILE')
        else:
            config_file = DEFAULT_CONFIG_FILE
    return os.path.expanduser(config_file)


def get_config_dir(config_dir=None):
    if not config_dir:
        if os.environ.get('AWS_CONFIG_DIR'):
            config_dir = os.environ.get('AWS_CONFIG_DIR')
        else:
            config_dir = DEFAULT_CONFIG_DIR
    return os.path.expanduser(config_dir)


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


