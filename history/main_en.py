from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time, sys
from Maix import FPIOA, GPIO

try:
    from cocorobo import firmware_info
except BaseException as e:
    print(str(e))
    pass

gc.enable()
gc.collect()

count = 0

def gc_log():
    global count
    gc.collect()
    count = count + 1
    # print(str(count) + ":" +str(gc.mem_free()/1000)+"kb")

ai_flash_freespace = (os.statvfs("/flash")[0]*os.statvfs("/flash")[3])/(1024*1024)
# ai_sd_freespace = (os.statvfs("/sd")[0]*os.statvfs("/sd")[3])/(1024*1024)

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

time.sleep(1)

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)

ksl,ksr,ksd = 0, 0, 0

def main_program():
    global key_state_left, key_gpio_right, key_state_down, current_selection, ksl, ksr, ksd
    gc_log()

    key_state_left = key_gpio_left.value()
    key_state_right = key_gpio_right.value()
    key_state_down = key_gpio_down.value()

    if (key_state_left == 1 and ksl == 0):
        current_selection = current_selection - 1
        if current_selection == 0: current_selection = 2
        # print(str(current_selection))

        if current_selection == 1:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            splash.draw_string(btn_col[0]+10, btn_row+6, main_title[0], color=txt_selected, scale=2, mono_space=False)
            splash.draw_string(btn_col[0]+10, btn_row+26, main_title[1], color=txt_selected, scale=2, mono_space=False)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            splash.draw_string(btn_col[1]+10, btn_row+6, main_title[2], color=txt_unselected, scale=2, mono_space=False)
            splash.draw_string(btn_col[1]+10, btn_row+26, main_title[3], color=txt_unselected, scale=2, mono_space=False)
        elif current_selection == 2:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            splash.draw_string(btn_col[0]+10, btn_row+6, main_title[0], color=txt_unselected, scale=2, mono_space=False)
            splash.draw_string(btn_col[0]+10, btn_row+26, main_title[1], color=txt_unselected, scale=2, mono_space=False)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            splash.draw_string(btn_col[1]+10, btn_row+6, main_title[2], color=txt_selected, scale=2, mono_space=False)
            splash.draw_string(btn_col[1]+10, btn_row+26, main_title[3], color=txt_selected, scale=2, mono_space=False)

        ksl = 1
    elif (key_state_left == 0 and ksl == 1):
        ksl = 0


    if (key_state_right == 1 and ksr == 0):
        current_selection = current_selection + 1
        if current_selection > 2: current_selection = 1
        # print(str(current_selection))

        if current_selection == 1:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            splash.draw_string(btn_col[0]+10, btn_row+6, main_title[0], color=txt_selected, scale=2, mono_space=False)
            splash.draw_string(btn_col[0]+10, btn_row+26, main_title[1], color=txt_selected, scale=2, mono_space=False)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            splash.draw_string(btn_col[1]+10, btn_row+6, main_title[2], color=txt_unselected, scale=2, mono_space=False)
            splash.draw_string(btn_col[1]+10, btn_row+26, main_title[3], color=txt_unselected, scale=2, mono_space=False)
        elif current_selection == 2:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            splash.draw_string(btn_col[0]+10, btn_row+6, main_title[0], color=txt_unselected, scale=2, mono_space=False)
            splash.draw_string(btn_col[0]+10, btn_row+26, main_title[1], color=txt_unselected, scale=2, mono_space=False)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            splash.draw_string(btn_col[1]+10, btn_row+6, main_title[2], color=txt_selected, scale=2, mono_space=False)
            splash.draw_string(btn_col[1]+10, btn_row+26, main_title[3], color=txt_selected, scale=2, mono_space=False)

        ksr = 1
    elif (key_state_right == 0 and ksr == 1):
        ksr = 0


    if (key_state_down == 1 and ksd == 0):
        if current_selection == 1: 
            try:
                print("executing lastest code")
                splash.draw_rectangle(btn_col[0], btn_row-22,210,12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_string(btn_col[0], btn_row-22, "Running your latest uploaded code...", color=txt_selected, scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))
                time.sleep(1)
                exec(open("user_latest_code.py").read())
            except BaseException as e:
                splash.draw_rectangle(btn_col[0], btn_row-22, 210, 12, color=splash_theme_color, fill=True, thickness=1)
                if "ENOENT" in str(e):
                    splash.draw_string(btn_col[0], btn_row-22, "Failed to run, check if your file exists.", color=(255,0,0), scale=1.332, mono_space=False)
                else:
                    splash.draw_string(btn_col[0], btn_row-22, "Failed to run or code was interrupted.", color=(255,0,0), scale=1.332, mono_space=False)
                    splash.draw_string(btn_col[0], 30, str(e), color=(255,0,0), scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))
                print(str(e))
                time.sleep_ms(2000)

                splash.draw_rectangle(btn_col[0], 30,210, 12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_rectangle(btn_col[0], btn_row-22,210, 12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_string(btn_col[0], btn_row-22, "Left key to Move, Right key to Choose:", color=txt_selected, scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))
        if current_selection == 2: 
            try:
                splash.draw_rectangle(btn_col[0], btn_row-22,210,12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_string(btn_col[0], btn_row-22, "Opening Demo Menu...", color=txt_selected, scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))
                time.sleep(1)
                # __import__("try_demo")
                exec(open("/sd/language/try_demo-en.py").read())
            except BaseException as e:
                print(str(e))
                splash.draw_rectangle(btn_col[0], btn_row-22, 220, 12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_string(btn_col[0], btn_row-22, "Open failed, make sure you have preset file.", color=(255,0,0), scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))
                time.sleep_ms(2000)
                splash.draw_rectangle(btn_col[0], btn_row-22,220, 12, color=splash_theme_color, fill=True, thickness=1)
                splash.draw_string(btn_col[0], btn_row-22, "Left key to Move, Right key to Choose:", color=txt_selected, scale=1.332, mono_space=False)
                lcd.display(splash, oft=(0,0))

        print(str(current_selection) + " select")

        ksd = 1
    elif (key_state_down == 0 and ksd == 1):
        ksd = 0

    lcd.display(splash, oft=(0,0))


if key_gpio_left.value() == 1 and key_gpio_right.value() == 0:
    try:
        lcd.clear(lcd.BLACK)
        lcd.draw_string(10,10, "Entering test mode...", lcd.WHITE, lcd.BLACK)
        time.sleep(1)
        exec(open("/sd/device_test.py").read())
        gc_log()
    except BaseException as e:
        gc.collect()
        lcd.clear(lcd.BLACK)
        lcd.draw_string(10,10,str(e), lcd.RED, lcd.BLACK)
        sys.exit(0)
        gc_log()
else:
    with open("board_type.cfg", "w") as f:
        f.write("ai")
    btn_selected = (255,255,255)
    btn_unselected = (76,86,127)
    txt_selected = (255,255,255)
    txt_unselected = (76,86,127)

    # gc.threshold(800000)
    # print("before splash")
    gc_log()
    splash = image.Image(size=(240, 240))
    # splash = image.Image("/sd/preset/images/splash_bg.jpg")
    # print("after splash")
    splash_theme_color = (15,21,46)
    # del splash
    gc_log()

    splash.clear()
    splash.draw_rectangle(0,0,240,240,color=splash_theme_color,fill=True)
    # splash.draw_string(btn_col, 7, "", color=(255,255,255), scale=2, mono_space=False)

    btn_width = 114
    btn_height = 52

    btn_y_base = 6
    btn_col = (btn_y_base, btn_y_base+btn_width, btn_y_base+152)
    btn_row = 180

    main_title = (
        "Run",
        "Last",
        "Try",
        "Demos"
    )

    gc_log()

    try:
        os.listdir("/sd")
        # print("[CocoRobo] SD Card Successfully Initiated.")
    except BaseException as e:
        print(str(e))
        splash.draw_rectangle(0,0,240,240,color=(0,0,0), fill=True)
        # splash.draw_string(btn_col[0]+40, 70, b"Cannot Load", color=(200,0,0), scale=3, mono_space=False)
        # splash.draw_string(btn_col[0]+43, 100, b"The SD Card", color=(200,0,0), scale=3, mono_space=False)
        splash.draw_line(101,66,75,92,color=(200,0,0),thickness=4)
        splash.draw_line(75,92,75,174,color=(200,0,0),thickness=4)
        splash.draw_line(75,174,165,174,color=(200,0,0),thickness=4)
        splash.draw_line(165,174,165,66,color=(200,0,0),thickness=4)
        splash.draw_line(165,66,101,66,color=(200,0,0),thickness=4)
        splash.draw_string(btn_col[0]+108, 85, "?", color=(200,0,0), scale=7, mono_space=False)
        # display_cjk_string(splash, btn_col[0]+20, 70, "无法读取SD卡", font_size=2, color=(0,255,255), auto_wrap=False)
        lcd.display(splash, oft=(0,0))
        print("[CocoRobo] SD Card Initiate Failed. Please Reset Now")
        sys.exit(0)
        # machine.reset()

    try:
        title_logo_text = image.Image("/sd/preset/images/cocorobo_text.jpg")
        splash.draw_image(title_logo_text, btn_col[0]+3, 10)
    except:
        splash.draw_string(btn_col[0]+1, 7, "CocoRobo AI Module", color=(255,255,255), scale=2, mono_space=False)

    # splash.draw_rectangle(btn_col[0], 124, 180, 14, color=splash_theme_color, fill=True, thickness=1)
    # splash.draw_string(btn_col[0], 124, "Free Memory: " + str(gc.mem_free()/1000) + "KB", color=(0,255,255), scale=1.332, mono_space=False)

    try:
        splash.draw_string(btn_col[0], 141, "Firmware Version: " + str(firmware_info.ai()), color=(0,255,255), scale=1.332, mono_space=False)
        # print("[CocoRobo] Firmware Version: " + str(firmware_info.ai()))
    except BaseException as e:
        splash.draw_string(btn_col[0], 141, "Firmware Version: Not Available", color=(0,255,255), scale=1.332, mono_space=False)
        # print("[CocoRobo] Firmware Version: Not Available")
        pass

    splash.draw_string(btn_col[0], btn_row-22, "Key A & B to Move, Key C to Choose:", color=txt_selected, scale=1.332, mono_space=False)

    splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
    splash.draw_string(btn_col[0]+10, btn_row+6, main_title[0], color=txt_selected, scale=2, mono_space=False)
    splash.draw_string(btn_col[0]+10, btn_row+26, main_title[1], color=txt_selected, scale=2, mono_space=False)

    splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
    splash.draw_string(btn_col[1]+10, btn_row+6, main_title[2], color=txt_unselected, scale=2, mono_space=False)
    splash.draw_string(btn_col[1]+10, btn_row+26, main_title[3], color=txt_unselected, scale=2, mono_space=False)

    lcd.display(splash, oft=(0,0))

    current_selection = 1

    # _thread.start_new_thread(main_program,()) 
    try:
        pass
        # main_program()
    except KeyboardInterrupt:
        print("exit")

gc_log()

while True:
    main_program()