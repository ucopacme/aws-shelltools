"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from aws_shelltools import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-shelltools',
    version=__version__,
    description='Yet another set of scripts and shell functions for managing AWS profiles and cross account access.',
    long_description=long_description,
    url='https://github.com/ashleygould/aws-shelltools',
    author='Ashley Gould',
    author_email='agould@ucop.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='aws awscli session',
    packages=find_packages(exclude=['scratch', 'notes' ]),
    install_requires=[
        'awscli>=1.14.68',
        'boto3>=1.6.21',
        'botocore>=1.9.21',
        'docopt>=0.6.2',
        'aws-orgs',
    ],
    package_data={
        'aws_shelltools': ['shell_functions/*'],
    },
    entry_points={
        'console_scripts': [
            'awstoken=aws_shelltools.awstoken:main',
            'awsassumerole=aws_shelltools.awsassumerole:main',
            'aws-make-config=aws_shelltools.awsconfig:main',
            'aws-shelltools-setup=aws_shelltools.shelltools_setup:main',
        ],
    },
)
