import rospy
from std_msgs.msg import String

amazon_ros_speech_publisher = None


def init():
    global amazon_ros_speech_publisher
    amazon_ros_speech_publisher = rospy.Publisher("polly", String, queue_size=10)


def say(text):
    if amazon_ros_speech_publisher is None:
        rospy.logwarn("Polly not initalized! Cannot talk")
        return

    amazon_ros_speech_publisher.publish(text)