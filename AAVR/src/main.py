#!/usr/bin/env python
import rospy
import db as db
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
from otpCreate import otpCreate
from SavingUser import userSave
from email_send import emailSend

if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

    userSave()
    otpCreate()
    emailSend()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
