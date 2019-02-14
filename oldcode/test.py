from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QMainWindow
app = QApplication([])
#window = QWidget()
class window(QWidget):
     def __init__(self, parent=None):
         __init__(self, parent)
         self.ui = Ui_myMain()
         self.ui.setupUi(self)

     def keyPressEvent(self, event):
         if type(event) == QKeyEvent:
             #here accept the event and do something
             print (event.key())
             event.accept()
         else:
             event.ignore()

    label = QLabel()
    pixmap = QPixmap('output.png')
    pixmapS = pixmap.scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
    label.setPixmap(pixmapS)

label2 = QLabel()
pixmap2 = QPixmap('output1.png')
pixmapS2 = pixmap2.scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
label2.setPixmap(pixmapS2)


layout = QGridLayout()
layout.addWidget(label, 0, 0)
layout.addWidget(label2, 0, 1)
window.setLayout(layout)
window.show()
window2 = QWidget()
button = QPushButton()
layout2 = QGridLayout()
icon = QIcon('output.png')
button.setIcon(icon)
button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
layout2.addWidget(button, 0, 0)
window2.setLayout(layout2)
#window2.show()

app.exec_()
