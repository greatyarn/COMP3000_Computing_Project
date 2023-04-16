#!/usr/bin/env python3
import email_send as eu
import rospy
from qt_robot_interface.srv import *
import db as db


def otpCreate():
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


def userSave(info_type, ):
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


if __name__ == '__main__':

    # Define ROS Services
    speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
    recognise = rospy.ServiceProxy(
        '/qt_robot/speech/recognize', speech_recognize)

    # Log that the service is being called
    rospy.loginfo("Waiting for service /qt_robot/speech/say")
    rospy.loginfo("Waiting for service /qt_robot/speech/recognize")

    # Waits for the service to be available
    rospy.wait_for_service('/qt_robot/speech/say')
    rospy.wait_for_service('/qt_robot/speech/recognize')

    # userSave()

    # TODO Call the email_upload function
    #user_name = "Greg"
    otpCreate()
    eu.email_upload()
