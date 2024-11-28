"""
Main window class for the bookmark application.
Provides a user interface for displaying and managing bookmarks.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QScrollArea, QMessageBox,
                           QMenu, QSystemTrayIcon, QLineEdit, QFrame)
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QIcon, QCloseEvent
import logging
from typing import Dict, List, Any, Optional
from sity_list import Bookmark, add_bookmark, remove_bookmark

logger = logging.getLogger(__name__)

class CollapsibleCategory(QWidget):
    """Widget for a collapsible category of bookmarks."""
    
    def __init__(self, category: str, parent=None):
        super().__init__(parent)
        self.category = category
        self.is_collapsed = False
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with category name and collapse button
        header = QHBoxLayout()
        self.toggle_button = QPushButton("▼")
        self.toggle_button.setFixedWidth(20)
        self.toggle_button.clicked.connect(self.toggle_collapse)
        header.addWidget(self.toggle_button)
        
        header.addWidget(QLabel(f"<b>{category}</b>"))
        header.addStretch()
        
        # Container for bookmarks
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        
        layout.addLayout(header)
        layout.addWidget(self.content)
        
        # Add separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
    def toggle_collapse(self):
        """Toggle the collapsed state of the category."""
        self.is_collapsed = not self.is_collapsed
        self.content.setVisible(not self.is_collapsed)
        self.toggle_button.setText("▶" if self.is_collapsed else "▼")

class BookmarkMainWindow(QMainWindow):
    """Main window class for the bookmark application."""
    
    bookmark_added = pyqtSignal(str, Bookmark)
    bookmark_removed = pyqtSignal(str, str)

    def __init__(self, bookmarks: Dict[str, List[Bookmark]], config: Dict[str, Any]):
        """
        Initialize the main window.

        Args:
            bookmarks (Dict[str, List[Bookmark]]): A dictionary of bookmarks
            config (Dict[str, Any]): Application configuration
        """
        super().__init__()
        self.setWindowTitle("Мой Портативный Браузер")
        self.setWindowIcon(QIcon("icons/app.png"))
        self.bookmarks = bookmarks
        self.config = config
        self.category_widgets = {}  # Store category widgets for easy access
        self.initUI()
        
        # Connect signals
        self.bookmark_added.connect(self.refresh_category)
        self.bookmark_removed.connect(self.refresh_category)

    def initUI(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Add search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск закладок...")
        self.search_input.textChanged.connect(self.filter_bookmarks)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Bookmark area
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
        try:
            categories = list(self.bookmarks.items())
            half = len(categories) // 2

            left_column = QVBoxLayout()
            right_column = QVBoxLayout()

            for i, (category, sites) in enumerate(categories):
                layout = left_column if i < half else right_column
                category_widget = CollapsibleCategory(category)
                self.category_widgets[category] = category_widget
                for site in sites:
                    self.add_site_to_layout(category_widget.content_layout, site, category)
                layout.addWidget(category_widget)

            left_column.addStretch()
            right_column.addStretch()
            
            self.scroll_layout.addLayout(left_column)
            self.scroll_layout.addLayout(right_column)
            
            logger.info(f"Successfully set up {len(categories)} bookmark categories")
            
        except Exception as e:
            logger.error(f"Error setting up bookmarks: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить все закладки")

    def add_site_to_layout(self, layout: QVBoxLayout, site: Bookmark, category: str):
        """
        Add a site button to the layout.

        Args:
            layout (QVBoxLayout): The layout to add the site button to
            site (Bookmark): A Bookmark object containing site information
            category (str): The category this bookmark belongs to
        """
        site_button = QPushButton(site.name)
        site_button.setContextMenuPolicy(Qt.CustomContextMenu)
        site_button.customContextMenuRequested.connect(
            lambda pos, s=site, c=category: self.show_bookmark_context_menu(pos, s, c))
        site_button.clicked.connect(lambda _, s=site: self.open_website(s))
        site_button.setFixedWidth(self.config["button_width"])
        
        if site.icon:
            try:
                site_button.setIcon(QIcon(site.icon))
            except Exception as e:
                logger.warning(f"Failed to load icon for {site.name}: {e}")
                
        layout.addWidget(site_button)

    def show_bookmark_context_menu(self, pos, bookmark: Bookmark, category: str):
        """Show context menu for bookmark."""
        menu = QMenu(self)
        
        # Add menu actions
        open_action = menu.addAction("Открыть")
        open_new_window = menu.addAction("Открыть в новом окне")
        menu.addSeparator()
        remove_action = menu.addAction("Удалить")
        
        # Show menu and handle actions
        action = menu.exec_(self.sender().mapToGlobal(pos))
        
        if action == open_action:
            self.open_website(bookmark)
        elif action == open_new_window:
            self.open_website(bookmark, new_window=True)
        elif action == remove_action:
            self.remove_bookmark_from_category(category, bookmark.name)

    def open_website(self, site: Bookmark, new_window: bool = False):
        """
        Open the website in the default browser.

        Args:
            site (Bookmark): A Bookmark object containing site information
            new_window (bool): If True, try to open in a new window
        """
        try:
            url = QUrl(site.url)
            if new_window:
                # Attempt to open in new window - note this may not work with all browsers
                url.setFragment("_blank")
            if not QDesktopServices.openUrl(url):
                raise Exception("QDesktopServices.openUrl returned False")
            logger.info(f"Successfully opened URL: {site.url}")
        except Exception as e:
            logger.error(f"Failed to open URL {site.url}: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть сайт: {site.name}")

    def filter_bookmarks(self, text: str):
        """Filter bookmarks based on search text."""
        search_text = text.lower()
        for category, widget in self.category_widgets.items():
            has_visible_items = False
            for i in range(widget.content_layout.count()):
                item = widget.content_layout.itemAt(i)
                if item and item.widget():
                    button = item.widget()
                    visible = search_text in button.text().lower()
                    button.setVisible(visible)
                    has_visible_items = has_visible_items or visible
            
            # Show/hide category based on whether it has visible items
            widget.setVisible(has_visible_items or not search_text)

    def remove_bookmark_from_category(self, category: str, name: str):
        """Remove a bookmark from a category."""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить закладку "{name}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if remove_bookmark(category, name):
                logger.info(f"Removed bookmark {name} from {category}")
                self.bookmark_removed.emit(category, name)
            else:
                logger.error(f"Failed to remove bookmark {name} from {category}")
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить закладку")

    def refresh_category(self, category: str, _=None):
        """Refresh the display of a category after changes."""
        if category in self.category_widgets:
            # Clear existing bookmarks
            while self.category_widgets[category].content_layout.count():
                item = self.category_widgets[category].content_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Add updated bookmarks
            for site in self.bookmarks[category]:
                self.add_site_to_layout(
                    self.category_widgets[category].content_layout,
                    site,
                    category
                )

    def adjust_window_size(self):
        """Adjust the window size based on configuration."""
        self.setMinimumSize(self.config["min_width"], self.config["min_height"])
        self.setMaximumSize(self.config["max_width"], self.config["max_height"])
        self.setFixedSize(self.config["window_width"], self.config["window_height"])

    def closeEvent(self, event: QCloseEvent):
        """
        Handle window close event.
        Minimize to tray if enabled in config, otherwise close the application.
        """
        if self.config["minimize_to_tray"]:
            event.ignore()
            self.hide()
        else:
            event.accept()

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier:
            self.search_input.setFocus()
        else:
            super().keyPressEvent(event)
