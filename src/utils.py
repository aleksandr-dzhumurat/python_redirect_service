from abc import ABC, abstractmethod
import hashlib
import json
import os
import logging

class DatabaseInterface(ABC):
    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def update_db(self, update_dict, new_items):
        pass


class PostgresInteractor(DatabaseInterface):
    def __init__(self):
        pass

    def read_all(self):
        from src.postgres_backend import read_links_mapping
        res = read_links_mapping()
        return res
    
    def update_db(self, update_dict, new_items):
        from src.postgres_backend import insert_links

        diff_dict = {k: update_dict[k] for k in new_items}
        insert_links(diff_dict)


class FileInteractor(DatabaseInterface):
    def __init__(self):
        self.db_file = os.environ['SHORTENER_DB_FILE']

    def read_all(self):
        res = {}
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                res = json.load(f)
        return res

    def update_db(self, update_dict, new_items):
        if len(new_items) > 0:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(update_dict, f, ensure_ascii=False)


class LinkShortener:
    def __init__(self):
        self.storage: DatabaseInterface = None
        self.cache = {}
        self.latest_short_urls = set()

    def init_db(self):
        if os.environ['STORAGE_BACKEND'] == 'json_file':
            self.storage = FileInteractor()
        elif os.environ['STORAGE_BACKEND'] == 'postgres':
            self.storage = FileInteractor()
        else:
            raise RuntimeError("Specify runtime backend: json_file or postgres")
        self.cache = self.storage.read_all()

    def persist(self):
        # TODO: add FastAPI backkground task to save every PERSIST_PERIOD_SEC = 30
        # import time; current_epoch_time = int(time.time())
        self.storage.update_db(self.cache, self.latest_short_urls)
        self.latest_short_urls = set()

    def generate_link(self, url: str):
        if url in self.cache:
            short_url = self.cache[url]
        else:
            short_url = str(hashlib.md5(url.encode('utf-8')).hexdigest())[:10]
            self.cache[short_url] = url
            self.latest_short_urls.add(short_url)
            self.persist()
        return short_url

    def get_origin_link(self, short_url: str):
        if short_url in self.cache:
            page_link = self.cache[short_url]
        else:
            page_link = None
        return page_link

    def list_links(self):
        NUM_LINKS = 10
        links = list(self.cache.keys())[:NUM_LINKS]
        res = {k: self.cache[k] for k in links}
        return res


logger = logging.getLogger('my_logger')
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

redirection_links = LinkShortener()
redirection_links.init_db()
