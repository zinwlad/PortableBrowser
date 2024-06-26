#bookmark_manager.py
import sys
import json
import os

def load_bookmarks():
    if getattr(sys, 'frozen', False):
        bookmarks_path = os.path.join(sys._MEIPASS, 'bookmarks.json')
    else:
        bookmarks_path = 'bookmarks.json'
    try:
        with open(bookmarks_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

bookmarks = load_bookmarks()



