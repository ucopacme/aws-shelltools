==============
aws-shelltools
==============


Yet another set of scripts and shell functions for managing AWS profiles
and cross account access.


**Install**

Site installation::

  sudo pip install git+https://www.github.com/ashleygould/aws-shelltools.git 

Local user installation::

  git clone https://github.com/ashleygould/aws-shelltools
  pip install --user -e aws-shelltools/

On RHEL6 you may need to update setuptools as well:

  sudo pip install -U setuptools


**Uninstall**::

  pip uninstall aws-shelltools

  # if installed as local user also run:
  rm ~/.local/bin/{awstoken,awsassumerole,awsconfig,aws-shelltools-setup}


**Configure**::

  aws-shelltools-setup
  . ~/.bashrc


The shelltools:
---------------

aws-profile
  Set or display value of shell environment var AWS_PROFILE.

aws-make-config
  Generate aws client config file by listing group assume role policies.
  
aws-list-roles
  Print list of available AWS assume role profiles.
  
aws-set-mfa-token
  Request temporary session credentials from AWS STS.  Export these credentials
  to environment vars in the current shell.

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
  aws-make-config
  aws-list-roles
  aws-set-mfa-token
  aws-assume-role <profile>
  aws-refresh
  
  aws-display-assumed-role
  aws-whoami
  aws-env
  aws-export-env
  aws-import-env

  aws-drop-assumed-role
  aws-unset-mfa-token



:Author: 
    Ashley Gould (agould@ucop.edu)

:Version: 0.0.6
