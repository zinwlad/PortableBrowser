"""
Module for managing bookmarks organized by categories.

This module provides functionality to store and manage bookmarks with their URLs and icons,
organized into different categories. It supports operations like adding, removing,
and retrieving bookmarks.

Example:
    >>> get_all_categories()
    ['ИИ', 'Учеба', 'Почта', ...]
    >>> get_bookmarks_for_category('ИИ')
    [Bookmark(name='ChatGPT', url='https://chat.openai.com', icon='icons/chatgpt.png'), ...]
"""

from typing import List, Dict, NamedTuple, Optional
from urllib.parse import urlparse

class Bookmark(NamedTuple):
    name: str
    url: str
    icon: str = ""

bookmarks: Dict[str, List[Bookmark]] = {
    "ИИ": [
        Bookmark(name="ChatGPT", url="https://chat.openai.com", icon="icons/chatgpt.png"),
        Bookmark(name="Google Gemini", url="https://gemini.google.com/app", icon="icons/gemini.png"),
        Bookmark(name="Яндекс Алиса", url="https://yandex.ru/alice", icon="icons/alice.png"),
        Bookmark(name="Bing AI", url="https://www.bing.com/new", icon="icons/bing.png")
    ],
    "Учеба": [
        Bookmark(name="Skillbox", url="https://skillbox.ru", icon="icons/skillbox.png"),
        Bookmark(name="GitHub", url="https://github.com", icon="icons/github.png"),
        Bookmark(name="Stepik", url="https://stepik.org", icon="icons/stepik.png"),
        Bookmark(name="GitLab", url="https://gitlab.com", icon="icons/gitlab.png")
    ],
    "Почта": [
        Bookmark(name="Gmail", url="https://mail.google.com", icon="icons/gmail.png"),
        Bookmark(name="Mail.ru", url="https://mail.ru", icon="icons/mailru.png"),
        Bookmark(name="Rambler", url="https://mail.rambler.ru", icon="icons/rambler.png"),
        Bookmark(name="Яндекс.Почта", url="https://mail.yandex.ru", icon="icons/yandex.png")
    ],
    "Развлечение": [
        Bookmark(name="YouTube", url="https://www.youtube.com", icon="icons/youtube.png"),
        Bookmark(name="ВКонтакте", url="https://vk.com", icon="icons/vk.png"),
        Bookmark(name="Лайфхакер", url="https://lifehacker.ru", icon="icons/lifehacker.png"),
        Bookmark(name="Fishki.net", url="https://fishki.net", icon="icons/fishki.png")
    ],
    "Полезное": [
        Bookmark(name="Google Диск", url="https://drive.google.com", icon="icons/gdrive.png"),
        Bookmark(name="2ГИС", url="https://2gis.ru", icon="icons/2gis.png"),
        Bookmark(name="Программы", url="https://howdyho.net", icon="icons/howdyho.png"),
        Bookmark(name="Temp-Mail", url="https://temp-mail.org", icon="icons/tempmail.png"),
        Bookmark(name="DropMeFiles", url="https://dropmefiles.com", icon="icons/dropmefiles.png")
    ],
    "Фильмы и новости": [
        Bookmark(name="Seasonvar", url="http://seasonvar.ru", icon="icons/seasonvar.png"),
        Bookmark(name="Kinobar", url="https://kinobar.vip", icon="icons/kinobar.png"),
        Bookmark(name="Reuters", url="https://www.reuters.com", icon="icons/reuters.png")
    ],
    "Переводчики": [
        Bookmark(name="DeepL", url="https://www.deepl.com/translator", icon="icons/deepl.png"),
        Bookmark(name="Google Переводчик", url="https://translate.google.com", icon="icons/gtranslate.png"),
        Bookmark(name="Яндекс.Переводчик", url="https://translate.yandex.ru", icon="icons/ytranslate.png")
    ],
    "Клипарты": [
        Bookmark(name="Freepik", url="https://www.freepik.com", icon="icons/freepik.png"),
        Bookmark(name="Vecteezy", url="https://www.vecteezy.com", icon="icons/vecteezy.png"),
        Bookmark(name="All-free-download", url="https://all-free-download.com/free-vectors",
         icon="icons/allfreedownload.png"),
        Bookmark(name="SVG Repo", url="https://www.svgrepo.com", icon="icons/svgrepo.png")
    ]
}

def validate_url(url: str) -> bool:
    """
    Validate if the given string is a proper URL.
    
    Args:
        url: String to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_all_categories() -> List[str]:
    """Return a list of all bookmark categories."""
    return list(bookmarks.keys())

def get_bookmarks_for_category(category: str) -> List[Bookmark]:
    """Return all bookmarks for a given category."""
    return bookmarks.get(category, [])

def search_bookmarks(query: str) -> List[tuple[str, Bookmark]]:
    """
    Search for bookmarks across all categories by name.
    
    Args:
        query: Search string to match against bookmark names
        
    Returns:
        List of tuples containing category and matching bookmarks
    """
    results = []
    for category, category_bookmarks in bookmarks.items():
        for bookmark in category_bookmarks:
            if query.lower() in bookmark.name.lower():
                results.append((category, bookmark))
    return results

def update_bookmark(category: str, old_name: str, new_name: str = None, 
                   new_url: str = None, new_icon: str = None) -> bool:
    """
    Update an existing bookmark's properties.
    
    Args:
        category: Category containing the bookmark
        old_name: Current name of the bookmark to update
        new_name: New name for the bookmark (optional)
        new_url: New URL for the bookmark (optional)
        new_icon: New icon path for the bookmark (optional)
        
    Returns:
        bool: True if bookmark was updated, False if not found
    """
    if category not in bookmarks:
        return False
        
    for i, bookmark in enumerate(bookmarks[category]):
        if bookmark.name == old_name:
            name = new_name or bookmark.name
            url = new_url or bookmark.url
            icon = new_icon or bookmark.icon
            
            if new_url and not validate_url(new_url):
                raise ValueError("Invalid URL provided")
                
            bookmarks[category][i] = Bookmark(name=name, url=url, icon=icon)
            return True
    return False

def add_bookmark(category: str, name: str, url: str, icon: str = "") -> None:
    """
    Add a new bookmark to a category.
    
    Args:
        category: Category to add the bookmark to
        name: Name of the bookmark
        url: URL of the bookmark
        icon: Path to the bookmark's icon (optional)
        
    Raises:
        ValueError: If the URL is invalid
    """
    if not validate_url(url):
        raise ValueError("Invalid URL provided")
        
    if category not in bookmarks:
        bookmarks[category] = []
    bookmarks[category].append(Bookmark(name=name, url=url, icon=icon))

def remove_bookmark(category: str, name: str) -> bool:
    """Remove a bookmark from a category."""
    if category in bookmarks:
        initial_count = len(bookmarks[category])
        bookmarks[category] = [b for b in bookmarks[category] if b.name != name]
        return len(bookmarks[category]) < initial_count
    return False

if __name__ == "__main__":
    print("Available categories:", get_all_categories())
    print("Bookmarks in 'ИИ' category:", get_bookmarks_for_category("ИИ"))
