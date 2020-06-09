import logging
import socket
from abc import ABC, abstractmethod

import requests
import asyncssh

log = logging.getLogger(__name__)


def generate_public_private_keypair(algo, key_size, exponent,
                                    passphrase, cipher, rounds, hash_name):
    if algo == 'ssh-rsa':
        _private_key = asyncssh.generate_private_key(
            algo,
            key_size=key_size,
            exponent=exponent
        )
    else:
        _private_key = asyncssh.generate_private_key(
            algo
        )
    private_key = _private_key.export_private_key(
        'openssh',
        passphrase=passphrase,
        cipher_name=cipher,
        hash_name=hash_name,
        rounds=rounds
    )
    public_key = _private_key.export_public_key('openssh')
    return private_key, public_key.decode("utf-8")


def does_hostname_resolve(url):
    try:
        domain_without_scheme = url.split("://")[1].split("/")[0]
        socket.gethostbyname(domain_without_scheme)
        return True
    except socket.error:
        return False


def validate_url_existence(url):
    if does_hostname_resolve(url):
        check_api_url = requests.get(url)
        if check_api_url.status_code == 404:
            return False
        else:
            return True
    else:
        return False


def find_api_url(urls, subpath):
    api_url = None
    found = False
    for url in urls:
        found = validate_url_existence(url + subpath)
        if found:
            api_url = url
            break

    if not found:
        log.warn("Unable to identify API url, please provide it manually")
        api_url = input("API url: ")

    return api_url


class VCS(ABC):
    def __init__(self, base_url, username, token=None, api_url=None):
        self.base_url = base_url
        self.username = username

        if not api_url:
            self.api_url = self._find_api_url()
        else:
            self.api_url = api_url

        if not token:
            self.token = self._run_token_setup()
        else:
            self.token = token

    @abstractmethod
    def _find_api_url(self):
        pass

    @abstractmethod
    def _run_token_setup(self):
        pass

    @abstractmethod
    def submit_ssh_key(self, public_key, ssh_label):
        pass

    #@abstractmethod
    #def submit_gpg_key(self):
    #    pass
