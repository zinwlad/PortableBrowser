from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QScrollArea, QMessageBox)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QIcon
from typing import Dict, List
from sity_list import Bookmark  # Убедитесь, что вы импортируете Bookmark

class BookmarkMainWindow(QMainWindow):
    """Main window class for the bookmark application."""

    def __init__(self, bookmarks: Dict[str, List[Bookmark]]):
        """
        Initialize the main window.

        Args:
            bookmarks (Dict[str, List[Bookmark]]): A dictionary of bookmarks.
        """
        super().__init__()
        self.setWindowTitle("Мой Портативный Браузер")
        self.bookmarks = bookmarks
        self.initUI()

    def initUI(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QHBoxLayout()

        self.setup_bookmarks()

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        central_widget.setLayout(main_layout)

        self.adjust_window_size()
        self.show()

    def setup_bookmarks(self):
        """Set up the bookmark layout."""
        categories = list(self.bookmarks.items())
        half = len(categories) // 2

        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        for i, (category, sites) in enumerate(categories):
            layout = left_column if i < half else right_column
            self.add_category_to_layout(layout, category, sites)

        self.scroll_layout.addLayout(left_column)
        self.scroll_layout.addLayout(right_column)

    def add_category_to_layout(self, layout: QVBoxLayout, category: str, sites: List[Bookmark]):
        """
        Add a category of bookmarks to the layout.

        Args:
            layout (QVBoxLayout): The layout to add the category to.
            category (str): The name of the category.
            sites (List[Bookmark]): A list of sites in the category.
        """
        category_widget = QWidget()
        category_layout = QVBoxLayout()
        category_layout.addWidget(QLabel(f"<b>{category}</b>"))
        for site in sites:
            self.add_site_to_layout(category_layout, site)
        category_widget.setLayout(category_layout)
        layout.addWidget(category_widget)

    def add_site_to_layout(self, layout: QVBoxLayout, site: Bookmark):
        """
        Add a site button to the layout.

        Args:
            layout (QVBoxLayout): The layout to add the site button to.
            site (Bookmark): A Bookmark object containing site information.
        """
        site_button = QPushButton(site.name)
        site_button.clicked.connect(lambda _, s=site: self.open_website(s))
        site_button.setFixedWidth(150)
        if site.icon:
            site_button.setIcon(QIcon(site.icon))
        layout.addWidget(site_button)

    def open_website(self, site: Bookmark):
        """
        Open the website in the default browser.

        Args:
            site (Bookmark): A Bookmark object containing site information.
        """
        url = QUrl(site.url)
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть сайт: {site.name}")

    def adjust_window_size(self):
        """Adjust the window size based on the number of bookmarks."""
        width = 450
        height = 650

        categories = list(self.bookmarks.items())
        half = len(categories) // 2

        item_height = 50
        total_height = max(half, len(categories) - half) * item_height

        # Установить максимальные размеры окна
        self.setMinimumSize(300, 400)
        self.setMaximumSize(800, 1200)

        self.setFixedSize(width, max(height, total_height))

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
