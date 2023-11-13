import hashlib
import json
import os
import logging


logger = logging.getLogger('my_logger')
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


# # Dictionary to store your redirection links
# redirection_links = {
#     "example": "https://www.example.com",
#     "google": "https://www.google.com",
#     # Add more redirection links as needed
# }


class LinkShortener:
    def __init__(self):
        self.db_file = '/srv/data/links_db.json'
        self.cache = {}

    def init_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.cache = json.load(f)

    def persist(self):
        if len(self.cache) > 0:
            with open(self.db_file, 'w') as f:
                json.dump(self.cache, f)

    def generate_link(self, url: str):
        if url in self.cache:
            page_link = self.cache[url]
        else:
            page_link = str(hashlib.md5(url.encode('utf-8')).hexdigest())[:6]
            self.cache[page_link] = url
            self.persist()
        return page_link

    def get_origin_link(self, short_url: str):
        if short_url in self.cache:
            page_link = self.cache[short_url]
        else:
            page_link = None
        return page_link

    def list(self):
        num_links = 10
        links = list(self.cache.keys())[:10]
        res = {}
        for k in links:
            res[k] = self.cache[k]
        return res


redirection_links = LinkShortener()
redirection_links.init_db()
