#!/bin/bash
#set -x

aws-unset-token() {
  unset AWS_SECRET_ACCESS_KEY
  unset AWS_ACCESS_KEY_ID
  unset AWS_SESSION_TOKEN
  unset AWS_SESSION_TOKEN_EXPIRATION
}
