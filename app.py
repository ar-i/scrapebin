#!/usr/bin/env python3

from paste import Paste

import sqlite3
import argparse
import requests
import os

scraping_url = "https://scrape.pastebin.com/api_scraping.php?limit=5"

argument_parser = argparse.ArgumentParser(description="A simple scraper / parser for pastes from pastebin.com")
argument_parser.add_argument("path", help="The full path for where the data will be stored", type=str)
argument_parser.add_argument("--debug", help="Increases output verbosity", action="store_true")
args = argument_parser.parse_args()

# Check if the provided path exists, try to create if if not - exit if that's
# not possible
if not os.path.isdir(args.path):
    try:
        os.mkdir(args.path)
    except:
        if args.debug:
            print(f"[!] ERROR: {args.path} does not exist!")
            print(f"[!] ERROR: Could not create {args.path}!")
            print(f"[!] Exiting ..")
else:
    # If the provided path exists, see if it can be written to - exit if that's
    # not possible
    if not os.access(args.path, os.W_OK):
        if args.debug:
            print(f"[!] ERROR: Could not write to {args.path}!")
            print(f"[!] Exiting ..")

# This is a function so it's easier to use if I have to implement
# multiprocessing
def paste_creation(raw_data):
	try:
		cur = Paste(raw_data["date"], raw_data["key"], raw_data["size"], raw_data["expire"], raw_data["title"], raw_data["user"])
		if args.debug:
			print(f"[*] Currently working on {cur.key} ..")
			print(f"[*] Storing the content for {cur.key} in {fp} ..")
		cur.store_locally(args.path, cur.fetch_content())

		cur.path = args.path + cur.key + ".txt"
		if args.debug:
			print(f"[*] Inserting {cur.key} into the database ..")

	except Exception as error:
		print(f"[!] Unable to create paste {cur.key}!")
	return cur

def insert_into_db(db_cursor, data):
    '''Inserts the metadata of a paste into a database table.'''
    insert_query = '''INSERT INTO pastes(date, key, size, expire, title, user,
    path) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    try:
        db_cursor.execute(insert_query, data)
        db_cursor.commit()
    except Exception as e:
        print(e)

# Main execution starts her, open database file, check if table exists & create
# if it does not
try:
    db_conn = sqlite3.connect(args.path + "pastes.db")
    create_db = "CREATE TABLE IF NOT EXISTS pastes (date text, key text PRIMARY KEY, expire INTEGER, size INTEGER, title TEXT, user TEXT, path TEXT)"
    db_conn.execute(create_db)
except Exception as e:
    print(e)
    
# Fetch the raw JSON for the latest pastes
paste_data = requests.get(scraping_url).json()

for paste in paste_data:
	cur = paste_creation(paste)
	print([y for x, y in cur.__dict__.items()])
	insert_into_db(db_conn, [y for x, y in cur.__dict__.items()])

db_conn.commit()
db_conn.close()
