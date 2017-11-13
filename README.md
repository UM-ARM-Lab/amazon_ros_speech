# amazon_ros_speech
Ros node handling calls to AWS TTS service

## Setup
- Set up [AWS credentials](http://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html) with an IAM user with polly access.
- `pip install boto3`
- `sudo apt install mpg123`
- Verify speaker is attached and working
- clone repo, build
- `rosrun amazon_ros_speech polly.py`
- send `std_msgs/String` to `/polly/` topic

## Remote launch setup
Follow the [ROS Multiple Machine](http://wiki.ros.org/ROS/Tutorials/MultipleMachines) tutorial if you want to run this node remotely.
