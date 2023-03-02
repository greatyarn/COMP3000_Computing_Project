import email_send as eu
import rospy
from qt_robot_interface.srv import *

def userSave():
    try:
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    #wait for the user to speak
    rospy.sleep(5)

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
    recognise = rospy.ServiceProxy('/qt_robot/speech/recognize', speech_recognize)


    # Log that the service is being called
    rospy.loginfo("Waiting for service /qt_robot/speech/say")
    rospy.loginfo("Waiting for service /qt_robot/speech/recognize")

    # Waits for the service to be available
    rospy.wait_for_service('/qt_robot/speech/say')
    rospy.wait_for_service('/qt_robot/speech/recognize')

    userSave()

    # Call the email_upload function
    eu.email_upload()
    

