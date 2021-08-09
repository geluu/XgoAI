print("Clearing Cached Variables...", end="")
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
print(" Done\n")
import gc
import KPU as kpu
from Maix import utils
utils.gc_heap_size(0xAF000)#GC 500KB
print("utils.gc_heap_size():\t" + str(utils.gc_heap_size()))

import os, Maix, lcd, image, sensor, gc, time, math
from Maix import FPIOA, GPIO
from fpioa_manager import *

gc.enable()

count = 0

def gc_log():
    global count
    gc.collect()
    count = count + 1
    print(str(count) + ":" +str(gc.mem_free()/1000)+"kb")

buttonLeft, buttonRight, buttonDown = 9, 10, 11

fpiol = FPIOA()
fpior = FPIOA()
fpiod = FPIOA()

fpiol.set_function(buttonLeft,FPIOA.GPIO0)
fpior.set_function(buttonRight,FPIOA.GPIO1)
fpiod.set_function(buttonDown,FPIOA.GPIO2)

key_gpio_left=GPIO(GPIO.GPIO0,GPIO.IN)
key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)
key_gpio_down=GPIO(GPIO.GPIO2,GPIO.IN)

ksl,ksr,ksd = 0, 0, 0

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)

color_splash_theme = (15,21,46)
color_blue = (31,61,185)
color_blue_lighter = (60,131,211)
color_white = (255,255,255)
color_gray = (60,73,126)
color_orange = (255,165,0)
color_red = (255,0,0)

splash = image.Image(size=(240, 240))
splash.clear()
splash.draw_rectangle(0,0,240,240,color=color_splash_theme,fill=True)

CATEGORY_ITEMS_DICT = {
	"null": (33, 3, 174, 30, 41, 8, '', "/sd/preset/images/icon_basics.jpg"),
	"basics": (33, 3, 174, 30, 41, 8, 'BASICS', "/sd/preset/images/icon_basics.jpg"),
	"vision": (33, 3, 174, 30, 41, 8, 'VISION', "/sd/preset/images/icon_vision.jpg"),
	"ml": (33, 3, 174, 30, 41, 10, 'A.I.', "/sd/preset/images/icon_ml.jpg"),
	"audiovideo": (33, 3, 174, 30, 41, 8, 'MEDIA', "/sd/preset/images/icon_av.jpg")
}

MENU_ITEM_PARENT_PATH = "/sd/preset/demos/"

MENU_ITEMS = [
	# Basics
	("Mini Camera", CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_mini_camera" + ".py"), 
	("Camera Shot Browser",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_camera_shot_browser" + ".py"), 
	("Button Rotate Clock",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_rotate_clock" + ".py"), 
	("Button Switch Color",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_switch_color" + ".py"), 
	("LCD Drawing Demo",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_lcd_drawing_demo" + ".py"), 
	("Generative Mondrian",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_generative_mondrian" + ".py"), 
	("Screen Rotation",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_screen_rotation" + ".py"), 
	("Button Resize Image",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_resize" + ".py"), 
	("Hanzi Character Demo",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_cjk-test" + ".py"), 
	# Machine Learning
	("Training Set Collector", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_training_set_collector" + ".py"), 
	("Face Tracking",  CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_face_recognition" + ".py"), 
	("Object Tracking", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_object_recognition" + ".py"), 
	("Coco Logo Recognition", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_coco_logo_recognition" + ".py"), 
	("Digit Recognition", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_handwritten_digit_recognition" + ".py"), 
	("Trash Classification", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_hongkong_trash_classification" + ".py"), 
	# ("HK Road Sign Recognition", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_hongkong_trash_classification" + ".py"), 
	("Facial Recognition", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_face-compare" + ".py"), 
	("Object Classifier", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_object-classifier" + ".py"), 
	# Machine Vision
	("Double Line Detection", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_double_line_detection" + ".py"), 
	("Single Line Detection", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_single_line_detection" + ".py"), 
	("Regional Color Analyze", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_reginal_color_analyze" + ".py"), 
	("Learn & Track Color", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_learn_track_color" + ".py"), 
	("Find Color Green Object", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_color_green" + ".py"),
	("Find Circles", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_circle" + ".py"),
	("Find Rectangles", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_rectangle" + ".py"),
	("Find Lines", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_lines" + ".py"),
	("Find QR Code and Decode", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_qr_code_2" + ".py"),
	# Audio & Video
	("Sound Spectrum Analyze", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_spectrum_analyze" + ".py"), 
	("Play Music File", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_play_music" + ".py"), 
	("Speech Recognition (Record)", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_speech_record" + ".py"),
	("Speech Recognition (Use)", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_speech_recognition" + ".py")
	# ("Record Camera to Video", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_camera_record" + ".py"), 
	# ("Play Recorded Video", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_play_recorded_video" + ".py")
]

BASE_COORD = [3, 33, 3+10, 33+5]
MENU_ITEM_BOX_SIZE = (234, 30)

MENU_ITEM_COORD = [
	[BASE_COORD[0], BASE_COORD[1], BASE_COORD[2], BASE_COORD[3]],
	[BASE_COORD[0], BASE_COORD[1]+29*1, BASE_COORD[2], BASE_COORD[3]+29*1],
	[BASE_COORD[0], BASE_COORD[1]+29*2, BASE_COORD[2], BASE_COORD[3]+29*2],
	[BASE_COORD[0], BASE_COORD[1]+29*3, BASE_COORD[2], BASE_COORD[3]+29*3],
	[BASE_COORD[0], BASE_COORD[1]+29*4, BASE_COORD[2], BASE_COORD[3]+29*4],
	[BASE_COORD[0], BASE_COORD[1]+29*5, BASE_COORD[2], BASE_COORD[3]+29*5],
	[BASE_COORD[0], BASE_COORD[1]+29*6, BASE_COORD[2], BASE_COORD[3]+29*6],
	[BASE_COORD[0], BASE_COORD[1]+29*7, BASE_COORD[2], BASE_COORD[3]+29*7]
] 

MENU_TOTAL_ITEMS = len(MENU_ITEMS) - 1
MENU_CURRENT_SELECT = 0
MENU_PAGE_SWAP_COUNT = 0
MENU_PAGES_TOTAL = math.ceil((MENU_TOTAL_ITEMS+1) / 6)

if isinstance((MENU_TOTAL_ITEMS+1) / 6, int) == True:
	print("Total page "+ str((MENU_TOTAL_ITEMS+1) / 6)  +" is integer!")
elif isinstance((MENU_TOTAL_ITEMS+1) / 6, int) == False:
	print("Total page "+ str((MENU_TOTAL_ITEMS+1) / 6)  +" is not integer!")
	print(MENU_PAGES_TOTAL*6 - (MENU_TOTAL_ITEMS+1))
	for i in range(0,MENU_PAGES_TOTAL*6 - (MENU_TOTAL_ITEMS+1)+1,1):
		MENU_ITEMS.append(("",CATEGORY_ITEMS_DICT["null"],MENU_ITEM_PARENT_PATH + "" + ".py"))

def draw_nav(type):
	if type == "init":
		# Draw Left-side Up Arrow
		splash.draw_rectangle(3,3,30,30,color=color_blue,fill=True)
		splash.draw_rectangle(3,3,30,30,color=color_blue,fill=False)
		nav_up = image.Image("/sd/preset/images/arrow_up_filled.jpg")
		splash.draw_image(nav_up, 5, 5)
		# splash.draw_rectangle(5,5,26,26,color=color_white,fill=False)
		# Draw Right-side Down Arrow
		splash.draw_rectangle(207,3,30,30,color=color_blue,fill=True)
		splash.draw_rectangle(207,3,30,30,color=color_blue,fill=False)
		nav_down = image.Image("/sd/preset/images/arrow_down_filled.jpg")
		splash.draw_image(nav_down, 209, 5)
		# splash.draw_rectangle(209,5,26,26,color=color_white,fill=False)
	elif type == "left":
		# Draw Left-side Up Arrow
		splash.draw_rectangle(3,3,30,30,color=color_blue,fill=True)
		nav_up = image.Image("/sd/preset/images/arrow_up_pressed.jpg")
		splash.draw_image(nav_up, 5, 5)
		# splash.draw_rectangle(5,5,26,26,color=color_white,fill=True)
	elif type == "right":
		# Draw Right-side Down Arrow
		splash.draw_rectangle(207,3,30,30,color=color_blue,fill=True)
		nav_down = image.Image("/sd/preset/images/arrow_down_pressed.jpg")
		splash.draw_image(nav_down, 209, 5)
		#splash.draw_rectangle(209,5,26,26,color=color_white,fill=True)

def draw_ok(type):
	if type == "released":
		splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=color_blue_lighter,thickness=1)
		splash.draw_string(MENU_ITEM_COORD[6][0]+8,MENU_ITEM_COORD[6][1]+6,"RUN", mono_space=False,color=color_splash_theme,scale=2)
	elif type == "pressed":
		splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=(26,81,143),thickness=1)
		splash.draw_string(MENU_ITEM_COORD[6][0]+8,MENU_ITEM_COORD[6][1]+6,"RUN", mono_space=False,color=color_splash_theme,scale=2)

def draw_title_bar(index):
	splash.draw_rectangle(MENU_ITEMS[index][1][0],MENU_ITEMS[index][1][1],MENU_ITEMS[index][1][2],MENU_ITEMS[index][1][3], color=color_blue, fill=True)
	splash.draw_string(MENU_ITEMS[index][1][4],MENU_ITEMS[index][1][5],MENU_ITEMS[index][1][6],color=color_white,mono_space=False,scale=2)
	
	splash.draw_string(190,213,str(index) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_splash_theme,mono_space=False,scale=2)
	splash.draw_string(190,213,str(index+2) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_splash_theme,mono_space=False,scale=2)
	splash.draw_string(190,213,str(index+1) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_white,mono_space=False,scale=2)

def draw_item(row, type, realindex):
	if type == "unselected":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)
	elif type == "selected":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_white, fill=False, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_white, scale=2, mono_space=False)
	elif type == "clearup":
		row = row - 1 
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)
	elif type == "cleardown":
		row = row + 1 
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)

def draw_run(row, type, text):
	if type == "running":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_orange, fill=True, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, color=color_white, scale=2, mono_space=False)
	elif type == "failed":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_red, fill=True, thickness=1)
		splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, color=color_white, scale=2, mono_space=False)

draw_nav('init')
draw_title_bar(0)

for i in range(0,6,1):
	draw_item(i, 'unselected', i)
draw_item(0, 'selected', 0)

draw_ok('released')


while True:

	gc_log()
	# print(str(gc.mem_free()/1000)+"kb")

	key_state_left = key_gpio_left.value()
	key_state_right = key_gpio_right.value()
	key_state_down = key_gpio_down.value()


	"""
	██   ██ ███████ ██    ██      █████  
	██  ██  ██       ██  ██      ██   ██ 
	█████   █████     ████       ███████ 
	██  ██  ██         ██        ██   ██ 
	██   ██ ███████    ██        ██   ██ 

	"""

	if (key_state_left == 1 and ksl == 0):
		MENU_CURRENT_SELECT -= 1
		if MENU_CURRENT_SELECT <= 0: MENU_CURRENT_SELECT = 0

		# draw_item(MENU_CURRENT_SELECT)
		draw_nav('left')
		draw_title_bar(MENU_CURRENT_SELECT)

		if (MENU_CURRENT_SELECT % 6 > 0) and (MENU_CURRENT_SELECT % 6 < 5): 
			draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
			draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
		elif (MENU_CURRENT_SELECT % 6 == 0): 
			draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
			draw_item(5, "unselected", MENU_CURRENT_SELECT+5)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
		elif (MENU_CURRENT_SELECT % 6 >= 5): 
			draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
			draw_item(0, "unselected", MENU_CURRENT_SELECT-5)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

		if ((MENU_CURRENT_SELECT % 6) == 0) and (MENU_CURRENT_SELECT != 0):
			MENU_PAGE_SWAP_COUNT -= 1 

		if ((MENU_CURRENT_SELECT % 6) == 5) and (MENU_CURRENT_SELECT != 0):
			for i in range(MENU_CURRENT_SELECT-5,MENU_CURRENT_SELECT+1,1):
				print(str(MENU_CURRENT_SELECT-5)+","+str(MENU_CURRENT_SELECT))
				draw_item(i % 6, 'unselected', i)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

		print("Key B Pressed, Current Selection: " + str(MENU_CURRENT_SELECT) + ", \t"+ str(MENU_CURRENT_SELECT % 6) + ", "+ str(MENU_PAGE_SWAP_COUNT) + ", "+ str(MENU_PAGES_TOTAL))

		ksl = 1
	elif (key_state_left == 0 and ksl == 1): 
		draw_nav('init')
		ksl = 0





	'''
	██   ██ ███████ ██    ██     ██████  
	██  ██  ██       ██  ██      ██   ██ 
	█████   █████     ████       ██████  
	██  ██  ██         ██        ██   ██ 
	██   ██ ███████    ██        ██████  
	                                     
	'''
	if (key_state_right == 1 and ksr == 0):
		MENU_CURRENT_SELECT += 1
		if MENU_CURRENT_SELECT >= MENU_TOTAL_ITEMS: MENU_CURRENT_SELECT = MENU_TOTAL_ITEMS
		# draw_item(MENU_CURRENT_SELECT)
		draw_nav('right')
		draw_title_bar(MENU_CURRENT_SELECT)

		if (MENU_CURRENT_SELECT % 6 > 0) and (MENU_CURRENT_SELECT % 6 < 5): 
			draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
			draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
		elif (MENU_CURRENT_SELECT % 6 == 0): 
			draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
			draw_item(5, "unselected", MENU_CURRENT_SELECT+5)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
		elif (MENU_CURRENT_SELECT % 6 >= 5): 
			draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
			draw_item(0, "unselected", MENU_CURRENT_SELECT-5)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

		if ((MENU_CURRENT_SELECT % 6) == 0) and (MENU_CURRENT_SELECT != 0):
			MENU_PAGE_SWAP_COUNT += 1 
			for i in range(MENU_CURRENT_SELECT,MENU_CURRENT_SELECT+6,1):
				print(str(MENU_CURRENT_SELECT)+","+str(MENU_CURRENT_SELECT+6))
				draw_item(i % 6, 'unselected', i)
			draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

		print("Key B Pressed, Current Selection: " + str(MENU_CURRENT_SELECT) + ", \t"+ str(MENU_CURRENT_SELECT % 6) + ", "+ str(MENU_PAGE_SWAP_COUNT) + ", "+ str(MENU_PAGES_TOTAL))

		ksr = 1
	elif (key_state_right == 0 and ksr == 1): 
		draw_nav('init')
		ksr = 0






	'''
	██   ██ ███████ ██    ██      ██████ 
	██  ██  ██       ██  ██      ██      
	█████   █████     ████       ██      
	██  ██  ██         ██        ██      
	██   ██ ███████    ██         ██████ 
	                                     
	'''
	if (key_state_down == 1 and ksd == 0):
		try:
			draw_ok('pressed')
			draw_run(MENU_CURRENT_SELECT % 6, "running", "Running Demo...")
			lcd.display(splash, oft=(0,0))
			print("Running: " + MENU_ITEMS[MENU_CURRENT_SELECT][2])
			time.sleep(1)

			exec(open(MENU_ITEMS[MENU_CURRENT_SELECT][2]).read())

		except BaseException as e:
			print(str(e))
			import machine
			machine.reset()
			draw_run(MENU_CURRENT_SELECT % 6, "failed", "Failed: " + str(e))


		print("Key C Pressed.")
		ksd = 1
	elif (key_state_down == 0 and ksd == 1): 
		draw_ok('released')
		ksd = 0 



	lcd.display(splash, oft=(0,0))
	