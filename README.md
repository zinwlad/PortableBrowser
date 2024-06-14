# Portable Browser Bookmarks Manager

This is a simple, portable browser bookmarks manager built using PyQt5. The application allows you to manage and organize your bookmarks into different categories, providing an easy-to-use interface for quick access to your favorite websites.

## Features

- **Add Bookmarks:** Add new bookmarks to different categories.
- **Delete Bookmarks:** Delete bookmarks through a context menu.
- **Search Bar:** Quickly search for bookmarks by category name.
- **Open Websites:** Click on bookmark buttons to open websites in your default browser.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/portable-browser-bookmarks-manager.git
    cd portable-browser-bookmarks-manager
    ```

2. **Install the required dependencies:**

    Make sure you have Python 3 installed. Then install the required packages using pip:

    ```bash
    pip install PyQt5
    ```

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Manage your bookmarks:**

    - **Add Bookmark:** Click on "Add Bookmark" button to add a new bookmark. Enter the category name, bookmark name, and URL.
    - **Delete Bookmark:** Right-click on a bookmark to delete it.
    - **Search:** Use the search bar to filter bookmarks by category.

## File Structure

- `main.py`: Entry point of the application. Initializes the main window.
- `bookmark_main_window.py`: Contains the main window class `BookmarkMainWindow` which manages the UI and bookmark operations.
- `sity_list.py`: Contains the bookmark data and functions to load and save bookmarks.


