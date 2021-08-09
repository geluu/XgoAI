import lcd, image, time

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
img = image.Image(size=(240, 240))


pos = [240, 0]

while True:
	img.draw_rectangle(0,0, 240, 240, color=(0,0,0),fill=True)
	display_cjk_string(img, pos[0], pos[1], '前方高能！', font_size=1, color=(255,255,255), auto_wrap=False)
	display_cjk_string(img, pos[0]-50, pos[1]+40, '高能准备！', font_size=1, color=(255,0,255), auto_wrap=False)
	display_cjk_string(img, pos[0]-35, pos[1]+140, '高能准备！！', font_size=2, color=(255,0,120), auto_wrap=False)
	display_cjk_string(img, pos[0]-30, pos[1]+100, '啊啊啊啊啊啊啊啊啊爆炸啦！', font_size=1, color=(255,0,0), auto_wrap=False)
	display_cjk_string(img, pos[0]-10, pos[1]+75, '高能准备！', font_size=1, color=(0,0,255), auto_wrap=False)
	display_cjk_string(img, pos[0]+10, pos[1]+180, '先行して高エネルギー!', font_size=1, color=(255,255,0), auto_wrap=False)
	display_cjk_string(img, 40, 210, 'High Energy Ahead!', font_size=1, color=(255,255,255), auto_wrap=False, mono_space=False)


	lcd.display(img)
	pos[0] -= 5
	if pos[0] < -240: pos[0]=240

	# time.sleep_ms(10)
