# /usr/env/python3.7
"""
Turns a non clickable object such as a label into a clickable object
"""
"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
from PySide6.QtCore import QEvent, Signal, QObject

me = '[Clickable]'


class ClickMixIn:
    clicked = Signal()

    def clickable(self, widget):
        class EventFilter(QObject):
            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        self.clicked.emit()
                        return True
                return False
        filter_obj = EventFilter()
        self.installEventFilter(filter_obj)
        return self.clicked

class MessageRecievedMixIn:
    recv = Signal()

    def recv(self, widget):
        class EventFilter(QObject):
            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.ActionChanged:
                        self.rev.emit()
                        return True
                return False
        filter_obj = EventFilter()
        self.installEventFilter(filter_obj)
        return self.recv


def clickable(widget):
    class Filter(QObject):
        clicked = Signal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        position = str(event.pos())
                        print(str(event.pos()))
                        self.clicked.emit()
                        position = position[position.index('(') + 1: position.index(')')]
                        xy = position.split(',')
                        print(int(xy[0]))
                        print(int(xy[1]))
                        xy = [int(xy[0]), int(xy[1])]
                        obj.curiousposition = xy
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
