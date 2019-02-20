AWS ShellTools
===============

 Functional Testing of commands after updating code.

Test **'aws-whoami'**:
---------------------
::


  (python36) [joe@scrap home]$ aws-whoami


  {
    "UserId": "AIDAIQDJAMKBRSWM6SLQM",
    "Account": "277777777777",
    "Arn": "arn:aws:iam::777777777777:user/awsauth/joe"
  }


Test **'aws-set-mfa-token' and 'aws-env'**:
------------------------------------------
::

  python36) [joe@scrap home]$ aws-env
  AWS_CONFIG_DIR=~/.aws/config.d
  AWS_CONFIG_FILE=~/.aws/config


  (python36) [joe@scrap home]$ aws-set-mfa-token
  please enter 6 digit token code for your MFA device: 508337
  (python36) [joe home]$ aws-env
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

  (python36) [joe@scrap ~]$ aws-refresh
  please enter 6 digit token code for your MFA device: 806005
  (python36) [joe@scrap ~]$



Test **'aws-list-roles'**:
--------------------------
::

  n36) [joe@scrap home]$ aws-list-roles

  profile joe-xxxxx-AccountAdmin
  profile joe-xxxxxx-AccountAdmin
  profile joe-xxxxxx-AccountAdmin
  (python36) [joe@scrap home]$


Test **'aws-assume-role'**:
---------------------------
::
 
  python36) [joe@scrap home]$ aws-whoami


  {  
    "UserId": "xxxxxxxxx:joe",
    "Account": xxxxxxxxxxxx",
    "Arn": "arn:aws:sts:xxxxxxxxxxxx:assumed-role/AccountAdmin/joe@AccountAdmin"
  }



Test **'aws-display-assumed-role'**:
------------------------------------
::

 (python36) [joe home]$ aws-display-assumed-role
 

  AWS_ASSUMED_ROLE_PROFILE:
  AWS_ASSUMED_ROLE_ARN:
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-10 04:47:22+00:00

  (python36) [joe@scrap home]$ aws-assume-role joexxxxxxxxxxxxxxxxxx-Account

  (python36) [joe@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:     joexxxxxxxxxxxxxxxxxx-Account
  AWS_ASSUMED_ROLE_ARN:         arn:aws:sts::xxxxxxxxxx:assumed-role/joexxxxxxxxx@Account
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-09 18:04:57+00:00
  (python36) [joe@scrap home]$



Test **'aws-drop-assume-role'**:
--------------------------------
::

  (python36) [joe@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:     joexxxxxxxxxxxxxxxxxx-Account
  AWS_ASSUMED_ROLE_ARN:         arn:aws:sts::xxxxxxxxxx:assumed-role/joexxxxxxxxx@Account
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-09 18:04:57+00:00

  (python36) [joe@scrap home]$ aws-drop-assumed-role

  (python36) [joe@scrap home]$ aws-display-assumed-role
  AWS_ASSUMED_ROLE_PROFILE:
  AWS_ASSUMED_ROLE_ARN:
  AWS_SESSION_TOKEN_EXPIRATION: 2019-01-10 04:47:22+00:00
  (python36) [joe@scrap home]$



Test **'aws-export-env'**:  
--------------------------
::

 
  (Initiated in Shell-One:)

  (python36) [joe@scrap cache]$ aws-export-env

  (python36) [joe@scrap cache]$ ls -l
  total 4
  -rw------- 1 joe joe 1089 Jan  9 13:50 exported_env
  (python36) [joe@scrap cache]$ head exported_env
  export AWS_ACCESS_KEY_ID=ASIATES
  export AWS_CONFIG_DIR=~/.aws/config.d
  export AWS_CONFIG_FILE=~/.aws/config
  export AWS_MFA_ACCESS_KEY_ID=ASIAT
  export AWS_MFA_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  export AWS_MFA_SESSION_TOKEN_EXPIRATION=2019-01-10 06:09:45+00:00
  export AWS_MFA_SESSION_TOKEN=FQ
  export AWS_PROFILE=joe-test
  export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  export AWS_SESSION_TOKEN_EXPIRATION=2019-01-10 06:09:45+00:00
  (python36) [joe@scrap cache]$



Test **'aws-import-env'**:
--------------------------
::

  (After Initiating 'aws-export-env in shell-one, run this command in shell-two)
  python36) [joe@scrap .aws]$ aws-env
  AWS_CONFIG_DIR=~/.aws/config.d
  AWS_CONFIG_FILE=~/.aws/config

  (python36) [joe@scrap .aws]$ ls
  cache  config  config.d  credentials

  (python36) [joe@scrap .aws]$ aws-import-env

  (python36) [joe@scrap .aws]$ aws-env
  AWS_ACCESS_KEY_ID=AXXXXX
  AWS_CONFIG_DIR=/home/joe/.aws/config.d
  AWS_CONFIG_FILE=/home/joe/.aws/config
  AWS_MFA_ACCESS_KEY_ID=XXXXXXXXXXXXXX
  AWS_MFA_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_MFA_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_PROFILE=joe-test
  AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx




Test **'aws-make-config'**:
---------------------------
::

  python36) [joe@scrap cache]$ aws-make-config

  (python36) [joe@scrap cache]$ aws-list-roles
  profile joe-xxxxxxxx-AccountAdmin
  profile joe-xxxxxxx-2-AccountAdmin
  profile joe-xxxxxxxxxx-3-AccountAdmin

