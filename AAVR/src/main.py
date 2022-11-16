#!/usr/bin/env python
import sys
import rospy

from qt_robot_interface.srv import *
from qt_vosk_app.srv import *
from qt_gesture_controller.srv import gesture_play
from qt_nuitrack_app.msg import Gestures

def greet():
    # greeting
    speechSay("Hello! This is the startup process")
    speechSay("This is a test")

if __name__ == '__main__':
    rospy.init_node('main')
    rospy.loginfo("AAVR started")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

    rospy.loginfo("finished!")
