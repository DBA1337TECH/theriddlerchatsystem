"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept code, No liabilities or warranties expressed or implied.
"""
"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
'''
CustomLabelType
'''
import sys

sys.path.insert(0, '../../Controllers')
sys.path.insert(1, '..')
sys.path.insert(2, '../../Views')

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os
import math
from TheRiddlerChatSystem.Views.BaseView import BaseView

me = '[CustomLabel]'


class CustomLabel(QLabel):
    '''
    A Draggable CustomLabel
    '''

    def __init__(self, view):
        super(CustomLabel, self).__init__(view)
        self.curiousposition = [0, 0]
        self.rotateby = 0
        self.setAlignment(Qt.AlignCenter)
        self.rotation = 0
        self.view = view
        self.origin = QPoint()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())

    def rotate_pixmap(self, rotateby):
        pixmap = self.view.p2
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** .5
        self.setMinimumSize(diag, diag)
        self.rotation = rotateby
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        self.__mousePressPos = None
        self.__mouseMovePos = None
        self.__newPos = None
        if event.button() == Qt.LeftButton:
            print("Made it to mousePressEvent")
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.origin = QPoint(self.x(), self.y())

            for i in range(2):
                j = (-1) ** i
                k = (-1) ** (i + 2)
                x = DropLabel(self.view, self)
                y = DropLabel(self.view, self)
                for comp in self.view.components:
                    if comp.inRange(self.origin - QPoint(75 * (-j), 75 * k)) and (
                            type(self) != type(comp)) and isinstance(comp, Submarines.Submarines) and (comp != self):
                        x.setPixmap(QPixmap(os.getcwd() + '/Views/images/1337_Logo_small.png'))
                        x.imagename = 'Red'
                        break
                    elif comp.inRange(self.origin - QPoint(75 * j, 75 * k)):
                        x.setPixmap(QPixmap(os.getcwd() + '/Views/images/SP_logo.png'))
                        x.imagename = 'Blue'
                        break
                    else:
                        x.setPixmap(QPixmap(os.getcwd() + '/Views/images/1337_Logo_small.png'))

                for comp in self.view.components:
                    if comp.inRange(self.origin - QPoint(75 * (-j), 75 * k)) and (
                            type(self) != type(comp)) and isinstance(comp, Submarines.Submarines) and (comp != self):
                        y.setPixmap(QPixmap(os.getcwd() + '/Views/images/1337_Logo_small.png'))
                        y.imagename = 'Red'
                        break
                    elif comp.inRange(self.origin - QPoint(75 * (-j), 75 * k)):
                        y.setPixmap(QPixmap(os.getcwd() + '/Views/images/SP_logo.png'))
                        y.imagename = 'Blue'
                        break

                    else:
                        y.setPixmap(QPixmap(os.getcwd() + '/Views/images/1337_Logo_small.png'))
                        y.imagename = 'Green'

                print(self.origin)
                x.move(self.origin - QPoint(75 * j, 75 * k))
                y.move(self.origin - QPoint(75 * (-j), 75 * (k)))

                self.view.components.append(x)
                self.view.components.append(y)
                x.show()
                y.show()
            self.view.showFullScreen()

    def mouseMoveEvent(self, event):
        # for comp in self.view.components:
        #      if isinstance(comp, DropLabel):
        #          if comp != None:
        #              comp.show()
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        # adjust offset from clicked point to origin of widget
        currPos = self.mapToGlobal(self.pos())
        globalPos = event.globalPos()
        diff = globalPos - self.__mouseMovePos
        newPos = self.mapFromGlobal(currPos + diff)

        if newPos != None:
            self.move(newPos)

        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        mimedata.setImageData(self.pixmap().toImage())

        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        self.move(newPos)
        self.__mouseMovePos = globalPos
        self.__newPos = newPos
        if (((math.fabs(diff.x()) ** 2 + math.fabs(diff.y()) ** 2) * 0.5) > (math.fabs(self.width()))):
            print("out of bounds")
            drag.setPixmap(QPixmap(os.getcwd() + '/Views/images/SP_logo.png'))
        drag.exec_(Qt.MoveAction | Qt.MoveAction, Qt.CopyAction)
        super(CustomLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos

            if moved.manhattanLength() > 3:
                print("made it here")
                event.ignore()
                return
            self.move(self.__newPos)

        super(CustomLabel, self).mouseReleaseEvent(event)


class DropLabel(QLabel):

    def __init__(self, view, *args, **kwargs):
        super(DropLabel, self).__init__(view)
        # QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.curiousposition = [0, 0]
        self.setAlignment(Qt.AlignCenter)
        self.args = args
        self.view = view
        self.imagename = 'Green'

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() and (self.imagename == 'Green' or self.imagename == 'Red'):
            print(me + "event accepted")
            event.accept()

        else:
            print(me + "event rejected")
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage():

            for a in self.args:
                if isinstance(a, CustomLabel):
                    if self.imagename == 'Red':
                        print('LET THE BATTLE BEGIN')
                        # TODO: OPEN a new window
                        # detect component that is in question
                        # make sure that the self.pos is within the collision distance
                        # of what is supposed to be battled out
                        self.GameEngine = GameEngine.GameEngine(self.view)
                        self.BattleWindow = self.GameEngine.BeginBattle(self.view)

                    elif self.imagename == 'Green':
                        print('CustomLabel move: ' + str(self.pos()))
                        a.xPos = self.pos().x()
                        a.yPos = self.pos().y()
                        a.move(self.pos())

            if isinstance(self.view, BaseView.BaseView):
                for c in self.view.components:
                    if isinstance(c, DropLabel):
                        c.hide()
                        c.deleteLater()
                        c = None
                self.view.components[:] = [x for x in self.view.components if not isinstance(x, DropLabel)]

            event.accept()

            return
            # self.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))


class LoadingLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None, **kwargs):
        super(LoadingLabel, self).__init__(**kwargs)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class LogoLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None, **kwargs):
        super(LogoLabel, self).__init__(parent, **kwargs)

    def mousePressEvent(self, ev):
        self.clicked.emit()
