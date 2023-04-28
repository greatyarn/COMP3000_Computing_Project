import rospy
import wave
import uuid
import speech_recognition as sr
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize
from audio_common_msgs.msg import AudioData
from os import path
from pydub import AudioSegment
from db import *

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

######################################################################
# confirmation starts here (Yes or No)


def confirmation(prompt):
    wf = wave.open(prompt + ".wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    try:
        speechSay(prompt)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    print("Recording confirmation...")
    rospy.sleep(5)

    confirmation = ''

    AUDIO_FILE = prompt + ".wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        confirmation = r.recognize_google(audio)
        confirmation_final = confirmation.strip()

    if "yes" in confirmation_final:
        print(prompt + " confirmed")
        try:
            speechSay(prompt + " confirmed")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        return True
    elif "no" in confirmation_final:
        print(prompt + " not confirmed")
        try:
            speechSay(prompt + " not confirmed")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return False
    else:
        print(prompt + " not confirmed")
        try:
            speechSay(prompt + " not confirmed due to invalid confirmation")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return False


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


def userSave():
    print("Saving UserName Starting Here")
    nameSpeak = str(uuid.uuid4())
    user_name = str

    try:
        speechSay("State your name")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(nameSpeak + "STATE_NAME.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(5)

    AUDIO_FILE = nameSpeak + "STATE_NAME.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        user_name = r.recognize_google(audio)
        user_name = user_name.strip()
        user_name = ''.join(user_name)  # remove spaces
        print(user_name)

    confirmation(
        "Are you sure you want to save " + user_name + "?")
    if confirmation == True:
        print("Saving User Name")
        return
    else:
        userSave()

##########################################################################################


def mailSave():

    mailSpeak = str
    mailCheck = str(uuid.uuid4())

    try:
        speechSay("State your email without @")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(mailSpeak + "mailSpeak.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(5)

    AUDIO_FILE = mailCheck + "mailCheck.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        mailCheck = r.recognize_google(audio)
        mailCheck = mailCheck.strip()
        mailCheck = ''.join(mailCheck)  # remove spaces
        # join any words together that are split by spaces

        print(mailCheck)

    confirmation(
        "Are you sure you want to save " + mailCheck + "?")
    if confirmation == True:
        print("Saving Email")
        return mailCheck
    else:
        mailSave()
