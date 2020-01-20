import argparse
from pathlib import Path
import logging
import webbrowser
import time
import socket
import os

import requests
from Crypto.PublicKey import RSA

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

HOSTNAME = socket.gethostname()


def generate_public_private_keypair(bits, rsa_exponent):
    key = RSA.generate(bits, e=rsa_exponent)
    private_key = key.export_key()
    public_key = key.publickey().export_key('OpenSSH')
    return private_key, public_key.decode("utf-8")


def github_handler(api_url, public_key, username, token, ssh_label):
    url = f"{api_url}/user/keys"
    data = {"title": ssh_label, "key": public_key}
    r = requests.post(url, json=data, auth=(username, token))
    if r.status_code != 201:
        raise Exception(f"Failed to add public key - {r.text}")


def gitlab_handler(api_url, public_key, username, token, ssh_label):
    url = f"{api_url}/user/keys"
    data = {"title": ssh_label, "key": public_key, "private_token": token}
    r = requests.post(url, json=data)
    if r.status_code != 201:
        raise Exception(f"Failed to add public key - {r.text}")


def bitbucket_handler(api_url, public_key, username, token, ssh_label):
    url = f"{api_url}/users/{username}/ssh-keys"
    data = {"label": ssh_label, "key": public_key}
    r = requests.post(url, json=data, auth=(username, token))
    if r.status_code != 201:
        raise Exception(f"Failed to add public key - {r.text}")


def gogs_handler(api_url, public_key, username, token, ssh_label):
    url = f"{api_url}/user/keys"
    headers = {"Authorization": "token " + token}
    data = {"title": ssh_label, "key": public_key}
    r = requests.post(url, json=data, headers=headers)
    if r.status_code != 201:
        raise Exception(f"Failed to add public key - {r.text}")


INSTANCES_SUPPORTED = {
    "github": github_handler,
    "gitlab": gitlab_handler,
    "bitbucket": bitbucket_handler,
    "gogs": gogs_handler
}


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

    username = args.u
    instance_type = args.it
    if not args.t:
        if instance_type == "github":
            log.info("Please create personal app token with scope 'write:public_key', opening related webpage in 3 seconds")
            time.sleep(3)
            webbrowser.open(f"{url}/settings/tokens/new?scopes=write:public_key&description=generatessh")
            token = input("Token: ")
        elif instance_type == "gitlab":
            log.info("Please create personal app token with scope 'api', opening related webpage in 3 seconds")
            time.sleep(3)
            webbrowser.open(f"{url}/profile/personal_access_tokens")
            token = input("Token: ")
        elif instance_type == "bitbucket":
            log.info("Please create app password with permissions 'Account/Write', opening related webpage in 3 seconds")
            time.sleep(3)
            webbrowser.open(f"{url}/account/user/{username}/app-passwords")
            token = input("Token: ")
        elif instance_type == "gogs":
            log.info("Please create personal app token, opening related webpage in 3 seconds")
            time.sleep(3)
            webbrowser.open(f"{url}/user/settings/applications")
            token = input("Token: ")
        else:
            raise Exception("Unsupported instance type")
    else:
        token = args.t

    api_url = None
    if instance_type == "github":
        api_url = "https://api." + domain_without_scheme
        check_api_url = requests.get(api_url)
        if check_api_url.status_code == 404:
            api_url = f"https://{domain_without_scheme}/v3/api"
            check_api_url = requests.get(api_url)
            if check_api_url.status_code == 404:
                log.warn("Unable to identify API url, please provide it manually")
                api_url = input("API url: ")
                check_api_url = requests.get(api_url)
                if check_api_url.status_code == 404:
                    raise Exception("Invalid api url, receiving 404 response")
    elif instance_type == "gitlab":
        api_url = "https://" + domain_without_scheme + "/api/v4"
        check_api_url = requests.get(api_url + "/projects")
        if check_api_url.status_code == 404:
            log.warn("Unable to identify API url, please provide it manually")
            api_url = input("API url: ")
            check_api_url = requests.get(api_url + "/projects")
            if check_api_url.status_code == 404:
                raise Exception("Invalid api url, receiving 404 response")
    elif instance_type == "bitbucket":
        api_url = "https://api." + domain_without_scheme + "/2.0"
        check_api_url = requests.get(api_url + "/user")
        if check_api_url.status_code == 404:
            log.warn("Unable to identify API url, please provide it manually")
            api_url = input("API url: ")
            check_api_url = requests.get(api_url + "/user")
            if check_api_url.status_code == 404:
                raise Exception("Invalid api url, receiving 404 response")
    elif instance_type == "gogs":
        api_url = "https://" + domain_without_scheme + "/api/v1"
        check_api_url = requests.get(api_url + "/repos/search")
        if check_api_url.status_code == 404:
            log.warn("Unable to identify API url, please provide it manually")
            api_url = input("API url: ")
            check_api_url = requests.get(api_url + "/repos/search")
            if check_api_url.status_code == 404:
                raise Exception("Invalid api url, receiving 404 response")

    private_key, public_key = generate_public_private_keypair(
        args.bits,
        args.rsa_exponent
    )
    INSTANCES_SUPPORTED[args.it](api_url, public_key, username, token, args.ssh_label)

    with open(f"{home}/.ssh/{name}.pem", "wb") as file_out:
        file_out.write(private_key)

    with open(f"{home}/.ssh/config", "a") as file_out:
        s = f"\nHost {domain_without_scheme}\n\tHostName {domain_without_scheme}\n\tUser git\n\tIdentityFile {home}/.ssh/{name}.pem\n\n"
        file_out.write(s)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("it", type=str,
                        choices=INSTANCES_SUPPORTED.keys(),
                        help="instance type")
    PARSER.add_argument("url", type=str,
                        help="instance url")
    PARSER.add_argument("-u", type=str,
                        help="instance username")
    PARSER.add_argument("-t", dest='t', type=str,
                        help="personal application token")
    PARSER.add_argument("-n", "--name", dest='n', type=str,
                        help="name for private key")
    PARSER.add_argument("-b", "--bits", dest='bits', type=int,
                        default=4096, help="bits size for RSA key")
    PARSER.add_argument("-re", "--rsa-exponent", dest='rsa_exponent', type=int,
                        default=65537, help="rsa exponent for RSA key")
    PARSER.add_argument("-sl", "--ssh-label", dest='ssh_label', type=str,
                        default=HOSTNAME, help="ssh label in VCS")
    PARSER.add_argument("-v", "--verbosity", dest='v', type=int,
                        help="increase output verbosity")
    ARGS = PARSER.parse_args()

    process(ARGS)
