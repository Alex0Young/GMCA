# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,QMainWindow,QAction,qApp
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGridLayout, QProgressBar, QFrame, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QBasicTimer

class Example(QWidget):
    def __init__(self):
        super().__init__()
        #self.stateInit()
        #self.initPanel()
        self.initGUI()
        #self.initFrame()

    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle('GM')
        self.show()
    def stateInit(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Statusbar')
        self.show()
    def initPanel(self):
        exitAct = QAction(QIcon('logo.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        self.setGeometry(500,500,300,300)
        self.setWindowTitle('Simple menu')
        self.show()
    def initTable(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(500, 500, 350, 300)
        self.setWindowTitle('Review')
        self.show()
    def initGUI(self):
        self.CountryName = QLabel('CountryName')
        self.StateName = QLabel('StateOrProvinceName')
        self.LocalName = QLabel('LocalityName')
        self.OrganizationName = QLabel('QrganizationName')
        self.UnitName = QLabel('QrganzationUnitName')
        self.CommonName = QLabel('CommonName')
        self.Email = QLabel('EmailAddress')
        self.KeyPass = QLabel('私钥加密口令')

        self.CNEdit = QLineEdit()
        self.SNEdit = QLineEdit()
        self.LNEdit = QLineEdit()
        self.ONEdit = QLineEdit()
        self.UNEdit = QLineEdit()
        self.CMEdit = QLineEdit()
        self.EEdit = QLineEdit()
        self.KPEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.CountryName, 1, 0)
        grid.addWidget(self.CNEdit, 1, 1)
        grid.addWidget(self.StateName, 1, 2)
        grid.addWidget(self.SNEdit, 1, 3)

        grid.addWidget(self.LocalName, 2, 0)
        grid.addWidget(self.LNEdit, 2, 1)
        grid.addWidget(self.OrganizationName, 2, 2)
        grid.addWidget(self.ONEdit, 2, 3)

        grid.addWidget(self.UnitName, 3, 0)
        grid.addWidget(self.UNEdit, 3, 1)
        grid.addWidget(self.CommonName, 3, 2)
        grid.addWidget(self.CMEdit, 3, 3)

        grid.addWidget(self.Email, 4, 0)
        grid.addWidget(self.EEdit, 4, 1)
        grid.addWidget(self.KeyPass, 4, 2)
        grid.addWidget(self.KPEdit, 4, 3)

        #self.certFrame.setLayout(grid)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid)

        self.genKey = QPushButton('生成用户私钥')
        self.genReq = QPushButton('生成证书请求')
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.genKey)
        hbox.addWidget(self.genReq)

        self.info = QLabel('日志信息')
        self.infoText = QTextEdit()
        grid1 = QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.info, 1, 0)
        grid1.addWidget(self.infoText, 1, 1)

        self.CAIP = QLabel('CA IP')
        self.CAPort = QLabel('CA 端口')
        self.IPEdit = QLineEdit()
        self.PortEdit = QLineEdit()
        self.choseFile = QPushButton('选取文件')
        self.sendCert = QPushButton('发送请求', self)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.prog = QLabel('传输进度')

        grid2 = QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(self.CAIP, 1, 0)
        grid2.addWidget(self.IPEdit, 1, 1)
        grid2.addWidget(self.CAPort, 1, 2)
        grid2.addWidget(self.PortEdit, 1, 3)
        grid2.addWidget(self.choseFile, 2, 0)
        grid2.addWidget(self.sendCert, 2, 2)
        hbox1= QHBoxLayout()
        hbox1.addWidget(self.prog)
        hbox1.addWidget(self.pbar)

        vbox.addLayout(hbox)
        vbox.addLayout(grid1)
        vbox.addLayout(grid2)
        vbox.addLayout(hbox1)

        self.sendCert.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        self.step = 0

        self.setLayout(vbox)
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('GM Client')
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.sendCert.setText('Finished')
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.sendCert.setText('Start')
        elif self.step < 100:
            self.timer.start(100, self)
            self.sendCert.setText('Stop')
        else:
            self.step = 0
            #self.timer.start(100, self)
            self.sendCert.setText('发送请求')

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:/')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()


    def initFrame(self):
        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        #topright.setLayout()
        #bottom = QFrame(self)
        #bottom.setFrameShape(QFrame.StyledPanel)

        hbox.addWidget(topleft)
        hbox.addWidget(topright)
        self.setLayout(hbox)
        self.setGeometry(300,300,300,200)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())