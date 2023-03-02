from main import *
import smtplib


def email_upload():
    # Email Address for sender is written here
    email_address = ""
    password = ""

    # Email Address for receiver is written here
    email_address_receiver = ""

    # Email Subject
    subject = "Hello! Here is the OTP that you requested " + user_name

    # Email Body
    body = "Your OTP is " + otp + "Please say this OTP to verify your account to the robot once requested. Thank you very much!"

