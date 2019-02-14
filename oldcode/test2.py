import sys, os
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog, QListWidgetItem, QListWidget, QVBoxLayout
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
list = QListWidget()
#itm = QListWidgetItem("")
#itm.setIcon(QIcon("output.png"))
#list.addItem(itm)
label = QLabel()
pixmap = QPixmap("output.png")
label.setPixmap(pixmap)
itm = QListWidgetItem()
itm.setSizeHint(label.sizeHint())
list.addItem(itm)
list.setItemWidget(itm, label)
layout.addWidget(list)
window.setLayout(layout)
window.show()
app.exec_()
