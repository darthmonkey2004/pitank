import pyproj
from pitank.host.browser import *
import gmplot
import requests
import keyring
from random import randint
from testgps import *

class target():
	def __init__(self, _id, lat=None, lon=None, name=None):
		self.id = _id
		self.lat = lat
		self.lon = lon
		self.coords = self.lat, self.lon
		self.name = name
		self.heading = None
		self.distance = -1

		

class mapper():
	def __init__(self, origin=(), zoom=20, origin_name='You Are Here!'):
		self.gps = gps()
		if origin == ():
			print("Getting current location...")
			self.origin = None
			while self.origin is None:
				ret, data = self.gps.poll()
				if ret:
					self.origin = data['lat'], data['lon']
					break
		else:
			self.origin = origin
		self.zoom = zoom
		self.origin_name = origin_name
		self.api_key = self.get_api_key()
		self.origin_color = 'green'
		self.target_color = 'red'
		self.map = self.new_map(origin=self.origin)
		self.targets = {}

	def add_target(self, coords, name=None):
		_id = len(list(self.targets.keys()))
		t_lat, t_lon = coords
		if name is None:
			name = f"target_{_id}"
		t = target(_id=_id, lat=t_lat, lon=t_lon, name=name)
		t.heading, t.distance = self.get_telemetry(t.coords, self.origin)
		print("heading, distance:", t.heading, t.distance)
		self.targets[_id] = t
		return self.targets

	def get_current_pos(self):
		origin = None
		attempts = 0
		while origin is None:
			ret, data = self.gps.poll()
			if ret:
				origin = data['lat'], data['lon']
				break
			else:
				attempts += 1
				if attempts >= 20:
					print("Retries exceeded! Must not have a good fix...")
					origin = (None, None)
					break
		self.origin = origin
		return self.origin
			
				
		

	def update(self):
		self.origin = self.get_current_pos()
		targets = list(self.targets.values())
		for t in targets:
			try:
				t.heading, t.distance = self.get_telemetry(t.coords, self.origin)
			except Exception as e:
				print(f"Failed to update target ({t.id}, {e})! Removing...")
				self.targets = self.remove_target(t.id)
		return self.targets

	def remove_target(self, _id):
		try:
			del self.targets[_id]
			return True
		except Exception as e:
			print(f"Unable to remove target with id {_id}: {e}")
			return False
		

	def set_api_key(self):
		try:
			self.api_key = input("enter api key: ")
			keyring.set_password('API_KEY', 'MAPS', self.api_key)
			return True, self.api_key
		except Exception as e:
			print("Couldn't set api key:", e)	
			return False


	def get_api_key(self):
		try:
			self.api_key = keyring.get_password('API_KEY', 'MAPS')
		except Exception as e:
			print("Key isn't set! Setting...", e)
			ret = self.set_api_key()
			if ret:
				self.api_key = ret
			else:
				self.api_key = None
		return self.api_key




	def get_telemetry(self, next_target, src_coords=None):
		if src_coords is not None:
			self.origin = src_coords
		self.next_target = next_target
		src_lat, src_lon = self.origin
		t_lat, t_lon = self.next_target
		g = pyproj.Geod(ellps='WGS84')
		self.next_target_heading, _, self.next_target_distance = g.inv(src_lon, src_lat, t_lon, t_lat)
		return self.next_target_heading, self.next_target_distance


	def new_map(self, origin=None):
		if origin is not None:
			self.origin = origin
		lat, lon = self.origin
		self.map = gmplot.GoogleMapPlotter(lat, lon, self.zoom, apikey=self.api_key)
		self.map.marker(lat, lon, color=self.origin_color)
		return self.map

	def create_targets_list(self, targets):
		target_lats = []
		target_lons = []
		for target in targets:
			lat, lon = target
			target_lats.append(lat)
			target_lons.append(lon)
		return target_lats, target_lons


	def plot_targets(self, targets=[], coords=None, gmap=None):
		self.targets = targets
		if gmap is not None:
			self.map = gmap
		if coords is not None:
			self.origin = coords
		color = 'red'
		pos = 0
		for target in self.targets:
			pos += 1
			if self.origin is not None:
				heading, distance = get_telemetry(self.origin, target)
				name = f"target_{pos}:heading={heading}, distance={distance}"
			else:
				name = f"target_{pos}"
			#self.map.scatter(lats, lons, color='#3B0B39', size=40, marker=False)
			self.map.marker(target[0], target[1], color=color, title=name)
		return self.map


	def draw_fence(self, pois=[], gmap=None, coords=None):
		if gmap is not None:
			self.map = gmap
		color = 'blue'
		rois = zip(*pois)
		self.map.polygon(*rois, color=color, edge_width=10)
		return self.map

	def open(filepath='map.html'):
		self.filepath = filepath
		self.map.draw(self.filepath)


if __name__ == "__main__":
	#right = lon + step
	#left = lon - step
	#down = lat - step
	#up = lat + step
	step = 1
	lon = 0
	lat = 0
	coords = lat, lon
	targets = []
	t_lat = -1
	t_lon = lon
	targets.append((t_lat, t_lon))
	for i in range(0, 8):
		t_lat = t_lat - step
		#t_lon = t_lon + step
		targets.append((t_lat, t_lon))


	m = new_map(coords[0], coords[1])
	m = plot_targets(targets=targets, coords=coords, gmap=m)
	m.draw('map.html')
