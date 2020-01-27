import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="gitsshgen",
    version="1.2.2",
    author="Dmitry Romanenko",
    author_email="Dmitry@Romanenko.in",
    description="Automatic generation of SSH keys for VCS",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dimon222/py-gitsshgen",
    packages=setuptools.find_packages(),
    license="Apache License 2.0",
    install_requires=[
        'requests',
        'pycryptodome'
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gitsshgen = gitsshgen:main'
        ]
    }
)
