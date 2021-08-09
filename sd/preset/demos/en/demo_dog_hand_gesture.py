print("Clearing Cached Variables...", end="")
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
print(" Done")
import KPU as kpu
kpu.memtest()
from Maix import utils
import gc
gc.enable()
utils.gc_heap_size()

################# Done Init #################

import time

import machine, time
from fpioa_manager import fm

import lcd
import image
import sensor
import time
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

import KPU as kpu
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

_camera_x, _camera_y = 0, 0

task_customized_model = kpu.load("/sd/preset/models/hand/us-hand-signs-20210707162548GO_last.kmodel")
anchor_customized_model = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
a = kpu.init_yolo2(task_customized_model, 0.6, 0.3, 5, anchor_customized_model)

classes_customized_model = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.skip_frames(30)
sensor.run(1)
sensor.set_hmirror(True)
sensor.set_windowing((224,224))
_timer_tim.start()
old_time = _timer_current_time_elapsed
while True:
    camera = sensor.snapshot()
    if (_timer_current_time_elapsed) - old_time >= 100:
        code_customized_model = kpu.run_yolo2(task_customized_model, camera)
        if code_customized_model:
            for i in (code_customized_model):
                camera.draw_rectangle((i.x()),(i.y()), (i.w()), (i.h()), color=(51,102,255), thickness=2, fill=False)
                camera.draw_rectangle((i.x()),(i.y()), (i.w()), 25, color=(51,102,255), thickness=2, fill=True)
                dstr = classes_customized_model[i.classid()]
                if dstr == "A" or dstr == "E" or dstr == "S" or dstr == "M" or dstr == "O" or dstr == "T":
                    action = "fist"
                elif dstr == "B":
                    action = "stop"
                elif dstr == "V":
                    action = "victory"
                elif dstr == "Y":
                    action = "six"
                elif dstr == "F":
                    action = "ok"
                else:
                    action = dstr
                lcd_draw_string(camera,(i.x()),(i.y()), action, color=(255,255,255), scale=1, mono_space=False)
            _camera_x, _camera_y = 8, 8
            lcd.display(camera, oft=(_camera_x,_camera_y))
            if len(code_customized_model) == 1:
                if action == "fist":
                    robot_dog_setup_uart.write(bytes([54]))
                    time.sleep_ms(20)
                    time.sleep_ms(3000)
                elif action == "stop":
                    robot_dog_setup_uart.write(bytes([51]))
                    time.sleep_ms(20)
                    time.sleep_ms(3000)
                elif action == "victory":
                    robot_dog_setup_uart.write(bytes([60]))
                    time.sleep_ms(20)
                    time.sleep_ms(3000)
                elif action == "six":
                    robot_dog_setup_uart.write(bytes([65]))
                    time.sleep_ms(20)
                    time.sleep_ms(3000)
                elif action == "ok":
                    robot_dog_setup_uart.write(bytes([62]))
                    time.sleep_ms(20)
                    time.sleep_ms(3000)
            _timer_tim.start()
            old_time = _timer_current_time_elapsed
    _camera_x, _camera_y = 8, 8
    lcd.display(camera, oft=(_camera_x,_camera_y))
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                machine.reset()

action = "three"
