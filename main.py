import sys
from PyQt5.QtWidgets import QApplication
from bookmark_main_window import BookmarkMainWindow
import sity_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BookmarkMainWindow(sity_list.bookmarks)
    sys.exit(app.exec_())
