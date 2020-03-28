import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from ui_main import Ui_MainWindow
from mainwindow import MainWindow

class Main:
    def __init__(self):
        pass
    def init(self):
        self.app=QApplication(sys.argv)
        file = QFile("./dark.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        qss = stream.readAll()
        # self.app.setStyleSheet(qss)
        self.ui_main=Ui_MainWindow()
        self.mainapp=MainWindow()
        self.ui_main.setupUi(self.mainapp)
        self.mainapp.init()
        self.mainapp.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    a=Main()
    a.init()
