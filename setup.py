import setuptools

import sshtop

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="sshtop",
    version="1.2.0",
    license="MIT",
    author="Kamil 'EXLER' Marut",
    author_email="kakkmar@gmail.com",
    description="Remote server monitoring tool over plain SSH.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exler/sshtop",
    install_requires=["paramiko"],
    packages=["sshtop"],
    entry_points={"console_scripts": ["sshtop = sshtop.cli:connection"]},
    classifiers=[
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
