import os, Maix, lcd, image, sensor, gc, time, math
from Maix import FPIOA, GPIO
from fpioa_manager import *
from cocorobo import display_cjk_string

gc.enable()

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
	"basics": (33, 3, 174, 30, 41, 8, '基础', "/sd/preset/images/icon_basics.jpg"),
	"vision": (33, 3, 174, 30, 41, 8, '视觉', "/sd/preset/images/icon_vision.jpg"),
	"ml": (33, 3, 174, 30, 41, 10, '人工智能', "/sd/preset/images/icon_ml.jpg"),
	"audiovideo": (33, 3, 174, 30, 41, 8, '多媒体       ', "/sd/preset/images/icon_av.jpg")
}

MENU_ITEM_PARENT_PATH = "/sd/preset/demos/"

MENU_ITEMS = [
	# Basics
	("迷你照相机", CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_mini_camera" + ".py"), 
	("相机照片浏览器",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_camera_shot_browser" + ".py"), 
	("按键控制时针转动",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_rotate_clock" + ".py"), 
	("按键控制颜色变化",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_switch_color" + ".py"), 
	("简易线条动画",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_lcd_drawing_demo" + ".py"), 
	("按键随机生成蒙德里安  ",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_generative_mondrian" + ".py"), 
	("按键控制屏幕转动",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_screen_rotation" + ".py"), 
	("按键控制图片尺寸调整   ",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_button_resize" + ".py"), 
	("汉字文字显示",CATEGORY_ITEMS_DICT["basics"], MENU_ITEM_PARENT_PATH + "demo_cjk-test" + ".py"), 
	# Machine Learning
	("图片数据采集器", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_training_set_collector" + ".py"), 
	("人脸追踪",  CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_face_recognition" + ".py"), 
	("物体追踪", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_object_recognition" + ".py"), 
	("可可标志识别", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_coco_logo_recognition" + ".py"), 
	("手写数字识别  ", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_handwritten_digit_recognition" + ".py"), 
	("自定义垃圾分类识别", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_hongkong_trash_classification" + ".py"), 
	# ("HK Road Sign Recognition", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_hongkong_trash_classification" + ".py"), 
	("人脸辨识", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_face-compare" + ".py"), 
	("物体分类器", CATEGORY_ITEMS_DICT["ml"], MENU_ITEM_PARENT_PATH + "demo_object-classifier" + ".py"), 
	# Machine Vision
	("双线监测", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_double_line_detection" + ".py"), 
	("单线监测", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_single_line_detection" + ".py"), 
	("区域颜色分析   ", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_reginal_color_analyze" + ".py"), 
	("自动学习并追踪", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_learn_track_color" + ".py"), 
	("寻找绿色的物体", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_color_green" + ".py"),
	("寻找圆圈", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_circle" + ".py"),
	("寻找矩形", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_rectangle" + ".py"),
	("寻找线条", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_lines" + ".py"),
	("寻找二维码并解码  ", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_find_qr_code_2" + ".py"),
	# Audio & Video
	("音乐频谱分析", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_spectrum_analyze" + ".py"), 
	("播放音乐文件", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_play_music" + ".py"), 
	("语音识别（录制）", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_speech_record" + ".py"),
	("语音识别（运行）", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_speech_recognition" + ".py")
	# ("Record Camera to Video", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_camera_record" + ".py"), 
	# ("Play Recorded Video", CATEGORY_ITEMS_DICT["audiovideo"], MENU_ITEM_PARENT_PATH + "demo_play_recorded_video" + ".py")
]

BASE_COORD = [3, 33, 3+6, 33+5]
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
		splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=color_blue,thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[6][0]+8,MENU_ITEM_COORD[6][1]+6,"RUN", mono_space=False,color=color_splash_theme,scale=2)
		display_cjk_string(splash,MENU_ITEM_COORD[6][0]+8,MENU_ITEM_COORD[6][1]+6, "运行     ", font_size=1, color=txt_selected, auto_wrap=False)
	elif type == "pressed":
		splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=(26,81,143),thickness=1)
		display_cjk_string(splash,MENU_ITEM_COORD[6][0]+8,MENU_ITEM_COORD[6][1]+6, "运行     ", font_size=1, color=color_splash_theme, auto_wrap=False)

def draw_title_bar(index):
	splash.draw_rectangle(MENU_ITEMS[index][1][0],MENU_ITEMS[index][1][1],MENU_ITEMS[index][1][2],MENU_ITEMS[index][1][3], color=color_blue, fill=True)
	
	# splash.draw_string(MENU_ITEMS[index][1][4],MENU_ITEMS[index][1][5],MENU_ITEMS[index][1][6],color=color_white,mono_space=False,scale=2)
	display_cjk_string(splash,MENU_ITEMS[index][1][4]+2,MENU_ITEMS[index][1][5], MENU_ITEMS[index][1][6], font_size=1, color=color_white, auto_wrap=False)

	display_cjk_string(splash,200,215, str(index) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_splash_theme, auto_wrap=False, mono_space=False)
	display_cjk_string(splash,200,215, str(index+2) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_splash_theme, auto_wrap=False, mono_space=False)
	display_cjk_string(splash,200,215, str(index+1) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_white, auto_wrap=False, mono_space=False)

	# splash.draw_string(190,213,str(index) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_splash_theme,mono_space=False,scale=2)
	# splash.draw_string(190,213,str(index+2) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_splash_theme,mono_space=False,scale=2)
	# splash.draw_string(190,213,str(index+1) + "/" + str(MENU_TOTAL_ITEMS+1),color=color_white,mono_space=False,scale=2)

def draw_item(row, type, realindex):
	if type == "unselected":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], font_size=1, color=color_gray, auto_wrap=False)
	elif type == "selected":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_white, fill=False, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_white, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], font_size=1, color=color_white, auto_wrap=False)
	elif type == "clearup":
		row = row - 1 
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], font_size=1, color=color_gray, auto_wrap=False)
	elif type == "cleardown":
		row = row + 1 
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
		splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], color=color_gray, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], MENU_ITEMS[realindex][0], font_size=1, color=color_gray, auto_wrap=False)

def draw_run(row, type, text):
	if type == "running":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_orange, fill=True, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, color=color_white, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, font_size=1, color=color_white, auto_wrap=False)
	elif type == "failed":
		splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_red, fill=True, thickness=1)
		# splash.draw_string(MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, color=color_white, scale=2, mono_space=False)
		display_cjk_string(splash,MENU_ITEM_COORD[row][2], MENU_ITEM_COORD[row][3], text, font_size=1, color=color_white, auto_wrap=False)

draw_nav('init')
draw_title_bar(0)

for i in range(0,6,1):
	draw_item(i, 'unselected', i)
draw_item(0, 'selected', 0)

draw_ok('released')


while True:

	gc.collect()
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
			draw_run(MENU_CURRENT_SELECT % 6, "running", "运行程序中…")
			lcd.display(splash, oft=(0,0))
			print("Running: " + MENU_ITEMS[MENU_CURRENT_SELECT][2])
			time.sleep(1)

			exec(open(MENU_ITEMS[MENU_CURRENT_SELECT][2]).read())

		except BaseException as e:
			print(str(e))
			import machine
			machine.reset()
			draw_run(MENU_CURRENT_SELECT % 6, "failed", "运行失败" + str(e))


		print("Key C Pressed.")
		ksd = 1
	elif (key_state_down == 0 and ksd == 1): 
		draw_ok('released')
		ksd = 0 



	lcd.display(splash, oft=(0,0))
	