import rospy
import wave
import uuid
import speech_recognition as sr
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize
from audio_common_msgs.msg import AudioData
from os import path
from pydub import AudioSegment

# Define ROS Services
print("Defining ROS Services")
speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
recognise = rospy.ServiceProxy(
    '/qt_robot/speech/recognize', speech_recognize)

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_WIDTH = 2

# Waits for the service to be available
print("Waiting for service to be available")
rospy.wait_for_service('/qt_robot/speech/say')
rospy.wait_for_service('/qt_robot/speech/recognize')

# list_of_name = ['Adam', 'Greg']


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


def userSave():
    print("Saving UserName")
    # user_name = recognise("en-US", ['Adam', 'Gregory'], 5)
    # rospy.loginfo(user_name)
    temp = str(uuid.uuid4())

    try:
        speechSay("State your Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
    wf = wave.open(temp + ".wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(3)

    speechSay("Recording complete")

    user_name = ''

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

    AUDIO_FILE = temp + ".wav"
    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))

    print("Is this the right name?")
    user_name = r.recognize_google(audio)

    try:
        speechSay("Hello %s, Is this the right name?" % user_name.transcript)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    rospy.sleep(5)
