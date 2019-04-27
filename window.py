#!/usr/bin/python
# -*- coding: utf-8 -*-

# openfiledialog.py

import sys

from Crypto.Cipher import AES
from PyQt4 import QtCore
from PyQt4 import QtGui


class DeCodeTools(QtGui.QWidget):
    def __init__(self):
        super(DeCodeTools, self).__init__()

        self.initUI()

    def initUI(self):
        # logLabel = QtGui.QLabel("xp Log:")
        src = QtGui.QPushButton('select srcFile')
        dst = QtGui.QPushButton('input dstFile')
        run = QtGui.QPushButton('run decode')
        result = QtGui.QLabel('result:')
        # review = QtGui.QLabel('result')


        self.srcEdit = QtGui.QLineEdit()
        self.dstEdit = QtGui.QLineEdit()
        # reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        # grid.addWidget(logLabel, 0, 1)
        grid.addWidget(src, 1, 0)
        grid.addWidget(self.srcEdit, 1, 1)

        grid.addWidget(dst, 2, 0)
        grid.addWidget(self.dstEdit, 2, 1)
        grid.addWidget(run, 3, 1)
        grid.addWidget(result, 4, 1)

        # grid.addWidget(review, 3, 0)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        self.setWindowTitle('DecodeTool')

        # # self.srchbox = QtGui.QHBoxLayout(self)
        # # self.srchbox.addStretch(1)
        # self.srcEdit = QtGui.QLineEdit(self)
        # # self.setCentralWidget(self.textEdit)
        # self.srclabel = QtGui.QLabel('srcFile',self)
        #
        # # self.srchbox.addWidget(self.srclabel)
        # # self.srchbox.addWidget(self.srcEdit)
        # self.srclabel.move(30, 30)
        # self.srcEdit.move(50, 30)
        #
        # self.dsthbox = QtGui.QHBoxLayout(self)
        # self.dsthbox.addStretch(1)
        # self.dstEdit = QtGui.QLineEdit(self)
        # # self.setCentralWidget(self.textEdit)
        # self.dstlabel = QtGui.QLabel('dstFile')
        # self.dsthbox.addWidget(self.dstlabel)
        # self.dsthbox.addWidget(self.dstEdit)
        #
        # # self.vbox = QtGui.QVBoxLayout(self)
        # # self.vbox.addStretch(1)
        # # self.vbox.addLayout(self.srchbox)
        # # self.vbox.addLayout(self.dsthbox)
        # # self.setLayout(self.vbox)
        # self.setFocus()

        # openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        # openFile.setShortcut('Ctrl+O')
        # openFile.setStatusTip('Open new File')
        self.connect(src, QtCore.SIGNAL('clicked()'), self.showDialog)

        self.connect(run, QtCore.SIGNAL('clicked()'), self.decodeLog)
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('OpenFile')

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Decode XP Log',
                                                     '/home')
        # fname = open(filename)
        # data = fname.read()
        self.srcEdit.setText(filename)

    def decodeLog(self):
        filePath = self.srcEdit.text()
        print (filePath)
        plaintFilePath = filePath + ".zip"
        self.dstEdit.setText(plaintFilePath)
        # if os.path.exists(filePath):
        #     os.remove(filePath)
        print "the filepath %s" % filePath
        fileCipher = open(filePath, 'rb+')
        plaintFile = open(plaintFilePath, "wb+")
        encryptText = fileCipher.read()
        plaintText = self.decrypt_CBC(encryptText, "size为16的passwd")
        plaintFile.write(plaintText)
        plaintFile.close()
        fileCipher.close()

    def align(self, str, isKey=False):
        # 如果接受的字符串是密码，需要确保其长度为16
        if isKey:
            if len(str) > 16:
                return str[0:16]
            else:
                return self.align(str)
        # 如果接受的字符串是明文或长度不足的密码，则确保其长度为16的整数倍
        else:
            zerocount = 16 - len(str) % 16
            for i in range(0, zerocount):
                str = str + '\0'
            return str

    def decrypt_CBC(self, str, key):
        # key = self.align(key, True)
        print key
        AESCipher = AES.new(key, AES.MODE_CBC, key)
        paint = AESCipher.decrypt(str)
        return paint


app = QtGui.QApplication(sys.argv)
ex = DeCodeTools()
ex.show()
app.exec_()
