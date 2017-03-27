import os

from distutils.core import setup
from setuptools import find_packages

# Get version from defined python file
with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'bandit',
        'version.py'
    )
) as fh:
    version = fh.read().strip()
exec(version)

setup(
    name="bandit-cli",
    version=__version__,
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    url="https://github.com/yhat/yhat-client",
    packages=find_packages(),
    package_data={
        "bandit": [
            "dashboards/*.html",
        ]
    },
    description="Bandit client for Yhat (http://yhat.com/)",
    license="BSD",
    classifiers=(
    ),
    install_requires=[
        "pybars3==0.9.3",
        "requests==2.11.1"
    ],
    keywords=['yhat', 'bandit'],
)
