from random import randint
import threading
import serial
import os
import keyring
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions




def get_api_key():
	try:
		api_key = keyring.get_password('API_KEY', 'MAPS')
	except Exception as e:
		print("Key isn't set! Setting...", e)
		ret = set_api_key()
		if ret:
			api_key = ret
		else:
			api_key = None
	return api_key

def set_api_key():
	try:
		api_key = input("enter api key: ")
		keyring.set_password('API_KEY', 'MAPS', api_key)
		return True, api_key
	except Exception as e:
		print("Couldn't set api key:", e)	
		return False

def rgb_to_hex(rgb):
	val = '%02x%02x%02x' % rgb
	val = f"#{val}"
	return val

def rdm_color():
	return randint(0, 255), randint(0, 255), randint(0, 255)

def new_plot(lat, lon, zoom=10, map_type='satellite'):
	bokeh_width, bokeh_height = 500,400
	api_key = get_api_key()
	gmap_options = GMapOptions(lat=lat, lng=lon, map_type=map_type, zoom=zoom)
	p = gmap(api_key, gmap_options, title='test', width=bokeh_width, height=bokeh_height, tools=['hover', 'reset', 'wheel_zoom', 'pan'])
	return p

def plot(coords=(), targets=[], p=None):
	lat, lon = coords
	if p is None:
		p = new_plot(lat, lon)
	for target in targets:
		t_lat, t_lon = target
		color = rdm_color()
		center = p.circle([t_lon], [t_lat], size=10, alpha=0.5, color=color)
	show(p)
	return p		
		

def parse_coord(coord):
	c = float(coord) / 100
	if c != 0.0 and c != -0.0:
		l = len(str(c)) + 4
		return round(c, l)

def parse_coords(lat, lat_direction, lon, lon_direction):
	lat = parse_coord(lat)
	lon = parse_coord(lon)
	if lat_direction == 'S':
		if lat >= 0:
			lat = 0 - c
		else:
			pass
	if lat_direction == 'N':
		pass
	if lon_direction == 'E':
		pass
	if lon_direction == 'W':
		if lon >= 0:
			lon = 0 - lon
		else:
			pass
	return lat, lon
	


def map_coords(lat, lon):
	api_key = get_api_key()

class gps():
	def __init__(self, dev='/dev/ttyACM0', baud=9600, timeout=0.5):
		self.device = dev
		self.gps = serial.Serial(dev, baudrate=baud, timeout=timeout)
		self.info = {0: 'tag', 1: 'utc', 2: 'status', 3: 'lat', 4: 'lat_direction', 5: 'lon', 6: 'lon_direction', 7: 'speed Kn', 8: 'track true', 9: 'date', 10: 'mag var', 11: 'var dir', 12: 'mode ind', 13: 'checksum', 14: 'terminator'}
		self.data = None
		self.start()
		
	def read_loop(self):
		self.run_loop = True
		while self.run_loop:
			data = self.get_data()
			if data != {}:
				self.data = data
			

	def get_data(self):
		keepers = [1, 3, 4, 5, 6, 7, 9]
		d = {}
		data = self.gps.readline().decode()
		tag = data.split(',')[0]
		if tag == '$GPRMC':
			data = data.split(',')
			valid = data[2]
			if valid == 'V':
				pass
			elif valid == 'A':
				pos = -1
				ct = len(data)
				for chunk in data:
					pos += 1
					#print(pos, ct)
					k = self.info[pos]
					if chunk is not None and chunk != '' and pos in keepers:
						d[k] = chunk
						if k == 'speed Kn':
							mph = round(float(chunk) * 1.15078, 3)
							d['mph'] = mph
							fps = round(mph * 1.46667, 3)
							d['fps'] = fps
			d['lat'], d['lon'] = parse_coords(lat=d['lat'], lat_direction=d['lat_direction'], lon=d['lon'], lon_direction=d['lon_direction'])
		return d
				

	def start(self):
		self.gps_thread = threading.Thread(target=self.read_loop)
		self.gps_thread.setDaemon(True)
		self.gps_thread.start()
		print("GPS read loop started!")

	def poll(self):
		if self.data is None:
			return False, None
		else:
			return True, self.data

	def close(self):
		print("closing connection...")
		try:
			self.gps.close()
			return True
		except Exception as e:
			print(f"Couldn't close device: {e}, device:{self.device}")
			return False

if __name__ == "__main__":
	g = gps()
	while True:
		ret, data = g.poll()
		if ret:
			print(data)
