#!/usr/bin/env python
import rospy
from qt_robot_interface.srv import speech_say, speech_recognize
import db as db
import smtplib
import os
from dotenv import load_dotenv, find_dotenv


def otpCreate():
    print("Creating OTP")
    import random
    global otp
    otp = ""

    # Create a for loop that will run 6 times
    for i in range(6):
        # Create a variable called num and set it to a random number between 0 and 9
        num = random.randint(0, 9)

        # Add the value of num to the end of the otp variable
        otp += str(num)

    return otp

# usersave(info_type)
# usersave("name")
# usersave("phone")


def userSave():
    print("Saving User")
    try:
        # speechSay(query(db, info=name & action = ask))
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    # wait for the user to speak
    rospy.sleep(5)

    global user_name
    user_name = recognise("en-US")
    rospy.loginfo(user_name)

    speechSay("Hello " + user_name + " Is this the right name?")
    rospy.sleep(5)

    try:
        confirmation = recognise("en-US")
        if confirmation == "yes":
            rospy.loginfo("Yes")
            speechSay("Ok, I will remember that")
        else:
            rospy.loginfo("No")
            speechSay("Let's try that again!")
            userSave()
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)


def email_send():
    print("Sending Email")
    load_dotenv(find_dotenv())

    # Email Address for sender is written here
    email_address = os.getenv("EMAILSEND")
    password = os.getenv("EMAILPASS")

    # Email Address for receiver is written here
    email_address_receiver = os.getenv("EMAILSEND")

    # Email Subject
    subject = "Hello! Here is the OTP that you requested " + user_name

    # Email Body
    body = "Your OTP is " + otp + \
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


if __name__ == '__main__':

    # Initialize the node
    print("Starting AAVR")
    rospy.init_node('AAVR')

    # Define ROS Services
    print("Defining ROS Services")
    speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
    recognise = rospy.ServiceProxy(
        '/qt_robot/speech/recognize', speech_recognize)

    # Log that the service is being called
    print("Waiting for service /qt_robot/speech/say")
    rospy.loginfo("Waiting for service /qt_robot/speech/say")

    print("Waiting for service /qt_robot/speech/recognize")
    rospy.loginfo("Waiting for service /qt_robot/speech/recognize")

    # Waits for the service to be available
    print("Waiting for service to be available")
    rospy.wait_for_service('/qt_robot/speech/say')
    rospy.wait_for_service('/qt_robot/speech/recognize')

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
