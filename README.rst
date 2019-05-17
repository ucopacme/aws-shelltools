==============
aws-shelltools
==============


Yet another set of scripts and shell functions for managing AWS profiles
and cross account access.


**Install**

Install into python virual environment::

  source ~/path-to-venv/bin/activate
  pip install aws-shelltools

Install from editable local repository::

  git clone https://github.com/ucopacme/aws-shelltools
  cd aws-shelltools
  pip install -r requirements.txt
  pip install -e .


**Uninstall**::

  pip uninstall aws-shelltools


**Configure**::

  aws-shelltools-setup
  . ~/.bashrc


The shelltools:
---------------

aws-profile
  Set or display value of shell environment var AWS_PROFILE.
  
aws-set-mfa-token
  Request temporary session credentials from AWS STS.  Export these credentials
  to environment vars in the current shell.

aws-make-config
  Generate aws client config file by listing group assume role policies.  You
  must set your MFA token before you run this command.
  
aws-list-roles
  Print list of available AWS assume role profiles.

aws-assume-role
  Run 'aws sts assume-role' operation to obtain temporary assumed role
  credentials for the specified profile.  Export these credentials to
  environment vars in the current shell.

aws-refresh
  Reset mfa token. If environment var AWS_ASSUMED_ROLE_PROFILE is already
  set from a previous session, then rerun 'aws sts assume-role' operation
  for that profile.

aws-display-assumed-role
  Print current values of AWS assumed role environment vars
  
aws-whoami
  Print output of 'aws sts get-caller-identity'
  
aws-env
  Print current values of all AWS environment vars

aws-export-env
  Cache AWS environment vars to local file for use by other shells

aws-import-env
  Evaluate cached AWS evironment vars into current shell

aws-drop-assumed-role
  Reset AWS session environment vars to values prior to assuming role
  
aws-unset-mfa-token
  Unset all AWS session token environemt vars
  


**Usage**::

  # Run each command with -h option for full usage info.

  aws-profile <profile>
  aws-set-mfa-token
  aws-make-config
  aws-list-roles
  aws-assume-role <profile>
  aws-refresh
  
  aws-display-assumed-role
  aws-whoami
  aws-env
  aws-export-env
  aws-import-env

  aws-drop-assumed-role
  aws-unset-mfa-token


Configure Assume Role Profiles
------------------------------

If you have not yet set up your AWS CLI access, skip to section `Awscli/Python Setup`_
before proceeding.

Set your MFA token and assume role to one of your configured assume role profiles::

  (python3.6) ashleygould$ aws-set-mfa-token 
  please enter 6 digit token code for your MFA device: 351918
  (python3.6) ashleygould$ aws-assume-role ashley-training-OrgAdmin
  (python3.6) ashleygould$ aws-whoami 
  {
      "UserId": "AROAIMADVT2W7CODNCP7W:agould@ashley-training-OrgAdmin",
      "Account": "111111111111",
      "Arn": "arn:aws:sts::111111111111:assumed-role/OrgAdmin/agould@ashley-training-OrgAdmin"
  }

Now you can run `aws-make-config` to generate your assume role profiles based
on your group membership in a central *auth* account.  These are written to
`~/.aws/config.d/config.aws_shelltools`::

  (python3.6) ashleygould$ aws-make-config
  (python3.6) ashleygould$ head ~/.aws/config.d/config.aws_shelltools 
  [profile ashley-training-OrgAdmin]
  role_arn = arn:aws:iam::111111111111:role/awsauth/OrgAdmin
  role_session_name = agould@ashley-training-OrgAdmin
  source_profile = default
  
  [profile Auth-OrgAdmin]
  role_arn = arn:aws:iam::222222222222:role/awsauth/OrgAdmin
  role_session_name = agould@Auth-OrgAdmin
  source_profile = default

See a listing or all your available AWS profiles::

  (python3.6) ashleygould$ aws-list-roles 
  profile Auth-OrgAdmin
  profile OrgMaster-OrgAdmin
  profile ashley-training-OrgAdmin
  profile eas-dev-OrgAdmin
  profile eas-prod-OrgAdmin


You can shorten the profile name at the command line to a unique prefix::

  (python3.6) ashleygould$ aws-assume-role eas
  Your specified profile 'eas' matches multiple configured profiles. Select one from 
  the list below and try again: 
    eas-dev-OrgAdmin eas-prod-OrgAdmin 
    ucop-itssandbox-eas-OrgAdmin
  (python3.6) ashleygould$ aws-assume-role eas-dev
  (python3.6) ashleygould$ aws-whoami 
  {
      "UserId": "AROAJFPJVRDRDFUZJLZVG:agould@eas-dev-OrgAdmin",
      "Account": "111111111111",
      "Arn": "arn:aws:sts::111111111111:assumed-role/OrgAdmin/agould@eas-dev-OrgAdmin"
  }




Awscli/Python Setup
-------------------

The above install insturctions assume you have a working knowledge of python
and awscli.  If you are new at this, refer to the excellent AWS documentation:
https://docs.aws.amazon.com/cli/latest/userguide/installing.html

This covers installation of python and python virtual environments for Linux,
MacOS, and Windows.  Once your python is happy, running the installation of
`aws-shelltools` will ensure `awscli`and `boto3` are also properly installed.




AWS Access Key Setup
--------------------

Before you can use any of this stuff, you must create your AWS access key and
secret access key and confiture your AWS shell profile.  see:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Log into AWS console and create an AWS Access key as per AWS doc.  From your
shell run the `aws configure` command and cut-n-paste your access key/secret
key from the console to the command line as prompted.  This creates your
`default` profile::

  (python3.6) ashleygould$ aws configure
  AWS Access Key ID [None]: AKI**********W5AFPSNQ
  AWS Secret Access Key [None]: U/QotA**********************543vuYB
  Default region name [None]: us-west-2
  Default output format [None]:
  
  (python3.6) ashleygould$ cat .aws/config 
  [default]
  region = us-west-2
  
  (python3.6) its-agould-9m:~ ashleygould$ aws-whoami 
  {
      "UserId": "AIDAJ2SLREGRDKVFOB6CI",
      "Account": "112233445566",
      "Arn": "arn:aws:iam::112233445566:user/awsauth/orgadmin/agould"
  }

Working With Codecommit Repositories
------------------------------------

To access codecommit repositories from the commandline after assuming a role,
you must first configure git to use the AWS codecommit credential-helper::

  git config --global credential.helper '!aws codecommit credential-helper $@'
  git config --global credential.UseHttpPath true



