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

# Overlay Function
def ApplyOverlays(SelectRange):
    TakePicture()
    for i in range(SelectRange):
        photo = Image.open('photo.png')
        overlay = Image.open('overlays/overlay{}.png'.format(i)).resize(photo.size, Image.ANTIALIAS)
        photo.paste(overlay, (0,0), overlay)
        photo.save('output/output{}.png'.format(i))

# Email Function
def SendEmail(ToAddr):
    global SelectList
    FromAddr = "cs.newglarus@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = FromAddr
    msg['To'] = ToAddr
    msg['Subject'] = "Your Photobooth Photos"
    msg.attach(MIMEText("Your photos are attached to this email.", 'plain'))
    def AttachPicture(i):
        MsgPicture = open("output/output{}.png".format(i), 'rb')
        MsgImage = MIMEImage(MsgPicture.read())
        MsgPicture.close()
        MsgImage.add_header('Content-Disposition', 'attachment', filename="output{}.png".format(i))
        msg.attach(MsgImage)
    for i in SelectList:
        if SelectList[i].Fstate == True:
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
counter = 5
timer = QTimer()
def num():
    global counter, timer
    if counter > 0:
        StartLabel.setText(str(counter))
        counter -= 1
    else:
        timer.stop()
        StartLabel.setText("Done! Please wait while we process your photo.")
        ApplyOverlays(SelectRange)
        SelectFunction()
def StartFunction():
    timer.timeout.connect(num)
    timer.start(1000)
StartButton.clicked.connect(StartFunction)

# Select Class
class SelectWindow(QWidget):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setFocusPolicy(Qt.StrongFocus)
    def keyPressEvent(self, event):
        global SelectCurrentX, SelectCurrentY, SelectList
        print (event.key())
        if event.key() == Qt.Key_Left and SelectCurrentX > 0:
            SelectCurrentX -= 1
            SelectButton.setText(str(SelectCurrentX))
            SelectList[SelectCurrentX + 1].setFrameShape(QFrame.NoFrame)
            SelectList[SelectCurrentX].setFrameShape(QFrame.Panel)
        elif event.key() == Qt.Key_Right and SelectCurrentX < SelectRange - 1:
            SelectCurrentX += 1
            SelectButton.setText(str(SelectCurrentX))
            if SelectCurrentX != 0:
                SelectList[SelectCurrentX - 1].setFrameShape(QFrame.NoFrame)
            SelectList[SelectCurrentX].setFrameShape(QFrame.Panel)
        elif event.key() == Qt.Key_Up:
            print ("Up Arrow Pressed")
        elif event.key() == Qt.Key_Down:
            print ("Down Arrow Pressed")
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            SelectButton.setText("Enter" + str(SelectCurrentX))
            SelectList[SelectCurrentX].Fstate = not SelectList[SelectCurrentX].Fstate
            if SelectList[SelectCurrentX].Fstate == True:
                SelectList[SelectCurrentX].setStyleSheet("background-color: black;")
                #SelectList[SelectCurrentX].setFrameShape(QFrame.Panel)
            else:
                #SelectList[SelectCurrentX].setFrameShape(QFrame.NoFrame)
                SelectList[SelectCurrentX].setStyleSheet("")

# Select Window
SelectWindow = SelectWindow()
SelectLayout = QGridLayout()
SelectLayoutB = QVBoxLayout()
SelectButton = QPushButton('Continue')
SelectButton.setDefault(False)
SelectList = dict()
SelectCurrentX = 0
SelectCurrentY = 0

# Select Function
def SelectFunction():
    for i in range(SelectRange):
        label = QLabel()
        label.setFrameShadow(QFrame.Sunken)
        label.setLineWidth(3)
        pixmap = QPixmap('output/output{}.png'.format(i))
        pixmap = pixmap.scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        label.setObjectName('label{}'.format(i))
        SelectList[i] = label
        SelectList[i].Fstate = False
        SelectLayout.addWidget(SelectList[i], 0, i)
    SelectList[0].setFrameShape(QFrame.Panel) 
    SelectLayoutB.addLayout(SelectLayout)
    SelectLayoutB.addWidget(SelectButton)
    SelectWindow.setLayout(SelectLayoutB)
    StartWindow.close()
    SelectWindow.showFullScreen()
    SelectButton.setText(str(SelectCurrentX))

def SelectContinueFunction():
    SelectWindow.close()
    EmailWindow.showFullScreen()
SelectButton.clicked.connect(SelectContinueFunction)

# Email Window
EmailWindow = QWidget()
EmailTextBox = QLineEdit()
EmailButton = QPushButton('Send')
EmailCancelButton = QPushButton("Don't Send (Cancel)")
EmailLabel = QLabel('Email To Send Pictures To:')
EmailLabel.setAlignment(Qt.AlignBottom)
EmailLabel.setFont(QFont('Arial', 20))

EmailLayout = QVBoxLayout()
EmailLayout.setAlignment(Qt.AlignCenter)
EmailLayout.addWidget(EmailLabel)
EmailLayout.addWidget(EmailTextBox)
EmailLayout.addWidget(EmailButton)
EmailLayout.addWidget(EmailCancelButton)
EmailWindow.setLayout(EmailLayout)

# Email Function
def EmailFunction():
    ToAddr = EmailTextBox.text()
    EmailLabel.setText('Email sent to: ' + ToAddr)
    SendEmail(ToAddr)
    #This most likely is going to cause a memory leak over time
    os.execv(sys.executable, ['python3'] + sys.argv)

EmailButton.clicked.connect(EmailFunction)
EmailCancelButton.clicked.connect(lambda: os.execv(sys.executable, ['python3'] + sys.argv))
EmailTextBox.returnPressed.connect(EmailFunction)


app.exec_()
