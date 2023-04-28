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

    user_name = userSave()
    print(user_name)

    otp = otpCreate()
    print(otp)
    # upload_user()

    print(user_name, otp)

    emailSend()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
