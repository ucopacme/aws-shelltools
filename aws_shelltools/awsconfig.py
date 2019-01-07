#!/usr/bin/env python

"""Generate aws client config file by listing group assume role policies.

Usage:
  aws-make-config (-h | --help)
  aws-make-config [--profile <profile>] [--config <path>] [--config-dir <path>]

Options:
  -p, --profile <profile>   AWS credentials profile to use.  Defaults to
                            $AWS_PROFILE env var, then to 'default'.
  -f, --config <path>       Path of the aws config file to create.  Defaults
                            to $AWS_CONFIG_FILE, then to '~/.aws/config'.
  -d, --config-dir <path>   Directory where to create aws
                            config files.  Defaults to
                            $AWS_CONFIG_DIR, then to '~/.aws/config.d/'.
  -h, --help                Show this help message and exit.

"""


import os
import boto3
import yaml
from botocore.exceptions import ClientError
from docopt import docopt
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from aws_shelltools import util
from awsorgs.loginprofile import list_delegations
from awsorgs.utils import lookup


DEFAULT_CONFIG_FILE = '~/.aws/config'
DEFAULT_CONFIG_DIR = '~/.aws/config.d'
#BUCKET_NAME = 'ait-awsorgs-updates'
BUCKET_NAME = 'awsauth-962936672038'
OBJECT_NAME = 'accounts-file.yaml'



#def get_profile(args):
#    if args['--profile']:
#        return args['--profile']
#    if os.environ.get('AWS_PROFILE'):
#        return os.environ.get('AWS_PROFILE')
#    return DEFAULT_PROFILE


def get_user_name():
    """
    Returns the IAM user_name of the calling identidy (i.e. you)
    """
    sts = boto3.client('sts')
    return sts.get_caller_identity()['Arn'].split('/')[-1]


def get_config_dir(args):
    if args['--config-dir']:
        config_dir = args['--config-dir']
    elif os.environ.get('AWS_CONFIG_DIR'):
        config_dir = os.environ.get('AWS_CONFIG_DIR')
    else:
        config_dir = DEFAULT_CONFIG_DIR
    return os.path.expanduser(config_dir)


def get_deployed_accounts_from_s3(bucket_name, object_name):
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(bucket_name, object_name)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The bucket does not exist.")
            return None
        else:
            raise
    body = obj.get()['Body'].read()
    deployed_accounts = yaml.load(body)
    return deployed_accounts


def create_config(args, user_name, role_arns, deployed_accounts):
    """
    Write the config file into aws config dir.
    """
    aws_profile = util.get_profile(args['--profile'])
    aws_config_dir = get_config_dir(args)
    try: 
        os.makedirs(aws_config_dir)
    except OSError:
        if not os.path.isdir(aws_config_dir):
            raise
    config_file = os.path.join(aws_config_dir, 'config.aws_shelltools')
    config = configparser.SafeConfigParser()


    #for policy in assume_role_policies:
    for arn in assume_role_arns:
        # generate title from account alias and role name of arn
        #alias = lookup(lkjlkj)
        # role_name = parse the arn string
        title = "profile %s" % policy.name
        #title = "profile %s-%s" % (alias, role_name)
        config.add_section(title)
        config.set(title, 'role_arn',
                 policy.policy_document['Statement'][0]['Resource'])
        #config.set(title, 'role_arn', arn)
        config.set(title, 'role_session_name', user_name+ '@' + policy.name) # fix this too
        config.set(title, 'source_profile', aws_profile)
    with open(config_file, 'w') as cf:
        config.write(cf)




def main():
    args = docopt(__doc__)
    user_name = get_user_name()
    iam = boto3.resource('iam')
    user = iam.User(user_name)
    deployed_accounts = get_deployed_accounts_from_s3(BUCKET_NAME,OBJECT_NAME)
    role_arns = list_delegations(None, user, deployed_accounts)
    print(role_arns)
    create_config(args, user_name, role_arns, deployed_accounts)



if __name__ == "__main__":
    main()
