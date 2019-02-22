# Misc Imports
from PIL import Image
import os
import sys # not sure if necessary anymore
# Picture Imports
cv2Installed = True
try:
    import cv2
except ImportError:
    print("cv2 not installed")
    cv2Installed = False
PicamInstalled = True
try:
    from picamera import PiCamera
except ImportError:
    PicamInstalled = False
# Email Imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import smtplib
# PyQt Imports
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QFrame
# Misc Stuff
SelectRange = len([name for name in os.listdir('overlays') if os.path.isfile(os.path.join('overlays', name))])
os.makedirs("output", exist_ok=True)
import datetime
now = datetime.datetime.now()
timedir = "output/" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
os.makedirs(timedir)
# Picture Function
def TakePicture():
    global cv2Installed, PicamInstalled
    if cv2Installed == True:
        cam = cv2.VideoCapture(0)
        retval, img = cam.read()
        cv2.imwrite("photo.png", img)
        cam.release()
    if PicamInstalled == True:
        cam = PiCamera()
        cam.capture('photo.png')


def ApplyOverlays(SelectRange):
    TakePicture()
    for i in range(SelectRange):
        photo = Image.open('photo.png')
        overlay = Image.open('overlays/overlay{}.png'.format(i)).resize(photo.size, Image.ANTIALIAS)
        photo.paste(overlay, (0,0), overlay)
        photo.save(timedir + '/output{}.png'.format(i))

# PyQt Gui
app = QApplication([])
# Start Window
StartWindow = QWidget()
StartLabel = QLabel('CS Club Photobooth!\n Press the enter key or the button to get started!')
StartLabel.setAlignment(Qt.AlignCenter)
StartLabel.setFont(QFont('Arial', 40))
StartButton = QPushButton('Start!')
StartButton.setDefault(True)
#StartButton.clicked.connect(StartFunction)
# Start Layout
StartLayout = QVBoxLayout()
StartLayout.addWidget(StartLabel)
StartLayout.addWidget(StartButton)
StartWindow.setLayout(StartLayout)
StartWindow.showFullScreen()

# Start Logic
counter = 7
timer = QTimer()
def num():
    global counter, timer
    if counter > 0:
        StartLabel.setText(str(counter))
        counter -= 1
    elif counter = 0:
        StartLabel.setText("Done! Please wait while we process your photo.")
        counter -= 1
    else:
        timer.stop()
        ApplyOverlays(SelectRange)
        SelectFunction()
def StartFunction():
    timer.timeout.connect(num)
    timer.start(1000)
StartButton.clicked.connect(StartFunction)

# Select Window
SelectWindow = QWidget()
SelectLayout = QGridLayout()
SelectLayoutB = QVBoxLayout()
SelectButton = QPushButton('Continue')
SelectButton.setDefault(True)

def SelectFunction():
    for i in range(SelectRange):
        label = QLabel()
        #label.setFrameShadow(QFrame.Sunken)
        pixmap = QPixmap(timedir + '/output{}.png'.format(i))
        pixmap = pixmap.scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        label.setObjectName('label{}'.format(i))
        SelectLayout.addWidget(label, 0, i)
    SelectLayoutB.addLayout(SelectLayout)
    SelectLayoutB.addWidget(SelectButton)
    SelectWindow.setLayout(SelectLayoutB)
    StartWindow.close()
    SelectWindow.showFullScreen()

def SelectContinueFunction():
    SelectWindow.close()
    sys.exit()
SelectButton.clicked.connect(SelectContinueFunction)

app.exec_()
