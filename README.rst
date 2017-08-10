Yet another set of script and shell functions for managing AWS profiles and cross account access.


Install (as local user):

git clone https://github.com/ashleygould/aws-shelltools
pip install --user -e aws-shelltools/


Configure:
aws-shelltools-setup
. ~/.bashrc


Usage:
aws-profile <profile>
aws-make-config (awsconfig)
aws-list-profiles
aws-set-mfa-token
aws-assume-role <profile>

aws-display-assumed-role
aws-whoami
aws-env

aws-drop-assumed-role
aws-unset-mfa-token




Uninstall:
pip uninstall aws-shelltools
rm ~/.local/bin/{awstoken,awsassumerole,awsconfig,aws-shelltools-setup}
rm ./lib/python2.7/site-packages/aws-shelltools.egg-link
