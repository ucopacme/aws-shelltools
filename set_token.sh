#!/bin/bash

read -p "please enter 6 digit token code for your MFA device: " code
eval `awstools.py --mfa-token $code`

