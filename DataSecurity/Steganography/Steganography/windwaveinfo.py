# -*- coding: utf-8 -*-
#-------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
#-------------------------------------------
# Graphics
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation as anim
#-------------------------------------------
#WorkObj
import workObj
#-------------------------------------------

Data = None
Worker = None
General = None


def info_speak(self):
    global Data, Worker, General
    print('child window info: ')
    Worker.printInfo(General)

class Ui_windWaveInfo(object):
    def setupUi(self, windWaveInfo):
        windWaveInfo.setObjectName("windWaveInfo")
        windWaveInfo.resize(400, 280)
        windWaveInfo.setMaximumHeight(280)
        windWaveInfo.setMaximumWidth(400)
        windWaveInfo.setMinimumHeight(280)
        windWaveInfo.setMinimumWidth(400)

        self.centralWidget = QtWidgets.QWidget(windWaveInfo)
        self.centralWidget.setObjectName("centralWidget")
        self.widgetFigure = QtWidgets.QWidget(self.centralWidget)
        self.widgetFigure.setGeometry(QtCore.QRect(10, 10, 381, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetFigure.sizePolicy().hasHeightForWidth())
        self.widgetFigure.setSizePolicy(sizePolicy)
        self.widgetFigure.setObjectName("widgetFigure")
        self.btnPlay = QtWidgets.QPushButton(self.centralWidget)
        self.btnPlay.setGeometry(QtCore.QRect(160, 250, 75, 30))
        self.btnPlay.setObjectName("btnPlay")
        self.btnInfo = QtWidgets.QPushButton(self.centralWidget)
        self.btnInfo.setGeometry(QtCore.QRect(294, 250, 100, 30))
        self.btnInfo.setObjectName("btnInfo")
        windWaveInfo.setCentralWidget(self.centralWidget)

        global Data, Worker, General
        m = workObj.PlotCanvas(self.widgetFigure, Data)
        m.move(0, 0)
        print('child window creator: '+str(General))
        self.retranslateUi(windWaveInfo)

        self.btnPlay.clicked.connect(Worker.playwav)
        self.btnInfo.clicked.connect(info_speak)

        self.info_speaking()


        QtCore.QMetaObject.connectSlotsByName(windWaveInfo)

    def retranslateUi(self, windWaveInfo):
        _translate = QtCore.QCoreApplication.translate
        windWaveInfo.setWindowTitle(_translate("windWaveInfo", "windWaveInfo"))
        self.btnPlay.setText(_translate("windWaveInfo", "Проиграть"))
        self.btnInfo.setText(_translate("windWaveInfo", "Показать\n информацию"))

    def closeEvent(self, event):

        if event:
            event.accept()
        else:
            global Data, Worker, General
            Data = None
            Worker = None
            General = None

            self.close()

    def info_speaking(self):
        print('child window info: ')
        #global Data, Worker, General
        #print('child window info: ' + str(General))
        #Worker.printInfo(General)

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    windWaveInfo = QtWidgets.QMainWindow()
    ui = Ui_windWaveInfo()
    ui.setupUi(windWaveInfo)
    windWaveInfo.show()
    sys.exit(app.exec_())
"""
