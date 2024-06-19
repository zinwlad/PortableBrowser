from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices

class BookmarkMainWindow(QMainWindow):
    def __init__(self, bookmarks):
        super().__init__()
        self.setWindowTitle("Мой Портативный Браузер")
        self.bookmarks = bookmarks
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QHBoxLayout()

        self.setup_bookmarks(self.bookmarks, self.scroll_layout)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        central_widget.setLayout(main_layout)

        self.adjust_window_size()
        self.show()

    def setup_bookmarks(self, bookmarks, layout):
        categories = list(bookmarks.items())
        half = len(categories) // 2

        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        for i in range(half):
            category, sites = categories[i]
            self.add_category_to_layout(left_column, category, sites)

        for i in range(half, len(categories)):
            category, sites = categories[i]
            self.add_category_to_layout(right_column, category, sites)

        layout.addLayout(left_column)
        layout.addLayout(right_column)

    def add_category_to_layout(self, layout, category, sites):
        category_widget = QWidget()
        category_layout = QVBoxLayout()
        category_layout.addWidget(QLabel(category))
        for site in sites:
            self.add_site_to_layout(category_layout, site)
        category_widget.setLayout(category_layout)
        layout.addWidget(category_widget)

    def add_site_to_layout(self, layout, site):
        site_button = QPushButton(site["name"])
        site_button.clicked.connect(lambda _, s=site: self.open_website(s))
        layout.addWidget(site_button)

        # Установка фиксированной ширины кнопки
        site_button.setFixedWidth(150)

    def open_website(self, site):
        url = QUrl(site['url'])
        if not QDesktopServices.openUrl(url):
            print(f"Не удалось открыть сайт: {site['name']}")

    def adjust_window_size(self):
        width = 450
        height = 650

        categories = list(self.bookmarks.items())
        half = len(categories) // 2

        item_height = 50
        total_height = max(half, len(categories) - half) * item_height

        if total_height > height:
            height = total_height

        self.setFixedSize(width, height)
