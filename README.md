# py-gitsshgen
Automatic generation of SSH keys for VCS

## Why?
I was incredibly tired of doing the same procedure over and over for dozens of different VCS hosted in cloud and on-prem. There was no full-pledge solution offered even in `hub` and `lab` for end-to-end setup of SSH key for login to Git across different platforms.

## How to use?
The script generates RSA 4096 bits keypair and pushes public key to VCS using PAT (Personal Access Token) or App Password (Bitbucket only). The private key automatically goes to `~/.ssh/{name}.pem` + reference to it is appended to `~/.ssh/config` for automatic pickup by Git with OpenSSH configuration. The setup is assumed OpenSSH always.

```
usage: py-gitsshgen.py [-h] [-u U] [-t T] [-n N] [-b BITS] [-re RSA_EXPONENT] [-sl SSH_LABEL] [-v V] {github,gitlab,bitbucket,gogs} url

positional arguments:
  {github,gitlab,bitbucket,gogs}
                        instance type
  url                   instance url

optional arguments:
  -h, --help            show this help message and exit
  -u U                  instance username
  -t T                  personal application token
  -n N, --name N        name for private key
  -b BITS, --bits BITS  bits size for RSA key
  -re RSA_EXPONENT, --rsa-exponent RSA_EXPONENT
                        rsa exponent for RSA key
  -sl SSH_LABEL, --ssh-label SSH_LABEL
                        ssh label in VCS
  -v V, --verbosity V   increase output verbosity
```

Example with token:
`python create_ssh_key.py bitbucket bitbucket.org -u testusername -t testtoken`

If you don't provide token, script will open browser on page where you can make one, and ask you to enter it.
`python create_ssh_key.py bitbucket bitbucket.org -u testusername`

### VCS Compatibility
1. Github
2. Gitlab
3. Gogs
4. Bitbucket
