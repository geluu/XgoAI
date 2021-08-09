from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time
from Maix import FPIOA, GPIO

gc.enable()

buttonLeft, buttonRight = 0, 1

fpiol = FPIOA()
fpior = FPIOA()

fpiol.set_function(buttonLeft,FPIOA.GPIO0)
fpior.set_function(buttonRight,FPIOA.GPIO1)

key_gpio_left=GPIO(GPIO.GPIO0,GPIO.IN)
key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)

ksl,ksr = 0, 0

button_count = 0

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(3)
lcd.clear(0,0,0)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((0,0,224,224))
sensor.set_colorbar(False)

# turn on selfie mode by changing 0 to 1, # turn on normal mode by changing 1 to 0
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.run(1)
sensor.skip_frames()

img_raw = sensor.snapshot()

def take_picture(button_count):
    lcd.clear(0,0,0)
    img_captured = img_raw.resize(200,200)
    img_raw.save("/sd/user/camera/cocoshot"+ str(button_count) +".jpg", quality=60)
    img_captured.draw_string(4,4,"saved as cocoshot_"+str(button_count)+".jpg", color=(255,255,255), scale=2, mono_space=False)
    lcd.display(img_captured,oft=(20,20))
    time.sleep_ms(1000)

while True:
    gc.collect()
    
    img_raw = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

    key_state_left = key_gpio_left.value()
    key_state_right = key_gpio_right.value()

    if (key_state_left == 0 and ksl == 0):
        ksl = 1
    elif (key_state_left == 1 and ksl == 1):
        ksl = 0

    if (key_state_right == 0 and ksr == 0):
        print("capturing")
        button_count = button_count + 1
        take_picture(button_count)
        ksr = 1
    elif (key_state_right == 1 and ksr == 1):
        ksr = 0
    
    lcd.display(img_raw,oft=(8,8))
