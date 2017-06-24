#!/bin/bash

read -p "please enter 6 digit  otp for default aws account: " awsotp
eval `awstools.py --otp $awsotp`

