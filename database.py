#!/usr/bin/env python3

import sqlite3

def insert_into_db(db_cursor, data):
    '''Inserts the metadata of a paste into a database table.'''
    insert_query = '''INSERT INTO pastes(key, path, date, size, expire, title,
    user) VALUES (?, ?, ?, ?, ?, ?, ?,)'''
    try:
        db_cursor.execute(insert_query, data)
        db_cursor.commit()
    except Exception as e:
        pass

def search_for_author(author):
    '''Searches for all pastes by the provided author, returns the result as a
    list'''
    pass

def search_for_regex(regex):
    '''Searches for one or more regular expressions in the content of all
    pastes, returns a list of keys of pastes which a match was found in.'''
    pass
