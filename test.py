from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
app = QApplication([])
window = QWidget()
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
app.exec_()
