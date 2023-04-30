#!/usr/bin/env python
import rospy
from db import *
from SavingUser import *
from otpCreate import *
from email_send import *
from otpConfirm import *
from SavingEmail import *

if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

    user_name = userSave()
    otp = otpCreate()

    print(user_name, otp)  # For testing purposes
    print(type(user_name))  # Testing Purposes

    email_address = emailSave()

    upload_user(user_name, otp)
    emailSend(user_name, otp)
    confirmOTP(otp)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
