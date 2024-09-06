import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from bookmark_main_window import BookmarkMainWindow

def import_bookmarks():
    """Import bookmarks from the appropriate module."""
    try:
        from sity_list import bookmarks
    except ImportError:
        raise ImportError("Не удалось импортировать данные закладок из 'sity_list.py'. Убедитесь, что файл существует и доступен.")
    return bookmarks

def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    try:
        bookmarks = import_bookmarks()
        main_window = BookmarkMainWindow(bookmarks)
        main_window.show()
        return app.exec_()
    except ImportError as e:
        show_error_message(f"Ошибка импорта: {e}\nПроверьте, установлены ли все необходимые библиотеки и существуют ли нужные файлы.")
    except Exception as e:
        show_error_message(f"Произошла непредвиденная ошибка: {e}")
    return 1

def show_error_message(message):
    """Display an error message box."""
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setText("Ошибка запуска приложения")
    error_box.setInformativeText(message)
    error_box.setWindowTitle("Ошибка")
    error_box.exec_()

if __name__ == "__main__":
    sys.exit(main())
