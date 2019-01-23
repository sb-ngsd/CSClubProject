#from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit
#app = QApplication([])
#label = QLabel('Hello World!')
#line = QLineEdit()
#line.show()
#label.show()
#app.exec_()

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
import time
#Init PyQt5
app = QApplication([])
#Startup Vars
startupWindow = QWidget()
startupLabel = QLabel('CS Club Photobooth!\n Press the button to get started!')
startupButton = QPushButton('Simulate Physical Button')

#Startup Window Layout
startupLayout = QVBoxLayout()
startupLayout.addWidget(startupLabel)
startupLayout.addWidget(startupButton)
startupWindow.setLayout(startupLayout)
startupLabel.setAlignment(Qt.AlignCenter)
startupLabel.setFont(QFont('Arial', 40))

#Show Startup Window
startupWindow.show()

#Startup Logic (somehow this works, I have no clue how but just go with it)
def start_timer(slot, count=1, interval=1000):
    counter = 11
    def handler():
        nonlocal counter
        counter -= 1
        slot(counter)
        if counter <= 0:
            timer.stop()
            timer.deleteLater()
    timer = QTimer()
    timer.timeout.connect(handler)
    timer.start(interval)

def timer_func(count):
    startupLabel.setText(str(count))
    if count <= 0:
        startupLabel.setText("Done!")
        #TAKE PICTURE CODE HERE
        startupWindow.close()
        emailWindow.show()

def startupFunction():
    startupButton.setText('Clicked (Temp)')
    start_timer(timer_func, 11)

startupButton.clicked.connect(lambda: startupFunction())

#Email Vars
emailWindow = QWidget()
emailTextBox = QLineEdit()
emailButton = QPushButton('Send')
emailLabel = QLabel('Email To Send Picture:')

#Email Window Layout
emailLayout = QVBoxLayout()
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
emailButton.clicked.connect(lambda: buttonFunction())

app.exec_()
