#!/usr/bin/env python3

class Paste:

    standard_url = "https://pastebin.com/"
    raw_url = "https://pastebin.com/raw/"

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
        pass

    def store_locally(key, content):
        '''Stores the content for the paste belonging to the provided key in a
        local file. Returns the full file path as a string'''
        pass

    def all_pastes_for_user(username, database_object):
        '''Queries the database for all pastes authored by a supplied user,
        returns a list of URLs'''
        pass
