import sys
import asyncio
import websocket
import os
import threading
from adafruit_motorkit import MotorKit
from pitank.tank.servo_ctl import *
from pitank.tank.video_streamer import *
from pitank.tank.websocket_server import *
turret, kit, m1, m2 = None, None, None, None
def i2c_makeWriteable():
	try:
		subprocess.check_output(f"sudo chmod a+rwx /dev/i2c*", shell=True).decode().strip()
		ret = True, None
	except Exception as e:
		ret = False, e
		print("Failed to get i2c permissions! (root?)")
	return ret

def arduino_makeWriteable():
	try:
		ret = subprocess.check_output(f"sudo chmod a+rwx /dev/ttyACM*", shell=True).decode().strip()
	except Exception as ret:
		print(ret)
	if ret is not None:
		return False, ret
		print("Failed to get serial permissions! (root?)")
	else:
		return True, "Ok!"

def get_permissions():
	has_serial = arduino_makeWriteable()
	has_i2c = i2c_makeWriteable()
	return has_serial, has_i2c


has_serial, has_i2c = get_permissions()
if has_serial:
	turret = servo()
else:
	turret = None
if has_i2c:
	kit = MotorKit()
	m1 = kit.motor1
	m2 = kit.motor2
else:
	kit, m1, m1 = None, None, None

def serve_video(ip='192.168.2.22', port=8080):
	vid_thread = threading.Thread(target=vid_stream_run, args=(ip, port))
	vid_thread.setDaemon(True)
	vid_thread.start()

def input_handler(line):
	global turret, kit, m1, m2
	ret = None
	control = None
	out = []
	control = line.split('|')[0]
	if control == 'aim':
		ps = line.split('|')[1].split(',')
		try:
			x = ps[0]
		except:
			ret = f"Bad value:{ps}! Defaulting x to -1..."
			x = -1
		try:
			y = ps[1]
		except:
			ret = f"Bad value:{ps}! Defaulting y to -1..."
			y = -1
		turret.send(f"1:{x},{y}")
		x = -1
		y = -1
	elif control == 'fire':
		turret.send("3:-1,-1")
		ret = "Firing!"
	elif control == 'ceaseFire':
		turret.send("4:-1,-1")
		ret = "Cease Fire!"
	elif control == 'drive':
		print("drive command received!")
		vals = line.split('|')[1].split(',')
		try:
			s1 = vals[0]
		except:
			ret = f"Bad value:{vals}! Skipping set value for 's1'..."
			s1 = None
		try:
			s2 = vals[1]
		except:
			ret = f"Bad value:{vals}! Skipping set value for 's2'..."
			s2 = None
		if s1 is not None:
			m1.throttle = float(s1)
		if s2 is not None:
			m2.throttle = float(s2)
		print("set throttle:", s1, s2)
		s1 = None
		s2 = None
	elif control == 'test':
		localip = subprocess.check_output(f"ifconfig | grep \"inet 192.168\" | xargs | cut -d ' ' -f 2", shell=True).decode().strip()
		ret = f"Tank online! Address: {localip}, Port:9876"
	return ret

class server():
	def __init__(self, host='192.168.2.22', port=9876):
		self.clients = {}
		self.localip = self.get_localip
		self.message = None
		try:
			self.server = WebsocketServer(host=host, port=port)
			self.server.set_fn_new_client(self.new_client)
			self.server.set_fn_client_left(self.client_left)
			self.server.set_fn_message_received(self.message_received)
		except Exception as e:
			print(f"Exception running server: {e}. (Already running?)", 'warning')



	# Called for every client connecting (after handshake)
	def new_client(self, client, server):
	
		client = client
		add, port = client['address']
		mac = self.get_mac(add)
		client['mac'] = mac
		self.update_client(client)
		_id = client['id']
		self.server.send_message_to_all(f"DEVICE_CONNECT:({_id}@{add} (MAC={mac})")
		print(f"DEVICE_CONNECTED:{_id}:{add}:{port}:{mac}", 'info')

# Called for every client disconnecting
	def client_left(self, client, server):
		add, port = client['address']
		_id = client['id']
		mac = client['mac']
		print(f"DEVICE_DISCONNECTED:{_id}:{add}:{port}:{mac}", 'info')


	# Called when a client sends a message
	def message_received(self, client, server, message):
		print("message received!", client, message)
		add, port = client['address']
		_id = client['id']
		mac = client['mac']
		if len(message) > 200:
			message = message[:200]+'..'
		self.message = message
		ret = self.send_input(client, self.message)

	def get_mac(self, ip=None):
		mac = None
		if ip == None:
			return None
		elif ip == '127.0.0.1' or ip == self.localip:
			com = (f"ifconfig")
			ret = subprocess.check_output(com, shell=True).decode().strip().split("\n")
			for i in ret:
				if 'ether' in i:
					mac = i.strip().split(' ')[1]
					return mac
		else:
			try:
				com = (f"ping -c 1 {ip}")
				ret = subprocess.check_output(com, shell=True).decode().strip()
			except Exception as e:
				print(f"Ping shell command failed for {ip}:{e}", 'error')
				pass
		try:
			com = (f"arp -n {ip}")
			string = subprocess.check_output(com, shell=True).decode().strip().split(' ')
			for chunk in string:
				if ':' in chunk:
					mac = chunk
					return mac
		except Exception as e:
			print(f"Unable to get mac address for ip {ip}:{e}", 'error')
			mac = 'Unknown'
			return mac

	def get_localip(self):
		com = (f"ifconfig")
		ret = subprocess.check_output(com, shell=True).decode().strip().split("\n")
		for i in ret:
			if 'inet' in i and '192.168' in i:
				ret = i
				break
		self.localip = ret.strip().split(' ')[1]
		return self.localip


	def send_input(self, client, input_string):
		print("input string:", input_string)
		if input_string is not None:
			ret = input_handler(input_string)
			print("input_handler_ret:", ret)
			response = self.server.send_message(client, ret)
			print("Send response to client:", client, ret)
			if response is not None:
				print(f"EVENT: Remote command response: '{response}'", 'info')	
		else:
			print(f"server.py, command is None! {input_string}", 'warning')



	def update_client(self, client):
		client = client
		idx = self.server.clients.index(client)
		self.server.clients[idx] = client
		self.clients = self.server.clients

	def start(self):
		print(f"Server running at '192.168.2.22' on port 9876", 'info')
		self.server.run_forever()

def start(host='192.168.2.22', port=9876):
	global turret, kit, m1, m2
	serve_video()
	s = server(host=host, port=port)
	s.start()

if __name__ == "__main__":
	start()
