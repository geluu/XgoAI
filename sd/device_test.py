from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time, sys
import audio
from Maix import FPIOA, GPIO, I2S, FFT
from board import board_info
import image, lcd, math

buttonLeft, buttonRight, buttonDown = 9, 10, 11

fpiol = FPIOA()
fpior = FPIOA()
fpiod = FPIOA()

fpiol.set_function(buttonLeft,FPIOA.GPIO0)
fpior.set_function(buttonRight,FPIOA.GPIO1)
fpiod.set_function(buttonDown,FPIOA.GPIO2)

fm.register(31, fm.fpioa.GPIO3)
fm.register(32, fm.fpioa.GPIO4)

led_red=GPIO(GPIO.GPIO3,GPIO.OUT)
led_blue=GPIO(GPIO.GPIO4,GPIO.OUT)

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
time.sleep(1)
lcd.draw_string(10,60, "1. Screen RGB Testing...", lcd.WHITE, lcd.BLACK)
time.sleep_ms(1000)


lcd.clear(lcd.RED)
time.sleep_ms(500)
lcd.clear(lcd.GREEN)
time.sleep_ms(500)
lcd.clear(lcd.BLUE)
time.sleep_ms(500)


lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing...", lcd.WHITE, lcd.BLACK)

try:
	sensor.reset()
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_framesize(sensor.QVGA)
	sensor.set_windowing((0,0,224,224))
	sensor.set_colorbar(False)
	sensor.set_vflip(0)
	sensor.set_hmirror(0)
	sensor.run(1)
	sensor.skip_frames()
	lcd.clear(lcd.BLACK)
	for i in range(100):
		img_raw = sensor.snapshot()    
		lcd.display(img_raw,oft=(8,8))
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing...", lcd.WHITE, lcd.BLACK)
	time.sleep(1)
except BaseException as e:
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: Error", lcd.RED, lcd.BLACK)
	lcd.draw_string(10,100, str(e), lcd.RED, lcd.BLACK)
	sys.exit(0)

def mic_test():
	sample_rate = 38640
	sample_points = 1024
	fft_points = 512
	hist_x_num = 50

	fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
	fm.register(19,fm.fpioa.I2S0_WS, force=True)    # 19 on Go Board and Bit(new version)
	fm.register(18,fm.fpioa.I2S0_SCLK, force=True)  # 18 on Go Board and Bit(new version)

	rx = I2S(I2S.DEVICE_0)
	rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
	rx.set_sample_rate(sample_rate)

	def _microphone_read_average(lst): 
	    return int((sum(lst)/len(lst))*100)

	img = image.Image()
	screen_width = 240

	if hist_x_num > screen_width:
	    hist_x_num = screen_width
	hist_width = int(screen_width / hist_x_num)#changeable
	x_shift = 0

	for i in range(200):
	    audio = rx.record(sample_points)
	    fft_res = FFT.run(audio.to_bytes(),fft_points)
	    fft_amp = FFT.amplitude(fft_res)
	    print(_microphone_read_average(fft_amp))
	    img = img.clear()
	    x_shift = 0
	    for i in range(hist_x_num):
	        if fft_amp[i] > 240:
	            hist_height = 240
	        else:
	            hist_height = fft_amp[i]
	        img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[0,0,255],2,True)
	        x_shift = x_shift + hist_width
	    lcd.display(img)
	    fft_amp.clear()
try:
	mic_test()
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
	time.sleep(1)
except BaseException as e:
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing: Error", lcd.RED, lcd.BLACK)
	lcd.draw_string(10,120, str(e), lcd.RED, lcd.BLACK)
	sys.exit(0)


lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,120, "4. SD Card Testing...", lcd.WHITE, lcd.BLACK)
time.sleep(1)

try:
	lcd.clear(lcd.BLACK)
	filelist = os.listdir("/sd")
	for row in range(len(filelist)):
		lcd.draw_string(10,10+(row*15), str(filelist[row]), lcd.WHITE, lcd.BLACK)
	time.sleep(2)
	if "try_demo.py" in filelist:
		lcd.clear(lcd.BLACK)
		lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
		lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
		lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
		time.sleep(1)
	else:
		lcd.clear(lcd.BLACK)
		lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
		lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
		lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
		lcd.draw_string(10,120, "4. SD Card Testing: Failed", lcd.RED, lcd.BLACK)
		lcd.draw_string(10,140, "   try_demo.py not found", lcd.RED, lcd.BLACK)
		sys.exit(0)
except BaseException as e:
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,120, "4. SD Card Testing: Error", lcd.RED, lcd.BLACK)
	lcd.draw_string(10,140, str(e), lcd.RED, lcd.BLACK)
	sys.exit(0)


lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,140, "5. Speaker Testing... ", lcd.WHITE, lcd.BLACK)
time.sleep(1)

try:
	fm.register(34,fm.fpioa.I2S0_OUT_D1) # DIN: 17
	fm.register(35,fm.fpioa.I2S0_SCLK) # BCLK: 15
	fm.register(33,fm.fpioa.I2S0_WS) #LRCLK: 14
	rx = I2S(I2S.DEVICE_0)
	player = audio.Audio(path = "/sd/preset/songs/boot.wav")
	player.volume(95)
	wav_info = player.play_process(rx)
	rx.channel_config(rx.CHANNEL_1, I2S.TRANSMITTER, resolution = I2S.RESOLUTION_16_BIT, align_mode = I2S.STANDARD_MODE)
	rx.set_sample_rate(wav_info[1])

	while True:
	    ret = player.play()
	    if ret == None:
	        break
	    elif ret==0:
	        break

	player.finish()
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,140, "5. Speaker Testing: OK ", lcd.GREEN, lcd.BLACK)
	time.sleep(1)
except BaseException as e:
	lcd.clear(lcd.BLACK)
	lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
	lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
	lcd.draw_string(10,140, "5. Speaker Testing: Error ", lcd.RED, lcd.BLACK)
	lcd.draw_string(10,160, str(e), lcd.RED, lcd.BLACK)


lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,140, "5. Speaker Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,160, "6. Button Testing...", lcd.WHITE, lcd.BLACK)
time.sleep(1)



lcd.clear(lcd.BLACK)
button_a_state, button_b_state, button_c_state = 0, 0, 0

while button_a_state == 0:
	key_gpio_left = GPIO(GPIO.GPIO0,GPIO.IN)

	lcd.draw_string(10,10, "Press Button A:", lcd.WHITE, lcd.BLACK)
	if key_gpio_left.value() == 1:
		lcd.draw_string(10,10, "Press Button A: OK", lcd.GREEN, lcd.BLACK)
		button_a_state = 1


while button_b_state == 0:
	key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)

	lcd.draw_string(10,30, "Press Button B:", lcd.WHITE, lcd.BLACK)
	if key_gpio_right.value() == 1:
		lcd.draw_string(10,30, "Press Button B: OK", lcd.GREEN, lcd.BLACK)
		button_b_state = 1


while button_c_state == 0:
	key_gpio_down=GPIO(GPIO.GPIO2,GPIO.IN)

	lcd.draw_string(10,50, "Press Button C:", lcd.WHITE, lcd.BLACK)
	if key_gpio_down.value() == 1:
		lcd.draw_string(10,50, "Press Button C: OK", lcd.GREEN, lcd.BLACK)
		button_c_state = 1

time.sleep(1)

lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,140, "5. Speaker Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,160, "6. Button Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,180, "7. LED Testing... ", lcd.WHITE, lcd.BLACK)

time.sleep(0.5)

for i in range(20):
	led_red.value(1)
	led_blue.value(1)
	time.sleep_ms(100)
	led_red.value(0)
	led_blue.value(0)
	time.sleep_ms(100)

lcd.clear(lcd.BLACK)
lcd.draw_string(10,10, "A.I. Module", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,30, "General Testing", lcd.WHITE, lcd.BLACK)
lcd.draw_string(10,60, "1. Screen RGB Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,80, "2. Camera Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,100, "3. Microphone Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,120, "4. SD Card Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,140, "5. Speaker Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,160, "6. Button Testing: OK", lcd.GREEN, lcd.BLACK)
lcd.draw_string(10,180, "7. LED Testing: OK", lcd.GREEN, lcd.BLACK)

lcd.draw_string(10,210, "Rebooting now...", lcd.WHITE, lcd.BLACK)
time.sleep(1)


import machine
machine.reset()
