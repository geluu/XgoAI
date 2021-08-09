import os, json, time, utime, struct
from Maix import I2S, GPIO
from modules import SpeechRecognizer
from fpioa_manager import *
fm.register(31, fm.fpioa.GPIO3)
fm.register(32, fm.fpioa.GPIO4)

_led_red = GPIO(GPIO.GPIO3, GPIO.OUT)
_led_blue = GPIO(GPIO.GPIO4, GPIO.OUT)

def _sr_data_save(s,content,keyword_num, model_num, path):
    data = _s_daemon.get_model_data(keyword_num, model_num)
    with open(path,'w') as f:
        f.write(data)

def _sr_data_load(s, keyword_num, model_num,frame_num, path):
    print(path)
    with open(path,'r') as f:
        data = f.read()
        _s_daemon.add_voice_model(keyword_num, model_num, frame_num, data)

def _sr_init_remove_old_recording():
    global _voice_record
    try:
        for i in os.listdir("/sd/sr"):
            print("deleting " + str(i) + "...")
            os.remove("/sd/sr/"+str(i))
        print("file deleting done.")
        os.rmdir("/sd/sr")
        print("directory deleting done.")
        os.mkdir("/sd/sr")
        print("directory creating done.")
    except:
        os.mkdir("/sd/sr")
        print("directory creating done.")
    _voice_record = True

# Enable Microphone and Disable Wifi Feature
fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18, fm.fpioa.I2S0_SCLK, force=True)
fm.register(19, fm.fpioa.I2S0_WS, force=True)
fm.register(8, fm.fpioa.GPIO5, force=True)
wifi_en=GPIO(GPIO.GPIO5,GPIO.OUT)
wifi_en.value(0)

# Init recording device parameteres
sample_rate = 8000
i2s_dev = I2S(I2S.DEVICE_0)
# config i2s according to speechrecognizer
i2s_dev.channel_config(i2s_dev.CHANNEL_0,I2S.RECEIVER,resolution = I2S.RESOLUTION_16_BIT,cycles = I2S.SCLK_CYCLES_32,align_mode = I2S.STANDARD_MODE)
i2s_dev.set_sample_rate(sample_rate)
_s_daemon = SpeechRecognizer(i2s_dev)
_s_daemon.set_threshold(0,0,20000)



# Remove old recordings
_sr_init_remove_old_recording()

import lcd
import image
try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

_canvas_x, _canvas_y = 0, 0
lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
canvas.clear()
canvas.draw_rectangle(0,0, 240, 240, color=(0,0,0), thickness=1, fill=True)
lcd_draw_string(canvas, 85,0, "press A", color=(255,255,255), scale=2, mono_space=False)

_voice_keyword_num = 6
_voice_model_num = 3
for k in range(_voice_keyword_num):
    lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
    for l in range(_voice_model_num):
        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

lcd.display(canvas, oft=(_canvas_x,_canvas_y))

from fpioa_manager import *
from Maix import FPIOA, GPIO
import time
from machine import Timer

_gp_side_buttons = [9, 10, 11]
FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_voice_button_status = False

def _on_read_voice_recog_button_timer(timer):
    global _voice_button_status
    if _gp_side_a.value() == True: _voice_button_status = True
    elif _gp_side_a.value() == False: _voice_button_status = False

_on_read_voice_recog_periodic_tim = Timer(Timer.TIMER2, Timer.CHANNEL2, mode=Timer.MODE_PERIODIC, period=1, callback=_on_read_voice_recog_button_timer, arg=_on_read_voice_recog_button_timer)
_on_read_voice_recog_periodic_tim.start()

try:
    while _voice_record == True:

        for i in range(_voice_keyword_num):
            for j in range(_voice_model_num):
                print("Press the button to record the {} keyword, the {}".format(i+1, j+1))

                while True:
                    if _voice_button_status == True:
                        break
                    else:
                        print(".", end="")
                        _led_red.value(1)
                        time.sleep_ms(100)
                        _led_red.value(0)
                        time.sleep_ms(100)

                # Start recoding procedure
                _led_red.value(0)
                _s_daemon.record(i, j)
                time.sleep_ms(500)

                # Check recording state
                while (_s_daemon.get_status() != 2):
                    if (_s_daemon.get_status() == 1):
                        print("[CocoRobo] 现在开始说!")
                        _led_red.value(1)
                        _led_blue.value(1)
                        canvas.clear()
                        lcd_draw_string(canvas, 65,0, "Speak Now", color=(255,0,0), scale=2, mono_space=False)

                    if (_s_daemon.get_status() == 5):
                        print("[CocoRobo] 收集噪音...")
                        _led_red.value(1)
                        canvas.clear()
                        lcd_draw_string(canvas, 45,0, "Gathering Noise...", color=(255,0,0), scale=2, mono_space=False)

                    if i == 0:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 1:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 2:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 3:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 1:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 2:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 3:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 4:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    else:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
                    time.sleep_ms(500)
                if (_s_daemon.get_status() == 2):
                    canvas.clear()
                    lcd_draw_string(canvas, 95,0, "OK", color=(10,255,0), scale=2, mono_space=False)

                    if i == 0:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 1:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 2:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 3:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 4:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 1:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 2:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 3:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 4:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4  or (k == 4 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    else:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
                    for t in range(0,6,1):
                        _led_blue.value(1)
                        _led_red.value(1)
                        time.sleep_ms(100)
                        _led_blue.value(0)
                        _led_red.value(0)
                        time.sleep_ms(100)
                    time.sleep(1)

                    canvas.clear()
                    lcd_draw_string(canvas, 85,0, "press A", color=(255,255,255), scale=2, mono_space=False)

                    if i == 0:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 1:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 2:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 3:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k == 0 and l < 4:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 1:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 1 or (k == 1 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 2:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 2 or (k == 2 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 3:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 3 or (k == 3 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    elif i == 4:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4  or (k == 4 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 4 or (k == 4 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    else:
                        if j == 0:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 1):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 1:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 2):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        elif j == 2:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 3):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)
                        else:
                            for k in range(_voice_keyword_num):
                                lcd_draw_string(canvas, 30,30 + (k % _voice_keyword_num) * 35, str(k+1), color=(255,255,255), scale=2, mono_space=False)
                                for l in range(_voice_model_num):
                                    if k < 5 or (k == 5 and l < 4):
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=True)
                                    else:
                                        canvas.draw_rectangle(70 + (l % _voice_model_num) * 35,30 + (k % _voice_keyword_num) * 35, 25, 25, color=(255,255,255), thickness=3, fill=False)

                    lcd.display(canvas, oft=(_canvas_x,_canvas_y))

                # Done Recording
                content = str(i) + '_' + str(j)
                file_name = "/sd/sr/" + str(i) + '_' + str(j)+"_" + str(_s_daemon.get_model_info(i,j)).strip("[]") +".sr"
                _sr_data_save(_s_daemon, content, i, j, file_name)
                print("frm_num is: " + str(_s_daemon.get_model_info(i,j)))

        print("Record successful! Next, Run your speech recognition code!")
        _voice_record = False

        canvas.clear()
        canvas.draw_image(image.Image("/sd/preset/images/tick.jpg"), 70,70,  x_scale=0.5,  y_scale=0.5)
        lcd.display(canvas, oft=(_canvas_x,_canvas_y))
        _led_blue.value(1)
        _led_red.value(0)
        time.sleep(2)
except BaseException as e:
    print(str(e))
    canvas.clear()
    lcd_draw_string(canvas,30,40, "Voice Sample", color=(255,0,0), scale=1, mono_space=False)
    lcd_draw_string(canvas,30,70, "Recording", color=(255,0,0), scale=1, mono_space=False)
    lcd_draw_string(canvas,30,100, "Failed!", color=(255,0,0), scale=1, mono_space=False)
    lcd_draw_string(canvas,30,140, "Reason: " + str(e), color=(255,0,0), scale=1, mono_space=False)
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    _led_blue.value(0)
    _led_red.value(1)

import machine
machine.reset()
