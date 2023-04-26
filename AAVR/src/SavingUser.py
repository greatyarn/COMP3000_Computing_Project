import rospy
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize
import wave
from audio_common_msgs.msg import AudioData
import uuid

# Define ROS Services
print("Defining ROS Services")
speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
recognise = rospy.ServiceProxy(
    '/qt_robot/speech/recognize', speech_recognize)
rospy.init_node('audio_record')
rospy.loginfo("audio_record node started")

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_WIDTH = 2

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


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


def userSave():
    print("Saving User")
    try:
        # speechSay(query(db, info=name & action = ask))
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    # wait for the user to speak
    rospy.sleep(5)

    # user_name = recognise("en-US", ['Adam', 'Gregory'], 5)
    # rospy.loginfo(user_name)

    temp = str(uuid.uuid4())

    wf = wave.open(temp + ".wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)

    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")

    # stops the recording after 10 seconds
    rospy.sleep(3)

    speechSay("Recording complete")

    # print("Is this the right name?")
    # speechSay("Hello %s, Is this the right name?" % user_name.transcript)
    # rospy.sleep(5)

    # try:
    #     confirmation = ''
    #     confirmation.transcript = recognise("en-US", ['yes', 'no'], 5)
    #     if confirmation.transcript == "yes":
    #         rospy.loginfo("Yes")
    #         speechSay("Ok, I will remember that")
    #         return user_name
    #     else:
    #         rospy.loginfo("No")
    #         speechSay("Let's try that again!")
    #         userSave()
    # except rospy.ServiceException as e:
    #     print("Service call failed: %s" % e)
