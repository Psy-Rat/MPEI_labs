# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Workspace\Python_Anaconda\Library\bin\main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import sys
import os
import shutil
import DecisionTree as dt
import matplotlib.pyplot as plt
import pandas as pd
import math

sys.setrecursionlimit(1000000)


def getName(fileName):
    stPoint = 0
    print((str(fileName).find('/', stPoint)))
    while ((str(fileName).find('/', stPoint)) > 0):
        stPoint = (str(fileName).find('/', stPoint)) + 1

    dbname = str(fileName)[stPoint:]
    dbname = dbname[:dbname.find('.', 0)]

    return dbname


class Ui_WidgetTree(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(1, 9, 401, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lEdit_TreeName = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lEdit_TreeName.setReadOnly(True)
        self.lEdit_TreeName.setObjectName("lEdit_TreeName")
        self.horizontalLayout.addWidget(self.lEdit_TreeName)
        self.cb_selected = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.cb_selected.setObjectName("cb_selected")
        self.horizontalLayout.addWidget(self.cb_selected)
        self.btn_ShowTree = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_ShowTree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_ShowTree.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../see.ico"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ShowTree.setIcon(icon)
        self.btn_ShowTree.setObjectName("btn_ShowTree")
        self.horizontalLayout.addWidget(self.btn_ShowTree)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.cb_selected.setText(_translate("WidgetTree", "CheckBox"))


class WidgetTree(QtWidgets.QWidget):
    def __init__(self, TreePath):
        super().__init__()

        self.setMaximumHeight(40)

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.lEditName = QtWidgets.QLineEdit(self.frame)
        self.lEditName.setReadOnly(True)
        self.lEditName.setText(getName(TreePath))

        self.cb_select = QtWidgets.QCheckBox(self.frame)
        self.cb_select.setText(' ')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("see.ico"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_show = QtWidgets.QPushButton(self.frame)
        self.btn_show.setIcon(icon)

        self.boxx = QtWidgets.QHBoxLayout(self.frame)
        self.boxx.addWidget(self.lEditName)
        self.boxx.addWidget(self.cb_select)
        self.boxx.addWidget(self.btn_show)

        self.frame.adjustSize()

        self.setLayout(self.boxx)
        self.path = TreePath

        self.btn_show.clicked.connect(self.showTree)

    def showTree(self):
        tree = dt.DecisionTree.createFromFile(self.path)
        tree.drawTree()

    def get_tree(self):
        return dt.DecisionTree.createFromFile(self.path)

# Класс проекта


class TProject():
    # Создание проекта
    def __init__(self, aName, aMainDir, database, trees=[]):

        self.name = aName
        self.trees = trees
        self.dir = aMainDir

        self.trees_dir = aMainDir + '/trees/'
        self.database_dir = aMainDir + '/database/'
        if(not os.path.isdir(self.dir)):
            os.mkdir(self.dir)
        if (not os.path.isdir(self.trees_dir)):
            os.mkdir(self.trees_dir)
        if (not os.path.isdir(self.database_dir)):
            os.mkdir(self.database_dir)

        self.database = self.database_dir + self.name + '.csv'
        if(not os.path.isfile(self.database)):
            shutil.copyfile(database, self.database)

        self.save_project()

    # Загрузка проекта
    @classmethod
    def load_project(cls, filename):
        jsn = []

        print(filename)
        print(str(filename))
        print(os.path.realpath(filename))
        print(os.path.dirname(os.path.realpath(filename)))

        with open(os.path.realpath(filename), 'r') as openfile:
            jsn = json.load(openfile)

        print("finnaly")

        vName = jsn[0]
        vMainDir = os.path.dirname(os.path.realpath(filename))
        vDatabase = vMainDir + jsn[1]
        vTrees = []
        for path in jsn[2]:
            vTrees.append(vMainDir + path)

        return cls(vName, vMainDir, vDatabase, vTrees)

    # Сохранение проекта
    def save_project(self):
        relative_db = self.database[len(self.dir):]
        relative_trees = []
        for path in self.trees:
            relative_trees.append(path[len(self.dir):])
        with open(self.dir + '/' + self.name + '.json', 'w') as openfile:
            json.dump([self.name, relative_db, relative_trees],
                      openfile, indent=2, separators=(',', ': '))

    # Создание нового дерева
    def add_tree(self, name, begin, end, labels=None):

        print("new tree created")
        # Читаем базу проекта и выделяем пул и классы
        fixed_df = pd.read_csv(self.database)
        tree_pool, labels, translations = dt.bagging(
            fixed_df, end, begin, labels)

        # Создаём класс даты
        checkingData = dt.DataWorks(tree_pool, labels, translations)

        # Создаём и сохраняем дерево
        tree = dt.DecisionTree.createFromData(
            checkingData)  # DecisionTree(checkingData)
        tree.drawTree()
        tree.saveTree(self.trees_dir + name + '.json')
        self.trees.append(self.trees_dir + name + '.json')

        self.save_project()

        # возвращаем список деревьев
        return self.trees


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumWidth(640)
        MainWindow.setMinimumHeight(480)
        MainWindow.setMaximumWidth(640)
        MainWindow.setMaximumHeight(480)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lEdit_name = QtWidgets.QLineEdit(self.centralWidget)
        self.lEdit_name.setGeometry(QtCore.QRect(110, 10, 191, 20))
        self.lEdit_name.setObjectName("lEdit_name")
        self.lEdit_name.setReadOnly(True)

        self.lEdit_database = QtWidgets.QLineEdit(self.centralWidget)
        self.lEdit_database.setGeometry(QtCore.QRect(110, 50, 191, 20))
        self.lEdit_database.setObjectName("lEdit_database")
        self.lEdit_database.setReadOnly(True)

        self.lbl_name = QtWidgets.QLabel(self.centralWidget)
        self.lbl_name.setGeometry(QtCore.QRect(30, 10, 81, 21))
        self.lbl_name.setObjectName("lbl_name")

        self.lbl_database = QtWidgets.QLabel(self.centralWidget)
        self.lbl_database.setGeometry(QtCore.QRect(30, 50, 81, 21))
        self.lbl_database.setObjectName("lbl_database")
# ---------------------------------------------------------------------------
# 'Scroll area for tree widgets'
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.scrollArea.setGeometry(QtCore.QRect(310, 10, 281, 361))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 277, 357))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.box_v_scroll = QtWidgets.QVBoxLayout()
        self.box_v_scroll.setContentsMargins(3, 3, 11, 11)
        self.box_v_scroll.setSpacing(6)
        self.box_v_scroll.setObjectName("box_v_scroll")

        self.gridLayout.addLayout(self.box_v_scroll, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
# ---------------------------------------------------------------------------
        self.btn_chooseall = QtWidgets.QPushButton(self.centralWidget)
        self.btn_chooseall.setGeometry(QtCore.QRect(560, 380, 31, 23))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("chooseall.ico"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btn_chooseall.setIcon(icon)
        self.btn_chooseall.setObjectName("btn_chooseall")

        self.btn_test = QtWidgets.QPushButton(self.centralWidget)
        self.btn_test.setGeometry(QtCore.QRect(320, 380, 190, 23))
        self.btn_test.setObjectName("btn_test")

        self.btn_compare = QtWidgets.QPushButton(self.centralWidget)
        self.btn_compare.setGeometry(QtCore.QRect(320, 410, 190, 23))
        self.btn_compare.setObjectName("btn_compare")

        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(20, 90, 280, 343))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.btn_Tree = QtWidgets.QPushButton(self.frame)
        self.btn_Tree.setGeometry(QtCore.QRect(170, 290, 101, 23))
        self.btn_Tree.setObjectName("pushButton")
        self.btn_Tree.clicked.connect(self.add_tree)

        self.hslider_samplesize = QtWidgets.QSlider(self.frame)
        self.hslider_samplesize.setGeometry(QtCore.QRect(10, 70, 251, 16))
        self.hslider_samplesize.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_samplesize.setObjectName("hslider_samplesize")
        self.hslider_samplesize.setRange(0, 100)
        self.hslider_samplesize.setValue(10)
# ---------------------------------------------------------------------------
# 'Scroll area for attributes'
        self.scrollArea_attr = QtWidgets.QScrollArea(self.frame)
        self.scrollArea_attr.setGeometry(QtCore.QRect(10, 160, 260, 121))
        self.scrollArea_attr.setWidgetResizable(True)
        self.scrollArea_attr.setObjectName("scrollArea_attr")

        self.scrollAreaWidgetContents_attr = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_attr.setGeometry(
            QtCore.QRect(0, 0, 260, 120))
        self.scrollAreaWidgetContents_attr.setObjectName(
            "scrollAreaWidgetContents")

        self.gridLayout_attr = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_attr)
        self.gridLayout_attr.setContentsMargins(0, 0, 11, 11)
        self.gridLayout_attr.setSpacing(6)
        self.gridLayout_attr.setObjectName("gridLayout_attr")

        self.box_v_scroll_attr = QtWidgets.QVBoxLayout()
        self.box_v_scroll_attr.setContentsMargins(3, 3, 11, 11)
        self.box_v_scroll_attr.setSpacing(6)
        self.box_v_scroll_attr.setObjectName("box_v_scroll_attr")

        self.gridLayout_attr.addLayout(self.box_v_scroll_attr, 0, 0, 1, 1)
        self.scrollArea_attr.setWidget(self.scrollAreaWidgetContents_attr)
# ---------------------------------------------------------------------------

        self.btn_check_all_params = QtWidgets.QPushButton(self.frame)
        self.btn_check_all_params.setGeometry(QtCore.QRect(10, 290, 31, 23))
        self.btn_check_all_params.setIcon(icon)
        self.btn_check_all_params.setObjectName("btn_check_all_params")
        # self.btn_check_all_params.clicked.connect(self.add_tree)

        self.lbl_samplesize = QtWidgets.QLabel(self.frame)
        self.lbl_samplesize.setGeometry(QtCore.QRect(10, 50, 161, 16))
        self.lbl_samplesize.setObjectName("lbl_samplesize")

        self.cb_solid = QtWidgets.QCheckBox(self.frame)
        self.cb_solid.setGeometry(QtCore.QRect(10, 90, 251, 18))
        self.cb_solid.setObjectName("cb_solid")
        self.cb_solid.setChecked(True)

        self.cb_randomize_attr = QtWidgets.QCheckBox(self.frame)
        self.cb_randomize_attr.setGeometry(QtCore.QRect(10, 120, 251, 18))
        self.cb_randomize_attr.setObjectName("cb_randomice_attr")
        self.cb_randomize_attr.setChecked(True)

        self.lEdit_TreeName = QtWidgets.QLineEdit(self.frame)
        self.lEdit_TreeName.setGeometry(QtCore.QRect(90, 10, 171, 20))
        self.lEdit_TreeName.setObjectName("lEdit_TreeName")

        self.lbl_TreeName = QtWidgets.QLabel(self.frame)
        self.lbl_TreeName.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.lbl_TreeName.setObjectName("lbl_TreeName")

        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 609, 18))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuBar.sizePolicy().hasHeightForWidth())

        self.menuBar.setSizePolicy(sizePolicy)
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menuBar)

        #self.statusBar = QtWidgets.QStatusBar(MainWindow)
        # self.statusBar.setObjectName("statusBar")

        # MainWindow.setStatusBar(self.statusBar)

        self.act_New = QtWidgets.QAction(MainWindow)
        self.act_New.setObjectName("act_New")

        self.act_Open = QtWidgets.QAction(MainWindow)
        self.act_Open.setObjectName("act_Open")

        self.act_Save = QtWidgets.QAction(MainWindow)
        self.act_Save.setObjectName("act_Save")

        self.act_Help = QtWidgets.QAction(MainWindow)
        self.act_Help.setObjectName("act_Help")

        self.menuFile.addAction(self.act_New)
        self.menuFile.addAction(self.act_Open)
        self.menuFile.addAction(self.act_Save)

        self.menuHelp.addAction(self.act_Help)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.projDir = os.getcwd() + '/proj/'
        self.dataDir = os.getcwd() + '/database/'

        if (not os.path.isdir(self.projDir)):
            os.mkdir(self.projDir)

        if (not os.path.isdir(self.dataDir)):
            os.mkdir(self.dataDir)

        self.projDir += '/'
        self.dataDir += '/'
        self.projType = ".tproj"
        self.currProject = None
        self.tree_widgets = []
        self.attr_cb = []

        self.act_New.triggered.connect(self.create_project)
        self.act_Open.triggered.connect(self.open_project)
        self.act_Save.triggered.connect(self.save_project)
        self.btn_test.clicked.connect(self.test_trees)
        self.btn_chooseall.clicked.connect(self.check_all)
        self.btn_check_all_params.clicked.connect(self.check_all_attr)
        self.btn_compare.clicked.connect(self.compare_choosen)
        self.cb_randomize_attr.clicked.connect(self.set_attr_avalible)
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Random forest research project"))
        self.lbl_name.setText(_translate("MainWindow", "Имя проекта"))
        self.lbl_database.setText(_translate("MainWindow", "База данных"))
        self.btn_test.setText(_translate(
            "MainWindow", "Тестировать выбранные деревья"))
        self.btn_compare.setText(_translate(
            "MainWindow", "Сравнить выбранные деревья"))
        self.btn_Tree.setText(_translate("MainWindow", "Добавить дерево"))
        self.lbl_samplesize.setText(_translate(
            "MainWindow", "Максимальный размер сэмпла:"))
        self.cb_solid.setText(_translate("MainWindow", " Случайный сэмпл"))
        self.lbl_TreeName.setText(_translate("MainWindow", "Имя дерева"))
        self.menuFile.setTitle(_translate("MainWindow", "Файл"))
        self.menuHelp.setTitle(_translate("MainWindow", "Помощь"))
        self.act_New.setText(_translate("MainWindow", "Новый проект"))
        self.act_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.act_Open.setText(_translate("MainWindow", "Открыть проект"))
        self.act_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.act_Save.setText(_translate("MainWindow", "Сохранить проект"))
        self.act_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.act_Help.setText(_translate("MainWindow", "Справка"))
        self.act_Help.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.cb_randomize_attr.setText(_translate(
            "cb_randomize_attr", "Случайные аттрибуты"))

    def create_project(self):
        proj_path = ""      # Путь к проекту
        text = ""           # Название проекта
        dbname = ""         # Название базы
        f_exists = True     # Проверка на коллизию проектов
        FileWid = QtWidgets.QFileDialog()

        # Чтобы нельзя было создать проект с одинаковым названием
        while f_exists:
            text, ok = QtWidgets.QInputDialog.getText(
                None, 'Новый проект', 'Введите имя проекта:')
            if (not ok):
                return
            proj_path = str(self.projDir + text)
            f_exists = os.path.isdir(proj_path)
            if len(text) is 0:
                msg = QtWidgets.QMessageBox(None)
                msg.setText("Введите имя проекта")
                msg.exec()
                continue

            if f_exists:
                msg = QtWidgets.QMessageBox(None)
                msg.setText("Такой проект уже существует!")
                msg.exec()

        # Зачищаем скролл
        self.clear_scroll()

        # Берём путь к базе данных для переноса её в папку проекта
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            FileWid, caption="Откройте базу данных",  filter="Data Base (*.csv)")
        if len(fileName) is 0:
            return

        stPoint = 0
        print((str(fileName).find('/', stPoint)))
        while((str(fileName).find('/', stPoint)) > 0):
            stPoint = (str(fileName).find('/', stPoint))+1

        dbname = str(fileName)[stPoint:]
        dbname = dbname[:dbname.find('.', 0)]

        newprojDir = self.projDir + text
        # Создаём проект и устанавливаем currProject для редактирования
        self.currProject = TProject(text, newprojDir, fileName)

        self.lEdit_database.setText(getName(fileName))
        self.lEdit_name.setText(text)

        fixed_df = pd.read_csv(self.currProject.database)
        names = fixed_df.columns.values.tolist()[:-1]
        self.refresh_attr(names)
        self.set_attr_avalible()

    def open_project(self):
        FileWid = QtWidgets.QFileDialog()
        # Берём путь к базе данных для переноса её в папку проекта
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(FileWid, caption="Откройте Проект",
                                                            filter="Project File (*.json)")

        try:
            self.currProject = TProject.load_project(fileName)
        except:
            print("Project wasn`t open")
            return

        self.lEdit_database.setText(getName(self.currProject.database))
        self.lEdit_name.setText(self.currProject.name)

        fixed_df = pd.read_csv(self.currProject.database)
        names = fixed_df.columns.values.tolist()[:-1]
        self.refresh_attr(names)
        self.set_attr_avalible()

        # Зачищаем скролл
        self.clear_scroll()

        # Восстанавливаем деревья
        trees = self.currProject.trees
        for path in trees:
            treeWidget = WidgetTree(path)
            self.box_v_scroll.addWidget(treeWidget)
            self.tree_widgets.append(treeWidget)

    def save_project(self):
        if(self.currProject is None):
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Невозможно сохранить пустой проект")
            msg.exec()
            return

        self.currProject.save_project()

    def refresh_attr(self, a_names):

        for i in reversed(range(self.box_v_scroll_attr.count())):
            self.box_v_scroll_attr.itemAt(i).widget().setParent(None)

        self.attr_cb.clear()

        for name in a_names:
            at_cb = QtWidgets.QCheckBox(self.centralWidget)
            at_cb.setGeometry(QtCore.QRect(0, 0, 150, 23))
            at_cb.setChecked(True)
            at_cb.setText(name)
            self.attr_cb.append(at_cb)
            self.box_v_scroll_attr.addWidget(at_cb)

    def clear_scroll(self):
        for i in reversed(range(self.box_v_scroll.count())):
            self.box_v_scroll.itemAt(i).widget().setParent(None)
        self.tree_widgets.clear()

    def add_tree(self):
        # Если открыт проект, то добавляем дерево
        if self.currProject is None:
            return
        name = self.lEdit_TreeName.text()
        begin = 0.01
        end = self.hslider_samplesize.value()*0.99*0.01 + 0.01

        if not self.cb_solid.isChecked():
            begin = end

        labels = None

        if not self.cb_randomize_attr.isChecked():
            labels = []
            for i in self.attr_cb:
                if i.isChecked():
                    labels.append(i.text())

        aaa = os.path.realpath(self.currProject.trees_dir + name + ".json")
        if os.path.isfile(aaa):
            msg = QtWidgets.QMessageBox(None)
            msg.setWindowTitle("Внимание")
            msg.setText("Дерево с данным именем уже существует!")
            msg.exec()
            return

        trees = self.currProject.add_tree(name, begin, end, labels)

        map = []
        for i in self.tree_widgets:
            print(i.cb_select.isChecked())
            map.append(i.cb_select.isChecked())
        # Зачищаем скролл
        self.clear_scroll()

        for path in trees:
            treeWidget = WidgetTree(path)
            self.box_v_scroll.addWidget(treeWidget)
            self.tree_widgets.append(treeWidget)

        for i in range(min(len(self.tree_widgets), len(map))):
            self.tree_widgets[i].cb_select.setChecked(map[i])

    def test_trees(self, trees=None, show=True):
        if(not self.currProject):
            msg = QtWidgets.QMessageBox(None)
            msg.setWindowTitle("Ошибка")
            msg.setText("Отсутствует проект.")
            msg.exec()
            return

        try:
            fixed_df = pd.read_csv(self.currProject.database)
        except Exception:
            msg = QtWidgets.QMessageBox(None)
            msg.setWindowTitle("Ошибка")
            msg.setText("База данных отсутствует или повреждена.")
            msg.exec()
            return

        all = len(fixed_df)
        correct = 0
        wrong = 0

        if(not trees):
            trees = []
            for i in self.tree_widgets:
                if (i.cb_select.isChecked()):
                    trees.append(i.get_tree())

        if (len(trees) is 0):
            msg = QtWidgets.QMessageBox(None)
            msg.setWindowTitle("Ошибка")
            msg.setText("Не выбрано ни одного дерева.")
            msg.exec()
            return

        for dataRow in fixed_df.values:
            ansv = 0
            for tree in trees:
                answer = str(tree.findAnswer(dataRow))
                label = str(dataRow[-1])
                if answer == label:
                    ansv += 1
            if ansv >= math.ceil(len(trees) / 2):
                correct += 1
            else:
                wrong += 1

        if(show):
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Выбрано: " + str(len(trees)) + " деревьев\n" +
                        "========================================\n" +
                        "Правильных ответов: " + str(correct) + "\n" +
                        "Неправильных ответов: " + str(wrong) + "\n" +
                        "========================================\n" +
                        "[" + str(correct) + " | " + str(wrong) + "] }-" + str(len(fixed_df)) + "\n" +
                        "========================================\n" +
                        "Точность: " + str(math.floor((correct/len(fixed_df))*100)) + " % ")

            msg.exec()

        return(math.floor((correct/len(fixed_df))*100))

    def check_all(self):
        for i in self.tree_widgets:
            i.cb_select.setChecked(True)

    def check_all_attr(self):
        setter = True
        for i in self.attr_cb:
            if(i.isChecked()):
                setter = False
                break
        for i in self.attr_cb:
            i.setChecked(setter)

    def set_attr_avalible(self):
        setter = not self.cb_randomize_attr.isChecked()

        for i in self.attr_cb:
            i.setEnabled(setter)

    def compare_choosen(self):
        trees = []
        labels = []
        accuracy = []

        size = len(self.tree_widgets)

        for i in self.tree_widgets:
            if (i.cb_select.isChecked()):
                trees.append([i.get_tree()])
                labels.append(str(i.lEditName.text()))

        if len(trees) is 0:
            msg = QtWidgets.QMessageBox(None)
            msg.setWindowTitle("Ошибка")
            msg.setText("Не выбрано ни одного дерева.")
            msg.exec()
            return

        for tree in trees:
            accuracy.append(self.test_trees(tree, False))

        # plt.ylabel('Scores')
        #plt.title('Scores by group and gender')
        plt.figure(1, figsize=(9, 3))
        ax1 = plt.subplot(111)
        bar1 = ax1.bar(range(len(accuracy)), accuracy)
        plt.xticks(range(len(accuracy)), labels, size='small')
        plt.setp(ax1.get_xticklabels(), visible=True)
        plt.show()

        return


if __name__ == "__main__":

    QtWidgets.QApplication.setStyle(
        QtWidgets.QStyleFactory.create('Cleanlooks'))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
