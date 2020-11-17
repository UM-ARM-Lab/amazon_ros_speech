import rospy
from std_msgs.msg import String

amazon_ros_speech_publisher = None
is_mute = False


def init():
    global amazon_ros_speech_publisher
    amazon_ros_speech_publisher = rospy.Publisher("polly", String, queue_size=10)


def say(text):
    try:
        init()
    except Exception as e:
        rospy.logwarn("Attempted to init talker but failed {}".format(e))
        return

    if amazon_ros_speech_publisher is None:
        rospy.logwarn("Polly not initalized! Cannot talk")
        return

    if not is_mute:
        amazon_ros_speech_publisher.publish(text)
    else:
        rospy.logout("Talker: {}".format(text))


def mute():
    global is_mute
    is_mute = True


def unmute():
    global is_mute
    is_mute = False
