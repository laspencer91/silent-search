from setuptools import setup, find_packages

setup(
    name="silent-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=7.0",
        "toml>=0.10.0",
    ],
    entry_points={
        "console_scripts": [
            "sils=sils:sils",
        ],
    },
    author="Silent Commando",
    author_email="laspencer@live.com",
    description="A powerful command-line tool for searching and managing files by name and type",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/laspencer91/silent-search",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 