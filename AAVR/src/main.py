#!/usr/bin/env python
import rospy
from db import *
from SavingUser import *
from otpCreate import *
from email_send import *

if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

    user_name = userSave()
    otp = otpCreate()

    upload_user(user_name, otp)

    print(user_name, otp)  # For testing purposes

    emailSend(user_name, otp)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
