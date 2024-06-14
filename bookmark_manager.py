import sys
import json
import os

def load_bookmarks():
    # Проверяем, запущено ли приложение через PyInstaller
    if getattr(sys, 'frozen', False):
        # Если да, используем sys._MEIPASS для получения пути к файлу bookmarks.json
        bookmarks_path = os.path.join(sys._MEIPASS, 'bookmarks.json')
    else:
        # Если нет, предполагаем, что файл bookmarks.json находится в текущей директории
        bookmarks_path = 'bookmarks.json'

    try:
        with open(bookmarks_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

bookmarks = load_bookmarks()



def save_bookmarks(bookmarks):
    with open('bookmarks.json', 'w') as file:
        json.dump(bookmarks, file, indent=4, ensure_ascii=False)
