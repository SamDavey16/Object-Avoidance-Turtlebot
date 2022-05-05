#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class Chatter:

    def __init__(self):
        rospy.init_node("chatter")
        self.publisher = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1) #creates the publisher
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.laser_cb) #creates the subscriber

    def forward(self):
        t = Twist()
        t.linear.x = 0.1 #moves forward at a speed of 0.1
        t.angular.z = 0.0
        return t

    def right(self):
        t = Twist()
        t.linear.x = -0.1
        t.angular.z = -2.0 #turns anti-clockwise 
        return t

    def left(self):
        t = Twist()
        t.linear.x = -0.1
        t.angular.z = 2.0 #turns clockwise
        return t

    def laser_cb(self, laser_msg):
        right = min(laser_msg.ranges[0:90]) #finds the minimum value in the sensors on the right of the robot
        left = min(laser_msg.ranges[520:560]) #as above for the left
        print(left)
        print(right)
        print(min(laser_msg.ranges[140:520]))
        print(min(laser_msg.ranges[0:560]))
        if min(laser_msg.ranges[90:560]) > 0.5:
            velocity = self.forward()
            self.publisher.publish(velocity) #publishes the velocity which moves the robot
            print("forward")
        elif min(laser_msg.ranges[520:560]) < 0.5 or min(laser_msg.ranges[520:560]) == "nan" and right > left: #if the wall is approaching the left and the distance from the wall is greater on the right than on the left
            velocity = self.right()
            self.publisher.publish(velocity)
            print("right")
        elif min(laser_msg.ranges[0:90]) < 0.5 or min(laser_msg.ranges[0:90]) == "nan" and right < left:
            velocity = self.left()
            self.publisher.publish(velocity)
            print("left")
        elif min(laser_msg.ranges[0:560]) == "nan" < 0.5 or min(laser_msg.ranges[0:560]): #if the robot gets too close to a wall the robot will turn left to avoid collision
            velocity = self.left()
            self.publisher.publish(velocity)
            print("stuck")
            
                

    def run(self):
        rospy.spin()

c = Chatter()
c.run()