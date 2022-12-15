import websocket


class sender():
	def __init__(self, host=None, port=None):
		if host is None:
			host = '192.168.2.22'
		if port is None:
			port = 9876
		self.host = host
		self.port = int(port)
		self.connection_string =  f"ws://{host}:{port}/"
		self.connection = self.connect(self.connection_string)
		self.is_connected = False
		self.runloop = False

	def connect(self, connection_string=None):
		try:
			if connection_string is not None:
				self.connection_string = connection_string
			self.connection = websocket.create_connection(self.connection_string)
			self.is_connected = True
			return self.connection
		except Exception as e:
			self.is_connected = False
			print("Unable to connect:", e)
			return None

	def send(self, message):
		try:
			if self.connection.connected:
				self.connection.send(message)
				self.is_connected = True
				return True
			else:
				print("Not connected!")
				self.is_connected = False
				return False
		except Exception as e:
			print("Failed to send:", e)
			self.is_connected = False
			return False

	def close(self):
		print("Connection closed!")
		self.connection.close()
		self.is_connected = False

	def start(self):
		t = threading.Thread(target=self.loop)
		t.setDaemon(True)
		t.start()
		print("Socket sender loop started!")

	def loop(self):
		self.runloop = True
		while self.runloop:
			if self.message is not None:
				self.send(self.message)
				self.message = None
		self.close()
		print("exited!")
