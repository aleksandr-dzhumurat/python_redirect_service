import hashlib
import json
import os
import logging
import time


logger = logging.getLogger('my_logger')
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


class LinkShortener:
    def __init__(self):
        # TODO implement STORAGE interface
        self.db_file = '/srv/data/links_db.json'
        self.cache = {}

    def init_db(self):
        # TODO implement STORAGE interface
        if os.environ['STORAGE_BACKEND'] == 'json':
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    self.cache = json.load(f)
        elif os.environ['STORAGE_BACKEND'] == 'postgres':
            from src.postgres_backend import read_links

            self.cache = read_links()
        else:
            raise RuntimeError("Specify runtime backend")

    def persist(self):
        # TODO: add FastAPI backkground task
        # PERSIST_PERIOD_SEC = 30
        # current_epoch_time = int(time.time())
        # TODO implement STORAGE interface
        if os.environ['STORAGE_BACKEND'] == 'json':
            if len(self.cache) > 0:
                with open(self.db_file, 'w') as f:
                    json.dump(self.cache, f)
        elif os.environ['STORAGE_BACKEND'] == 'postgres':
            from src.postgres_backend import insert_links

            insert_links(self.cache)
        else:
            raise RuntimeError("Specify runtime backend")

    def generate_link(self, url: str):
        if url in self.cache:
            short_url = self.cache[url]
        else:
            short_url = str(hashlib.md5(url.encode('utf-8')).hexdigest())[:10]
            self.cache[short_url] = url
            self.persist()
        return short_url

    def get_origin_link(self, short_url: str):
        if short_url in self.cache:
            page_link = self.cache[short_url]
        else:
            page_link = None
        return page_link

    def list(self):
        NUM_LINKS = 10
        links = list(self.cache.keys())[:10]
        res = {}
        cnt = 0
        for k in links:
            if cnt > NUM_LINKS:
                break
            res[k] = self.cache[k]
            cnt += 1
        return res


redirection_links = LinkShortener()
redirection_links.init_db()
