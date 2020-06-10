# py-gitsshgen
Automatic generation of SSH keys for VCS

## Why?
I was incredibly tired of doing the same procedure over and over for dozens of different VCS hosted in cloud and on-prem. There was no full-pledge solution offered even in `hub` and `lab` for end-to-end setup of SSH key for login to Git across different platforms.

## How to use?
The script generates OpenSSH keypair and pushes public key to VCS using PAT (Personal Access Token) or App Password (Bitbucket only). The private key automatically goes to `~/.ssh/{name}.pem` + reference to it is appended to `~/.ssh/config` for automatic pickup by Git with OpenSSH configuration. The setup is assumed OpenSSH always.

Supported parameters for key generation - https://asyncssh.readthedocs.io/en/latest/api.html#asyncssh.generate_private_key   
Supported parameters for private key export - https://asyncssh.readthedocs.io/en/latest/api.html#asyncssh.SSHKey.export_private_key

Default settings:
* Algo for generation - ssh-ed25519
* No passphrase
* Output private key with cipher AES256 with SHA256 hashing and 128 rounds of bcrypt.

You can install it using pip  
`pip install gitsshgen`

All actions are done interactively in terminal:  
```
usage: gitsshgen [-h] [-t T] [-api API_URL] [-n N] [-a ALGO] [-ks KEY_SIZE] [-e EXPONENT] [-p PASSPHRASE] [-c CIPHER] [-r ROUNDS] [-hn HASH_NAME] [-sl SSH_LABEL]
                 {github,gitlab,bitbucket,gogs,gitea} url u

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
  -a ALGO, --algorithm ALGO
                        algorithm for keypair (default is ssh-ed25519)
  -ks KEY_SIZE, --key-size KEY_SIZE
                        key size (only for RSA)
  -e EXPONENT, --exponent EXPONENT
                        exponent (only for RSA)
  -p PASSPHRASE, --passphrase PASSPHRASE
                        passphrase for OpenSSH key (default is None)
  -c CIPHER, --cipher CIPHER
                        cipher for OpenSSH key (default is aes256)
  -r ROUNDS, --rounds ROUNDS
                        rounds for OpenSSH key (default is 128)
  -hn HASH_NAME, --hash-name HASH_NAME
                        hash name for OpenSSH key (default is sha256)
  -sl SSH_LABEL, --ssh-label SSH_LABEL
                        ssh label in VCS
```

Example with token:  
`gitsshgen bitbucket bitbucket.org testusername -t testtoken`

If you don't provide token, script will open browser on page where you can make one, and ask you to enter it.  
`gitsshgen bitbucket bitbucket.org testusername`

### VCS Compatibility
1. Github
2. Gitlab
3. Gogs
4. Bitbucket
5. Gitea
