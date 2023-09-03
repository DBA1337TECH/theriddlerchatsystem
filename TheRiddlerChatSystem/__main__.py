from PyQt5.QtWidgets import QApplication
from TheRiddlerChatSystem.Views import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())