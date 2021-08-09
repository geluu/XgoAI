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

lcd.init(type=2,freq=19000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)

img = image.Image(size=(240, 240))

bg = (242,227,210)
img.draw_rectangle(0,0,240,240,fill=True,color=bg)

# display_cjk_string(img, 0, 0, '今天的weather不错的', font_size=size, color=(299,299,299), auto_wrap=True)
mixed_text = "简体中文 ENGLISH 繁體中文 にほんご 한국어"

alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
alphabet_upper = "ABCDEFGHIJKLMNOPQRST"
arabic_number = "0123456789"
special_characters = "~`!@#$%^&*()_+-={}|:\"<>?[]\\;',./"
roman_text = [alphabet_lower, alphabet_upper, arabic_number, special_characters]

test_text = "Hello World!"

while True:
	img.draw_rectangle(0,0,240,240,fill=True,color=bg)
	lcd_draw_string(img, 10, 10, "月が綺麗ですね", font_size=2, color=(0,0,0))
	lcd_draw_string(img, 10, 45, "夏目漱石               ", font_size=1, color=(0,0,0))
	lcd.display(img)
	time.sleep(1)


# while True:
	# for i in range(10, 0, -1):
	# 	cocorobo_draw_text(0,0, img, str(i), size=1)
	#	lcd.display(img)
	#	time.sleep_ms(200)

