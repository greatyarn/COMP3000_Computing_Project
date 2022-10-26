#!/usr/bin/env python
import sys
import rospy

if __name__ == '__main__':
    rospy.init_node('main')
    rospy.loginfo("my_tutorial_node started!")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

    rospy.loginfo("finsihed!")
