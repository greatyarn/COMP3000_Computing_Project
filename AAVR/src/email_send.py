import smtplib
import os
from dotenv import load_dotenv, find_dotenv
from SavingUser import *
from otpCreate import *
load_dotenv(find_dotenv())


def emailSend(user_name, otp):

    # Email Address for sender is written here
    email_address = os.getenv("EMAILSEND")
    password = os.getenv("EMAILPASS")

    # Email Address for receiver is written here
    email_address_receiver = os.getenv("EMAILSEND")

    # Email Subject
    subject = "Hello! Here is the OTP that you requested " + user_name

    # Email Body
    body = "Your OTP is " + str.otp + \
        "Please say this OTP to verify your account to the robot once requested. Thank you very much!"

    try:
        # SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("Connection to mail server established")
        # server.ehlo()
        print("a")
        server.starttls()
        print("b")
        server.login(email_address, password)
        print("c")
        server.sendmail(email_address, email_address_receiver, subject + body)
        print("D")
        server.quit()
    except Exception as E:
        print(str(E))
