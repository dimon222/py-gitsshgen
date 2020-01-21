from ..helpers import VCS, find_api_url
import webbrowser
import time
import logging

import requests

log = logging.getLogger(__name__)


class Gogs(VCS):
    def _find_api_url(self):
        api_url_variants = [
            f"https://{self.base_url}/api/v1"
        ]
        subpath = "/repos/search"

        return find_api_url(api_url_variants, subpath)

    def _run_token_setup(self):
        log.info("Please create personal app token, opening related webpage in 3 seconds")
        time.sleep(3)
        webbrowser.open(f"https://{self.base_url}/user/settings/applications")
        return input("Token: ")

    def submit_ssh_key(self, public_key, ssh_label):
        url = f"{self.api_url}/user/keys"
        headers = {"Authorization": "token " + self.token}
        data = {"title": ssh_label, "key": public_key}
        r = requests.post(url, json=data, headers=headers)
        if r.status_code != 201:
            raise Exception(f"Failed to add public key - {r.text}")
