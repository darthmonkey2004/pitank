import os
import subprocess

def get_py_version():
	py_v = None
	py3_v = None
	ret = False
	try:
		py3_v = subprocess.check_output("python3 --version", shell=True).decode().strip()
		ret = True
	except:
		py3_v = None
		ret = False
	if py3_v is None:
		try:
			py_v = subprocess.check_output("python --version", shell=True).decode().strip()
			ret = True
		except:
			py_v = None
			print("No suitable python version found!")
			ret = False
	if py_v is not None and py_v != '':
		v = py_v
	elif py3_v is not None and py3_v != '':
		v = py3_v
	v = ".".join(v.split('.')[:2]).replace(' ', '').lower()
	return ret, v
	
def ensure_templates_dir(index_file_path):
	d = os.path.dirname(index_file_path)
	try:
		ret = subprocess.check_output(f"mkdir -p \"{d}\"", shell=True).decode().strip()
		if ret != '':
			return False, ret
		else:
			return True, None
	except Exception as e:
		print(f"Error occured attempting to create templates directory: {e}")
		return False, e

html_header = """<!doctype html>
<html lang="en">
<head>
	<title>CAMVIEWER</title>
	<style type="text/css">
	.mover  {
		 width:640px; height:352px; line-height:4em; margin:10px; padding:5px; float:left; border:1px dotted #333333; text-align:center;
"""
html_footer = """
		</div>
	</body> 
</html>"""

html_body = """
	</style>
	<script type="text/javascript">
		function dragWord(dragEvent){
			dragEvent.dataTransfer.setData("Id",	dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
			}				   
		function dropWord(dropEvent){ 
			var dropData = dropEvent.dataTransfer.getData("Id");
			dropItems = dropData.split("|"); 
			var prevElem = document.getElementById(dropItems[1]); 
			prevElem.getElementsByTagName("div")[0].id = dropEvent.target.id;			  
			dropEvent.target.id = dropItems[0]; 
			dropEvent.preventDefault(); 
			} 
	</script> 
	</head> 
	<body>
		<div id="camsection">
"""

def new_camera(camera_id, _type):
	if _type == 'css':
		cam_css1 = f"			#box_{camera_id}"
		cam_css2 = """{
				background-image: url({{ url_for('video_feed', id='"""
		cam_css3 = f"{camera_id}"
		cam_css4 = """') }})
			 }"
"""
		css = f"{cam_css1}{cam_css2}{cam_css3}{cam_css4}"
		return css
	elif _type == 'html':
		html = f"""			<div id="box{camera_id}" ondragover="event.preventDefault()" ondrop="dropWord(event)">
			<div class="mover" id="box_{camera_id}" draggable="true" ondragstart="dragWord(event)"></div>
			</div>"""
		return html

def get_css(cam_list):
	css_list = []
	for camera_id in cam_list:
		css = new_camera(camera_id, 'css')
		css_list.append(css)
	j = "\n"
	css = j.join(css_list)
	return css

def get_html(cam_list):
	html_list = []
	for camera_id in cam_list:
		html = new_camera(camera_id, 'html')
		html_list.append(html)
	j = "\n\n"
	html = j.join(html_list)
	return html

def mkhtml(camera_ids):
	cams_css = get_css(camera_ids)
	cams_html = get_html(camera_ids)
	html = f"{html_header}{cams_css}{html_body}{cams_html}{html_footer}"
	return html

def setup(number_of_cameras=0):
	if number_of_cameras == 0:
		number_of_cameras = int(input("Enter number of cameras to view on page: "))
	l = []
	for i in range(number_of_cameras):
		l.append(i)
	html = mkhtml(l)
	ret, v = get_py_version()
	if ret:
		index_path = os.path.join(os.path.expanduser("~"), '.local', 'lib', v, 'site-packages', 'pitank', 'tank', 'templates', 'index.html')
	else:
		index_path = None
		raise Exception(Exception, ret)
	ret, errmsg = ensure_templates_dir(index_path)
	if ret:
		with open(index_path, 'w') as f:
			f.write(html)
			f.close()
		print(f"Index written to templates directory ({index_path})!")
	else:
		print("Failed to write html! Do we have write permissions?")
	return
