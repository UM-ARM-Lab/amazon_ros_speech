#! /usr/bin/env python

"""Ros node for interfacing with AWS Polly service.
This node will say (as audio) any string sent to the "/polly" topic
Will first say the command line argument
"""


from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
import rospy
from std_msgs.msg import String
from tempfile import gettempdir

overload_str = "You have been saying an awful lot. It is going to cost money"
overload_char_limit = 100000

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="adminuser")
polly = session.client("polly")

char_count = 0

def call_polly(words):
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=words, OutputFormat="mp3",
                                           VoiceId="Matthew")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

        # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important as the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                rospy.logerr(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        rospy.logerr("Could not stream audio")
        sys.exit(-1)

        # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])

def polly_callback(ros_str):
    global char_count
    words = ros_str.data
    char_count += len(words)
    if char_count > overload_char_limit:
        rospy.logerr("Speech limit reached")
        call_polly(overload_str)
        return
    rospy.loginfo("Saying: " + words)
    call_polly(words)
    
if __name__ == "__main__":
    rospy.init_node("polly")
    print sys.argv
    rospy.loginfo("Polly ready for speach requests")

    if len(sys.argv) > 1 and not sys.argv[1].startswith('__name:='):
        rospy.loginfo("Saying startup string: " + sys.argv[1])
        call_polly(sys.argv[1])
    
    rospy.Subscriber("/polly", String, polly_callback)
    rospy.spin()
