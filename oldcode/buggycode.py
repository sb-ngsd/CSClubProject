#import and check if gpio pins are available
isGpioAvailable = True
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
#Overlay logic
def overlayFunction():
    for i in range(1,4):
        photo = Image.open('photo.png')
        overlay = Image.open('overlay{0}.png'.format(i))
        photo.paste(overlay, (0,0), overlay)
        photo.save('output{0}.png'.format(i))

#Email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
#Email function
def sendEmail():
    #to/from vars
    fromaddr = "samuel.brand@ngsd.k12.wi.us"
    toaddr = toAddrInput

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    #subject
    msg['Subject'] = "Python Email Test"
    #body
    body = "Testing sending an email with an attachment with python"
    #attachment stuff
    msg.attach(MIMEText(body, 'plain'))
    filename = "output.png"
    attachment = open("output.png", "rb")
    #more attachment stuff
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    #start smtp
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #get password from environment variable
    #set it on linux with: export INPLAINSITE="passwd"
    #set it on windows with: SET INPLAINSITE=passwd
    passwd = os.environ['INPLAINSITE']
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
#Keypress imports
from pynput.keyboard import KeyCode, Key, Listener

#Keypress logic
pressedNum = 10
def on_release(key):
    for i in range(1,5):
        if key == KeyCode(char=str(i)):
            global pressedNum
            pressedNum = i
            overlayFunction()
            previewWindow.close()
            emailWindow.show()
            return False
#with Listener(
#        on_release=on_release) as listener:
#    listener.join()

#Countdown Stuff
import os, sys
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
startupWindow.show()

#Startup Logic
counter=10
timer = QTimer()
def num():
    global counter, timer
    if counter > 0:
        startupLabel.setText(str(counter))
        counter -= 1
    else:
        timer.stop()
        startupLabel.setText("Done!")
        startupWindow.close()
        previewWindow.show()
        #with Listener(
        #        on_release=on_release) as listener:
        #    listener.join()

def startupFunction():
    timer.timeout.connect(num)
    timer.start(1000)

if isGpioAvailable == False:
    startupButton.setDefault(True)
    startupButton.clicked.connect(lambda: startupFunction())

#Preview Vars
previewWindow = QWidget()
preview1 = QLabel()
preview1.setPixmap(QPixmap('output1.png'))
preview2 = QLabel()
preview2.setPixmap(QPixmap('output2.png'))
preview3 = QLabel()
preview3.setPixmap(QPixmap('output3.png'))
preview4 = QLabel()
preview4.setPixmap(QPixmap('output4.png'))

#Preview Window Layout
previewLayout = QGridLayout()
previewLayout.setColumnStretch(1, 4)
previewLayout.setColumnStretch(2, 4)
previewLayout.addWidget(preview1,0,0)
previewLayout.addWidget(preview2,0,1)
#previewLayout.addwidget(preview3,1,0)
#previewLayout.addwidget(preview4,1,1)
previewWindow.setLayout(previewLayout)

#Email Vars
emailWindow = QWidget()
emailTextBox = QLineEdit()
emailButton = QPushButton('Send')
emailLabel = QLabel('Email To Send Picture:')
emailLabel.setAlignment(Qt.AlignBottom)
emailLabel.setFont(QFont('Arial', 20))

#Email Window Layout
emailLayout = QVBoxLayout()
emailLayout.setAlignment(Qt.AlignCenter)
emailLayout.addWidget(emailLabel)
emailLayout.addWidget(emailTextBox)
emailLayout.addWidget(emailButton)
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
emailTextBox.returnPressed.connect(lambda: buttonFunction())

app.exec_()
