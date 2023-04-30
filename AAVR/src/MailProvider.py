import rospy
import wave
import uuid
import speech_recognition as sr
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize
from audio_common_msgs.msg import AudioData
from os import *

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


def mailProvider(email_address):
    # Append the email provider to the email address based on number asked by the user
    print("Appending email provider")
    try:
        speechSay(
            "What is your email provider?")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open("STATE_EMAIL_PROVIDER.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(15)

    email_provider = ''
    email_address = email_address.replace(" ", "")

    AUDIO_FILE = "STATE_EMAIL_PROVIDER.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

        print("Transcription: " + r.recognize_google(audio))
        email_provider = r.recognize_google(audio)
        confirmation_final = email_provider.strip()
        confirmation_final = confirmation_final.lower()

    if confirmation_final == "1" or confirmation_final == "one" or confirmation_final == "gmail":
        email_address = email_address + "@gmail.com"
        return email_address
    elif confirmation_final == "2" or confirmation_final == "two" or confirmation_final == "yahoo":
        email_address = email_address + "@yahoo.com"
        return email_address
    elif confirmation_final == "3" or confirmation_final == "three" or confirmation_final == "outlook":
        email_address = email_address + "@outlook.com"
        return email_address
    elif confirmation_final == "4" or confirmation_final == "four" or confirmation_final == "hotmail":
        email_address = email_address + "@hotmail.com"
        return email_address
    else:
        email_address = email_address + "@" + confirmation_final + ".com"
        return email_address
