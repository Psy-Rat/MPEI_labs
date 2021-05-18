# -*- coding: utf-8 -*-
# -------------------------------------------
# QtForms
from PyQt5 import QtCore, QtGui, QtWidgets
# -------------------------------------------
# FileWork
import wave
import os
import winsound
# -------------------------------------------
# Graphics
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation as anim
# -------------------------------------------
# Math
# import scipy as sci
import numpy as np
import math
# -------------------------------------------
# WorkObj
import workObj
# -------------------------------------------

# Forms
import windwaveinfo as wavinfo
# -------------------------------------------


class Ui_StegWindow(object):
    def setupUi(self, StegWindow):
        StegWindow.setObjectName("StegWindow")
        StegWindow.resize(600, 250)
        StegWindow.setMaximumHeight(280)
        StegWindow.setMaximumWidth(600)
        StegWindow.setMinimumHeight(280)
        StegWindow.setMinimumWidth(600)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            StegWindow.sizePolicy().hasHeightForWidth())
        StegWindow.setSizePolicy(sizePolicy)

        self.centralWidget = QtWidgets.QWidget(StegWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 600, 240))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabEmbed = QtWidgets.QWidget()
        self.tabEmbed.setObjectName("tabEmbed")

        self.lblCurrStat = QtWidgets.QLabel(self.centralWidget)
        self.lblCurrStat.setGeometry(QtCore.QRect(3, 240, 630, 20))
        self.lblCurrStat.setObjectName("lblCurrStat")
        self.loadbar = QtWidgets.QProgressBar(self.centralWidget)
        self.loadbar.setGeometry(QtCore.QRect(3, 260, 630, 20))

        self.ledWavPath = QtWidgets.QLineEdit(self.tabEmbed)
        self.ledWavPath.setGeometry(QtCore.QRect(90, 10, 370, 20))
        self.ledWavPath.setReadOnly(True)
        self.ledWavPath.setObjectName("ledWavPath")
        self.btnOpenWav = QtWidgets.QPushButton(self.tabEmbed)
        self.btnOpenWav.setGeometry(QtCore.QRect(0, 10, 81, 23))
        self.btnOpenWav.setObjectName("btnOpenWav")

        self.btnOpenFile = QtWidgets.QPushButton(self.tabEmbed)
        self.btnOpenFile.setGeometry(QtCore.QRect(0, 40, 81, 23))
        self.btnOpenFile.setObjectName("btnOpenFile")

        self.ledMesHead = QtWidgets.QLineEdit(self.tabEmbed)
        self.ledMesHead.setGeometry(QtCore.QRect(0, 108, 200, 20))
        self.ledMesHead.setReadOnly(True)
        self.ledMesHead.setObjectName("ledMesHead")

        # Группа кодировок печатного текста
        self.groupTextCode = QtWidgets.QGroupBox(self.tabEmbed)
        self.groupTextCode.setGeometry(QtCore.QRect(90, 34, 101, 71))
        self.groupTextCode.setObjectName("groupTextCode")
        self.rbASCII = QtWidgets.QRadioButton(self.groupTextCode)
        self.rbASCII.setGeometry(QtCore.QRect(10, 20, 82, 18))
        self.rbASCII.setObjectName("rbASCII")
        self.rbUTF = QtWidgets.QRadioButton(self.groupTextCode)
        self.rbUTF.setGeometry(QtCore.QRect(10, 50, 82, 18))
        self.rbUTF.setChecked(True)
        self.rbUTF.setObjectName("rbUTF")
        self.teMessage = QtWidgets.QPlainTextEdit(self.tabEmbed)
        self.teMessage.setGeometry(QtCore.QRect(210, 40, 371, 71))
        self.teMessage.setObjectName("teMessage")

        # Группа алгоритмов стеганографиии
        self.groupAlgSteg = QtWidgets.QGroupBox(self.tabEmbed)
        self.groupAlgSteg.setGeometry(QtCore.QRect(120, 140, 111, 71))
        self.groupAlgSteg.setObjectName("groupAlgSteg")
        self.rbLSB = QtWidgets.QRadioButton(self.groupAlgSteg)
        self.rbLSB.setGeometry(QtCore.QRect(10, 30, 82, 18))
        self.rbLSB.setChecked(True)
        self.rbLSB.setEnabled(False)  # других алгоритмов пока не завезли
        self.rbLSB.setObjectName("rbLSB")

        # Группа алгоритимов криптографии
        self.groupAlgCrypt = QtWidgets.QGroupBox(self.tabEmbed)
        self.groupAlgCrypt.setGeometry(QtCore.QRect(0, 140, 111, 71))
        self.groupAlgCrypt.setObjectName("groupAlgCrypt")
        self.rbShift = QtWidgets.QRadioButton(self.groupAlgCrypt)
        self.rbShift.setGeometry(QtCore.QRect(10, 30, 91, 18))
        self.rbShift.setChecked(True)
        self.rbShift.setEnabled(False)  # других алгоритмов пока не завезли
        self.rbShift.setObjectName("rbShift")

        self.line = QtWidgets.QFrame(self.tabEmbed)
        self.line.setGeometry(QtCore.QRect(0, 115, 591, 31))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.ledPassword = QtWidgets.QLineEdit(self.tabEmbed)
        self.ledPassword.setGeometry(QtCore.QRect(250, 160, 211, 20))
        self.ledPassword.setObjectName("ledPassword")
        self.ledPasswordRepeat = QtWidgets.QLineEdit(self.tabEmbed)
        self.ledPasswordRepeat.setGeometry(QtCore.QRect(250, 190, 211, 20))
        self.ledPasswordRepeat.setObjectName("ledPasswordRepeat")
        self.ledPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledPasswordRepeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lblCreateKey = QtWidgets.QLabel(self.tabEmbed)
        self.lblCreateKey.setGeometry(QtCore.QRect(250, 140, 211, 16))
        self.lblCreateKey.setObjectName("lblCreateKey")
        self.btnMerge = QtWidgets.QPushButton(self.tabEmbed)
        self.btnMerge.setGeometry(QtCore.QRect(510, 160, 90, 50))
        self.btnMerge.setObjectName("btnMerge")

        self.btnSeeNew = QtWidgets.QPushButton(self.tabEmbed)
        self.btnSeeNew.setGeometry(QtCore.QRect(470, 170, 30, 20))
        self.btnSeeNew.setObjectName("btnSeeNew")
        self.btnSeeNew.setFocusPolicy(QtCore.Qt.NoFocus)
        icon_see = QtGui.QIcon()
        icon_see.addPixmap(QtGui.QPixmap("icon/seeNEW.ico"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSeeNew.setIcon(icon_see)

        self.lblEnabledSize = QtWidgets.QLabel(self.tabEmbed)
        self.lblEnabledSize.setGeometry(QtCore.QRect(470, 110, 91, 16))
        self.lblEnabledSize.setObjectName("lblEnabledSize")
        self.btnWavInfoClear = QtWidgets.QPushButton(self.tabEmbed)
        self.btnWavInfoClear.setGeometry(QtCore.QRect(470, 10, 121, 23))
        self.btnWavInfoClear.setObjectName("btnWavInfoClear")
        self.tabWidget.addTab(self.tabEmbed, "")
        self.tabExtract = QtWidgets.QWidget()
        self.tabExtract.setObjectName("tabExtract")
        self.ledOpenSteg = QtWidgets.QLineEdit(self.tabExtract)
        self.ledOpenSteg.setGeometry(QtCore.QRect(100, 10, 360, 20))
        self.ledOpenSteg.setReadOnly(True)
        self.ledOpenSteg.setObjectName("ledOpenSteg")
        self.btnOpenSteg = QtWidgets.QPushButton(self.tabExtract)
        self.btnOpenSteg.setGeometry(QtCore.QRect(10, 10, 81, 23))
        self.btnOpenSteg.setObjectName("btnOpenSteg")
        self.line_2 = QtWidgets.QFrame(self.tabExtract)
        self.line_2.setGeometry(QtCore.QRect(0, 30, 581, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.lblPasswordDec = QtWidgets.QLabel(self.tabExtract)
        self.lblPasswordDec.setGeometry(QtCore.QRect(10, 50, 141, 16))
        self.lblPasswordDec.setObjectName("lblPasswordDec")
        self.ledPasswordDec = QtWidgets.QLineEdit(self.tabExtract)
        self.ledPasswordDec.setGeometry(QtCore.QRect(0, 70, 561, 20))
        self.ledPasswordDec.setObjectName("ledPasswordDec")
        self.line_3 = QtWidgets.QFrame(self.tabExtract)
        self.line_3.setGeometry(QtCore.QRect(0, 90, 581, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.ted_extracted = QtWidgets.QPlainTextEdit(self.tabExtract)
        self.ted_extracted.setGeometry(QtCore.QRect(110, 110, 451, 101))
        self.ted_extracted.setReadOnly(True)
        self.ted_extracted.setObjectName("plainTextEdit_3")
        self.btnDeSteg = QtWidgets.QPushButton(self.tabExtract)
        self.btnDeSteg.setGeometry(QtCore.QRect(10, 110, 81, 41))
        self.btnDeSteg.setObjectName("btnDeSteg")
        self.btnSave = QtWidgets.QPushButton(self.tabExtract)
        self.btnSave.setGeometry(QtCore.QRect(10, 170, 81, 41))
        self.btnSave.setObjectName("btnSave")
        self.btnWavInfoMessage = QtWidgets.QPushButton(self.tabExtract)
        self.btnWavInfoMessage.setGeometry(QtCore.QRect(470, 10, 121, 23))
        self.btnWavInfoMessage.setObjectName("btnWavInfoMessage")
        self.tabWidget.addTab(self.tabExtract, "")
        self.tabAbout = QtWidgets.QWidget()
        self.tabAbout.setObjectName("tabAbout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tabAbout)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 561, 201))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.tabWidget.addTab(self.tabAbout, "")
        StegWindow.setCentralWidget(self.centralWidget)
        # -------------------------------------------

        self.child = None
        self.Worker = workObj.Worker(self)
        # -------------------------------------------
        # Открыть wav файл для записи стеганографического сообщения
        self.btnOpenWav.clicked.connect(self.Worker.load_clearwav)
        # Открыть окно информации о wav-файле
        self.btnWavInfoClear.clicked.connect(self.add_clear)
        self.btnWavInfoMessage.clicked.connect(self.add_steg)
        # Изменить форму ввода пароля
        self.btnSeeNew.clicked.connect(self.Worker.changeEcho)
        # Ввод сообщения
        self.teMessage.setEnabled(False)
        self.teMessage.textChanged.connect(self.Worker.onMessageChange)
        # -------------------------------------------
        # Переключение кодировки
        self.rbASCII.clicked.connect(self.Worker.changeCode)
        self.rbUTF.clicked.connect(self.Worker.changeCode)

        # Сокрытие информации
        self.btnMerge.clicked.connect(self.Worker.merger)

        # Вскрытие
        self.btnOpenSteg.clicked.connect(self.Worker.open_steg)
        # Выписываем
        self.btnDeSteg.clicked.connect(self.Worker.get_out_steg)
        # Запись расшифровки
        self.btnSave.clicked.connect(self.Worker.save_decription)

        self.btnOpenFile.clicked.connect(self.Worker.binaryLoad)

        self.retranslateUi(StegWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(StegWindow)

    def retranslateUi(self, StegWindow):
        _translate = QtCore.QCoreApplication.translate
        StegWindow.setWindowTitle(_translate(
            "StegWindow", "Аудиостеганография"))
        self.lblCurrStat.setText(_translate("StegWindow", "..."))
        self.btnOpenWav.setText(_translate("StegWindow", "Открыть wav"))
        self.btnOpenFile.setText(_translate("StegWindow", "Скрыть файл"))
        self.btnSeeNew.setText(_translate("StegWindow", " "))
        self.groupTextCode.setTitle(_translate("StegWindow", "Кодировка"))
        self.rbASCII.setText(_translate("StegWindow", "ASCII"))
        self.rbUTF.setText(_translate("StegWindow", "utf-8"))
        self.groupAlgSteg.setTitle(_translate("StegWindow", "Стеганография"))
        self.rbLSB.setText(_translate("StegWindow", "LSB"))
        self.groupAlgCrypt.setTitle(_translate("StegWindow", "Шифрование"))
        self.rbShift.setText(_translate("StegWindow", "Перестановка"))
        self.lblCreateKey.setText(_translate(
            "StegWindow", "Введите и повторите пароль"))
        self.btnMerge.setText(_translate("StegWindow", "Скрыть"))
        self.lblEnabledSize.setText(_translate("StegWindow", "[ 0 / 0 ]"))
        self.btnWavInfoClear.setText(_translate(
            "StegWindow", "Информация о файле"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tabEmbed), _translate("StegWindow", "Embed"))
        self.btnOpenSteg.setText(_translate("StegWindow", "Открыть"))
        self.lblPasswordDec.setText(_translate(
            "StegWindow", "Пароль для расшифровки"))
        self.btnDeSteg.setText(_translate("StegWindow", "Восстановить \n"
                                          "Сообщение"))
        self.btnSave.setText(_translate("StegWindow", "Сохранить \n"
                                        "в файл"))
        self.btnWavInfoMessage.setText(
            _translate("StegWindow", "Информация о файле"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tabExtract), _translate("StegWindow", "Extract"))
        self.plainTextEdit.setPlainText(_translate("StegWindow", "**************************************************************************\n"
                                                   "Лабораторная работа по теме: «Стеганография в аудиофайлах» \n"
                                                   "Сделал: студент группы А-05-14 Почкин И.Н.\n"
                                                   "Проверил: Хорев П.Б.\n"
                                                   "**************************************************************************\n"
                                                   "Алгоритмы стеганографии: \n"
                                                   "    •  LSB\n"
                                                   "Алгоритмы шифрования:\n"
                                                   "    • Перестановка по ключу\n"
                                                   "Доступные форматы:\n"
                                                   "    • wave\n"
                                                   "**************************************************************************\n"
                                                   "Последняя версия  10.12.2017\n"
                                                   "**************************************************************************"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tabAbout), _translate("StegWindow", "About"))

    def add_steg(self):
        self.add_wind(1)

    def add_clear(self):
        self.add_wind(2)

    def add_wind(self, type=1):
        try:
            self.child.setParent(None)
            self.child.show()
        except Exception:
            self.child = None
        self.child = None

        if type == 2 and self.Worker.Data is None:
            return
        if type == 1 and self.Worker.SecondData is None:
            return

        if self.child is None:
            self.child = QtWidgets.QMainWindow()
            if type == 2:
                wavinfo.Data = self.Worker.Data
            else:
                wavinfo.Data = self.Worker.SecondData
            wavinfo.Worker = self.Worker
            wavinfo.General = type
            print('curr type' + str(type))
            ui = wavinfo.Ui_windWaveInfo()
            ui.setupUi(self.child)
            self.child.show()
