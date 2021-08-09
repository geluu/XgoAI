import time

import lcd
import image
import sensor
import KPU as kpu
import machine, time
from fpioa_manager import fm

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

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

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

_canvas_x, _canvas_y = 0, 0

task_objectrecognition = None
classes_objectrecognition = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task_objectrecognition = kpu.load("/sd/preset/models/tinyyolo_v2_20class.kmodel")
object_anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task_objectrecognition, 0.5, 0.3, 5, object_anchor)



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
object_name = ""
canvas = image.Image(size=(240, 35))
_canvas_x, _canvas_y = 0, 0
while True:
    img_objectrecognition = sensor.snapshot()
    code_objectrecognition = kpu.run_yolo2(task_objectrecognition, img_objectrecognition)
    img_objectrecognition.ai_to_pix()
    img_display = img_objectrecognition.resize(224, 168)
    img_display.draw_circle((int((224 / 2))),(int((168 / 2))), 2, color=(255, 255, 255), thickness=1, fill=True)
    if code_objectrecognition:
        for i in code_objectrecognition:
            canvas.clear()
            img_display.draw_rectangle((int((i.x() / 1.42))),(int((i.y() / 1.42))), (int((i.w() / 1.42))), (int((i.h() / 1.42))), color=(255,255,255), thickness=2, fill=False)
            object_name = str(classes_objectrecognition[i.classid()])
            lcd_draw_string(img_display,8,8, object_name, color=(51,51,255), scale=1, mono_space=False)
        if object_name == "cat":
            robot_dog_setup_uart.write(bytes([60]))
            time.sleep_ms(20)
            time.sleep_ms(3000)
        if object_name == "dog":
            robot_dog_setup_uart.write(bytes([61]))
            time.sleep_ms(20)
            time.sleep_ms(3000)
        if object_name == "person":
            robot_dog_setup_uart.write(bytes([66]))
            time.sleep_ms(20)
            time.sleep_ms(3000)
    else:
        lcd_draw_string(canvas,0,0, "Nothing Detected.", color=(255,0,0), scale=1, mono_space=False)
    _img_display_x, _img_display_y = 8, 36
    lcd.display(img_display, oft=(_img_display_x,_img_display_y))
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    _timer_tim.start()
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
