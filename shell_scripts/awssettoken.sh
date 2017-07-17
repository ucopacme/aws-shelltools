#!/bin/bash
#set -x

aws-set-token() {
  read -p "please enter 6 digit token code for your MFA device: " code
  if [ -n "$code" ]; then
    eval `./awstools.py token --mfa-token $code`
  else
    eval `./awstools.py token`
  fi
}
