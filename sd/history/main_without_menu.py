from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time, sys
from Maix import FPIOA, GPIO

ai_flash_freespace = (os.statvfs("/flash")[0]*os.statvfs("/flash")[3])/(1024*1024)
ai_sd_freespace = (os.statvfs("/sd")[0]*os.statvfs("/sd")[3])/(1024*1024)

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(3)
lcd.clear(lcd.BLACK)

splash = image.Image("/sd/preset/images/splash_bg.jpg")

try:
	splash.clear()
	splash.draw_string(40, 100, "Running Last Code...", color=(255,255,255), scale=2, mono_space=False)
	lcd.display(splash, oft=(0,0))
	time.sleep_ms(1000)
	splash.clear()
	lcd.display(splash, oft=(0,0))
	exec(open("/sd/user_latest_code.py").read())
	print("running code...")
except BaseException as e:
	splash.clear()
	lcd.display(splash, oft=(0,0))
	if str(e) == "[Errno 2] ENOENT":
		splash.clear()
		splash.draw_string(35, 90, "Upload your code via:", color=(0,255,255), scale=2, mono_space=False)
		splash.draw_string(35, 110, "http://x.cocorobo.hk", color=(255,255,255), scale=2, mono_space=False)
		lcd.display(splash, oft=(0,0))
	elif str(e) != "[Errno 2] ENOENT":
		splash.clear()
		splash.draw_string(10,10, "Failed to run your last code,", color=(255,0,0), scale=2, mono_space=False)
		splash.draw_string(10,30, "Re-upload and try again.", color=(255,0,0), scale=2, mono_space=False)
		splash.draw_string(10,60, "Error Info:", color=(255,255,255), scale=2, mono_space=False)
		splash.draw_string(10,80, str(e), color=(255,0,0), scale=2, mono_space=False)
		lcd.display(splash, oft=(0,0))
	print("failed")
	sys.exit(0)