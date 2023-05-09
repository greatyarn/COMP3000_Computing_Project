import rospy
import wave
import uuid
import speech_recognition as sr
from qt_robot_interface.srv import speech_say
from qt_vosk_app.srv import speech_recognize
from audio_common_msgs.msg import AudioData


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

# Confirm the OTP stated by user
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
    rospy.sleep(20)  # 20 seconds to record the OTP

    AUDIO_FILE = temp + "otpconfirm.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    
    # Formatting
    print("Transcription: " + r.recognize_google(audio))
    otpRec = r.recognize_google(audio)
    otpRec = otpRec.strip()
    otpRec = otpRec.replace(" ", "")
    otpRec = otpRec.replace("o", "0")
    otpRec = otpRec.replace("O", "0")

    otpRec = ''.join(i for i in otpRec if i.isdigit())

    print("OTP: " + str(otp))
    print("OTP Received: " + str(otpRec))

    if int(otpRec) == int(otp):
        print("OTP Confirmed")
        speechSay("OTP Confirmed")

        return True
    else:
        print("OTP Incorrect")
        speechSay("OTP Incorrect")
        # TODO - Add a way to re-enter the OTP

        return False
