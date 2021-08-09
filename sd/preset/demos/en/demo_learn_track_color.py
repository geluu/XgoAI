import sensor, image, time, lcd, gc
from cocorobo import display_cjk_string

print("Letting auto algorithms run. Don't put anything in front of the camera!")
from fpioa_manager import *
from Maix import FPIOA, GPIO
import time
import machine
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)
lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(0,0,0)

gc.enable()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_colorbar(False)

# turn on selfie mode by changing 0 to 1, # turn on normal mode by changing 1 to 0
sensor.set_vflip(0)
sensor.set_hmirror(True)
sensor.run(1)
sensor.skip_frames()


i = 0
tim = time.ticks_ms()

# Capture the color thresholds for whatever was in the center of the image.
r = [(240//2)-(50//2), (240//2)-(50//2), 50, 50] # 50x50 center of QVGA.

print("Auto algorithms done. Hold the object you want to track in front of the camera in the box.")
print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")

for i in range(80):
    gc.collect()
    img = sensor.snapshot()
    img.draw_rectangle(0,0, 240, 50, fill=True, color=(0,0,0))
    display_cjk_string(img, 0,0,"Put any color", font_size=1, color=(255,255,255))
    display_cjk_string(img, 0,25,"inside the box:", font_size=1, color=(255,255,255))
    img.draw_rectangle(r)
    lcd.display(img, oft=(8,8))
    # img_len = v.record(img)

print("Learning thresholds...")
threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.
for i in range(80):
    gc.collect()
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r)
    lo = hist.get_percentile(0.01) # Get the CDF of the histogram at the 1% range (ADJUST AS NECESSARY)!
    hi = hist.get_percentile(0.99) # Get the CDF of the histogram at the 99% range (ADJUST AS NECESSARY)!
    # Average in percentile values.
    threshold[0] = (threshold[0] + lo.l_value()) // 2
    threshold[1] = (threshold[1] + hi.l_value()) // 2
    threshold[2] = (threshold[2] + lo.a_value()) // 2
    threshold[3] = (threshold[3] + hi.a_value()) // 2
    threshold[4] = (threshold[4] + lo.b_value()) // 2
    threshold[5] = (threshold[5] + hi.b_value()) // 2
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)
        img.draw_rectangle(0,0, 240, 25, fill=True, color=(0,0,0))
        display_cjk_string(img, 0,0,"Learning thresholds...", font_size=1, color=(255,255,255))
        lcd.display(img, oft=(8,8))
    	# img_len = v.record(img)


time.sleep(2)

print("Thresholds learned...")
print("Tracking colors...")
time.sleep(2)

while(True):
    gc.collect()
    tim = time.ticks_ms()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())


    lcd.display(img, oft=(8,8))
    # img_len = v.record(img)
    # print(i)
    # i += 1
    # if i > 200:
    #     break
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                machine.reset()

print("finish")
# v.record_finish()