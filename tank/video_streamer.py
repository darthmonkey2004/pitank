from flask import Response
from flask import Flask
from flask import render_template
try:
	from pitank.tank.picap import *
except:
	print("Warning: picam module not found! (are we on host pc?)")
	picam = None
import time
app = Flask(__name__)
import cv2
import threading
from pitank.conf import *
from pitank.tank.screencap import screencap

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames(camera_id):
	conf = readConf()
	camera_id = int(camera_id)
	_type = conf['cameras'][camera_id]['capture_type']
	if _type == 'rpi':
		cap = picam()
	elif _type == 'cv2':
		src = conf['cameras'][camera_id]['src']
		cap = cv2.VideoCapture(src)
	elif _type == 'screen_grab':
		try:
			monitor = conf['cameras'][camera_id]['monitor']
		except:
			monitor = None
		cap = screencap(monitor=monitor)
	print("starting loop...")
	while True:
		success, frame = cap.read()  # read the camera frame
		if not success:
			print("Waiting for camera image...")
		else:
			ret, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed<string:camera_id>/', methods=["GET"])
def video_feed(id):
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def vid_stream_run(ip='0.0.0.0', port=8080):
	app.run(host=ip, port=port, debug=True, threaded=True, use_reloader=False)
	#app.run(debug=True)

if __name__ == "__main__":
	try:
		ip = sys.argv[1]
	except:
		ip = '0.0.0.0'
	try:
		port = int(sys.argv[2])
	except:
		port = 8080
	vid_stream_run(ip=ip, port=port)
