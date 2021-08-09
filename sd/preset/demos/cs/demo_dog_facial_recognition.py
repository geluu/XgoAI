
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
import gc
import KPU as kpu
import sensor
import image
import lcd
from Maix import FPIOA, GPIO
import gc
from fpioa_manager import fm
from board import board_info
import time

import utime
BOUNCE_PROTECTION = 200
ACCURACY = 85
try:from cocorobo import display_cjk_string
except:pass
def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)
import time

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

def set_key_state(*_):
    global start_processing
    start_processing = True
    utime.sleep_ms(BOUNCE_PROTECTION)


clock = None
task_fd = None
task_ld = None
task_fe = None

task_fd = kpu.load("/sd/preset/models/face/v2/FaceDetection.emodel") # 0x300000)
task_ld = kpu.load("/sd/preset/models/face/v2/FaceLandmarkDetection.emodel")# 0x400000)
task_fe = kpu.load("/sd/preset/models/face/v2/FeatureExtraction.emodel")# 0x500000)
clock = time.clock()

fm.register(10, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)
start_processing = False

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

lcd.init(type=2)
lcd.rotation(1)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(True)
sensor.run(1)

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437,6.92275, 6.718375, 9.01025)  # anchor for face detect
dst_point = [(44, 59), (84, 59), (64, 82), (47, 105),(81, 105)]  # standard face key point position
a = kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)
img_lcd = image.Image()
img_face = image.Image(size=(128, 128))
index = -1
a = img_face.pix_to_ai()
record_ftr = []
record_ftrs = []

names = ["master", "friend1", "friend2"]




_timer_tim.start()
while True:
    face_test = sensor.snapshot()
    clock.tick()
    code = kpu.run_yolo2(task_fd, face_test)
    if code:
        for i in code:
            # Cut face and resize to 128x128
            a = face_test.draw_rectangle(i.rect())
            face_cut = face_test.cut(i.x(), i.y(), i.w(), i.h())
            face_cut_128 = face_cut.resize(128, 128)
            a = face_cut_128.pix_to_ai()
            #a = face_test.draw_image(face_cut_128, (0,0))
            # Landmark for face 5 points
            fmap = kpu.forward(task_ld, face_cut_128)
            plist = fmap[:]
            le = (i.x()+int(plist[0]*i.w() - 10), i.y()+int(plist[1]*i.h()))
            re = (i.x()+int(plist[2]*i.w()), i.y()+int(plist[3]*i.h()))
            nose = (i.x()+int(plist[4]*i.w()), i.y()+int(plist[5]*i.h()))
            lm = (i.x()+int(plist[6]*i.w()), i.y()+int(plist[7]*i.h()))
            rm = (i.x()+int(plist[8]*i.w()), i.y()+int(plist[9]*i.h()))
            a = face_test.draw_circle(le[0], le[1], 4)
            a = face_test.draw_circle(re[0], re[1], 4)
            a = face_test.draw_circle(nose[0], nose[1], 4)
            a = face_test.draw_circle(lm[0], lm[1], 4)
            a = face_test.draw_circle(rm[0], rm[1], 4)
            # align face to standard position
            src_point = [le, re, nose, lm, rm]
            T = image.get_affine_transform(src_point, dst_point)
            a = image.warp_affine_ai(face_test, img_face, T)
            a = img_face.ai_to_pix()
            #a = face_test.draw_image(img_face, (128,0))
            del(face_cut_128)
            # calculate face feature vector
            fmap = kpu.forward(task_fe, img_face)
            feature = kpu.face_encode(fmap[:])
            reg_flag = False
            scores = []
            for j in range(len(record_ftrs)):
                score = kpu.face_compare(record_ftrs[j], feature)
                scores.append(score)
            max_score = 0
            index = 0
            for k in range(len(scores)):
                if max_score < scores[k]:
                    max_score = scores[k]
                    index = k
            if max_score > ACCURACY:
                a = lcd_draw_string(face_test, i.x(), i.y(), ("%s :%2.1f" % (names[index], max_score)), color=(0, 255, 0), scale=2, mono_space=False)
            else:
                a = lcd_draw_string(face_test, i.x(), i.y(), ("X :%2.1f" % (max_score)), color=(255, 0, 0), scale=2, mono_space=False)
            if start_processing:
                record_ftr = feature
                record_ftrs.append(record_ftr)
                start_processing = False
            break
    fps = clock.fps()
    a = lcd.display(face_test)
    gc.collect()
        # kpu.memtest()
    if "master" == (names[index] if (index != -1 and len(names) > index) else ""):
        robot_dog_setup_uart.write(bytes([60]))
        time.sleep_ms(20)
        time.sleep_ms(2000)
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
