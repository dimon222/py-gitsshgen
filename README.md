# py-gitsshgen
Automatic generation of SSH keys for VCS

## Why?
I was incredibly tired of doing the same procedure over and over for dozens of different VCS hosted in cloud and on-prem. There was no full-pledge solution offered even in `hub` and `lab` for end-to-end setup of SSH key for login to Git across different platforms.

## How to use?
The script generates RSA 4096 bits keypair and pushes public key to VCS using PAT (Personal Access Token) or App Password (Bitbucket only). The private key automatically goes to `~/.ssh/{name}.pem` + reference to it is appended to `~/.ssh/config` for automatic pickup by Git with OpenSSH configuration. The setup is assumed OpenSSH always.

You can install it using pip  
`pip install gitsshgen`

All actions are done interactively in terminal:  
```
usage: gitsshgen [-h] [-t T] [-api API_URL] [-n N] [-b BITS] [-re RSA_EXPONENT] [-sl SSH_LABEL] {github,gitlab,bitbucket,gogs,gitea} url u

positional arguments:
  {github,gitlab,bitbucket,gogs,gitea}
                        instance type
  url                   instance url
  u                     instance username

optional arguments:
  -h, --help            show this help message and exit
  -t T                  personal application token
  -api API_URL          API URL endpoint
  -n N, --name N        name for private key
  -b BITS, --bits BITS  bits size for RSA key
  -re RSA_EXPONENT, --rsa-exponent RSA_EXPONENT
                        rsa exponent for RSA key
  -sl SSH_LABEL, --ssh-label SSH_LABEL
                        ssh label in VCS
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
