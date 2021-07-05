import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QStyle

from TheRiddlerChatSystem.Views import LandingPage

me = '[MainWindow]'


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ctrl = None
        self.components = []
        self.view = None

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        help_menu = menubar.addMenu('Help')

        # icons
        open_icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(QStyle.SP_DriveHDIcon)
        undo_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        redo_icon = self.style().standardIcon(QStyle.SP_ArrowForward)

        self.about_menu = help_menu.addAction('&About')

        self.undo_menu = edit_menu.addAction('&undo')
        self.undo_menu.setIcon(undo_icon)
        self.redo_menu = edit_menu.addAction('&redo')
        self.redo_menu.setIcon(redo_icon)

        self.open_action = file_menu.addAction('&Open')
        self.open_action.setIcon(open_icon)
        self.save_action = file_menu.addAction('&Save')
        self.save_action.setIcon(save_icon)

        self.initUI()

    def initUI(self) -> object:
        self.view = LandingPage.LandingPage()

        self.statusBar().showMessage('StatusBar: Initialized')

        self.setCentralWidget(self.view)

        self.setGeometry(300, 300, 796, 650)

        self.setWindowTitle('The Riddler Chat System')

        self.setWindowIcon(QIcon(os.getcwd() + '/images/1337_Logo_small.png'))

        self.setWindowOpacity(0.85)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
