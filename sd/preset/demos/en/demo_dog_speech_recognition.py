import time

import machine, time
from fpioa_manager import fm

import lcd
import image
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

import time
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

import time

_voice_recording_load = True
_voice_recording_ready = False

if _voice_recording_load == True:
    _sr_filelist = os.listdir("/sd/sr")
    for _sr_file in _sr_filelist:
        _sr_frm_num = int(_sr_file[4:_sr_file.find(".")])
        print(_sr_frm_num)
        print("/sd/sr/" + str(_sr_file))
        _sr_data_load(_s_daemon, int(_sr_file[0]), int(_sr_file[2]), _sr_frm_num, "/sd/sr/" + str(_sr_file))
    print("load successful!")

from fpioa_manager import *
from Maix import FPIOA, GPIO

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)

import machine

fm.register(13,fm.fpioa.UART2_TX)
fm.register(14,fm.fpioa.UART2_RX)
robot_dog_setup_uart = machine.UART(machine.UART.UART2,115200,bits=8,parity=None,stop=1)

def add(a,b):
    num1 = a ^ b
    num2 = (a & b) << 1
    while num2 != 0:
        temp  = num1 ^ num2
        num2 = (num1 & num2) << 1
        num1 = temp
    return num1

def calculate_sum(a,b):
    bytearr = [9, 1, a, b]
    sum = 0
    for i in bytearr:
        sum = add(sum,i)
    calculated_cksum = bin(sum).replace("0b","")
    while len(calculated_cksum) < 8:
        calculated_cksum = "0" + calculated_cksum
    ReturningChecksum = ""
    for index in range(len(calculated_cksum)):
        if calculated_cksum[index] == "1":
            ReturningChecksum += "0"
        elif calculated_cksum[index] == "0":
            ReturningChecksum += "1"
    return bytes([int(hex(int(ReturningChecksum,2)),16)])

def mapping(input_value,i_min,i_max,o_min,o_max):
    if input_value < i_min:
        input_value = i_min
    if input_value > i_max:
        input_value = i_max
    dat=(input_value-i_min)/(i_max-i_min)*(o_max-o_min)+o_min
    return int(dat)

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

_canvas_x, _canvas_y = 0, 0



robot_dog_setup_uart.write(bytes([0]))
time.sleep_ms(20)
lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
canvas.clear()
_timer_tim.start()
while True:
    speech = 0
    _s_recognition_state = 0
    _s_daemon.recognize()
    time.sleep_ms(500)

    canvas.clear()
    lcd_draw_string(canvas,0,90, "Say something", color=(192,192,192), scale=2, mono_space=False)
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    while _s_recognition_state == 0:
        if _gp_side_c.value() == 1:
            C_time = _timer_current_time_elapsed
            while _gp_side_c.value() == 1:
                time.sleep_ms(1)
                if (_timer_current_time_elapsed) - C_time >= 500:
                    robot_dog_setup_uart.write(bytes([0]))
                    time.sleep_ms(20)
                    machine.reset()
        if (_s_daemon.get_status() == 5):
            print("", end="")
        elif (_s_daemon.get_status() == 3):
            print("", end="")
        elif (_s_daemon.get_status() == 4):
            print("[CocoRobo] Record OK, Proceed!")
            _s_recognition_state = 1
        else:
            print("[CocoRobo] Current state: " + str(_s_daemon.get_status()))

    time.sleep_ms(800)
    _s_ret = _s_daemon.get_result()
    print("[CocoRobo] Result: " + str(_s_ret))

    if (_s_ret > 0):
        robot_dog_setup_uart.write(bytes([0]))
        time.sleep_ms(20)
        if (_s_ret == 1):
            speech = "Eat"
            robot_dog_setup_uart.write(bytes([68]))
            time.sleep_ms(20)
        elif (_s_ret == 2):
            speech = "Hand"
            robot_dog_setup_uart.write(bytes([69]))
            time.sleep_ms(20)
        elif (_s_ret == 3):
            speech = "Turn"
            robot_dog_setup_uart.write(bytes([54]))
            time.sleep_ms(20)
        elif (_s_ret == 4):
            speech = "Down"
            robot_dog_setup_uart.write(bytes([51]))
            time.sleep_ms(20)
        elif (_s_ret == 5):
            speech = "Sit"
            robot_dog_setup_uart.write(bytes([62]))
            time.sleep_ms(20)
        elif (_s_ret == 6):
            speech = "Bye"
            robot_dog_setup_uart.write(bytes([63]))
            time.sleep_ms(20)
        canvas.clear()
        lcd_draw_string(canvas,70,90, speech, color=(255,255,255), scale=3, mono_space=False)
        lcd.display(canvas, oft=(_canvas_x,_canvas_y))
        time.sleep_ms(3000)

