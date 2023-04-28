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

# Confirm the OTP


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


def confirmOTP(otp):
    print("Confirming OTP")
    temp = str(uuid.uuid4())

    try:
        speechSay("Please say the OTP that you received")
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

    wf = wave.open(temp + "otpconfirm.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0',
                     AudioData, channel_callback, wf)

    print("Recording...")
    rospy.sleep(10)

    AUDIO_FILE = temp + "otpconfirm.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    print("Transcription: " + r.recognize_google(audio))
    otpRec = r.recognize_google(audio)
    otpRec = otpRec.strip()
    otpRec = otpRec.replace(" ", "")
    otpRec = otpRec.replace("o", "0")
    otpRec = otpRec.replace("O", "0")

    print("OTP: " + str(otp))
    print("OTP Received: " + str(otpRec))

    if int(otpRec) == int(otp):
        print("OTP Confirmed")
        return True
    else:
        print("OTP Incorrect")
        return False
