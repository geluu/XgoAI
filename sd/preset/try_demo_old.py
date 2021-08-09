import os, Maix, lcd, image, sensor, gc, time
from Maix import FPIOA, GPIO
from fpioa_manager import *

buttonLeft, buttonRight = 0, 1

fpiol = FPIOA()
fpior = FPIOA()

fpiol.set_function(buttonLeft,FPIOA.GPIO0)
fpior.set_function(buttonRight,FPIOA.GPIO1)

key_gpio_left=GPIO(GPIO.GPIO0,GPIO.IN)
key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)

ksl,ksr = 0, 0

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(3)
lcd.clear(lcd.BLACK)

splash = image.Image("/sd/preset/images/splash_bg.jpg")
splash_theme_color = (15,21,46)
splash.clear()
splash.draw_rectangle(0,0,240,240,color=splash_theme_color,fill=True)

btn_width = 223
btn_height = 30
btn_col = 9

btn_row_base = 29
btn_row = ( 
	btn_row_base, 
	btn_row_base+29*1, 
	btn_row_base+29*2, 
	btn_row_base+29*3, 
	btn_row_base+29*4, 
	btn_row_base+29*5, 
	btn_row_base+29*6
)

btn_selected = (255,255,255)
btn_unselected = (76,86,127)
txt_selected = (255,255,255)
txt_unselected = (76,86,127)

item_title = (
	"Mini Camera", 
	"Training Set Collector", 
	"Face Recognition", 
	"Object Recognition",
	"Animal Recognition",
	"Coco Logo Recognition",
	"Digit Recognition"
)

item_code = (
	"/preset/demos/demo_mini_camera",
	"/preset/demos/demo_training_set_collector",
	"/preset/demos/demo_face_recognition",
	"/preset/demos/demo_object_recognition",
	"/preset/demos/demo_animal_recognition",
	"/preset/demos/demo_coco_logo_recognition",
	"/preset/demos/demo_handwritten_digit_recognition"
)

splash.draw_string(btn_col, btn_row[0]-22, "Left key to Move, Right key to Choose:", color=(255,255,255), scale=1.332, mono_space=False)

splash.draw_rectangle(btn_col, btn_row[1], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
splash.draw_rectangle(btn_col, btn_row[2], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
splash.draw_rectangle(btn_col, btn_row[3], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
splash.draw_rectangle(btn_col, btn_row[4], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
splash.draw_rectangle(btn_col, btn_row[5], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
splash.draw_rectangle(btn_col, btn_row[6], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)

splash.draw_rectangle(btn_col, btn_row[0], btn_width, btn_height, color=btn_selected, fill=False, thickness=1)

splash.draw_string(btn_col+10, btn_row[0]+5, item_title[0], color=txt_selected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[1]+5, item_title[1], color=txt_unselected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[2]+5, item_title[2], color=txt_unselected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[3]+5, item_title[3], color=txt_unselected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[4]+5, item_title[4], color=txt_unselected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[5]+5, item_title[5], color=txt_unselected, scale=2, mono_space=False)
splash.draw_string(btn_col+10, btn_row[6]+5, item_title[6], color=txt_unselected, scale=2, mono_space=False)

lcd.display(splash, oft=(0,0))

current_item = 1
total_items = len(item_title)

while True:

	key_state_left = key_gpio_left.value()
	key_state_right = key_gpio_right.value()

	if (key_state_left == 0 and ksl == 0):
		current_item = current_item + 1
		if current_item > total_items: current_item = 1

		splash.draw_rectangle(btn_col, btn_row[current_item-2], btn_width, btn_height, color=splash_theme_color, fill=True, thickness=1)
		splash.draw_rectangle(btn_col, btn_row[current_item-2], btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
		splash.draw_string(btn_col+10, btn_row[current_item-2]+5, item_title[current_item-2], color=txt_unselected, scale=2, mono_space=False)

		splash.draw_rectangle(btn_col, btn_row[current_item-1], btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
		splash.draw_string(btn_col+10, btn_row[current_item-1]+5, item_title[current_item-1], color=txt_selected, scale=2, mono_space=False)

		print("left: "+str(current_item))
		ksl = 1
	elif (key_state_left == 1 and ksl == 1):
		ksl = 0

	if (key_state_right == 0 and ksr == 0):
		gc.collect()

		print("right: " + str(current_item) + " choosed.")

		splash.draw_rectangle(btn_col, btn_row[current_item-1], btn_width, btn_height, color=(255,255,255), fill=True, thickness=1)
		splash.draw_string(btn_col+10, btn_row[current_item-1]+5, item_title[current_item-1], color=splash_theme_color, scale=2, mono_space=False)

		lcd.display(splash, oft=(0,0))

		time.sleep(1)
		__import__(item_code[current_item-1])

		ksr = 1
	elif (key_state_right == 1 and ksr == 1):
		ksr = 0

	lcd.display(splash, oft=(0,0))

	gc.collect()
	print(str(gc.mem_free()/1000))