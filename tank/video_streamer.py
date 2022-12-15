from flask import Response
from flask import Flask
from flask import render_template
from pitank.tank.picap import *
import time
app = Flask(__name__)
import cv2
import threading

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
	cap = picam()
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

@app.route('/video_feed')
def video_feed():
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
