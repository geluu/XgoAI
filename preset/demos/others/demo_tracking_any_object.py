import sensor, image, time, lcd, video, gc

gc.enable()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_colorbar(False)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)
sensor.skip_frames()

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "Object Color", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "Auto Tracking Demo", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,210, "Initalizing...", lcd.ORANGE, lcd.BLACK)

time.sleep(1)



from fpioa_manager import *
from Maix import FPIOA, GPIO

_buttonLeft, _buttonRight = 0, 1
fpiol, fpior = FPIOA(), FPIOA()
fpiol.set_function(_buttonLeft,FPIOA.GPIO0)
fpior.set_function(_buttonRight,FPIOA.GPIO1)
_key_gpio_left=GPIO(GPIO.GPIO0,GPIO.IN)
_key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)
buttonAState = False
buttonBState = False

'''
print("Letting auto algorithms run. Don't put anything in front of the camera!")
print("Auto algorithms done. Hold the object you want to track in front of the camera in the box.")
print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")
'''

i = 0

detection_box = [82, 82, 60, 60]

while True:
    gc.collect()

    img = sensor.snapshot()
    img.draw_string(24,5,"Press Left Key to Learn", color=(255,255,255), mono_space=False, scale=2)

    img.draw_string(30,185,"Please Put the Object", mono_space=False, scale=2)
    img.draw_string(55,205,"Inside the Box:", mono_space=False, scale=2)
    # img.draw_arrow(112,175,112,155, color=(255, 255,255), thickness=2)
    img.draw_rectangle(detection_box)
    lcd.display(img, oft=(8,8))

    if (_key_gpio_left.value() == 0) and buttonAState == False:
        print("A Pressed")
        break
        buttonAState = True
    elif (_key_gpio_left.value() == 1) and buttonAState == True:
        buttonAState = False
    if (_key_gpio_right.value() == 0) and buttonBState == False:
        print("B Pressed")
        buttonBState = True
    elif (_key_gpio_right.value() == 1) and buttonBState == True:
        buttonBState = False

print("Learning thresholds...")
threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.

for i in range(100):
    gc.collect()
    img = sensor.snapshot()
    hist = img.get_histogram(roi=detection_box)
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
        img.draw_rectangle(detection_box)
        img.draw_string(0,0,"Learning thresholds...", mono_space=False, scale=2)
        lcd.display(img, oft=(8,8))


time.sleep(1)

img.draw_string(0,0,"Thresholds learned...", mono_space=False, scale=2)
lcd.display(img, oft=(8,8))

time.sleep(1)

while(True):
    gc.collect()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())

    lcd.display(img, oft=(8,8))

print("finish")