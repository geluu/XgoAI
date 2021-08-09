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
import KPU as kpu
import time
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

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

_img_display_x, _img_display_y = 0, 0

task_customized_model = kpu.load("/sd/preset/models/hand/us-hand-signs-20210707162548GO_last.kmodel")
anchor_customized_model = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
a = kpu.init_yolo2(task_customized_model, 0.6, 0.3, 5, anchor_customized_model)

classes_customized_model = ["Object 1 Name"]



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
yaw = int(0)
pitch = int(0)
face_x = int(112)
face_y = int(112)
count = 0
while True:
    robot_dog_setup_uart.write(b'\x55\x00\x09\x01\x37' + bytes([pitch + 128]) + calculate_sum(ord(b'\x37'),pitch + 128) + b'\x00\xaa')
    time.sleep_ms(20)
    robot_dog_setup_uart.write(b'\x55\x00\x09\x01\x38' + bytes([yaw + 128]) + calculate_sum(ord(b'\x38'),yaw + 128) + b'\x00\xaa')
    time.sleep_ms(20)
    img_facerecognition = sensor.snapshot()
    code_customized_model = kpu.run_yolo2(task_customized_model, img_facerecognition)
    img_display = img_facerecognition.resize(224, 224)
    img_display.draw_circle((int((224 / 2))),(int((168 / 2))), 2, color=(255, 255, 255), thickness=1, fill=True)
    if code_customized_model:
        for i in (code_customized_model):
            count = 0
            face_x = int((i.x()+(i.w()/2)))
            hand_x0 = int((i.x()))
            hand_y0 = int((i.y()))
            face_y = int((i.y()+(i.h()/2)))
            if face_y < 92 or face_y > 132:
                pitch = pitch + int((0.65 * (face_y - 112)))
            if face_x < 92 or face_x > 132:
                yaw = yaw + int((0.65 * (face_x - 112)))
            if yaw < -128:
                yaw = int((-128))
            if yaw > 127:
                yaw = int(127)
            if pitch < -128:
                pitch = int((-128))
            if pitch > 127:
                pitch = int(127)
            img_display.draw_rectangle(hand_x0,hand_y0, (i.w()), (i.h()), color=(255,255,255), thickness=2, fill=False)
    else:
        count = count + 1
        if count >= 10:
            yaw = int(0)
            pitch = int(0)
    lcd_draw_string(img_display,60,60, "x: %.2d,y: %.2d" % (face_x, face_y), color=(51,102,255), scale=1, mono_space=False)
    _img_display_x, _img_display_y = 8, 36
    lcd.display(img_display, oft=(_img_display_x,_img_display_y))
    _timer_tim.start()
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
