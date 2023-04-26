import rospy
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize

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

# list_of_name = ['Adam', 'Greg']


def userSave():
    print("Saving User")
    try:
        # speechSay(query(db, info=name & action = ask))
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    # wait for the user to speak
    rospy.sleep(5)

    user_name = recognise("en-US", ['Adam', 'Gregory'], 5)
    rospy.loginfo(user_name)

    print("Is this the right name?")
    speechSay("Hello %s, Is this the right name?" % user_name.transcript)
    rospy.sleep(5)

    try:
        confirmation.transcript = recognise("en-US", ['yes', 'no'], 5)
        if confirmation.transcript == "yes":
            rospy.loginfo("Yes")
            speechSay("Ok, I will remember that")
            return user_name
        else:
            rospy.loginfo("No")
            speechSay("Let's try that again!")
            userSave()
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
