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


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


def userSave():
    print("Saving UserName")
    temp = str(uuid.uuid4())
    temp2 = str(uuid.uuid4())

    try:
        speechSay("State your name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(temp + "STATE_NAME.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(5)

    user_name = str

    AUDIO_FILE = temp + "STATE_NAME.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        user_name = r.recognize_google(audio)
        user_name = user_name.strip()
        user_name = ''.join(user_name)  # remove spaces
        print(user_name)

    # Confirmation starts here (Yes or No)

    try:
        speechSay("Hello %s, Is this the right name?" % user_name)
        print("Confirming Name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(temp2 + "CONFIRMATION.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording confirmation...")
    rospy.sleep(5)

    confirmation = ''

    AUDIO_FILE = temp2 + "CONFIRMATION.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        confirmation = r.recognize_google(audio)
        confirmation_final = confirmation.strip()

    if "yes" in confirmation_final:
        print("Saving Name")
        try:
            speechSay("Saving Name")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        user_name = user_name.strip()
        # If user_name is an array, make it a string
        if type(user_name) == list:
            user_name = user_name[0]
        return str(user_name)
    elif "no" in confirmation_final:
        print("Name not saved")
        try:
            speechSay("Name not saved")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        return userSave()
    else:
        print("Name not saved")
        try:
            speechSay("Name not saved due to invalid confirmation")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        return userSave()
