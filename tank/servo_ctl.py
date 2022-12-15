import os
import serial
import subprocess
from keymap import ctk, bt_ctk
import sys


def create_conf(speed='hi'):
	if speed != 'low' and speed != 'med' and speed != 'hi':
		print(f"Unrecognized speed option: {speed}. Defaulting to 'low'...")
		speed = 'low'
	coms = {}
	coms['move'] = 1
	coms['move_and_fire'] = 2
	coms['fire'] = 3
	coms['ceaseFire'] = 4
	coms['stepper_left'] = 5
	coms['stepper_right'] = 6
	coms['step_to_pos'] = 7
	opts = {}
	opts['speeds'] = {}
	opts['speeds']['dead_slow'] = 0.1
	opts['speeds']['low'] = 0.5
	opts['speeds']['med'] = 4
	opts['speeds']['hi'] = 8
	opts['speed'] = float(opts['speeds'][speed])
	opts['center_x'] = 90
	opts['center_y'] = 90
	mapped_keys = {'joy_down': {'KEY_DOWN': 'action:move=down', 'KEY_UP': None}, 'joy_left': {'KEY_DOWN': 'action:move=left', 'KEY_UP': None}, 'joy_right': {'KEY_DOWN': 'action:move=right', 'KEY_UP': None}, 'r': {'KEY_DOWN': 'reset', 'KEY_UP': None}, 'space': {'KEY_DOWN': 'action:fire', 'KEY_UP': 'action:ceaseFire'}, 'top_trigger': {'KEY_DOWN': 'action:fire', 'KEY_UP': 'action:ceaseFire'}, 'return': {'KEY_DOWN': None, 'KEY_UP': 'set:fire_flag'}, 'bottom_trigger': {'KEY_DOWN': None, 'KEY_UP': 'set:fire_flag'}, 'end': {'KEY_DOWN': 'action:center', 'KEY_UP': None}, 'f1': {'KEY_DOWN': 'set:speed=dead_slow', 'KEY_UP': None}, 'f2': {'KEY_DOWN': 'set:speed=low', 'KEY_UP': None}, 'f3': {'KEY_DOWN': 'set:speed=med', 'KEY_UP': None}, 'f4': {'KEY_DOWN': 'set:speed=hi', 'KEY_UP': None}, 'c': {'KEY_DOWN': 'action:set_center', 'KEY_UP': None}, 'up': {'KEY_DOWN': 'action:move=up', 'KEY_UP': None}, 'down': {'KEY_DOWN': 'action:move=down', 'KEY_UP': None}, 'left': {'KEY_DOWN': 'action:move=left', 'KEY_UP': None}, 'right': {'KEY_DOWN': 'action:move=right', 'KEY_UP': None}, 'joy_up': {'KEY_DOWN': 'action:move=up', 'KEY_UP': None}}
	d = {}
	d['commands'] = coms
	d['options'] = opts
	d['mapped_keys'] = mapped_keys
	return d

def get_dev():
	com = "ls /dev/ttyACM*"
	try:
		devs = subprocess.check_output(com, shell=True).decode().strip().split("\n")
	except:
		devs= []
	if len(devs) == 0:
		print(f"Unable to find serial! Exiting...", 'error')
		exit()
	elif len(devs) == 1:
		return devs[0]
	else:
		pos = -1
		for dev in devs:
			pos += 1
			print(f"{pos}. {dev}")
		no = input("Enter a device number: ")
		return devs[no]

class servo():
	def __init__(self, dev=None, baud=115200):
		if dev is None:
			dev = get_dev()
		self.dev = dev
		self.baud = baud
		print(f"Using device:{self.dev}, baud:{self.baud}")
		self.arduino = self.new_controller(self.dev, self.baud)
		if self.arduino is None:
			print("Failed to get device! Exiting...", 'error')
			exit()
		self.conf = create_conf()
		self.opts = self.conf['options']
		self.mapped_keys = self.conf['mapped_keys']
		self.coms = self.conf['commands']
		self.event = None
		self.key = None
		self.event_loop = True
		self.center_x = 90
		self.center_y = 90
		self.pos_x = self.center_x
		self.pos_y = self.center_y
		self.center()
		self.event_loop = True
		self.speed = 10
		self.fire_flag = False

	def new_controller(self, dev=None, baud=None):
		if dev is not None:
			self.dev = dev
		if baud is not None:
			self.baud = baud
		try:
			self.arduino = serial.Serial(self.dev, self.baud)
			return self.arduino
		except Exception as e:
			print(f"Unable to get device {self.dev} with baud {baud}: {e}", 'error')
			self.arduino = None


	def read(self):
		return str(self.arduino.readline())

	def send(self, command):
		if "\n" not in command:
			self.arduino.write(f"{command}\n".encode())
		else:
			self.arduino.write(command.encode())
		return

	def start_loop(self):
		try:
			from threading import Thread
			t = Thread(target=self.move_loop)
			t.setDaemon(True)
			t.start()
			print("Event loop started!", 'info')
			return True
		except Exception as e:
			print(f"Couldn't start loop: {e}", 'error')
			return False

	def make_writeable(self, dev=None):
		if dev is not None:
			self.dev = dev
		ret = subprocess.check_output(f"sudo chmod a+rwx \"{self.dev}\"", shell=True).decode().strip()
		if ret is not None and ret != '':
			print("Encountered error attempting to gain write access to device \'{self.dev}\'!", 'error')
			return False
		else:
			print("Ok!", 'info')
			return True

	def fire(self, val=False):
		if type(val) != bool:
			try:
				val = bool(val)
			except:
				print("Bad fire command! Should be boolean, defaulting to False")
				val = False
		self.fire_flag = val
		if self.fire_flag:
			print("Firing..")
			self.move('Fire')
		else:
			print("Cease fire!")
			self.move('ceaseFire')

	def move(self, action=None, arg1=-1, arg2=-1):
		if action is None:
			action = 'move'
		if arg1 is None:
			arg1 = -1
		if arg2 is None:
			arg2 = -1
		self.action = action
		self.arg1 = arg1
		self.arg2 = arg2
		if type(self.action) == str:
			self.action_name = action
			self.action = self.coms[self.action_name]
		elif type(self.action) == int:
			self.action = action
			self.action_name = self.coms[self.action]
		if type(self.arg1) == str:
			print("original x, y:", self.pos_x, self.pos_y)
			if self.arg1 == 'up':
				print(f"dir=up, y={self.pos_y}, s={self.speed}")
				self.pos_y += self.speed
			elif self.arg1 == 'down':
				print(f"dir=down, y={self.pos_y}, s={self.speed}")
				self.pos_y -= self.speed
			elif self.arg1 == 'left':
				print(f"dir=left, y={self.pos_x}, s={self.speed}")
				self.pos_x += self.speed
			elif self.arg1 == 'right':
				print(f"dir=right, y={self.pos_x}, s={self.speed}")
				self.pos_x -= self.speed
			else:
				print("argument not recognized:", self.arg1)
			if self.pos_x <= 0:
				self.pos_x = 0
			elif self.pos_x >= 180:
				self.pos_x = 180
			if self.pos_y <= 0:
				self.pos_y = 0
			elif self.pos_y >= 180:
				self.pos_y = 180
			self.arg1 = self.pos_x
			self.arg2 = self.pos_y
			print("adjusted x, y:", self.arg1, self.arg2)
		else:
			self.arg1 = int(self.arg1)
			self.arg2 = int(self.arg2)
		#elif self.pan_mode == 'stepper':
		#	self.tilt = tilt
		com = f"{self.action}:{self.arg1},{self.arg2}"
		print(f"action:{self.action_name}, pan pos:{self.arg1}, tilt pos:{self.arg2}")
		ret = self.send(com)
		#print(ret)

	def reset(self):
		print("resetting...")
		self.move('ceaseFire')
		self.center()

	def center(self):
		print("Centering..")
		self.move('move', self.center_x, self.center_y)
		print("Centerd!")

	def set_center(self):
		self.center_x = int(self.pos_x)
		sefl.center_y = int(self.pox_y)
		print(f"Center set! X:{self.center_x}, Y:{self.center_y}")

	def set_prop(self, var=None, val=None):
		if var is None:
			raise Exception(ValueError, 'variable name cannot be None!')
		if var == 'speed':
			if type(val) == str:
				self.speed = float(self.opts['speeds'][val])
			else:
				self.speed = float(val)
			print(f"Set speed to {val} ({self.speed})!")
		elif var == 'fire_flag':
			try:
				if self.fire_flag:
					self.fire_flag = False
				else:
					self.fire_flag = True
			except Exception as e:
				print(f"Exception in set_prop(fire_flag): {e}")
				self.fire_flag = False
			print("Set fire flag:", self.fire_flag)
			if self.fire_flag:
				self.move(action='fire')
			else:
				self.move(action='ceaseFire')
			self.event = None
			self.key = None
		else:
			self.__dict__[var] = val
			print(f"Set property {var} to {val}!")

	def move_loop(self):
		self.key = None
		self.event = None
		self.event_loop = True
		print("Starting loop...")
		while self.event_loop is True:
			arg1 = None
			arg2 = None
			function = None
			if self.event is not None and self.key is not None:
				self.key = self.key.lower()
				print(f"Event:{self.event}, Key:{self.key}")
				action = self.mapped_keys[self.key][self.event]
				if action is not None:
					#'action:move=left'
					chunks = action.split(':')
					t = chunks[0]
					string = chunks[1]
					if t == 'action':
						if '=' in string:
							a = string.split('=')[0]
							args = string.split('=')[1]
							if "," in args:
								arg1 = float(args.split(",")[0])
								arg2 = float(args.aplit(",")[1])
							else:
								arg1 = args
								arg2 = None
						else:
							a = string
							arg1 = None
							arg2 = None
						if a == 'move' or a == 'fire' or a == 'ceaseFire':
							ret = self.move(action=a, arg1=arg1, arg2=arg2)
							if ret is not None:
								print(ret)
							else:
								print("ok!")
							if a == 'fire' or a == 'ceaseFire':
								action = None
								self.event = None
								self.key = None
						else:
							print(f"Unknown action: {a}")
					elif t == 'set':
						if '=' in string:
							var = string.split('=')[0]
							val = string.split('=')[1]
						else:
							var = string
							val = None
						self.set_prop(var, val)
				else:
					self.event = None
					self.key = None
					action = None
					t = None
						
						
