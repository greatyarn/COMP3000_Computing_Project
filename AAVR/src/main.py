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

    userSave()
    otpCreate()
    # upload_user()

    print(otpCreate.otp)

    emailSend(userSave.user_name, otpCreate.otp)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
