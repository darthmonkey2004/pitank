from distutils.core import setup

setup(name='pitank',
	version='1.0',
	description='Raspberry Pi laser-tank control system',
	author='Matt McClellan',
	author_email='monkey@simiantech.biz',
	url='http://nplayer.simiantech.biz/',
	packages=['pitank.host', 'pitank.tank'],
	package_dir={'pitank.host': 'host', 'pitank.tank': 'tank'},
	scripts=['scripts/tank'],
	data_files=['data/keys.txt', 'data/chassis_bottom.stl', 'data/chassis_top.stl', 'data/motor_mount_plat.stl', 'data/treads_tpu.stl', 'data/upper_deck_shelf.stl'],
	)
