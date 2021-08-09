import lcd
import image
import sensor

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

_camera_x, _camera_y = 0, 0



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
_camera_x, _camera_y = 8, 8
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.skip_frames(30)
sensor.run(1)
sensor.set_auto_whitebal(True)
sensor.set_auto_exposure(True)
sensor.set_hmirror(True)
sensor.set_windowing((224,224))
while True:
    camera = sensor.snapshot()
    find_line_result = camera.find_lines(roi=(0, 0,224, 224), threshold = 1000, theta_margin = 25, rho_margin = 25)
    for j in find_line_result:
        camera.draw_line((j.x1()),(j.y1()), (j.x2()),(j.y2()), color=(51,102,255), thickness=1)
    lcd.display(camera, oft=(_camera_x,_camera_y))
