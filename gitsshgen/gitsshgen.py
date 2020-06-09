import argparse
from pathlib import Path
import logging
import os
import socket
from importlib import import_module

from .helpers import generate_public_private_keypair

HOSTNAME = socket.gethostname()
log = logging.getLogger(__name__)

SUPPORTED_INSTANCE_TYPES = [
    "github",
    "gitlab",
    "bitbucket",
    "gogs",
    "gitea"
]


def process(args):
    if args.u is None:
        raise Exception("Please provide username")

    if "://" not in args.url:
        url = "https://" + args.url.strip("/")
    else:
        url = args.url.strip("/")

    domain_without_scheme = url.split("://")[1]

    name = None
    if args.n is None:
        name = domain_without_scheme.replace(".", "_")
    else:
        name = args.n

    home = str(Path.home())
    if not os.path.exists(f"{home}/.ssh"):
        os.mkdir(f"{home}/.ssh")

    if os.path.exists(f"{home}/.ssh/{name}.pem"):
        raise Exception(f"There's already private key in {home}/.ssh/{name}.pem, please remove it first")

    vcs_package = import_module('.modules.' + args.it, 'gitsshgen')
    vcs_module = getattr(vcs_package, args.it.capitalize())(domain_without_scheme, args.u, args.t, args.api_url)
    private_key, public_key = generate_public_private_keypair(
        args.algo,
        args.key_size,
        args.exponent,
        args.passphrase,
        args.cipher,
        args.rounds,
        args.hash_name
    )
    vcs_module.submit_ssh_key(public_key, args.ssh_label)

    with open(f"{home}/.ssh/{name}.pem", "wb") as file_out:
        file_out.write(private_key)

    os.chmod(f"{home}/.ssh/{name}.pem", 0o700)

    with open(f"{home}/.ssh/config", "a") as file_out:
        s = f"\nHost {domain_without_scheme}\nHostName {domain_without_scheme}\nUser git\nIdentityFile {home}/.ssh/{name}.pem\nIdentitiesOnly yes\nPreferredAuthentications publickey\n\n"
        file_out.write(s)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("it", type=str,
                        choices=SUPPORTED_INSTANCE_TYPES,
                        help="instance type")
    parser.add_argument("url", type=str,
                        help="instance url")
    parser.add_argument("u", type=str,
                        help="instance username")
    parser.add_argument("-t", dest='t', type=str,
                        help="personal application token")
    parser.add_argument("-api", dest='api_url', type=str,
                        help="API URL endpoint")
    parser.add_argument("-n", "--name", dest='n', type=str,
                        help="name for private key")
    parser.add_argument("-a", "--algorithm", dest='algo', type=str,
                        default='ssh-ed25519', help="algorithm for keypair (default is ssh-ed25519)")
    parser.add_argument("-ks", "--key-size", dest='key_size', type=int,
                        default=None, help="key size (only for RSA)")
    parser.add_argument("-e", "--exponent", dest='exponent', type=int,
                        default=None, help="exponent (only for RSA)")
    parser.add_argument("-p", "--passphrase", dest='passphrase', type=int,
                        default=None, help="passphrase for OpenSSH key (default is None)")
    parser.add_argument("-c", "--cipher", dest='cipher', type=str,
                        default='aes256', help="cipher for OpenSSH key (default is aes256)")
    parser.add_argument("-r", "--rounds", dest='rounds', type=int,
                        default=128, help="rounds for OpenSSH key (default is 128)")
    parser.add_argument("-hn", "--hash-name", dest='hash_name', type=str,
                        default='sha256', help="hash name for OpenSSH key (default is sha256)")
    parser.add_argument("-sl", "--ssh-label", dest='ssh_label', type=str,
                        default=HOSTNAME, help="ssh label in VCS")
    #parser.add_argument("-v", "--verbosity", dest='v', type=int,
    #                    help="increase output verbosity")
    args = parser.parse_args()

    process(args)


if __name__ == "__main__":
    main()
