from setuptools import setup, find_packages

setup(
    name="pr-diff-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyGithub==2.2.0",
        "python-dotenv==1.0.0",
        "gitpython==3.1.44",
        "openai==1.12.0",
        "requests==2.31.0",
        "python-semantic-release==8.7.0",
        "commitizen==3.31.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "pytest-mock==3.12.0",
        ],
    },
)