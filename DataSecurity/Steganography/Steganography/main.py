import os
import sys
from PyQt5 import QtWidgets
from stegwindow import Ui_StegWindow

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    StegWindow = QtWidgets.QMainWindow()
    ui = Ui_StegWindow()
    ui.setupUi(StegWindow)
    StegWindow.show()
    sys.exit(app.exec_())
