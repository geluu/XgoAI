from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time, sys
from Maix import FPIOA, GPIO

gc.enable()
gc.collect()

import lcd, image, time
from cocorobo import display_cjk_string


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

splash = image.Image(size=(240, 240))

splash_theme_color = (15,21,46)
splash_white = (255,255,255)
splash_gray = (100,100,100)

splash.draw_rectangle(0,0, 240,240, color=splash_theme_color,fill=True)


splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_gray,fill=False)
splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_gray,fill=False)
splash.draw_rectangle(5,5, 230, 77, color=splash_white,fill=False)

display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_white, auto_wrap=False)
display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_gray, auto_wrap=False)
display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_gray, auto_wrap=False, spacing=12, mono_space=False)

lcd.display(splash)

lang_list = ['Simplified Chinese', 'Traditional Chinese', 'English']

current_selection = 0

while True:    
    key_state_left = key_gpio_left.value()
    key_state_right = key_gpio_right.value()
    key_state_down = key_gpio_down.value()

    if (key_state_left == 1 and ksl == 0):
        current_selection -= 1
        if current_selection < 0: current_selection = 0

        if current_selection == 0:
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5, 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_white, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_gray, auto_wrap=False, spacing=12, mono_space=False)
        elif current_selection == 1:
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_white, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_gray, auto_wrap=False, spacing=12, mono_space=False)
        elif current_selection == 2:
            splash.draw_rectangle(5,5, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_white, auto_wrap=False, spacing=12, mono_space=False)

        ksl = 1
    elif (key_state_left == 0 and ksl == 1):
        ksl = 0


    if (key_state_right == 1 and ksr == 0):
        current_selection += 1
        if current_selection > 2: current_selection = 2

        if current_selection == 0:
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5, 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_white, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_gray, auto_wrap=False, spacing=12, mono_space=False)
        elif current_selection == 1:
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_white, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_gray, auto_wrap=False, spacing=12, mono_space=False)
        elif current_selection == 2:
            splash.draw_rectangle(5,5, 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_gray,fill=False)
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_white,fill=False)

            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_gray, auto_wrap=False)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_white, auto_wrap=False, spacing=12, mono_space=False)

        ksr = 1
    elif (key_state_right == 0 and ksr == 1):
        ksr = 0


    if (key_state_down == 1 and ksd == 0):
        print(lang_list[current_selection])

        if current_selection == 0:
            splash.draw_rectangle(5,5, 230, 77, color=splash_white,fill=True)
            display_cjk_string(splash, 68, 30, '简体中文', font_size=2, color=splash_theme_color, auto_wrap=False)
            lcd.display(splash)

            exec(open("/sd/language/main_cs.py").read())
        elif current_selection == 1:
            splash.draw_rectangle(5,5+(77-1), 230, 77, color=splash_white,fill=True)
            display_cjk_string(splash, 68, 105, '繁體中文', font_size=2, color=splash_theme_color, auto_wrap=False)
            lcd.display(splash)

            exec(open("/sd/language/main_ct.py").read())
        elif current_selection == 2:
            splash.draw_rectangle(5,5+(77-1)*2, 230, 77, color=splash_white,fill=True)
            display_cjk_string(splash, 74, 185, 'ENGLISH', font_size=2, color=splash_theme_color, auto_wrap=False, spacing=12, mono_space=False)
            lcd.display(splash)
            exec(open("/sd/language/main_en.py").read())

        ksd = 1
    elif (key_state_down == 0 and ksd == 1):
        ksd = 0

    lcd.display(splash)