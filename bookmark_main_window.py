from functools import partial
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QAction, QMenu, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
import sity_list  # Импортируем модуль для работы со списком закладок

class BookmarkMainWindow(QMainWindow):
    def __init__(self, bookmarks):
        super().__init__()
        self.setWindowTitle("Мой Портативный Браузер")
        self.bookmarks = bookmarks  # Загружаем закладки из модуля sity_list
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()

        self.category_label = QLabel("Категории:")
        self.main_layout.addWidget(self.category_label)

        self.setup_bookmarks(self.bookmarks, self.main_layout)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Поиск...")
        self.search_bar.textChanged.connect(self.filter_bookmarks)
        self.main_layout.addWidget(self.search_bar)

        add_button = QPushButton("Добавить закладку")
        add_button.clicked.connect(self.add_bookmark)
        self.main_layout.addWidget(add_button)

        central_widget.setLayout(self.main_layout)

        # Контекстное меню для удаления закладок
        central_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        central_widget.customContextMenuRequested.connect(self.context_menu_event)

        self.show()

    def setup_bookmarks(self, bookmarks, layout):
        for category, sites in bookmarks.items():
            if sites:  # Добавлять только непустые категории
                self.add_category_to_layout(layout, category, sites)

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
        site_button.clicked.connect(partial(self.open_website, site))
        layout.addWidget(site_button)

    def open_website(self, site):
        url = QUrl(site['url'])
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть сайт: {site['name']}")

    def context_menu_event(self, event):
        context_menu = QMenu(self)
        for category, sites in self.bookmarks.items():
            for index, site in enumerate(sites):
                action_title = f"Удалить {site['name']}"
                action = QAction(action_title, context_menu)
                action.triggered.connect(partial(self.remove_bookmark, category, index))
                context_menu.addAction(action)
        context_menu.exec_(event.globalPos())

    def remove_bookmark(self, category, index):
        if category in self.bookmarks and index < len(self.bookmarks[category]):
            del self.bookmarks[category][index]
            if not self.bookmarks[category]:  # Если категория пустая, удалите её
                del self.bookmarks[category]
            sity_list.save_bookmarks(self.bookmarks)  # Сохранить изменения в модуле sity_list
            self.refresh_ui()  # Обновить интерфейс после удаления закладки

    def refresh_ui(self):
        layout = self.centralWidget().layout()
        # Удалить все виджеты из layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Заново добавить виджеты
        self.setup_bookmarks(self.bookmarks, layout)

        # Повторно добавить строку поиска и кнопку добавления закладок
        self.main_layout.addWidget(self.search_bar)
        add_button = QPushButton("Добавить закладку")
        add_button.clicked.connect(self.add_bookmark)
        self.main_layout.addWidget(add_button)

    def add_bookmark(self):
        category, ok = QInputDialog.getText(self, 'Новая категория', 'Введите имя категории:')
        if ok and category:
            site_name, ok = QInputDialog.getText(self, 'Новая закладка', 'Введите имя закладки:')
            if ok and site_name:
                site_url, ok = QInputDialog.getText(self, 'Новая закладка', 'Введите URL закладки:')
                if ok and site_url:
                    if category not in self.bookmarks:
                        self.bookmarks[category] = []
                    self.bookmarks[category].append({"name": site_name, "url": site_url})
                    sity_list.save_bookmarks(self.bookmarks)  # Сохранить изменения в модуле sity_list
                    self.refresh_ui()  # Обновить интерфейс после добавления закладки

    def filter_bookmarks(self, text):
        layout = self.centralWidget().layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QWidget):
                category_label = widget.layout().itemAt(0).widget()
                if text.lower() in category_label.text().lower():
                    widget.show()
                else:
                    widget.hide()
