import time

import lcd
import image
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
def aoye():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_5.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_6.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_7.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_8.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_9.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_10.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_11.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_12.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/sleepy/sleepy_13.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)

def anzhongguancha():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_5.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_6.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_7.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_8.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_9.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_10.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/seek/seek_11.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)

def er():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_5.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_6.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_7.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/swing/swing_8.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)

def laugh():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/smile/smile_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/smile/smile_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/smile/smile_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/smile/smile_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/smile/smile_5.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()

def yaobai():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_5.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_6.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_7.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/giddy/giddy_8.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)

def lengmo():
    global canvas, old_time
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/angry/angry_1.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/angry/angry_2.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/angry/angry_3.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(600)
    canvas.clear()
    canvas.draw_image(image.Image("/sd/preset/images/angry/angry_4.jpg"), 0,0,  x_scale=1,  y_scale=1 )
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    time.sleep_ms(100)

def reopen():
    global canvas, old_time
    if _gp_side_c.value() == 1:
        old_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - old_time >= 1000:
                robot_dog_setup_uart.write(b'\x55\x00\x09\x01\x03\x00\xf2\x00\xaa')
                time.sleep_ms(20)
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
robot_dog_setup_uart.write(b'\x55\x00\x09\x01\x03\x01\xf1\x00\xaa')
time.sleep_ms(20)
_timer_tim.start()
while True:
    aoye()
    reopen()
    anzhongguancha()
    reopen()
    er()
    reopen()
    laugh()
    reopen()
    lengmo()
    reopen()
    yaobai()
    reopen()
