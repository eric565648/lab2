#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray
from math import pi, radians
class Tracking:
	def __init__(self):
		self.node_name = rospy.get_name()	
		self.state = 1
		self.trig = None
		self.linear_err = 0.0
		self.angular_err = radians(0.1)
		self.motorhat = Adafruit_MotorHAT(addr= 0x60)
		self.leftMotor 	= self.motorhat.getMotor(1)
		self.rightMotor = self.motorhat.getMotor(2)
		self.right_pwm = 60
		self.left_pwm = 60
		self.leftMotor.setSpeed(self.left_pwm)
		self.rightMotor.setSpeed(self.right_pwm)
		self.subPosition=rospy.Subscriber("/serial_node/odometry",Float64MultiArray,self.cbPosition)

		rospy.on_shutdown(self.custom_shutdown)
		rospy.loginfo("[%s] Initialized!" %self.node_name)
	def cbPosition(self,msg):
		x     = msg.data[0]
		y     = msg.data[1]
		theta = msg.data[2]
		theta = theta % (2* pi)
		print x,y,theta

		# stages: 1) straight line,
		#         2) semi-circle
		#         3) straight line again.

		#if 1-x > self.linear_err:            ### straight line

		#if pi - theta > self.angular_err:    ### trun right/left

		
		if(self.state == 1):
			self.leftMotor.run(1)
			self.rightMotor.run(1)
			self.leftMotor.setSpeed(100)
			self.rightMotor.setSpeed(100)
			if(x > 1):
				self.state = 2;
		elif(self.state == 2):
			self.leftMotor.run(1)
			self.rightMotor.run(1)
			self.leftMotor.setSpeed(50)
			self.rightMotor.setSpeed(100)
			if(theta*180/np.pi >= 180):
				self.state = 3;
		else:
			self.leftMotor.run(1)
			self.rightMotor.run(1)
			self.leftMotor.setSpeed(100)
			self.rightMotor.setSpeed(100)	
			if(x < 0.05):
				self.state = 4;
				self.leftMotor.run(4)
				self.rightMotor.run(4)



	def custom_shutdown(self):
		self.leftMotor.run(4)
		self.rightMotor.run(4)
		del self.motorhat

if __name__ == '__main__':
	rospy.init_node('track', anonymous = False)
	Track = Tracking()
	rospy.spin()
