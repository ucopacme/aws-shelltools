#!/bin/bash
#set -x


aws-whoami() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Print output of 'aws sts get-caller-identity";;
      * ) return;;
    esac
  else
    aws sts get-caller-identity
  fi
}


aws-region ()
{
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Set or display value of shell environment var AWS_DEFAULT_PROFILE";;
      * ) export AWS_DEFAULT_REGION=$region;;
    esac
  else
      echo $AWS_DEFAULT_REGION;
  fi
}


aws-env() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Print current values of all AWS environment vars";;
      * ) return;;
    esac
  else
    env | grep ^AWS | sort
  fi
}


aws-unset-mfa-token() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Unset all AWS session token environemt vars";;
      * ) return;;
    esac
  else
    unset AWS_ACCESS_KEY_ID
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_SESSION_TOKEN
    unset AWS_SESSION_TOKEN_EXPIRATION
    unset AWS_MFA_ACCESS_KEY_ID
    unset AWS_MFA_SECRET_ACCESS_KEY
    unset AWS_MFA_SESSION_TOKEN
    unset AWS_MFA_SESSION_TOKEN_EXPIRATION
  fi
}

aws-display-assumed-role() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Print current values of AWS assumed role environment vars";;
      * ) return;;
    esac
  else
    echo "AWS_ASSUMED_ROLE_PROFILE:     $AWS_ASSUMED_ROLE_PROFILE"
    echo "AWS_ASSUMED_ROLE_ARN:         $AWS_ASSUMED_ROLE_ARN"
    echo "AWS_SESSION_TOKEN_EXPIRATION: $AWS_SESSION_TOKEN_EXPIRATION"
  fi
}


aws-drop-assumed-role() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Reset AWS session environment vars to values prior to assuming role";;
      * ) return;;
    esac
  else
    unset AWS_ASSUMED_ROLE_ARN
    unset AWS_ASSUMED_ROLE_PROFILE
    if [ -n "$AWS_MFA_ACCESS_KEY_ID" ]; then
      export AWS_ACCESS_KEY_ID=$AWS_MFA_ACCESS_KEY_ID
    else
      unset AWS_ACCESS_KEY_ID
    fi
    if [ -n "$AWS_MFA_SECRET_ACCESS_KEY" ]; then
      export AWS_SECRET_ACCESS_KEY=$AWS_MFA_SECRET_ACCESS_KEY
    else
      unset AWS_SECRET_ACCESS_KEY
    fi
    if [ -n "$AWS_MFA_SESSION_TOKEN" ]; then
      export AWS_SESSION_TOKEN=$AWS_MFA_SESSION_TOKEN
    else
      unset AWS_SESSION_TOKEN
    fi
    if [ -n "$AWS_MFA_SESSION_TOKEN_EXPIRATION" ]; then
      export AWS_SESSION_TOKEN_EXPIRATION=$AWS_MFA_SESSION_TOKEN_EXPIRATION
    else
      unset AWS_SESSION_TOKEN_EXPIRATION
    fi
  fi
}


aws-profile() {
  usage() {
    cat << EOF
Set or display value of shell environment var AWS_PROFILE.
If no args, echo the current value of AWS_PROFILE.

Usage: aws-profile [-h | -u | <profile_name>]

Args:
  -h: display help message
  -u: unset env var AWS_PROFILE
  <profile_name>: set env var AWS_PROFILE to "profile_name"

EOF
  }
  
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) usage;;
      '-u' ) unset AWS_PROFILE;;
      * ) export AWS_PROFILE=$1;;
    esac
  fi
  echo $AWS_PROFILE
}


aws-set-mfa-token() {
  usage() {
    cat << EOF
Request temporary session credentials from AWS STS.  Export these credentials
to environment vars in the current shell.  Affected vars:

  AWS_SECRET_ACCESS_KEY
  AWS_ACCESS_KEY_ID
  AWS_SESSION_TOKEN
  AWS_SESSION_TOKEN_EXPIRATION

Usage: aws-set-mfa-token [-h | -u | <profile_name>]

Args:
  -h: display help message
  -u: unset all AWS session environment vars
  <profile_name>: profile to use when setting AWS session token

EOF
  }

  request_session() {
    params=''
    read -p "please enter 6 digit token code for your MFA device: " code
    if [ -n "$code" ]; then
       params="${params}--mfa-token $code"
    fi
    if [ -n "$profile" ]; then
       params="${params} --profile $profile"
    fi
    eval $(awstoken $params)
  }
  
  if [ $# -eq 0 ]; then
    request_session
  elif [ $# -eq 1 ]; then
    case $1 in
      '-h' ) usage;;
      '-u' ) aws-unset-mfa-token;;
      * ) profile=$1; request_session;;
    esac
  elif [ $# -gt 1 ]; then
    usage
  fi

}


aws-list-roles() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Print list of available AWS assume role profiles." ;;
      * ) return ;;
    esac
  else
    awsassumerole --list-profiles
  fi
}


aws-assume-role() {
  usage() {
    cat << EOF
Run 'aws sts assume-role' operation to obtain temporary assumed role
credentials for the specified profile.  Export these credentials to
environment vars in the current shell.

Usage: aws-assume-role [-h]
Usage: aws-assume-role [--config-file <path>] [--config-dir <path>] <profile_name>

Args:
  -h: display help message
  --config-file <path>: path to aws config file where to look for profile
  --config-dir <path>:  path to directory wher to look for aws config files
  <profile_name>:       name of aws config profile defining the role to assume

EOF
  }

  local params
  case "$#" in
    1 )    case $1 in
             '-h' ) usage; return ;;
             * ) params="--profile $1" ;;
           esac ;;
    3 | 5) params=''
           while [ $# -gt 2 ]; do
             case $1 in
               '--config-file' ) params="${params} --config $2"; shift 2;;
               '--config-dir'  ) params="${params} --config-dir $2"; shift 2;;
               * ) usage; return ;;
             esac
           done
           params="${params} --profile $1" ;;
     * )   usage; return ;;
  esac

  if [ -n "$params" ]; then
    aws-drop-assumed-role
    result=$(awsassumerole $params)
    if [ "$?" -ne '0' ]; then
      echo $result
    else
      eval $result
    fi
  fi

}


aws-refresh() {
  usage() {
    cat << EOF

Reset mfa token. If environment var AWS_ASSUMED_ROLE_PROFILE is already
set from a previous session, then rerun 'aws sts assume-role' operation
for that profile.

Usage: aws-refresh [-h]

Args:
  -h: display help message
EOF
  }

  if [ $# -gt 0 ]; then
    #case $1 in
    #  '-h' ) usage ;;
    #  * ) return;;
    #esac
    usage
  else
    aws-set-mfa-token
    if [ -n "$AWS_ASSUMED_ROLE_PROFILE" ]; then
      aws-assume-role $AWS_ASSUMED_ROLE_PROFILE
    fi
  fi
}




aws-list-roles() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Print list of available AWS assume role profiles." ;;
      * ) return ;;
    esac
  else
    awsassumerole --list-profiles
  fi
}


aws-export-env() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Cache AWS environment vars to local file for use by other shells." ;;
      * ) return ;;
    esac
  else
    CACHE_DIR=$HOME/.aws/cache
    EXPORT_FILE=$CACHE_DIR/exported_env
    [ -d $CACHE_DIR ] || mkdir -p $CACHE_DIR
    env | grep --color=auto ^AWS | sort > $EXPORT_FILE
    perl -pi -e "s/^(.*)$/export \1/g" $EXPORT_FILE
    chmod 600 $EXPORT_FILE
  fi
}


aws-import-env() {
  if [ $# -gt 0 ]; then
    case $1 in
      '-h' ) echo "Evaluate cached AWS evironment vars into current shell." ;;
      * ) return ;;
    esac
  else
    CACHE_DIR=$HOME/.aws/cache
    EXPORT_FILE=$CACHE_DIR/exported_env
    if [ -f $EXPORT_FILE ]; then
      list=$(grep -v EXPIRATION $EXPORT_FILE)
      eval $list
    fi
  fi
}

