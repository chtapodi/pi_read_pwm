# Written by Xavier Quinn
# Reads in an estimate of PWM values to a pin using pigpio 'callbacks'

import time
import pigpio


class read_pwm :
	def __init__(self, receive_pin, average_length):

		self.receive_pin=receive_pin
		self.rising_list=[]
		self.falling_list=[]
		self.baud_len_list=[]
		self.period_list=[]
		self.pwm_list=[]

		self.pio=pigpio.pi()
		self.average_length=average_length

		self.init_listen()


	#initializes receiption and callback
	def init_listen(self) :
		self.pio.set_mode(self.receive_pin, pigpio.INPUT)
		print(self.pio.callback(self.receive_pin, pigpio.RISING_EDGE, self.rising_callback))
		print(self.pio.callback(self.receive_pin, pigpio.FALLING_EDGE, self.falling_callback))

	#Callback function for the falling edge
	def rising_callback(self, gpio, level, tick) :
		self.rising_list.append(tick)
		try:
			self.period_list.append(self.rising_list[-1]-self.rising_list[-2])
		except:
			pass


	#Callback function for the falling edge
	def falling_callback(self, gpio, level, tick) :
		self.falling_list.append(tick)
		self.baud_len_list.append(self.falling_list[-1]-self.rising_list[-1])
		# print(baud_len_list[-1])
		if(len(self.baud_len_list)>1) :
			self.calc_pwm()

	#calculates PWM and saves it to a list
	def calc_pwm(self) :
		period=self.get_n_average(self.period_list)
		av_baud=self.get_n_average(self.baud_len_list)
		ratio=float(av_baud)/float(period)
		self.pwm_list.append(ratio*255)
		print(self.pwm_list[-1])

	#Gets average value of last self.average_length values of list
	def get_n_average(self, list_of_vals) :
		if(len(list_of_vals)>self.average_length) :
			return sum(list_of_vals[-self.average_length:])/self.average_length
		else :
			return sum(list_of_vals)/len(list_of_vals)

	#returns the list of collected pwm values
	def get_pwm_list() :
		return self.pwm_list

	#updates the range over which values are averages
	def set_average_value(val) :
		self.average_length=val;

def main():
	receive_pin=17

	pwm=read_pwm(receive_pin, 5)
	while(True) :
		time.sleep(1)




if __name__== "__main__":
  main()
