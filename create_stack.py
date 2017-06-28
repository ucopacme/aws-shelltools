#!/usr/bin/python
"""Build AWS resources with cloudformation

Usage:
  create-stack.py (--stack-name NAME) (--template-file FILE) [--profile <profile>] [--verbose]
  create-stack.py (-h | --help)
  create-stack.py --version

Options:
  -h, --help                 Show this help message and exit.
  --version                  Display version info and exit.
  -p, --profile <profile>    AWS credentials profile to use [default: default].
  -f FILE, --template-file FILE  Cloudformation template file.
  -n NAME, --stack-name NAME  Name of the Cloudformation stack.

"""



import boto3
import json
from docopt import docopt


args = docopt(__doc__, version='awsorgs 0.0.0')
print args
#template_body = json.load(open(args['--template-file']).read())
template_body = open(args['--template-file']).read()
print template_body

session = boto3.Session(profile_name=args['--profile'])
client = session.client('cloudformation')
response = client.create_stack(
    StackName=args['--stack-name'],
    TemplateBody=template_body,
    Capabilities=[
        'CAPABILITY_IAM',
        'CAPABILITY_NAMED_IAM',
    ],
)
print response




