#! /usr/bin/python
import time
import RPi.GPIO as GPIO
import os
import picamera
import smtplib
import sys
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
cam = picamera.PiCamera()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Door detection
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#switch1
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#alarm
GPIO.setup(15, GPIO.OUT, GPIO.LOW)

def takePicture():
  time.sleep(3)
  cam.capture("/home/pi/Desktop/latest.jpg")
  time.sleep(3)

def sendPicture(ImgFileName):
  COMMASPACE = ', '
  me = 'cis191acct@gmail.com'
  family = ['akatsuka@sas.upenn.edu']

  #Root definitions
  msg = MIMEMultipart()
  msg['Subject'] = 'Door entry detected!'
  msg['From'] = me
  msg['To'] = COMMASPACE.join(family)
  msg.preamble = 'Someone has opened the door.'

  #Attach image
  fp = open(ImgFileName, 'rb')
  img = MIMEImage(fp.read())
  fp.close()
  msg.attach(img)

  #Attach text
  msg.attach(MIMEText('Hello, Someone has recently entered your room'))

  #Send email
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.ehlo()
  s.starttls()
  s.ehlo()
  s.login('cis191acct@gmail.com', 'PewPers123')
  s.sendmail(me, family, msg.as_string())
  s.quit()

while True:
  if (GPIO.input(7) == GPIO.HIGH):
    time.sleep(0.1)
    GPIO.output(15, GPIO.LOW)
  else:
    GPIO.output(15, GPIO.input(18))
    takePicture()
    sendPicture('/home/pi/Desktop/latest.jpg')
    time.sleep(0.1)

GPIO.cleanup()
