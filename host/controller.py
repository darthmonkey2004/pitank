from pitank.host.browser import *
import subprocess
from pitank.host.socket_sender import sender
import evdev
import subprocess


def start_tank():
	try:
		com = f"ssh monkey@192.168.2.22 \"/home/monkey/.local/bin/tank& disown\"&"
		subprocess.check_output(com, shell=True).decode().strip()
		return True
	except Exception as e:
		print("Couldn't connect to tank!", e)
		return False

def get_keyboard():
	kbd = None
	com = f"sudo chmod a+rwx /dev/input/event*"
	ret = subprocess.check_output(com, shell=True).decode().strip()
	if ret != '':
		print(f"Error setting device permissions: {ret}", 'error')
		return None
	else:
		devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
		kbds = []
		for dev in devices:
			if 'Keyboard' in dev.name:
				kbd = dev
				print(f"Grabbed keyboard:{dev.name} at path {dev.path}!", 'info')
				kbds.append(kbd)
		return kbds
	if kbd is None:
		print(f"Unable to grab keyboard! check permissions, and try again.", 'error')
		return kbd

class keyboard():
	def __init__(self):
		kbds = get_keyboard()
		if len(kbds) == 0:
			txt = "Whoops! Can't find any keyboards. Weird, right?"
			raise Exception(ValueError, txt)
		elif len(kbds) == 1:
			self.kbd = kbds[0]
		else:
			for kbd in kbds:
				if 'USB' in kbd.name:
					self.kbd = kbd
					break
		self.last_len = 0
		self.len = 0
		self.active_keys = []
		self.last_key = None
		self.last_keys = self.active_keys

	def get_keys(self):
		self.last_keys = self.active_keys
		self.active_keys = self.kbd.active_keys()
		temp = []
		event = None
		if len(self.active_keys) > len(self.last_keys):
			event = 'KEY_DOWN'
			for k in self.active_keys:
				if k not in self.last_keys:
					out = (event, k)
					temp.append(out)
		elif len(self.active_keys) < len(self.last_keys):
			event = 'KEY_UP'
			for k in self.last_keys:
				if k not in self.active_keys:
					out = (event, k)
					temp.append(out)
		if temp == [] and event is None:
			return [(None, None)]
		else:
			return temp


class controller():
	def __init__(self, host='192.168.2.22', port=9876):
		self.drive_direction = 'fwd'
		self.con = sender(host=host, port=port)
		self.speed = 0, 0
		self.s1 = 0
		self.s2 = 0
		self.step = 0.1
		self.aim_x = 90
		self.aim_y = 90
		self.send('aim|90,90')
		self.speeds_index = 0
		self.speeds = []
		self.speeds.append(2)
		self.speeds.append(3)
		self.speeds.append(4)
		self.speeds.append(5)
		self.speeds.append(6)
		self.set_speed(self.speeds_index)
		self.kbd = keyboard()
		self.pressed = []
		self.aim_speed = 1
		self.aim_left = 75
		self.aim_up = 72
		self.aim_right = 77
		self.aim_down = 80
		self.aim_up_left = 71
		self.aim_up_right = 73
		self.aim_down_left = 79
		self.aim_down_right = 81
		self.aim_actions = {"aim_left": self.aim_left, "aim_up": self.aim_up, "aim_right": self.aim_right, "aim_down": self.aim_down, "aim_up_left": self.aim_up_left, "aim_up_right": self.aim_up_right, "aim_down_left": self.aim_down_left, "aim_down_right:": self.aim_down_right}
		self.aim_codes = {self.aim_left: "aim_left", self.aim_up: "aim_up", self.aim_right: "aim_right", self.aim_down: "aim_down", self.aim_up_left: "aim_up_left", self.aim_up_right: "aim_up_right", self.aim_down_left: "aim_down_left", self.aim_down_right: "aim_down_right"}
		self.drive_fwd = 103
		self.drive_rev = 108
		self.drive_turn_left = 105
		self.drive_turn_right = 106
		self.drive_actions = {"drive_fwd": self.drive_fwd, "drive_rev": self.drive_rev, "drive_turn_left": self.drive_turn_left, "drive_turn_right": self.drive_turn_right}
		self.drive_codes = {self.drive_fwd: "drive_fwd", self.drive_rev: "drive_rev", self.drive_turn_left: "drive_turn_left", self.drive_turn_right: "drive_turn_right"}

		
	def open(self, host, port):
		self.con.open(host=host, port=port)
		print("Connected:", self.con.connection.connected)
		return self.con


	def send(self, input_string):
		if self.con.connection.connected is True:
			self.con.send(input_string)
			return True
		else:
			try:
				print("Not connected! Connecting...")
				self.open(host, port)
				self.con.send(input_string)
				return True
			except Exception as e:
				print("Error creating socket connection:", e)
				return False


	def close(self):
		self.con.close()
		print("connection closed!")

	def aim(self, d):
		print("Aim direction:", d)
		if d == 'up':
			self.aim_y += self.aim_speed
		elif d == 'up_left':
			self.aim_y += self.aim_speed
			self.aim_x -= self.aim_speed
		elif d == 'left':
			self.aim_x -= self.aim_speed
		elif d == 'down_left':
			self.aim_y -= self.aim_speed
			self.aim_x -= self.aim_speed
		elif d == 'down':
			self.aim_y -= self.aim_speed
		elif d == 'down_right':
			self.aim_y -= self.aim_speed
			self.aim_x += self.aim_speed
		elif d == 'right':
			self.aim_x += self.aim_speed
		elif d == 'up_right':
			self.aim_y += self.aim_speed
			self.aim_x += self.aim_speed
		elif d == 'center':
			print("centering..")
			self.aim_x = 90
			self.aim_y = 90
		else:
			print(f"Unknown direction! {d}")
		try:
			self.send(f"aim|{int(self.aim_x)},{int(self.aim_y)}")
			return True
		except Exception as e:
			print(f"Exception aiming turret: {e}")
			return False

	def fire(self):
		self.send("fire")
		print("firing...")

	def ceaseFire(self):
		self.send("ceaseFire")
		print("stopped firing!")

	def set_speed(self, spd):
		self.speeds_index = int(spd)
		if spd == 0:
			if self.drive_direction == 'fwd':
				self.s1 = 0.6
				self.s2 = 0.6
			else:
				self.s1 = -0.6
				self.s2 = -0.6
		elif spd == 1:
			if self.drive_direction == 'fwd':
				self.s1 = 0.7
				self.s2 = 0.7
			else:
				self.s1 = -0.7
				self.s2 = -0.7
		elif spd == 2:
			if self.drive_direction == 'fwd':
				self.s1 = 0.8
				self.s2 = 0.8
			else:
				self.s1 = -0.8
				self.s2 = -0.8
		elif spd == 3:
			if self.drive_direction == 'fwd':
				self.s1 = 0.9
				self.s2 = 0.9
			else:
				self.s1 = -0.9
				self.s2 = -0.9
		elif spd == 4:
			if self.drive_direction == 'fwd':
				self.s1 = 1.0
				self.s2 = 1.0
			else:
				self.s1 = -1.0
				self.s2 = -1.0
		#else:
		#	print(f"Weird speed provided:{spd}! Stopping...")
		#	self.stop()
		return self.s1, self.s2

	def constrain_speed(self, spd):
		spd = float(spd)
		if spd >= 1.0:
			spd = 1.0
		if spd <= -1.0:
			spd = -1.0
		return float(spd)


	def drive(self, spd = (0, 0)):
		self.s1, self.s2 = spd
		self.s1 = self.constrain_speed(self.s1)
		self.s2 = self.constrain_speed(self.s2)
		if self.s1 < 0 and self.s2 < 0:
			self.drive_direction = "rev"
		elif self.s1 >= 0 and self.s2 >= 0:
			self.drive_direction = "fwd"
		elif self.s1 >= 0 and self.s2 < 0:
			self.drive_direction = "left:skid"
		elif self.s2 >= 0 and self.s1 < 0:
			self.drive_direction = "right:skid"
		if self.drive_direction == 'rev' or self.drive_direction == 'fwd':
			if self.s1 > self.s2:
				self.drive_direction = f"{self.drive_direction}:turnRight"
			if self.s2 > self.s1:
				self.drive_direction = f"{self.drive_direction}:turnRight"
		self.send(f"drive|{self.s1},{self.s2}")
		print(f"Drive direction: {self.drive_direction}, s1:{self.s1}, s2:{self.s2}")


	def stop(self, s1=None, s2=None):
		self.s1 = 0
		self.s2 = 0
		self.speed = 0, 0
		self.drive(self.speed)

	def skid_turn(self, d=None):
		print("direction:", d)
		if d is None:
			self.stop()
		else:
			if d == 'right':
				spd1 = 0.8
				spd2 = -0.8
			if d == 'left':
				spd1 = -0.8
				spd2 = 0.8
			self.drive((spd1, spd2))


	def loop(self):
		keymap = {"center": 107, "turn_left": 105, "turn_right": 106, "forward": 103, "reverse": 108, "fire": 57, "ceaseFire": 57, "aim_up": 104, "aim_down": 109, "aim_center": 107, "aim_left": None, "aim_right": None, "estop": 1, "spd_1": 2, "spd_2": 3, "spd_3": 4, "spd_4": 5, "spd_5": 6}
		self.run_loop = True
		aim_codes = list(self.aim_codes.keys())
		drive_codes = list(self.drive_codes.keys())
		while self.run_loop:
			keys = self.kbd.get_keys()
			if keys != [(None, None)]:
				for key in keys:
					event, code = key
					self.event = event
					if event == 'KEY_DOWN' and code not in self.pressed:
						self.pressed.append(code)
					elif event == 'KEY_UP' and code in self.pressed:
						self.pressed.remove(code)
				if len(self.pressed) == 0:
					self.stop()
				elif self.pressed[0] in aim_codes:
					direction = None
					while self.pressed[0] in aim_codes:
						print("aiming...")
						# [105, 103, 106, 108]
						if self.pressed[0] == self.aim_left:
							direction = 'left'
						elif self.pressed[0] == self.aim_up:
							direction = 'up'
						elif self.pressed[0] == self.aim_right:
							direction = 'right'
						elif self.pressed[0] == self.aim_down:
							direction = 'down'
						elif self.pressed[0] == self.aim_up_left:
							direction = 'up_left'
						elif self.pressed[0] == self.aim_up_right:
							direction = 'up_right'
						elif self.pressed[0] == self.aim_down_left:
							direction = 'down_left'
						elif self.pressed[0] == self.aim_down_left: 
							direction = 'down_right'
						if direction is not None:
							self.aim(d=direction)
				elif self.pressed[0] in drive_codes:
					print("driving...")
					self.set_speed(self.speeds_index)
					if len(self.pressed) == 1:
						if self.pressed[0] == self.drive_fwd:
							self.drive((self.s1, self.s2))
						elif self.pressed[0] == self.drive_rev:
							self.s1 = 0 - self.s1
							self.s2 = 0 - self.s2
							self.drive((self.s1, self.s2))
						elif self.pressed[0] == self.drive_turn_left:
							self.skid_turn(d='left')
						elif self.pressed[0] == self.drive_turn_right:
							self.skid_turn(d='right')
				if len(self.pressed) > 0:
					if self.event == 'KEY_DOWN' and self.pressed[0] == self.fire:
						self.fire()
					elif self.event == 'KEY_UP' and self.pressed[0] == self.fire:
						self.ceaseFire()
					
						
					

if __name__ == "__main__":
	import time
	start_tank()
	print("waiting 5 seconds...")
	ctl = controller()
	time.sleep(5)
	start_thread()
	ctl.loop()
