#!/bin/bash
#set -x

# Set shell var $AWS_Profile

usage() {
  echo "Usage: $(basename $0) <profile_name>"
}

if [ $# -gt 0 ]; then
  profile_name=$1
else
  usage
  exit 1
fi
#eval $(echo "export AWS_PROFILE=$profile_name")
echo "export AWS_PROFILE=$profile_name"
