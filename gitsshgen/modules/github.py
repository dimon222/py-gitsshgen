from ..helpers import VCS, find_api_url
import webbrowser
import time
import logging

import requests

log = logging.getLogger(__name__)


class Github(VCS):
    def _find_api_url(self):
        api_url_variants = [
            f"https://api.{self.base_url}",
            f"https://{self.base_url}/api/v3"
        ]
        subpath = ""

        return find_api_url(api_url_variants, subpath)

    def _run_token_setup(self):
        log.info("Please create personal app token with scope 'write:public_key', opening related webpage in 3 seconds")
        time.sleep(3)
        webbrowser.open(f"https://{self.base_url}/settings/tokens/new?scopes=write:public_key&description=generatessh")
        return input("Token: ")

    def submit_ssh_key(self, public_key, ssh_label):
        url = f"{self.api_url}/user/keys"
        data = {"title": ssh_label, "key": public_key}
        r = requests.post(url, json=data, auth=(self.username, self.token))
        if r.status_code != 201:
            raise Exception(f"Failed to add public key - {r.text}")
