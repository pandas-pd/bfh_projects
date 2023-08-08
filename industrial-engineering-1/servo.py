# Import libraries
import RPi.GPIO as GPIO
import time

class Servo():
	
	def __init__(self,start_angle = 90):
		"""
		source of some code: https://www.explainingcomputers.com/pi_servos_video.html
		"""
		GPIO.setmode(GPIO.BOARD) # Set GPIO numbering mode
		
		GPIO.setup(11,GPIO.OUT) # Set pin 11 as an output, and define as servo1 as PWM pin
		self.servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
		
		self.servo1.start(0) # Start PWM running, with value of 0 (pulse off)
		self.set_angle(start_angle)
		self.direction = 1
        
	def set_angle(self,angle):
		try:
			self.servo1.ChangeDutyCycle(2+(angle/18))
			time.sleep(0.1) # give enough time to turn
			self.servo1.ChangeDutyCycle(0) # hold still
			self.last_angle = angle
			
		except Exception as e:
			print(e)
        
	def exit_clean(self):
		
		self.servo1.stop()
		GPIO.cleanup()
		
	def swing(self):

		step_size = 5

		min_angle : int = 10
		max_angle : int = 170

		#beginn swinging
		if self.last_angle < min_angle:
			self.direction = 1

		if self.last_angle > max_angle:
			self.direction = -1

		#print(self.last_angle + (step_size*self.direction),self.direction)
		self.set_angle(self.last_angle + (step_size*self.direction))
        
        
if __name__ == '__main__':
	servo = Servo()
	while True:
		angle = input('Enter angle between 0 & 180: ')
		if angle == 'q':
			servo.exit_clean()
			break
			
		servo.set_angle(float(angle))
		
