#sity_list.py

from typing import List, Dict, NamedTuple

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

def get_all_categories() -> List[str]:
    """Return a list of all bookmark categories."""
    return list(bookmarks.keys())

def get_bookmarks_for_category(category: str) -> List[Bookmark]:
    """Return all bookmarks for a given category."""
    return bookmarks.get(category, [])

def add_bookmark(category: str, name: str, url: str, icon: str = "") -> None:
    """Add a new bookmark to a category."""
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
