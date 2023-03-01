import email_upload as eu
import rospy
from qt_robot_interface.srv import *

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

    # Log that the service is now available
    try:
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    # Call the email_upload function
    eu.email_upload()
    

