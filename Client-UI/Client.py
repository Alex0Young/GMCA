import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QFont

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #static set show font
        QToolTip.setFont(QFont('SansSerif', 10))
        #build tips
        self.setToolTip('This is a <b>TEST</b> widget')
        #build button
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>TEST</b> widget')
        btn.resize(btn.sizeHint())
        #set location
        btn.move(50,50)
        #set windows size and location
        self.setGeometry(500,500,300,220)
        #set title
        self.setWindowTitle('GM Client')
        #set icon
        self.setWindowIcon(QIcon('logo.png'))
        #show window
        self.center()
        self.show()

    def center(self):
        #get window
        qr = self.frameGeometry()
        #get center point
        cp = QDesktopWidget().availableGeometry().center()
        #show in center
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())
