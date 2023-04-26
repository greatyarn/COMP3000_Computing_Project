#!/usr/bin/env python
import rospy
import db as db
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
from otpCreate import otpCreate
from SavingUser import userSave

if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

   
    userSave()
    otpCreate()
    email_send(user_name, otp)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
