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
    #to/from var
    fromaddr = "samuel.brand@ngsd.k12.wi.us"
    toaddr = mytext

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
    passwd = os.environ['INPLAINSITE']
    server.login(fromaddr, passwd)
    text = msg.as_string()
    #send and quit
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#GUI Stuff
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
#Init PyQt5
app = QApplication([])
#Vars
window = QWidget()
window2 = QWidget()
textBox = QLineEdit()
button = QPushButton('Send')
label = QLabel('Email To Send Picture:')
#Layout
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(textBox)
layout.addWidget(button)

#Show
window.setLayout(layout)
window2.show()
window.show()
window2.close()

#Logic
mytext = ""
def buttonFunction():
    global mytext
    mytext = textBox.text()
    sendEmail()
    label.setText('Email sent to: ' + mytext)
button.clicked.connect(lambda: buttonFunction())

app.exec_()
