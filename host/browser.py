import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from threading import Thread

#f"http://monkey:{pw}@192.168.2.22:6969/video"
class Window(QMainWindow):
	def __init__(self, url=None):
		if url is None:
			self.url = 'http://192.168.2.22:8080/'
		else:
			self.url = url
		super(Window,self).__init__()
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl(self.url))
		self.setCentralWidget(self.browser)
		self.showMaximized()
		self.searchBar = QLineEdit()
		self.searchBar.returnPressed.connect(self.loadUrl)
		self.thread_type = 'browser'
		self.pid = os.getpid()
	def home(self):
		self.browser.setUrl(QUrl(self.url))
	def loadUrl(self):
		#fetching entered url from searchBar
		self.url = self.searchBar.text()
		self.browser.setUrl(QUrl(self.url))
	def updateUrl(self, url):
		self.searchBar.setText(url.toString())

def run_browser(url=None):
	if url is None:
		url = 'http://192.168.2.22:8080/'
	MyApp = QApplication(sys.argv)
	#setting application name
	QApplication.setApplicationName('NicVision MPJG Viewer')
	#creating window
	window = Window(url=url)
	#executing created app
	MyApp.exec_()

def start_thread(url=None):
	if url is not None:
		t = Thread(target=run_browser, args=(url,))
	else:
		t = Thread(target=run_browser)
	t.setDaemon(True)
	t.start()
if __name__ == "__main__":
	import sys
	try:
		url = sys.argv[1]
	except:
		url = None
	start_thread(url)
