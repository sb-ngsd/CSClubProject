from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QFrame

app = QApplication([])

class SelectWindow(QWidget):
    def __init__(self):
        super(SelectWindow, self).__init__()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print ("escape pressed")

SelectWindowC = SelectWindow()
label = QLabel(SelectWindowC)
label.setText("Test")
label.setFrameShape(QFrame.Panel)
label.setFrameShadow(QFrame.Raised)
#label.setStyleSheet("border: 20px")
label.setFrameShape(QFrame.NoFrame)
SelectWindowC.show()
app.exec_()
