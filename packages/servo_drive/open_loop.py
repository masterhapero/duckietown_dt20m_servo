#!/usr/bin/python3


# Reference pointer
# https://github.com/duckietown/dt-core/tree/daffy/packages/indefinite_navigation/src

import rospy
from duckietown_msgs.msg import WheelEncoderStamped, WheelsCmdStamped


class DuckieOpenLoopNode():
    def __init__(self):
        self.pub_wheels_cmd = rospy.Publisher('/ankkuli/wheels_driver_node/wheels_cmd',
                                            WheelsCmdStamped,
                                            queue_size=1)
        rospy.Subscriber('/ankkuli/left_wheel_encoder_node/tick',
                        WheelEncoderStamped,
                        self.cbLeftEncoder,
                        queue_size=1)
        rospy.Subscriber('/ankkuli/right_wheel_encoder_node/tick',
                        WheelEncoderStamped,
                        self.cbRightEncoder,
                        queue_size=1)
        self.left_cmd = 0.2
        self.right_cmd = 0.2
        self.rate = None
        self.left_encoder_last = None
        self.right_encoder_last = None
        # 4 seconds
        self.iterationTarget = 30 * 4 
        self.iteration = 0

    def cbLeftEncoder(self, encoder_msg):
        # initializing ticks to stored absolute value
        ssec = encoder_msg.header.stamp.to_sec()
        ticks = encoder_msg.data
        if self.left_encoder_last is None:
            print(f'cbLeft init {ssec} {ticks}')
            self.left_encoder_last = encoder_msg
            return
        deltaTLeft = encoder_msg.header.stamp.to_sec() - self.left_encoder_last.header.stamp.to_sec()
        deltaTicksLeft = encoder_msg.data - self.left_encoder_last.data
        print(f'cbLeft {ssec} {ticks} deltaTicks {deltaTicksLeft} deltaT {deltaTLeft:.3f}')
        self.left_encoder_last = encoder_msg

    def cbRightEncoder(self, encoder_msg):
        # initializing ticks to stored absolute value
        ssec = encoder_msg.header.stamp.to_sec()
        ticks = encoder_msg.data
        if self.right_encoder_last is None:
            print(f'cbRight init {ssec} {ticks}')
            self.right_encoder_last = encoder_msg
            return
        deltaTRight = encoder_msg.header.stamp.to_sec() - self.right_encoder_last.header.stamp.to_sec()
        deltaRight = encoder_msg.data - self.right_encoder_last.data
        print(f'cbRight {ssec} {ticks} delta {deltaRight} deltaT {deltaTRight:.3f}')
        self.right_encoder_last = encoder_msg

    def openloopDrive(self):
        self.rate = rospy.Rate(30)
        print("Ducker")
        while not rospy.is_shutdown():
            self.iteration += 1
            print(f'SPIN {self.iteration}')
            if self.iteration == self.iterationTarget:
                self.left_cmd = 0.0
                self.right_cmd = 0.0
            if self.iteration > self.iterationTarget:
                rospy.signal_shutdown("Iterations complete")


            wheels_cmd_msg = WheelsCmdStamped()
            # spin right unless servoing or centered
            wheels_cmd_msg.header.stamp = rospy.Time.now()
            wheels_cmd_msg.vel_left = self.left_cmd
            wheels_cmd_msg.vel_right = self.right_cmd
            self.pub_wheels_cmd.publish(wheels_cmd_msg)
            # print(f'servoDrive publish {wheels_cmd_msg}')
            self.rate.sleep()


if __name__ == "__main__":
    rospy.init_node('openloop_drive', anonymous=False)

    # Create the NodeName object
    node = DuckieOpenLoopNode()
    node.openloopDrive()