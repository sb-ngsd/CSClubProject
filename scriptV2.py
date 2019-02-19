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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QFrame
# Misc Stuff
SelectRange = len([name for name in os.listdir('overlays') if os.path.isfile(os.path.join('overlays', name))])
os.makedirs("output", exist_ok=True)
# Picture Function
def TakePicture(cv2installed, PicamInstalled):
    if cv2installed == True:
        cam = cv2.VideoCapture(0)
        retval, img = cam.read()
        cv2.imwrite("photo.png", img)
        cam.release()
    if PicamInstalled == True:
        cam = PiCamera()
        cam.capture('photo.png')

# Overlay Function
def ApplyOverlays(SelectRange):
    TakePicture(cv2installed, PicamInstalled)
    for _ in range(SelectRange):
        photo = Image.open('photo.png')
        overlay = Image.open('overlays/overlay{}.png'.format(SelectRange)).resize(photo.size, Image.ANTIALIAS)
        photo.paste(overlay, (0,0), overlay)
        photo.save('output/output{}.png'.format(SelectRange))

# Email Function
def SendEmail(ToAddr):
    FromAddr = "cs.newglarus@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = FromAddr
    msg['To'] = ToAddr
    msg['Subject'] = "Your Photobooth Photos"
    msg.attach(MIMEText("Your photos are attached to this email.", 'plain'))
    def AttachPicture(i):
        MsgImage = MIMEImage(open("output/output{}.png".format(i), 'rb').read().close())
        MsgImage.add_header('Content-Disposition', 'attachment', filename="output{}.png".format(i))
        msg.attach(MsgImage)
    if not ItmArrCurrent:
        for i in range(SelectRange):
            AttachPicture(i)
    else:
        for i in ItmArrCurrent:
            AttachPicture(i)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    passwd = os.environ.get('INPLAINSITE')
    server.login(FromAddr, passwd)
    server.sendmail(FromAddr, ToAddr, msg.as_string())
    server.quit()

# PyQt Gui
app = QApplication([])
# Start Window
StartWindow = QWidget()
StartLabel = QLabel('CS Club Photobooth!\n Press the enter key or the button to get started!')
StartLabel.setAlignment(Qt.AlignCenter).setFont(QFont('Arial', 40))
StartButton = QPushButton('Start!')
StartButton.setDefault(True).clicked.connect(StartFunction)
# Start Layout
StartLayout = QVBoxLayout().addWidget(StartLabel).addWidget(StartButton)
StartWindow.setLayout(StartLayout)
StartWindow.showFullScreen()

# Start Logic
StartCounter = 5
StartTimer = QTimer()
def StartTimer():
    global StartCounter, StartTimer
    if StartCounter > 0:
        StartLabel.setText(str(StartCounter))
        StartCounter -= 1
    else:
        StartTimer.stop()
        StartLabel.setText("Done! Please wait while we process your photo.")
        ApplyOverlays(SelectRange)
        
def StartFunction():
    StartTimer.timeout.connect(StartTimer)
    StartTimer.start(1000)

# Select Class
class SelectWindow(QWidget):
    def __init__(self):
        super(SelectWindow, self).__init__()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            print ("Left Arrow Pressed")
        elif event.key() == Qt.Key_Right:
            print ("Right Arrow Pressed")
        elif event.key() == Qt.Key_Up:
            print ("Up Arrow Pressed")
        elif event.key() == Qt.Key_Down:
            print ("Down Arrow Pressed")

# Select Window
SelectWindow = SelectWindow()
SelectLayout = QGridLayout()
SelectLayoutB = QVBoxLayout()
SelectButton = QPushButton('Continue')
SelectButton.setDefault(True)
SelectButton.clicked.connect(SelectContinueFunction)
SelectList = dict()
SelectCurrent = ""

# Select Function
def SelectFunction():
    for i in range(SelectRange):
        label = QLabel().setFrameShadow(QFrame.Sunken)
        pixmap = QPixmap('output/output{}.png'.format(i)).scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        label.setObjectName('label{}'.format(i))
        SelectList[i] = label

# 
