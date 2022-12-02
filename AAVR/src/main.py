#!/usr/bin/env python3
import wave
import rospy
from audio_common_msgs.msg import AudioData

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_WIDTH = 2

def channel_callback(msg, wf):
    wf.writeframes(msg.data)

# main
if __name__ == '__main__':

    # call the relevant service
    rospy.init_node('audio_record')
    
    # Makes a new file called "recording.wav" 
    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(AUDIO_WIDTH)
    wf.setframerate(AUDIO_RATE)
    
    # Channel 0 is used because it is the processed audio from the microphone
    rospy.Subscriber('/qt_respeaker_app/channel0', AudioData, channel_callback, wf)

    print("recording...")
    rospy.spin()
    print("saving...")
    wf.close()