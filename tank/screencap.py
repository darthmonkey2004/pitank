from mss import mss

class screencap():
	def __init__(self, monitor=None):
		self.sct = mss()
		self.camera_id = camera_id
		if monitor is not None:
			self.monitor = monitor
		else:
			self.monitor = self.sct.monitors[len(sct.monitors) - 1]
		self.monitors = self.sct.monitors
		self.img = None
		self.runloop = True
		self._start()

	def _capture(self):
		while self.runloop:
			try:
				img = numpy.asarray(self.sct.grab(self.monitor))
				#go through convoluted transform to remove 4th channel (look this up, should be reshape possibilities)
				self.img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.COLOR_RGB2BGR)
				if self.img.shape[1] > 1024:
					self.img = imutils.resize(self.img, width=1024)
			except Exception as e:
				self.img = None
				log(f"screencap.read():Exception! ({e})", 'error')
				break
		self.img = None
		return

	def _start(self):
		try:
			self.t = Thread(target=self._capture)
			self.t.setDaemon(True)
			self.t.start()
			return True
		except Exception as e:
			log(f"capture._start():Failed to start thread:{e}", 'error')
			return False

	def read(self):
		img = self.img
		if img is None:
			return False, None
		else:
			return True, img

	def release(self):
		self.runloop = False
