import time

import machine, time
from fpioa_manager import fm

import KPU as kpu
import sensor
import lcd
from Maix import FPIOA, GPIO
from fpioa_manager import fm
import gc
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

from fpioa_manager import *

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)
try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
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

############### config #################
class_names = ["Bone", "Other"]
class_num = len(class_names)
sample_single_num = 5
sample_num = len(class_names) * sample_single_num
THRESHOLD = 11
board_cube = 0
button_state = False

########################################

lcd.init(type=2)
lcd.rotation(1)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(True)
sensor.run(1)

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((224, 224))
#if board_cube == 1:
#    sensor.set_vflip(True)
#    sensor.set_hmirror(True)
#    lcd.init(type=2)
#    lcd.rotation(2)
#else:
#    lcd.init()

#fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
#key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

FPIOA().set_function(10, FPIOA.GPIO1)
key1 = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)

try:
    del model
except Exception:
    pass
try:
    del classifier
except Exception:
    pass
gc.collect()
model = kpu.load("/sd/preset/models/object_classifier.emodel")
classifier = kpu.classifier(model, class_num, sample_num)

cap_num = 0
train_status = 0
last_cap_time = 0
last_btn_status = 0
res_index = -1



while True:
    img = sensor.snapshot()
    min_dist = 1
    if board_cube:
        img = img.rotation_corr(z_rotation=90)
        img.pix_to_ai()
    # capture img
    if train_status == 0:
        if key1.value() == 0 and last_btn_status == 1:
            #time.sleep_ms(30)
            #if key1.value() == 1 and (last_btn_status == 1) and (time.ticks_ms() - last_cap_time > 500):
            last_btn_status = 0
            last_cap_time = time.ticks_ms()
            if cap_num < class_num:
                index = classifier.add_class_img(img)
                cap_num += 1
            elif cap_num < class_num + sample_num:
                index = classifier.add_sample_img(img)
                cap_num += 1
            #else:
            #    img = draw_string(img, 2, 200, "release boot key please", color=lcd.WHITE,scale=1, bg=lcd.RED)
        else:
            #time.sleep_ms(30)
            if key1.value() == 1 and (last_btn_status == 0):
                last_btn_status = 1
            if cap_num < class_num:
                img.draw_rectangle(-2,0, len("press right key to cap "+class_names[cap_num])*10+4 , 24, fill=True, color=lcd.RED)
                img = lcd_draw_string(img, 0, 2, "press right key to cap "+class_names[cap_num], color=lcd.WHITE,scale=2,mono_space=False)
            elif cap_num < class_num + sample_single_num * 1:
                img.draw_rectangle(-2,0, len("right key to cap Bone{}".format(cap_num-class_num-sample_single_num*0))*10+4 , 24, fill=True, color=lcd.RED)
                img = lcd_draw_string(img, 0, 2, "right key to cap Bone{}".format(cap_num-class_num-sample_single_num*0), color=lcd.WHITE,scale=2,mono_space=False)
            elif cap_num < class_num + sample_single_num * 2:
                img.draw_rectangle(-2,0, len("right key to cap Other{}".format(cap_num-class_num-sample_single_num*1))*10+4 , 24, fill=True, color=lcd.RED)
                img = lcd_draw_string(img, 0, 2, "right key to cap Other{}".format(cap_num-class_num-sample_single_num*1), color=lcd.WHITE,scale=2,mono_space=False)
    # train and predict
    if train_status == 0:
        if cap_num >= class_num + sample_num:
            img.draw_rectangle(28,98, len("training...")*10+4 , 24, fill=True, color=lcd.RED)
            img = lcd_draw_string(img, 30, 100, "training...", color=lcd.WHITE,scale=2,mono_space=False)
            lcd.display(img)
            classifier.train()
            train_status = 1
    else:
        res_index = -1
        try:
            res_index, min_dist = classifier.predict(img)
        except Exception as e:
            print("predict err:", e)
        if res_index >= 0 and min_dist < THRESHOLD :
            img.draw_rectangle(0,0, len(class_names[res_index])*20+4 , 24, fill=True, color=lcd.RED)
            img = lcd_draw_string(img, 2, 2, class_names[res_index], color=lcd.WHITE,scale=2,mono_space=False)
        else:
            img.draw_rectangle(0,0, len('maybe {}'.format(class_names[res_index]))*20+4 , 24, fill=True, color=lcd.RED)
            img = lcd_draw_string(img, 2, 2, 'maybe {}'.format(class_names[res_index]), color=lcd.WHITE,scale=2,mono_space=False)
    img = img.cut(0,0,240,240)
    lcd.display(img, oft=(0,0))
    if _gp_side_c.value() == 1:
        old_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - old_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
    if min_dist < THRESHOLD :
        if "Bone" == (class_names[res_index] if (res_index != -1 and len(class_names) > res_index) else ""):
            robot_dog_setup_uart.write(bytes([66]))
            time.sleep_ms(20)
            time.sleep_ms(1000)
        elif "Other" == (class_names[res_index] if (res_index != -1 and len(class_names) > res_index) else ""):
            robot_dog_setup_uart.write(bytes([0]))
            time.sleep_ms(20)
            time.sleep_ms(1000)
