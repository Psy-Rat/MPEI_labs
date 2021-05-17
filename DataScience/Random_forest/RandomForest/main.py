import sys
import os
from PyQt5 import QtWidgets
from CuteForm import Ui_MainWindow

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    QtWidgets.QApplication.setStyle(
        QtWidgets.QStyleFactory.create('Cleanlooks'))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
