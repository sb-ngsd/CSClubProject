#import and check if gpio pins are available
isGpioAvailable = False
try:
    import RPi.GPIO as GPIO
except ImportError:
    #global isGpioAvailable
    isGpioAvailable = False
    print("GPIO pins not available, falling back to software button!")
#GPIO logic
if isGpioAvailable == True:
    import threading
    from queue import Queue
    import time
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    t = threading.Thread(target=gpioThread)
    t.start()
    def gpioThread():
        while True:
            input_state = GPIO.input(18)
            if input_state == False:
                startupFunction()
                print('Button Pressed')
                time.sleep(0.2)
#Pillow import
from PIL import Image
#cv2 support?
cv2Installed = True
try:
    import cv2
except ImportError:
    print("cv2 not installed")
    cv2Installed = False
picamInstalled = True
try:
    from picamera import PiCamera
except ImportError:
    print("picam not installed")
    picamInstalled = False
#Take Photo
def cameraFunction():
    global cv2Installed
    global picamInstalled
    if cv2Installed == True:
        cam = cv2.VideoCapture(0)
        retval, img = cam.read()
        cv2.imwrite("photo.png", img)
        cam.release()
    if picamInstalled == True:
        cam = PiCamera()
        cam.capture('photo.png')


#Overlay logic
pictureTaken = False
import os
os.makedirs("output", exist_ok=True)
def overlayFunction(count):
    #only take picture once
    global pictureTaken
    if pictureTaken == False:
        cameraFunction()
        pictureTaken = True
    photo = Image.open('photo.png')
    psize = pwidth, pheight = photo.size
    overlay = Image.open('overlays/overlay{}.png'.format(count))
    overlayS = overlay.resize((pwidth, pheight), Image.ANTIALIAS)
    photo.paste(overlayS, (0,0), overlayS)
    photo.save('output/output{}.png'.format(count))

#Email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import smtplib
#Email function
def sendEmail():
    global selectedP
    #to vars
    fromaddr = "cs.newglarus@gmail.com"
    toaddr = toAddrInput

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    #subject
    msg['Subject'] = "Photobooth Photos"
    #body
    body = "Your photos are attached to this email."
    #attachment stuff
    msg.attach(MIMEText(body, 'plain'))
    for i in range(selectedRange):
        #filename = "output{}.png".format(i)
        #attachment = open("output/output{}.png".format(i), "rb")
        #more attachment stuff
        #part = MIMEBase('application', 'octet-stream')
        #part.set_payload((attachment).read())
        #encoders.encode_base64(part)
        #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        #msg.attach(part)
        msgPicture = open("output/output{}.png".format(i), 'rb')
        msgImage = MIMEImage(msgPicture.read())
        msgPicture.close()
        msgImage.add_header('Content-Disposition', 'attachment', filename="output{}.png".format(i))
        msg.attach(msgImage)
    #start smtp
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #get password from environment variable
    #set it on linux with: export INPLAINSITE="passwd"
    #set it on windows with: SET INPLAINSITE=passwd
    passwd = os.environ.get('INPLAINSITE')
    if passwd == "None":
        print('DEBUGGING NOTE: cs.newglarus password must be input, instructions are in README.md')
    server.login(fromaddr, passwd)
    text = msg.as_string()
    #send and quit
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#GUI Stuff
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
#from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QGridLayout
#Countdown Stuff
import sys
#get amount of filters in overlays folder
selectedRange = len([name for name in os.listdir('overlays') if os.path.isfile(os.path.join('overlays', name))])
#Init PyQt5
app = QApplication([])
#Startup Vars
startupWindow = QWidget()
startupLabel = QLabel('CS Club Photobooth!\n Press the button to get started!')
startupButton = QPushButton('Simulate Physical Button')
#Startup Window Layout
startupLayout = QVBoxLayout()
startupLayout.addWidget(startupLabel)
if isGpioAvailable == False:
    startupLayout.addWidget(startupButton)
startupWindow.setLayout(startupLayout)
startupLabel.setAlignment(Qt.AlignCenter)
startupLabel.setFont(QFont('Arial', 40))

#Show Startup Window
startupWindow.showFullScreen()

#Startup Logic
counter=5
timer = QTimer()
def num():
    global counter, timer
    if counter > 0:
        startupLabel.setText(str(counter))
        counter -= 1
    else:
        timer.stop()
        startupLabel.setText("Done!")
        #overlayFunction()
        selectFunction()
        startupWindow.close()
        selectWindow.showFullScreen()
        #emailWindow.showFullScreen()

def startupFunction():
    timer.timeout.connect(num)
    timer.start(1000)

if isGpioAvailable == False:
    startupButton.setDefault(True)
    startupButton.clicked.connect(lambda: startupFunction())

#Filter Selection Window
selectWindow = QWidget()
selectLayout = QGridLayout()
selectLayoutB = QVBoxLayout()
selectButton = QPushButton('Continue')
selectButton.setDefault(True)
selectButton.clicked.connect(lambda: selectContinueFunction())
labelList = dict()
#range = number of filters, example: 3 = 0,1,2
def selectFunction():
    for i in range(selectedRange):
        overlayFunction(i)
        name = 'label{}'.format(i)
        label = QLabel()
        pixmap = QPixmap('output/output{}.png'.format(i))
        pixmapS = pixmap.scaled(480, 360, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmapS)
        #label.mousePressEvent = chooseFunction
        label.setObjectName(name)
        selectLayout.addWidget(label, 0, i)
        labelList[name] = label
    selectLayoutB.addLayout(selectLayout)
    selectLayoutB.addWidget(selectButton)
    selectWindow.setLayout(selectLayoutB)

def selectContinueFunction():
    selectWindow.close()
    emailWindow.showFullScreen()

#No longer used (for now)
def chooseFunction(event, num):
    global selectedP
    selectedP = num
    selectWindow.close()
    emailWindow.showFullScreen()

#Email Vars
emailWindow = QWidget()
emailTextBox = QLineEdit()
emailButton = QPushButton('Send')
emailCancelButton = QPushButton("Don't Send (Cancel)")
emailLabel = QLabel('Email To Send Pictures To:')
emailLabel.setAlignment(Qt.AlignBottom)
emailLabel.setFont(QFont('Arial', 20))

#Email Window Layout
emailLayout = QVBoxLayout()
emailLayout.setAlignment(Qt.AlignCenter)
emailLayout.addWidget(emailLabel)
emailLayout.addWidget(emailTextBox)
emailLayout.addWidget(emailButton)
emailLayout.addWidget(emailCancelButton)
emailWindow.setLayout(emailLayout)

#Email Logic
toAddrInput = ""
def buttonFunction():
    global toAddrInput
    toAddrInput = emailTextBox.text()
    sendEmail()
    emailLabel.setText('Email sent to: ' + toAddrInput)
    #if the program crashes here, trying changing python3 to python
    os.execv(sys.executable, ['python3'] + sys.argv)
emailButton.clicked.connect(lambda: buttonFunction())
emailCancelButton.clicked.connect(lambda: os.execv(sys.executable, ['python3'] + sys.argv))
emailTextBox.returnPressed.connect(lambda: buttonFunction())

app.exec_()
