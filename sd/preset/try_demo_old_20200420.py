import os, Maix, lcd, image, sensor, gc, time
from Maix import FPIOA, GPIO
from fpioa_manager import *

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

splash = image.Image("/sd/preset/images/splash_bg.jpg")
splash_theme_color = (15,21,46)
splash.clear()
splash.draw_rectangle(0,0,240,240,color=splash_theme_color,fill=True)

btn_selected = (255,255,255)
btn_unselected = (76,86,127)
txt_selected = (255,255,255)
txt_unselected = (76,86,127)

btn_width = 228
btn_height = 30
btn_col_base = 6
btn_row_base = 30

item_title = [
	"Mini Camera", 
	"Camera Shot Browser", 
	"Training Set Collector", 
	"Face Recognition", 
	"Object Recognition",
	"Animal Recognition",
	"Coco Logo Recognition",
	"Digit Recognition",
	"Double Line Detection",
	"Single Line Detection",
	"Regional Color Analyze",
	"Learn & Track Color",
	"Find Color Green Object",
	"Find QR Code and Decode"
]

demo_path = "/preset/demos/"
item_code = [
	"demo_mini_camera",
	"demo_camera_shot_browser", 
	"demo_training_set_collector",
	"demo_face_recognition",
	"demo_object_recognition",
	"demo_animal_recognition",
	"demo_coco_logo_recognition",
	"demo_handwritten_digit_recognition",
	"demo_double_line_detection",
	"demo_single_line_detection",
	"demo_reginal_color_analyze",
	"demo_learn_track_color",
	"demo_find_color_green",
	"demo_find_qr_code"
]

HOW_MANY_ITEMS = len(item_title)
btn_row = [None] * HOW_MANY_ITEMS
btn_row[0] = btn_row_base

for i in range(1, HOW_MANY_ITEMS, 1):
	btn_row[i] = btn_row_base+29*i

current_item = 1
total_items = len(item_title)
menu_page_items_total = 7
page_count = 1

def clear_menu():
	splash.draw_rectangle(btn_col_base-5, btn_row[0],235,210,color=splash_theme_color,fill=True)

def draw_item(row, row_title, selection_state, extra_text="", customized_color=(255,69,0)):
	if selection_state == 0:
		# unselected
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=splash_theme_color, fill=True, thickness=1)
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
		splash.draw_string(btn_col_base+10, btn_row[row-1]+5, item_title[row_title-1], color=txt_unselected, scale=2, mono_space=False)
	elif selection_state == 1:
		# selected
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=splash_theme_color, fill=True, thickness=1)
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
		splash.draw_string(btn_col_base+10, btn_row[row-1]+5, item_title[row_title-1], color=txt_selected, scale=2, mono_space=False)
	elif selection_state == 2:
		# filled white
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=btn_selected, fill=True, thickness=1)
		splash.draw_string(btn_col_base+10, btn_row[row-1]+5, item_title[row_title-1], color=splash_theme_color, scale=2, mono_space=False)
	elif selection_state == 3:
		# loading text
		splash.draw_rectangle(btn_col_base, btn_row[row-1], btn_width, btn_height, color=customized_color, fill=True, thickness=1)
		splash.draw_string(btn_col_base+10, btn_row[row-1]+5, extra_text, color=(255,255,255), scale=2, mono_space=False)

def draw_page_count():
	splash.draw_rectangle(btn_col_base+191, btn_row[0]-22,60,20,color=splash_theme_color,fill=True)
	splash.draw_string(btn_col_base+191, btn_row[0]-22, "Page: "+str(page_count), color=(255,255,255), scale=1.332, mono_space=False)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

clear_menu()
splash.draw_string(btn_col_base, btn_row[0]-22, "Left Key: Move, Right Key: Select", color=(255,255,255), scale=1.332, mono_space=False)
draw_page_count()
for i in range(0,menu_page_items_total+1,1): draw_item(i ,i, 0)
draw_item(1 ,1, True)
lcd.display(splash, oft=(0,0))

while True:

	gc.collect()
	# print(str(gc.mem_free()/1000)+"kb")

	key_state_left = key_gpio_left.value()
	key_state_right = key_gpio_right.value()
	key_state_down = key_gpio_down.value()

	if (key_state_left == 1 and ksl == 0):
		'''Select things
		'''
		current_item = current_item - 1
		if current_item == 0: current_item = total_items

		item_top_check = (current_item) % menu_page_items_total
		if item_top_check == 0: item_top_check = 7

		if item_top_check == 1:
			page_count = page_count + 1
			test = int(total_items / menu_page_items_total)
			clear_menu()
			if (current_item % 7) != 1:
				for i in range(item_top_check-1,total_items % menu_page_items_total,1):
					add_up = int(translate(menu_page_items_total-i,6,0,0,6))
					draw_item(i+1, current_item+add_up+1, 0)
				draw_item(item_top_check,current_item, 1)
				draw_page_count()
			elif (current_item % 7) == 1:
				if page_count > (test): page_count = 1
				for i in range(item_top_check-1,menu_page_items_total,1):
					add_up = int(translate(menu_page_items_total-i,6,0,0,6))
					draw_item(i+1, current_item+add_up+1, 0)
				draw_item(item_top_check,current_item, 1)
				draw_page_count()
		else:
			draw_item(item_top_check+1,current_item+1, 0)
			draw_item(item_top_check,current_item, 1)

		
		print("Now in: "+str(current_item))
		if item_top_check == 1: print("clear and show next page")

		# if item_top_check == 5 or item_top_check == 1: print("first")

		ksl = 1
	elif (key_state_left == 0 and ksl == 1): ksl = 0





	if (key_state_right == 1 and ksr == 0):
		'''Select things
		'''
		current_item = current_item + 1
		if current_item > total_items: current_item = 1
		item_top_check = (current_item) % menu_page_items_total
		if item_top_check == 0: item_top_check = 7

		if item_top_check == 1:
			page_count = page_count + 1
			test = int(total_items / menu_page_items_total)
			clear_menu()
			if (current_item % 7) != 1:
				for i in range(item_top_check-1,total_items % menu_page_items_total,1):
					add_up = int(translate(menu_page_items_total-i,6,0,0,6))
					draw_item(i+1, current_item+add_up+1, 0)
				draw_item(item_top_check,current_item, 1)
				draw_page_count()
			elif (current_item % 7) == 1:
				if page_count > (test): page_count = 1
				for i in range(item_top_check-1,menu_page_items_total,1):
					add_up = int(translate(menu_page_items_total-i,6,0,0,6))
					draw_item(i+1, current_item+add_up+1, 0)
				draw_item(item_top_check,current_item, 1)
				draw_page_count()
		else:
			draw_item(item_top_check-1,current_item-1, 0)
			draw_item(item_top_check,current_item, 1)

		
		print("Now in: "+str(current_item))
		if item_top_check == 1: print("clear and show next page")

		# if item_top_check == 5 or item_top_check == 1: print("first")

		ksr = 1
	elif (key_state_right == 0 and ksr == 1): ksr = 0





	if (key_state_down == 1 and ksd == 0):
		'''Choose thing
		'''
		gc.collect()

		if current_item == 1:
			draw_item(current_item-1, current_item-1, 0)
			draw_item(current_item,current_item, 2)
		elif current_item != 1:
			# draw_item(item_top_check-1, current_item-1, 0)
			draw_item(item_top_check-1, current_item-1, 3, "Loading Demo...")
			draw_item(item_top_check, current_item, 2)
		lcd.display(splash, oft=(0,0))

		print("loading: " + demo_path+item_code[current_item-1] + "...")
		time.sleep(1)
		gc.collect()
		try:
			# __import__(demo_path+item_code[current_item-1])
			# __import__(demo_path+item_code[current_item-1])
			print("/sd"+demo_path+item_code[current_item-1]+".py")
			gc.collect()
			exec(open("/sd"+demo_path+item_code[current_item-1]+".py").read())
		except BaseException as e:
			# print(error)
			draw_item(item_top_check-1, current_item-1, 3, "Error Loading...", (255,0,0))
			print(str(e))


		print(str(current_item)+" selected.")

		ksd = 1
	elif (key_state_down == 0 and ksd == 1): ksd = 0 

	lcd.display(splash, oft=(0,0))
	