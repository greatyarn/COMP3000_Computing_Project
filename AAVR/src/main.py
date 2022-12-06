#!/usr/bin/env python3
import wave
import rospy
from audio_common_msgs.msg import AudioData
from qt_respeaker_app.srv import SpeechSay

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_WIDTH = 2

def channel_callback(msg, wf):
    wf.writeframes(msg.data)

# Define Speech Service Class
speechSay = rospy.ServiceProxy('/qt_respeaker_app/speech_say', SpeechSay)

# main
if __name__ == '__main__':

    # call the relevant service
    rospy.init_node('audio_record')
    
   
    
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0', AudioData, channel_callback, wf)

    # Says "recording" and waits for the user to say something
    speechSay("recording in 5 seconds")

    # Waits for 5 seconds
    rospy.sleep(5)
    
     # Makes a new file called "recording.wav" 
    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)

    print("recording...")
    rospy.spin()
    print("saving...")
    wf.close()