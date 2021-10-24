'''
Although it is titled the Landing page it is being treated more like the initial
GameBoard.  Luckily this is just a view so it is subject to change, I can always
make a view called GameBoard which inherits the BaseView
'''

import sys
from PyQt5.QtCore import Qt
#from StenographyController import StenographyController
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QSplitter, QLabel, QHBoxLayout, QDockWidget, QPushButton, QTextEdit, QListWidget

from TheRiddlerChatSystem.Model.CustomLabel import *
from TheRiddlerChatSystem.Controllers.ReceiveController import ReceiveController
from TheRiddlerChatSystem.Model.RecvChatBox import RecvChatBox

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')

me = '[LandingPage]'

green = '#669933'
purple = '#CC663399'
darkRed = '#8B0000'
background_role = 'background-color: '
text_role = 'color: '


class LandingPage(BaseView.BaseView):

    def __init__(self):
        super(LandingPage, self).__init__()
        self.ctrl = None
        self.components = []
        self.controllers = []
        self.p = None
        self.p2 = None

        self.initUI()

    def initUI(self):
        """Initializes the UI Landing Page"""
        filePathHiddenImage = RecvChatBox("TheRiddlerChatSystem conversation", self)
        folderButton = QTextEdit("TheRiddlerChatSystem Message Here", self)
        folder_button = QPushButton("Click to Password Protect", self)
        Villian_List = QListWidget(self)
        go_baby_go = QPushButton("SEND", self)




        # format the buttons to look differently
        folder_button.setStyleSheet(background_role + purple + '; ' + text_role + green + ';')
        Villian_List.setStyleSheet(background_role + purple + '; ' + text_role + green + ';')
        folderButton.setStyleSheet(background_role + green + '; ' + text_role + purple + ';')
        filePathHiddenImage.setStyleSheet(background_role + purple + '; ' + text_role + green + ';')
        go_baby_go.setStyleSheet(background_role + green + '; ' + text_role + purple + ';')

        # Create and Attach Controllers
        # noinspection PyAttributeOutsideInit
        #self.hiddenImageController = StenographyController(self, filePathHiddenImage, folderButton, folder_button,
        #                                                  go_baby_go)

        ####ADD LISTS AS MOCKUP####
        Villian_List.addItem("Silver_Surfer")
        Villian_List.addItem("Mr_Freeze")
        Villian_List.addItem("SaberT00th")
        Villian_List.addItem("RasAlGhul")
        Villian_List.addItem("Venom")
        Villian_List.addItem("Green_Goblin")
        Villian_List.addItem("KingPin")
        Villian_List.addItem("Mr_Smith")
        Villian_List.addItem("General_Zod")
        Villian_List.addItem("DNS_Poisoned_Ivy")

        fileItems = QDockWidget("Chat Messages", self)
        BuddyList = QDockWidget("Fellow Villians", self)
        fileItems.setFeatures(QDockWidget.NoDockWidgetFeatures)
        folderItems = QDockWidget("Type a Message to be sent", self)
        viewOne = QPixmap(os.getcwd() + '/images/1337_Logo_small.png')

        # Adjust the Font
        options_font = QFont('Courier', 14, QFont.ExtraBold)

        filePathHiddenImage.setFont(options_font)
        folderButton.setFont(options_font)

        folder_button.setFont(options_font)

        go_baby_go.setFont(options_font)

        self.p2 = viewOne

        self.setWindowTitle('TheRiddlerChatSystem')

        fileItems.setWidget(filePathHiddenImage)
        fileItems.setFloating(False)

        folderItems.setWidget(folderButton)
        folderItems.setFloating(False)

        hbox = QHBoxLayout(self)

        splitter1 = QSplitter(self)
        splitter1.setOrientation(Qt.Horizontal)
        sizePolicyOne = splitter1.sizePolicy()
        sizePolicyOne.setHorizontalStretch(1)

        logo = QLabel()
        logo.setPixmap(self.p2)


        top_left = QFrame(splitter1)
        top_left.setFrameShape(QFrame.StyledPanel)

        splitter2 = QSplitter(splitter1)
        sizePolicy = splitter2.sizePolicy()
        sizePolicy.setHorizontalStretch(1)

        splitter1.setOrientation(Qt.Vertical)
        splitter1.addWidget(BuddyList)
        splitter1.addWidget(Villian_List)
        splitter1.addWidget(logo)


        splitter2.setSizePolicy(sizePolicy)
        splitter2.setOrientation(Qt.Vertical)

        top_right = QFrame(splitter2)
        top_right.setFrameShape(QFrame.StyledPanel)
        splitter2.addWidget(fileItems)

        bottom_right = QFrame(splitter2)
        bottom_right.setFrameShape(QFrame.StyledPanel)
        splitter2.addWidget(folderItems)
        splitter2.addWidget(folder_button)
        splitter2.addWidget(go_baby_go)

        hbox.addWidget(splitter1)
        hbox.addWidget(splitter2)
        self.setGeometry(300, 300, 796, 650)

        self.setAutoFillBackground(True)

        self.setStyleSheet(background_role + darkRed + ';')

        ####
        #
        # Register The Controllers to link The Functionality Together
        #
        ####
        recv = ReceiveController(self, filePathHiddenImage)
        self.controllers.append(recv)

        self.show()
