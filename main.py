import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QAction, QMenu, QMessageBox
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices

import site_data


class BookmarkMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мой Портативный Браузер")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        self.category_label = QLabel("Категории:")
        main_layout.addWidget(self.category_label)

        self.setup_bookmarks(main_layout)

        central_widget.setLayout(main_layout)

        # Контекстное меню для удаления закладок
        central_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        central_widget.customContextMenuRequested.connect(self.context_menu_event)

        self.show()

    def setup_bookmarks(self, layout):
        for category, sites in site_data.sites.items():
            category_widget = QWidget()
            category_layout = QVBoxLayout()
            category_layout.addWidget(QLabel(category))
            for site in sites:
                site_button = QPushButton(site["name"])
                site_button.clicked.connect(lambda _, s=site: self.open_website(s))
                category_layout.addWidget(site_button)
            category_widget.setLayout(category_layout)
            layout.addWidget(category_widget)

    def open_website(self, site):
        url = QUrl(site['url'])
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть сайт: {site['name']}")

    def context_menu_event(self, event):
        context_menu = QMenu(self)
        for category, sites in site_data.sites.items():
            for index, site in enumerate(sites):
                action_title = f"Удалить {site['name']}"
                action = QAction(action_title, context_menu)
                action.triggered.connect(lambda _, c=category, i=index: self.remove_bookmark(c, i))
                context_menu.addAction(action)
        context_menu.exec_(event.globalPos())

    def remove_bookmark(self, category, index):
        del site_data.sites[category][index]
        if not site_data.sites[category]:  # Если категория пустая, удалите её
            del site_data.sites[category]
        self.refresh_ui()  # Обновить интерфейс после удаления закладки

    def refresh_ui(self):
        # Очистить текущий интерфейс и перестроить его заново
        layout = self.centralWidget().layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.initUI()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BookmarkMainWindow()
    sys.exit(app.exec_())
