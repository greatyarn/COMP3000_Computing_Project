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

    print(userSave.user_name)

    emailSend()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
