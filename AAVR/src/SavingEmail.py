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

# Save the email that user state
def emailSave():
    print("Saving Email")
    temp = str(uuid.uuid4())
    temp2 = str(uuid.uuid4())

    try:
        speechSay("State your Email without the @")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(temp + "STATE_EMAIL.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(5)

    email_address = ''

    AUDIO_FILE = temp + "STATE_EMAIL.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
        email_address = r.recognize_google(audio)
        confirmation_final = email_address.strip()
        confirmation_final = ''.join(confirmation_final)  # remove spaces
        print(confirmation_final)

    # Confirmation starts here (Yes or No)

    try:
        speechSay("%s, Is this the right email name?" % confirmation_final)
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
        confirmation_final = confirmation.strip() # Formatting
        confirmation_final = ''.join(confirmation_final)

    # Confirmation phase
    if "yes" in confirmation_final:
        print("Saving Email")
        try:
            speechSay("Saving Email")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        email_address = email_address.strip()
        print(email_address)

        return email_address
    elif "no" in confirmation_final:
        print("Email not saved")
        try:
            speechSay("Email not saved")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        return emailSave()
    else:
        print("Email not saved")
        try:
            speechSay("Email not saved due to invalid confirmation")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
        return emailSave()
