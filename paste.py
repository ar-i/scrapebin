#!/usr/bin/env python3

import requests

class Paste:

    raw_url = "https://scrape.pastebin.com/api_scrape_item.php?i="
    metadata_url = "https://scrape.pastebin.com/api_scrape_item_meta.php?i="

    def __init__(self, date, key, size, expire, title, user):
        self.date = date
        self.key = key
        self.size = size
        self.expire = expire or "none"
        self.title = title or "none"
        self.user = user or "none"

    def fetch_content(self):
        '''Fetches the (raw) content for the paste belonging to the provided
        key. Returns the data as a string'''
        full_content = requests.get(self.raw_url + self.key).text
        return full_content

    def store_locally(self, path, content):
        '''Stores the content for the paste belonging to the provided key in a
        local file. Returns the full file path as a string'''
        try:
            with open(path + self.key + ".txt", "w") as local_file:
                local_file.write(content)
        except Exception as error:
            print(f"[!] An error occured: {error}!")

    def regex_comparison(self,regex):
        '''Compares the content of the paste against a list of regular
        expressions for matches. Unclear if the comparison will be done before
        the local storage / database insertion or by manually checking all
        files.'''
