from ..helpers import VCS, find_api_url
import webbrowser
import time
import logging

import requests

log = logging.getLogger(__name__)


class Gitlab(VCS):
    def _find_api_url(self):
        api_url_variants = [
            f"https://{self.base_url}/api/v4"
        ]
        subpath = "/projects"

        return find_api_url(api_url_variants, subpath)

    def _run_token_setup(self):
        log.info("Please create personal app token with scope 'api', opening related webpage in 3 seconds")
        time.sleep(3)
        webbrowser.open(f"https://{self.base_url}/profile/personal_access_tokens")
        return input("Token: ")

    def submit_ssh_key(self, public_key, ssh_label):
        url = f"{self.api_url}/user/keys"
        data = {"title": ssh_label, "key": public_key, "private_token": self.token}
        r = requests.post(url, json=data)
        if r.status_code != 201:
            raise Exception(f"Failed to add public key - {r.text}")