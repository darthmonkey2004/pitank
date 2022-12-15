from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


class picam():
	def __init__(self):
		try:
			self.cam = PiCamera()
			self.cam.vflip = True
			self.cam.resolution = (640, 480)
			self.cam.framerate = 60
			self.rawcap = PiRGBArray(self.cam)
			self.connected = True
			self.streaming = False
			self.img = None
			time.sleep(0.1)
			self.start()
		except Exception as e:
			self.connected = False
			print("Unable to connect to camera!", e)

	def _loop(self):
		self.run_loop = True
		while self.run_loop:
			for frame in self.cam.capture_continuous(self.rawcap, format="bgr", use_video_port=True):
				self.img = frame.array
				self.rawcap.truncate(0)

	def start(self):
		self.thread = Thread(target=self._loop)
		self.thread.setDaemon(True)
		self.thread.start()
		print("capture started!")

	def read(self):
		if self.img is not None:
			self.streaming = True
			img = self.img
		else:
			self.streaming = False
			img = None
		return self.streaming, img

	def release(self):
		self.run_loop = False
		print("Exiting...")
		exit()
