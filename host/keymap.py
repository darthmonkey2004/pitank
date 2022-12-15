import pickle
import os

ctk = {1: 'Escape', 2: 'exclam', 3: 'at', 4: 'numbersign', 5: 'dollar', 6: 'percent', 7: 'asciicircum', 8: 'ampersand', 9: 'asterisk', 10: 'parenleft', 11: 'parenright', 12: 'underscore', 13: 'plus', 14: 'BackSpace', 15: 'ISO_Left_Tab', 16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P', 26: 'braceleft', 27: 'braceright', 28: 'Return', 29: 'Control_L', 30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L', 39: 'colon', 40: 'quotedbl', 41: 'asciitilde', 42: 'Shift_L', 43: 'bar', 44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M', 51: 'less', 52: 'greater', 53: 'question', 54: 'Shift_R', 55: 'XF86ClearGrab', 56: 'Meta_L', 57: 'space', 58: 'Caps_Lock', 59: 'F1', 60: 'F2', 61: 'F3', 62: 'F4', 63: 'F5', 64: 'F6', 65: 'F7', 66: 'F8', 67: 'F9', 68: 'F10', 69: 'Num_Lock', 70: 'Scroll_Lock', 71: 'KP_7', 72: 'KP_8', 73: 'KP_9', 74: 'XF86Prev_VMode', 75: 'KP_4', 76: 'KP_5', 77: 'KP_6', 78: 'XF86Next_VMode', 79: 'KP_1', 80: 'KP_2', 81: 'KP_3', 82: 'KP_0', 83: 'KP_Decimal', 84: 'ISO_Level3_Shift', 85: '     93    \t', 86: 'bar', 87: 'XF86Switch_VT_11', 88: 'XF86Switch_VT_12', 89: '     97    \t', 90: 'Katakana', 91: 'Hiragana', 92: 'Henkan_Mode', 93: 'Hiragana_Katakana', 94: 'Muhenkan', 95: '    103    \t', 96: 'KP_Enter', 97: 'Control_R', 98: 'XF86Ungrab', 99: 'Sys_Req', 100: 'Meta_R', 101: 'Linefeed', 102: 'Home', 103: 'Up', 104: 'Prior', 105: 'Left', 106: 'Right', 107: 'End', 108: 'Down', 109: 'Next', 110: 'Insert', 111: 'Delete', 112: '    120    \t', 113: 'XF86AudioMute', 114: 'XF86AudioLowerVolume', 115: 'XF86AudioRaiseVolume', 116: 'XF86PowerOff', 117: 'KP_Equal', 118: 'plusminus', 119: 'Break', 120: 'XF86LaunchA', 121: 'KP_Decimal', 122: 'Hangul', 123: 'Hangul_Hanja', 124: '    132    \t', 125: 'Super_L', 126: 'Super_R', 127: 'Menu', 128: 'Cancel', 129: 'Redo', 130: 'SunProps', 131: 'Undo', 132: 'SunFront', 133: 'XF86Copy', 134: 'XF86Open', 135: 'XF86Paste', 136: 'Find', 137: 'XF86Cut', 138: 'Help', 139: 'XF86MenuKB', 140: 'XF86Calculator', 141: '    149    \t', 142: 'XF86Sleep', 143: 'XF86WakeUp', 144: 'XF86Explorer', 145: 'XF86Send', 146: '    154    \t', 147: 'XF86Xfer', 148: 'XF86Launch1', 149: 'XF86Launch2', 150: 'XF86WWW', 151: 'XF86DOS', 152: 'XF86ScreenSaver', 153: 'XF86RotateWindows', 154: 'XF86TaskPane', 155: 'XF86Mail', 156: 'XF86Favorites', 157: 'XF86MyComputer', 158: 'XF86Back', 159: 'XF86Forward', 160: '    168    \t', 161: 'XF86Eject', 162: 'XF86Eject', 163: 'XF86AudioNext', 164: 'XF86AudioPause', 165: 'XF86AudioPrev', 166: 'XF86Eject', 167: 'XF86AudioRecord', 168: 'XF86AudioRewind', 169: 'XF86Phone', 170: '    178    \t', 171: 'XF86Tools', 172: 'XF86HomePage', 173: 'XF86Reload', 174: 'XF86Close', 175: '    183    \t', 176: '    184    \t', 177: 'XF86ScrollUp', 178: 'XF86ScrollDown', 179: 'parenleft', 180: 'parenright', 181: 'XF86New', 182: 'Redo', 183: 'XF86Tools', 184: 'XF86Launch5', 185: 'XF86Launch6', 186: 'XF86Launch7', 187: 'XF86Launch8', 188: 'XF86Launch9', 189: '    197    \t', 190: 'XF86AudioMicMute', 191: 'XF86TouchpadToggle', 192: 'XF86TouchpadOn', 193: 'XF86TouchpadOff', 194: '    202    \t', 195: 'Mode_switch', 196: 'Alt_L', 197: 'Meta_L', 198: 'Super_L', 199: 'Hyper_L', 200: 'XF86AudioPlay', 201: 'XF86AudioPause', 202: 'XF86Launch3', 203: 'XF86Launch4', 204: 'XF86LaunchB', 205: 'XF86Suspend', 206: 'XF86Close', 207: 'XF86AudioPlay', 208: 'XF86AudioForward', 209: '    217    \t', 210: 'Print', 211: '    219    \t', 212: 'XF86WebCam', 213: 'XF86AudioPreset', 214: '    222    \t', 215: 'XF86Mail', 216: 'XF86Messenger', 217: 'XF86Search', 218: 'XF86Go', 219: 'XF86Finance', 220: 'XF86Game', 221: 'XF86Shop', 222: '    230    \t', 223: 'Cancel', 224: 'XF86MonBrightnessDown', 225: 'XF86MonBrightnessUp', 226: 'XF86AudioMedia', 227: 'XF86Display', 228: 'XF86KbdLightOnOff', 229: 'XF86KbdBrightnessDown', 230: 'XF86KbdBrightnessUp', 231: 'XF86Send', 232: 'XF86Reply', 233: 'XF86MailForward', 234: 'XF86Save', 235: 'XF86Documents', 236: 'XF86Battery', 237: 'XF86Bluetooth', 238: 'XF86WLAN'}
ktc = {'Escape': 1, 'exclam': 2, 'at': 3, 'numbersign': 4, 'dollar': 5, 'percent': 6, 'asciicircum': 7, 'ampersand': 8, 'asterisk': 9, 'parenleft': 179, 'parenright': 180, 'underscore': 12, 'plus': 13, 'BackSpace': 14, 'ISO_Left_Tab': 15, 'Q': 16, 'W': 17, 'E': 18, 'R': 19, 'T': 20, 'Y': 21, 'U': 22, 'I': 23, 'O': 24, 'P': 25, 'braceleft': 26, 'braceright': 27, 'Return': 28, 'Control_L': 29, 'A': 30, 'S': 31, 'D': 32, 'F': 33, 'G': 34, 'H': 35, 'J': 36, 'K': 37, 'L': 38, 'colon': 39, 'quotedbl': 40, 'asciitilde': 41, 'Shift_L': 42, 'bar': 86, 'Z': 44, 'X': 45, 'C': 46, 'V': 47, 'B': 48, 'N': 49, 'M': 50, 'less': 51, 'greater': 52, 'question': 53, 'Shift_R': 54, 'XF86ClearGrab': 55, 'Meta_L': 197, 'space': 57, 'Caps_Lock': 58, 'F1': 59, 'F2': 60, 'F3': 61, 'F4': 62, 'F5': 63, 'F6': 64, 'F7': 65, 'F8': 66, 'F9': 67, 'F10': 68, 'Num_Lock': 69, 'Scroll_Lock': 70, 'KP_7': 71, 'KP_8': 72, 'KP_9': 73, 'XF86Prev_VMode': 74, 'KP_4': 75, 'KP_5': 76, 'KP_6': 77, 'XF86Next_VMode': 78, 'KP_1': 79, 'KP_2': 80, 'KP_3': 81, 'KP_0': 82, 'KP_Decimal': 121, 'ISO_Level3_Shift': 84, '     93    \t': 85, 'XF86Switch_VT_11': 87, 'XF86Switch_VT_12': 88, '     97    \t': 89, 'Katakana': 90, 'Hiragana': 91, 'Henkan_Mode': 92, 'Hiragana_Katakana': 93, 'Muhenkan': 94, '    103    \t': 95, 'KP_Enter': 96, 'Control_R': 97, 'XF86Ungrab': 98, 'Sys_Req': 99, 'Meta_R': 100, 'Linefeed': 101, 'Home': 102, 'Up': 103, 'Prior': 104, 'Left': 105, 'Right': 106, 'End': 107, 'Down': 108, 'Next': 109, 'Insert': 110, 'Delete': 111, '    120    \t': 112, 'XF86AudioMute': 113, 'XF86AudioLowerVolume': 114, 'XF86AudioRaiseVolume': 115, 'XF86PowerOff': 116, 'KP_Equal': 117, 'plusminus': 118, 'Break': 119, 'XF86LaunchA': 120, 'Hangul': 122, 'Hangul_Hanja': 123, '    132    \t': 124, 'Super_L': 198, 'Super_R': 126, 'Menu': 127, 'Cancel': 223, 'Redo': 182, 'SunProps': 130, 'Undo': 131, 'SunFront': 132, 'XF86Copy': 133, 'XF86Open': 134, 'XF86Paste': 135, 'Find': 136, 'XF86Cut': 137, 'Help': 138, 'XF86MenuKB': 139, 'XF86Calculator': 140, '    149    \t': 141, 'XF86Sleep': 142, 'XF86WakeUp': 143, 'XF86Explorer': 144, 'XF86Send': 231, '    154    \t': 146, 'XF86Xfer': 147, 'XF86Launch1': 148, 'XF86Launch2': 149, 'XF86WWW': 150, 'XF86DOS': 151, 'XF86ScreenSaver': 152, 'XF86RotateWindows': 153, 'XF86TaskPane': 154, 'XF86Mail': 215, 'XF86Favorites': 156, 'XF86MyComputer': 157, 'XF86Back': 158, 'XF86Forward': 159, '    168    \t': 160, 'XF86Eject': 166, 'XF86AudioNext': 163, 'XF86AudioPause': 201, 'XF86AudioPrev': 165, 'XF86AudioRecord': 167, 'XF86AudioRewind': 168, 'XF86Phone': 169, '    178    \t': 170, 'XF86Tools': 183, 'XF86HomePage': 172, 'XF86Reload': 173, 'XF86Close': 206, '    183    \t': 175, '    184    \t': 176, 'XF86ScrollUp': 177, 'XF86ScrollDown': 178, 'XF86New': 181, 'XF86Launch5': 184, 'XF86Launch6': 185, 'XF86Launch7': 186, 'XF86Launch8': 187, 'XF86Launch9': 188, '    197    \t': 189, 'XF86AudioMicMute': 190, 'XF86TouchpadToggle': 191, 'XF86TouchpadOn': 192, 'XF86TouchpadOff': 193, '    202    \t': 194, 'Mode_switch': 195, 'Alt_L': 196, 'Hyper_L': 199, 'XF86AudioPlay': 207, 'XF86Launch3': 202, 'XF86Launch4': 203, 'XF86LaunchB': 204, 'XF86Suspend': 205, 'XF86AudioForward': 208, '    217    \t': 209, 'Print': 210, '    219    \t': 211, 'XF86WebCam': 212, 'XF86AudioPreset': 213, '    222    \t': 214, 'XF86Messenger': 216, 'XF86Search': 217, 'XF86Go': 218, 'XF86Finance': 219, 'XF86Game': 220, 'XF86Shop': 221, '    230    \t': 222, 'XF86MonBrightnessDown': 224, 'XF86MonBrightnessUp': 225, 'XF86AudioMedia': 226, 'XF86Display': 227, 'XF86KbdLightOnOff': 228, 'XF86KbdBrightnessDown': 229, 'XF86KbdBrightnessUp': 230, 'XF86Reply': 232, 'XF86MailForward': 233, 'XF86Save': 234, 'XF86Documents': 235, 'XF86Battery': 236, 'XF86Bluetooth': 237, 'XF86WLAN': 238}
bt_ktc = {'joy_left': 168, 'joy_right': 208, 'joy_up': 165, 'joy_down': 163, 'top_trigger': 164, 'bottom_trigger': 113, 'btn_a': 114, 'btn_y': 115}
bt_ctk = {168: 'joy_left', 208: 'joy_right', 165: 'joy_up', 163: 'joy_down', 164: 'top_trigger', 113: 'bottom_trigger', 114: 'btn_a', 115: 'btn_y'}
keymap = {"turn_left": 105, "turn_right": 106, "forward": 103, "reverse": 108, "fire": 57, "ceaseFire": 57, "aim_up": 104, "aim_down": 109, "aim_center": 107, "aim_left": None, "aim_right": None, "estop": 1, "spd_1": 2, "spd_2": 3, "spd_3": 4, "spd_4": 5, "spd_5": 6}

def read_map(filepath=None):
	if filepath is None:
		filepath = os.path.join(os.getcwd(), 'button_map.dat')
		print("Default filepath used:", filepath)
	try:
		with open(filepath, 'rb') as f:
			data = pickle.load(f)
			f.close()
		print("Button map loaded!")
		return data
	except:
		print(f"No button map file found at '{filepath}'! Creating with defaults...")
		filepath = os.path.join(os.getcwd(), 'button_map.dat')
		write_map(keymap, filepath)
		return keymap

	

def write_map(data, filepath=None):
	if filepath is None:
		filepath = os.path.join(os.getcwd(), 'button_map.dat')
	with open(filepath, 'wb') as f:
		pickle.dump(data, f)
		f.close()
	return data

class btn(object):
	def __init__(self, name=None, code=None, ctrl=None, button_map=None):
		self.name = name
		self.code = code
		self.ctrl = ctrl
		self.value = 0
		if button_map is not None:
			self.map = self.set_map(button_map=button_map)
		else:
			self.map = read_map()

	def set_defaults(self):
		self.map = read_map()
		return self.map

	def set_map(self, button_map):
		if type(button_map) == dict:
			#if type is dictionary, map provided.
			self.map = button_map
		elif type(button_map) == str:
			#if type is string, assume it's a filepath to previous map pickle data
			self.map = read_map(button_map)
		elif self.map is None:
			self.map = read_map()
		return self.map


	def new(self, value=None, name=None, code=None, ctrl=None, button_map=None):
		#parent class function for creation of a new btn object.
		#needs eiher name or code, optionally set a control
		if value is not None:
			self.value = int(value)
		else:
			self.value = 0
		if name is not None:
			self.name = name
			self.code = ktc[self.name]
		if code is not None:
			self.code = code
			self.name = ctk[self.code]
		if ctrl is not None:
			if type(ctrl) == int:
				self.ctrl = set_ctrl(code=ctrl)
			elif type(ctrl) == str:
				self.ctrl = set_ctrl(name=name)
			elif isinstance(ctrl, control):
				self.ctrl = ctrl
		if self.name is None and self.code is None:
			errmsg = "Error creating new button object: Must have either name or code!"
			raise Exception(Exception, errmsg)
		return self

	def set(self, value):
		try:
			self.value = int(value)
			return True
		except Exception as e:
			print("invalid type for btn.value:", e)
			return False

	def set_ctrl(self, name=None, code=None, button_map=None):
		try:
			self.ctrl = control(name=name, code=code, button_map=button_map)
			return self.ctrl
		except Exception as e:
			txt = f"Couldn't set control! Error message: e"
			raise Exception(Exception, txt)
			return None


class control():
	def __init__(self, button_map, name=None, code=None):
		#base class for control objects, used in btn class as ctrl property
		self.map = button_map
		if code is not None:
			self.code = code
			names, codes = list(self.map.keys()), list(self.map.values())
			self.name = names[codes.index(self.code)]
		if name is not None:
			self.name = name
			self.code = self.map[self.name]



def set_controls(button_map=None):
	if button_map is None:
		print("loading default map...")
		button_map = read_map(filepath=os.path.join(os.getcwd(), 'button_map.dat'))
	controls = {}
	for name in button_map.keys():
		code = button_map[name]
		b = btn(code=code, button_map=button_map)
		b.set_ctrl(name=name, button_map=button_map)
		controls[name] = b
	return controls
