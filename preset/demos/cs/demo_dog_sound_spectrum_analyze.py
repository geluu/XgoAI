import time

import machine, time
from fpioa_manager import fm

import lcd
import image
from Maix import GPIO, I2S, FFT
from board import board_info
from fpioa_manager import fm

sample_rate = 38640
sample_points = 1024
fft_points = 512
hist_x_num = 50

fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(19,fm.fpioa.I2S0_WS, force=True)
fm.register(18,fm.fpioa.I2S0_SCLK, force=True)

_recorder_rx = I2S(I2S.DEVICE_0)
_recorder_rx.channel_config(_recorder_rx.CHANNEL_0, _recorder_rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
_recorder_rx.set_sample_rate(sample_rate)
def _microphone_read_average(lst):
    return int((sum(lst)/len(lst))*100)

import time

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

_canvas_x, _canvas_y = 0, 0

read_all_channel = [0, 0, 0, 0, 0, 0, 0, 0]



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
while True:
    time.sleep_ms(10)
    _audio = _recorder_rx.record(sample_points)
    fft_res = FFT.run(_audio.to_bytes(),fft_points)
    fft_amp = FFT.amplitude(fft_res)

    read_all_channel[0] = int(_microphone_read_average(fft_amp[0:63]))
    read_all_channel[1] = int(_microphone_read_average(fft_amp[64:127]))
    read_all_channel[2] = int(_microphone_read_average(fft_amp[127:191]))
    read_all_channel[3] = int(_microphone_read_average(fft_amp[192:255]))
    read_all_channel[4] = int(_microphone_read_average(fft_amp[256:319]))
    read_all_channel[5] = int(_microphone_read_average(fft_amp[320:383]))
    read_all_channel[6] = int(_microphone_read_average(fft_amp[384:447]))
    read_all_channel[7] = int(_microphone_read_average(fft_amp[448:514]))
    radius1 = int(((read_all_channel[0]) / 10))
    radius2 = int(((read_all_channel[2]) / 10))
    radius3 = int(((read_all_channel[4]) / 10))
    radius4 = int(((read_all_channel[6]) / 10))
    canvas.clear()
    canvas.draw_circle(120,120, radius1, color=(255, 0, 0), thickness=2, fill=True)
    canvas.draw_circle(120,120, radius2, color=(51, 255, 51), thickness=5, fill=False)
    canvas.draw_circle(120,120, radius3, color=(51, 51, 255), thickness=5, fill=False)
    canvas.draw_circle(120,120, radius4, color=(204, 51, 204), thickness=5, fill=False)
    _canvas_x, _canvas_y = 0, 0
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    if radius1 > 10:
        robot_dog_setup_uart.write(bytes([51]))
        time.sleep_ms(20)
        time.sleep_ms(3000)
    elif radius2 > 10:
        robot_dog_setup_uart.write(bytes([64]))
        time.sleep_ms(20)
        time.sleep_ms(3000)
    elif radius3 > 10:
        robot_dog_setup_uart.write(bytes([62]))
        time.sleep_ms(20)
        time.sleep_ms(3000)
    elif radius4 > 10:
        robot_dog_setup_uart.write(bytes([52]))
        time.sleep_ms(20)
        time.sleep_ms(3000)
    _timer_tim.start()
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
