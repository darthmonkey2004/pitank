import pickle
import os
from mss import mss
sct = mss()

def initConf():
	conf = {}
	conf['cameras'] = {}
	conf['cameras'][0]  = {}
	conf['cameras'][0]['capture_type'] = 'rpi'
	conf['cameras'][0]['capture_types'] = ['rpi', 'cv2', 'oak-d', 'screen_grab', 'zmq']
	#initialize src as 'picap', as capture object won't use a src if it's an rpi camera
	# in event of usb or ipcam, set src option to uri (0, '/dev/video0', 'rtsp://myip:myport/mypath.sdp', ...)
	conf['cameras'][0]['src'] = 'picap'
	conf['cameras'][0]['w'] = 640
	conf['cameras'][0]['h'] = 480
	conf['cameras'][0]['monitor'] = sct.monitors[len(sct.monitors) - 1]
	return conf

def writeConf(conf, conf_file=None):
	if conf_file is None:
		conf_file = os.path.join(os.path.expanduser("~"), 'pitank', 'pitank.conf')
	try:
		with open(conf_file, 'wb') as f:
			pickle.dump(conf, conf_file)
			f.close()
		print("Tank configuration updated!")
		return True
	except Exception as e:
		print("Failed to update conf file!", e)
		return False

def readConf(conf_file=None):
	if conf_file is None:
		conf_file = os.path.join(os.path.expanduser("~"), 'pitank', 'pitank.conf')
	try:
		with open(conf_file, 'rb') as f:
			conf = picke.load(f)
			f.close()
		return conf
	except:
		print("Failed to read conf file! Re-initializing...")
		conf = initConf()
		writeConf(conf)
		return conf

