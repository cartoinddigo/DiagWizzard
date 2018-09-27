# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IsoIgnQt.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Isochrones_IGN(object):
    def setupUi(self, Isochrones_IGN):
        Isochrones_IGN.setObjectName(_fromUtf8("Isochrones_IGN"))
        Isochrones_IGN.resize(500, 300)
        Isochrones_IGN.setMinimumSize(QtCore.QSize(500, 300))
        Isochrones_IGN.setMaximumSize(QtCore.QSize(500, 300))
        self.centralwidget = QtGui.QWidget(Isochrones_IGN)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Titre = QtGui.QLabel(self.centralwidget)
        self.Titre.setGeometry(QtCore.QRect(10, 0, 161, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Myriad Pro"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Titre.setFont(font)
        self.Titre.setObjectName(_fromUtf8("Titre"))
        self.soustitre = QtGui.QLabel(self.centralwidget)
        self.soustitre.setGeometry(QtCore.QRect(120, 30, 41, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Myriad Pro"))
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.soustitre.setFont(font)
        self.soustitre.setObjectName(_fromUtf8("soustitre"))
        self.console = QtGui.QTextEdit(self.centralwidget)
        self.console.setGeometry(QtCore.QRect(180, 10, 311, 281))
        self.console.setObjectName(_fromUtf8("console"))
        self.btSource = QtGui.QPushButton(self.centralwidget)
        self.btSource.setGeometry(QtCore.QRect(10, 80, 161, 32))
        self.btSource.setObjectName(_fromUtf8("btSource"))
        self.btSave = QtGui.QPushButton(self.centralwidget)
        self.btSave.setGeometry(QtCore.QRect(10, 120, 161, 32))
        self.btSave.setObjectName(_fromUtf8("btSave"))
        self.btSource_2 = QtGui.QPushButton(self.centralwidget)
        self.btSource_2.setGeometry(QtCore.QRect(10, 240, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btSource_2.setFont(font)
        self.btSource_2.setObjectName(_fromUtf8("btSource_2"))
        self.btkey = QtGui.QPushButton(self.centralwidget)
        self.btkey.setGeometry(QtCore.QRect(10, 30, 71, 31))
        self.btkey.setObjectName(_fromUtf8("btkey"))
        self.btDistance = QtGui.QRadioButton(self.centralwidget)
        self.btDistance.setGeometry(QtCore.QRect(20, 170, 61, 17))
        self.btDistance.setObjectName(_fromUtf8("btDistance"))
        self.btTemps = QtGui.QRadioButton(self.centralwidget)
        self.btTemps.setGeometry(QtCore.QRect(90, 170, 61, 17))
        self.btTemps.setObjectName(_fromUtf8("btTemps"))
        self.btVoiture = QtGui.QRadioButton(self.centralwidget)
        self.btVoiture.setGeometry(QtCore.QRect(20, 200, 61, 20))
        self.btVoiture.setObjectName(_fromUtf8("btVoiture"))
        self.btMarche = QtGui.QRadioButton(self.centralwidget)
        self.btMarche.setGeometry(QtCore.QRect(80, 200, 91, 20))
        self.btMarche.setObjectName(_fromUtf8("btMarche"))
        self.Titre.raise_()
        self.soustitre.raise_()
        self.console.raise_()
        self.btSource.raise_()
        self.btSave.raise_()
        self.btVoiture.raise_()
        self.btSource_2.raise_()
        self.btkey.raise_()
        self.btVoiture.raise_()
        self.btMarche.raise_()
        self.btDistance.raise_()
        self.btTemps.raise_()
        self.btTemps.raise_()
        self.btDistance.raise_()
        self.btTemps.raise_()
        self.btVoiture.raise_()
        self.btMarche.raise_()
        Isochrones_IGN.setCentralWidget(self.centralwidget)

        self.retranslateUi(Isochrones_IGN)
        QtCore.QMetaObject.connectSlotsByName(Isochrones_IGN)

    def retranslateUi(self, Isochrones_IGN):
        Isochrones_IGN.setWindowTitle(_translate("Isochrones_IGN", "MainWindow", None))
        self.Titre.setText(_translate("Isochrones_IGN", "IDD Isochrones", None))
        self.soustitre.setText(_translate("Isochrones_IGN", "@IGN", None))
        self.btSource.setText(_translate("Isochrones_IGN", "1. Fichier OD ...", None))
        self.btSave.setText(_translate("Isochrones_IGN", "2. Enregistrez vos résutats...", None))
        self.btSource_2.setText(_translate("Isochrones_IGN", "Rechercher", None))
        self.btkey.setText(_translate("Isochrones_IGN", "Clés d\'API", None))
        self.btDistance.setText(_translate("Isochrones_IGN", "Distance ", None))
        self.btTemps.setText(_translate("Isochrones_IGN", "Temps", None))
        self.btVoiture.setText(_translate("Isochrones_IGN", "Voiture", None))
        self.btMarche.setText(_translate("Isochrones_IGN", "Marche à Pied", None))

