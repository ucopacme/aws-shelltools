AWS ShellTools
===============

 Functional Testing of commands after updating code.

Test **'aws-whoami'**:
---------------------
::


  (python36) [david@scrap home]$ aws-whoami


  {
    "UserId": "AIDAIQDJAMKBRSWM6SLQM",
    "Account": "215824054945",
    "Arn": "arn:aws:iam::215824054945:user/awsauth/david"
  }


Test **'aws-set-mfa-token' and 'aws-env'**:
------------------------------------------
::

  python36) [david@scrap home]$ aws-env
  AWS_CONFIG_DIR=~/.aws/config.d
  AWS_CONFIG_FILE=~/.aws/config


  (python36) [david@scrap home]$ aws-set-mfa-token
  please enter 6 digit token code for your MFA device: 508337
  (python36) [david@scrap home]$ aws-env
  AWS_ACCESS_KEY_ID=ASIATE
  AWS_CONFIG_DIR=~/.aws/config.d
  AWS_CONFIG_FILE=~/.aws/config
  AWS_MFA_ACCESS_KEY_ID=ASIATA
  AWS_MFA_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
  AWS_MFA_SESSION_TOKEN_EXPIRATION=2019-01-10 04:47:22+00:00
  AWS_MFA_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_SESSION_TOKEN_EXPIRATION=2019-01-10 04:47:22+00:00
  AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
 


Test **'aws-refresh**'
----------------------
::

  (python36) [david@scrap ~]$ aws-refresh
  please enter 6 digit token code for your MFA device: 806005
  (python36) [david@scrap ~]$



Test **'aws-list-roles'**:
--------------------------
::

  n36) [david@scrap home]$ aws-list-roles

  profile david-xxxxx-AccountAdmin
  profile david-xxxxxx-AccountAdmin
  profile david-xxxxxx-AccountAdmin
  (python36) [david@scrap home]$


Test **'aws-assume-role'**:
---------------------------
::
 
  python36) [david@scrap home]$ aws-whoami


  {  
    "UserId": "xxxxxxxxx:david@AccountAdmin",
    "Account": xxxxxxxxxxxx",
    "Arn": "arn:aws:sts:xxxxxxxxxxxx:assumed-role/AccountAdmin/david@AccountAdmin"
  }



Test **'aws-display-assumed-role'**:
------------------------------------
::

 (python36) [david@scrap home]$ aws-display-assumed-role
 

  AWS_ASSUMED_ROLE_PROFILE:
  AWS_ASSUMED_ROLE_ARN:
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-10 04:47:22+00:00

  (python36) [david@scrap home]$ aws-assume-role davidxxxxxxxxxxxxxxxxxx-Account

  (python36) [david@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:     davidxxxxxxxxxxxxxxxxxx-Account
  AWS_ASSUMED_ROLE_ARN:         arn:aws:sts::xxxxxxxxxx:assumed-role/davidxxxxxxxxx@Account
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-09 18:04:57+00:00
  (python36) [david@scrap home]$



Test **'aws-drop-assume-role'**:
--------------------------------
::

  (python36) [david@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:     davidxxxxxxxxxxxxxxxxxx-Account
  AWS_ASSUMED_ROLE_ARN:         arn:aws:sts::xxxxxxxxxx:assumed-role/davidxxxxxxxxx@Account
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-09 18:04:57+00:00

  (python36) [david@scrap home]$ aws-drop-assumed-role

  (python36) [david@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:
  AWS_ASSUMED_ROLE_ARN:
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-10 04:47:22+00:00
  (python36) [david@scrap home]$



Test **'aws-export-env'**:  
--------------------------
::

 
  (Initiated in Shell-One:)

  (python36) [david@scrap cache]$ aws-export-env

  (python36) [david@scrap cache]$ ls -l
  total 4
  -rw------- 1 david david 1089 Jan  9 13:50 exported_env
  (python36) [david@scrap cache]$ head exported_env
  export AWS_ACCESS_KEY_ID=ASIATES
  export AWS_CONFIG_DIR=~/.aws/config.d
  export AWS_CONFIG_FILE=~/.aws/config
  export AWS_MFA_ACCESS_KEY_ID=ASIAT
  export AWS_MFA_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  export AWS_MFA_SESSION_TOKEN_EXPIRATION=2019-01-10 06:09:45+00:00
  export AWS_MFA_SESSION_TOKEN=FQ
  export AWS_PROFILE=david-test
  export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  export AWS_SESSION_TOKEN_EXPIRATION=2019-01-10 06:09:45+00:00
  (python36) [david@scrap cache]$



Test **'aws-import-env'**:
--------------------------
::

  (After Initiating 'aws-export-env in shell-one, run this command in shell-two)
  python36) [david@scrap .aws]$ aws-env
  AWS_CONFIG_DIR=~/.aws/config.d
  AWS_CONFIG_FILE=~/.aws/config

  (python36) [david@scrap .aws]$ ls
  cache  config  config.d  credentials

  (python36) [david@scrap .aws]$ aws-import-env

  (python36) [david@scrap .aws]$ aws-env
  AWS_ACCESS_KEY_ID=AXXXXX
  AWS_CONFIG_DIR=/home/david/.aws/config.d
  AWS_CONFIG_FILE=/home/david/.aws/config
  AWS_MFA_ACCESS_KEY_ID=XXXXXXXXXXXXXX
  AWS_MFA_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_MFA_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_PROFILE=david-test
  AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx




Test **'aws-make-config'**:
---------------------------
::

  python36) [david@scrap cache]$ aws-make-config

  (python36) [david@scrap cache]$ aws-list-roles
  profile david-xxxxxxxx-AccountAdmin
  profile david-xxxxxxx-2-AccountAdmin
  profile david-xxxxxxxxxx-3-AccountAdmin

