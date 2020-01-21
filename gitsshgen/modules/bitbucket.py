from ..helpers import VCS, find_api_url
import webbrowser
import time
import logging

import requests

log = logging.getLogger(__name__)


class Bitbucket(VCS):
    def _find_api_url(self):
        api_url_variants = [
            f"https://{self.base_url}/2.0"
        ]
        subpath = "/user"

        return find_api_url(api_url_variants, subpath)

    def _run_token_setup(self):
        log.info("Please create app password with permissions 'Account/Write', opening related webpage in 3 seconds")
        time.sleep(3)
        webbrowser.open(f"{self.base_url}/account/user/{self.username}/app-passwords")
        return input("Token: ")

    def submit_ssh_key(self, public_key, ssh_label):
        url = f"{self.api_url}/users/{self.username}/ssh-keys"
        data = {"label": ssh_label, "key": public_key}
        r = requests.post(url, json=data, auth=(self.username, self.token))
        if r.status_code != 201:
            raise Exception(f"Failed to add public key - {r.text}")
