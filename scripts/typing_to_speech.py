#! /usr/bin/env python

# Simple node that passes text input from the terminal to the polly service

import rospy
from std_msgs.msg import String
from amazon_ros_speech import talker


if __name__ == "__main__":
    rospy.init_node("type_to_speech")
    # pub = rospy.Publisher("polly", String, queue_size=10)
    #
    # print ("Type what you want me to say")
    # while not rospy.is_shutdown():
    #     msg = raw_input('')
    #     pub.publish(msg)
    talker.init()
    while not rospy.is_shutdown():
        talker.say(raw_input(''))



