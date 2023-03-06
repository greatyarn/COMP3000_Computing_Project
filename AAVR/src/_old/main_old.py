#!/usr/bin/env python3
import wave
import rospy
from audio_common_msgs.msg import AudioData
from qt_robot_interface.srv import *
import uuid
import speech_recognition as sr
#from uploader import *

# Setting up the audio file
AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_WIDTH = 2


def channel_callback(msg, wf):
    wf.writeframes(msg.data)


# main
if __name__ == '__main__':

    # call the relevant service
    rospy.init_node('audio_record')
    rospy.loginfo("audio_record node started")

    # Define Speech Service Class
    speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)

    # Log that the service is being called
    rospy.loginfo("Waiting for service /qt_robot/speech/say")

    # Waits for the service to be available
    rospy.wait_for_service('/qt_robot/speech/say')

    # Log that the service is now available
    try:
        # Calls the service
        speechSay("Recording in five seconds")
        rospy.sleep(5)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

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
    rospy.sleep(10)

    speechSay("Recording complete")

    # Uploads the file to S3
    print("Uploading...")

    try:
        upload_file(temp + ".wav", "greatyarn-comp3000", temp + ".wav")
        speechSay("Uploading complete")
        rospy.loginfo("File uploaded")
    except:
        speechSay("Upload failed")
        rospy.loginfo("File upload failed")

    wf.close()
