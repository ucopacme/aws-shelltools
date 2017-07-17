"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-shelltools',
    version='0.0.1.dev1',
    description='Yet another set of script and shell functions for managing AWS profiles and cross account access.',
    long_description=long_description,
    url='https://github.com/ashleygould/aws-shelltools',
    author='Ashley Gould',
    author_email='agould@ucop.edu',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='aws session',
    packages=find_packages(exclude=['shell_scripts', 'scratch', 'notes' ]),
    install_requires=['boto3', 'docopt'],
    package_data={
        'aws-shelltools': ['shell_functions'],
    },
    entry_points={
        'console_scripts': [
            'awstoken.py=awstoken:main',
        ],
    },
)
