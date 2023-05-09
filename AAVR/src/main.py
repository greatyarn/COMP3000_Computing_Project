#!/usr/bin/env python
import rospy
from db import *
from SavingUser import *
from otpCreate import *
from email_send import *
from otpConfirm import *
from SavingEmail import *
from MailProvider import *

if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

    user_name = userSave()
    otp = otpCreate()
    email_address = emailSave()
    email_address_Confirmed = mailProvider(email_address)

    # print(user_name, otp)  # For testing purposes
    # print(type(user_name))  # Testing Purposes
    # print(email_address_Confirmed)  # For testing purposes

    # Check if email exists in database
    if email_check(email_address_Confirmed) == True:
        print("Email exists")
        otp = otpCreate()
        emailSend(user_name, otp)
        confirmOTP(otp)
    else:
        print("Email does not exist")
        otp = otpCreate()
        upload_user(user_name, otp, email_address_Confirmed)
        emailSend(user_name, otp)
        confirmOTP(otp)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
