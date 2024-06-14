import sys
from PyQt5.QtWidgets import QApplication
from bookmark_main_window import BookmarkMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BookmarkMainWindow()
    sys.exit(app.exec_())
