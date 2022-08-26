#!/usr/bin/env python3

from paste import Paste

import sqlite3
import argparse
import requests
import os
import configparser

# Temporarily set to 1 for development / debugging purposes
scraping_url = "https://scrape.pastebin.com/api_scraping.php?limit=100"

argument_parser = argparse.ArgumentParser(description="A simple scraper / parser for pastes from pastebin.com")
argument_parser.add_argument("--config", help="Path to config.ini, default is ./config.ini", default="./config.ini")
args = argument_parser.parse_args()

def configuration_parsing(filepath):
    '''Takes a file path, tries to open it and parse the content as .ini-based
    configuration'''
    try:
        with open(filepath, 'r') as configuration_file:
           file_content = configuration_file.read()
        try:
            configuration = configparser.ConfigParser()
            configuration.read(filepath)
            return configuration
        except Exception as e:
            print(f"[!] Could not parse {filepath}")
    except (FileNotFoundError, PermissionError):
        print(f"[!] Couldn't find / open {filepath}")

def smtp_notification(configuration, metadata):
    '''Notifies a pre-defined recipient via mail if a regular expression scores
    a hit on a fetched paste'''
    pass

def filesystem_check(conf):
    '''Checks if the provided path exists and is read-/writeable, tries to
    create it if it doesn't exist, exits on failure'''
    path = conf["general"]["path"]
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            if conf["general"]["debug"]:
                print(f"[!] ERROR: {path} does not exist!")
                print(f"[!] ERROR: Could not create {path}!")
                print(f"[!] Exiting ..")
    if not os.access(path, os.W_OK):
        if conf["general"]["debug"]:
            print(f"[!] ERROR: Could not write to {path}!")
            print(f"[!] Exiting ..")

def paste_creation(raw_data, conf, db_cursor):
	'''Creates a paste from the raw data provided to the function'''
	try:
		cur = Paste(raw_data["date"], raw_data["key"], raw_data["size"], raw_data["expire"], raw_data["title"], raw_data["user"])
		if conf["general"]["debug"]:
			print(f"[*] Currently working on {cur.key} ..")
			print(f"[*] Checking if {cur.key} is a duplicate ..")
		if cur.check_duplicates(db_cursor):
			if args.debug:
				print(f"[*] {key} is a duplicate!")
			return None
		if conf["general"]["debug"]:
			print(f"[*] Storing the content for {cur.key} ..")
		cur.store_locally(conf["general"]["path"], cur.fetch_content())
		if conf["general"]["debug"]:
			print(f"[*] Inserting {cur.key} into the database ..")
		cur.insert_into_db(db_cursor)

	except Exception as error:
		if conf["general"]["debug"]:
			print(f"[!] Unable to create paste {cur.key}!")

	return cur

def database_cursor(conf):
    '''Tries to connect to an SQLite-database and create the necessary table,
	returns a database cursor object'''
    create_db = "CREATE TABLE IF NOT EXISTS pastes (date text, key text PRIMARY KEY, expire INTEGER, size INTEGER, title TEXT, user TEXT, path TEXT)"
    try:
	    db_conn = sqlite3.connect(conf["general"]["path"] + "pastes.db")
	    db_cursor = db_conn.cursor()
	    db_cursor.execute(create_db)
	    return [db_cursor, db_conn]
    except Exception as e:
        print(e)

def scraping(conf, scraping_url):
	'''Scrapes the latest 100 (or whatever number is defined in scraping_url)
	pastes from pastebin.com, returns the JSON-object.'''
	try:
		paste_data = requests.get(scraping_url).json()
		return paste_data
	except Exception as e:
		if "debug" in conf["general"]:
			print("[!] Couldn't connect to Pastebin .. is your address whitelisted?\nError:\n\n\n{e}")
		else:
			print("[!] Couldn't connect to Pastebin .. is your address whitelisted?")
    
if __name__ == "__main__":
    conf = configuration_parsing(args.config)
    filesystem_check(conf)
    json_pastes = scraping(conf, scraping_url)
    db_cursor, db_conn = database_cursor(conf)
    for paste in json_pastes:
        paste_creation(paste, conf, db_cursor)
