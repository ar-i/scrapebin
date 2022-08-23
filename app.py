#!/usr/bin/env python3

from paste import Paste

import sqlite3
import argparse
import requests
import os

# Temporarily set to 1 for development / debugging purposes
scraping_url = "https://scrape.pastebin.com/api_scraping.php?limit=100"

argument_parser = argparse.ArgumentParser(description="A simple scraper / parser for pastes from pastebin.com")
argument_parser.add_argument("path", help="The full path for where the data will be stored", type=str)
argument_parser.add_argument("--debug", help="Increases output verbosity", action="store_true")
argument_parser.add_argument("--regex", help="Textfile containing regular expressions to be checked for")
args = argument_parser.parse_args()

def smtp_notification(configuration, metadata):
    '''Notifies a pre-defined recipient via mail if a regular expression scores
    a hit on a fetched paste'''
    pass

def filesystem_check(path):
    '''Checks if the provided path exists and is read-/writeable, tries to
    create it if it doesn't exist, exits on failure'''
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            if args.debug:
                print(f"[!] ERROR: {args.path} does not exist!")
                print(f"[!] ERROR: Could not create {args.path}!")
                print(f"[!] Exiting ..")
    if not os.access(args.path, os.W_OK):
        if args.debug:
            print(f"[!] ERROR: Could not write to {args.path}!")
            print(f"[!] Exiting ..")

def paste_creation(raw_data):
    '''Creates a paste from the raw data provided to the function'''
    try:
        cur = Paste(raw_data["date"], raw_data["key"], raw_data["size"], raw_data["expire"], raw_data["title"], raw_data["user"])
        if args.debug:
            print(f"[*] Currently working on {cur.key} ..")
            print(f"[*] Storing the content for {cur.key} in {args.path} ..")
        cur.store_locally(args.path, cur.fetch_content())

        cur.path = args.path + cur.key + ".txt"
        if args.debug:
            print(f"[*] Inserting {cur.key} into the database ..")

    except Exception as error:
        print(error)
        print(f"[!] Unable to create paste {cur.key}!")
    return cur

# Main execution starts here, open database file, check if table exists & create
# if it does not
try:
    db_conn = sqlite3.connect(args.path + "pastes.db")
    create_db = "CREATE TABLE IF NOT EXISTS pastes (date text, key text PRIMARY KEY, expire INTEGER, size INTEGER, title TEXT, user TEXT, path TEXT)"
    db_conn.execute(create_db)
except Exception as e:
    print(e)
    
# Fetch the raw JSON for the latest pastes
# FIXME: Error handling, currently dies quietly
paste_data = requests.get(scraping_url).json()

for paste in paste_data:
    cur = paste_creation(paste)
    insert_into_db(db_conn, [y for x, y in cur.__dict__.items()])
    if args.regex:
        cur.regex_comparison(regexes)
    

db_conn.commit()
db_conn.close()
