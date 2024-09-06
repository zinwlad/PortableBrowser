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
            data = json.load(file)
            print("Loaded bookmarks:", data)  # Для отладки
            return data
    except FileNotFoundError:
        print("Bookmarks file not found. Returning empty dictionary.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

bookmarks = load_bookmarks()
