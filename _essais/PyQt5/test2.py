from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *
import sys


class Signals(QObject):
    asignal = pyqtSignal(str)

    def __init__(self):
        super(Signals, self).__init__()
        self.do_something()

    def do_something(self):
        self.asignal.emit('Hi, im a signal')


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setGeometry(300, 250, 400, 300)
        self.show()
        self.coso()

    def coso(self):
        btn = QPushButton('click me')
        s = Signals()
        s.asignal.connect(lambda sig: print("Signal recieved" + sig))
        s.do_something()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    app.exec_()