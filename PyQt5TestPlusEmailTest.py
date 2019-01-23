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
    msg['Subject'] = "Python Email Test 3"
    #body
    body = "Testing sending an email with an attachment with python"
    #attachment stuff
    msg.attach(MIMEText(body, 'plain'))
    filename = "TestImg.png"
    attachment = open("TestImg.png", "rb")
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
from PyQt5.QtGui import QFont
#from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
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
        #TAKE PICTURE CODE HERE
        startupWindow.close()
        emailWindow.show()

def startupFunction():
    #startupButton.setText('Clicked (Temp)')
    timer.timeout.connect(num)
    timer.start(1000)

if isGpioAvailable == False:
    startupButton.setDefault(True)
    startupButton.clicked.connect(lambda: startupFunction())

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
