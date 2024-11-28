"""
Main entry point for the Portable Browser application.
This module initializes the application and handles high-level configuration and error management.
"""

import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from bookmark_main_window import BookmarkMainWindow

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('browser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Load application configuration from config.json.
    If the file doesn't exist, create it with default values.
    """
    config_path = Path('config.json')
    default_config = {
        "window_width": 450,
        "window_height": 650,
        "min_width": 300,
        "min_height": 400,
        "max_width": 800,
        "max_height": 1200,
        "button_width": 150,
        "minimize_to_tray": True
    }
    
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return default_config

def import_bookmarks():
    """Import bookmarks from the appropriate module."""
    try:
        from sity_list import bookmarks
        logger.info("Successfully imported bookmarks")
        return bookmarks
    except ImportError as e:
        logger.error(f"Failed to import bookmarks: {e}")
        raise ImportError("Не удалось импортировать данные закладок из 'sity_list.py'. "
                        "Убедитесь, что файл существует и доступен.")

def create_tray_icon(app: QApplication, window: BookmarkMainWindow) -> QSystemTrayIcon:
    """Create system tray icon with context menu."""
    tray_icon = QSystemTrayIcon(QIcon("icons/app.png"), app)
    tray_icon.activated.connect(lambda reason: window.show() if reason == QSystemTrayIcon.DoubleClick else None)
    tray_icon.setToolTip("Мой Портативный Браузер")
    tray_icon.show()
    return tray_icon

def show_error_message(message: str):
    """Display an error message box."""
    logger.error(message)
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setText("Ошибка запуска приложения")
    error_box.setInformativeText(message)
    error_box.setWindowTitle("Ошибка")
    error_box.exec_()

def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    config = load_config()
    
    try:
        bookmarks = import_bookmarks()
        main_window = BookmarkMainWindow(bookmarks, config)
        main_window.show()
        
        if config["minimize_to_tray"]:
            tray_icon = create_tray_icon(app, main_window)
        
        logger.info("Application started successfully")
        return app.exec_()
        
    except ImportError as e:
        show_error_message(f"Ошибка импорта: {e}\n"
                          f"Проверьте, установлены ли все необходимые библиотеки и существуют ли нужные файлы.")
    except Exception as e:
        show_error_message(f"Произошла непредвиденная ошибка: {e}")
        logger.exception("Unexpected error occurred")
    return 1

if __name__ == "__main__":
    sys.exit(main())
