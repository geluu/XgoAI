import sensor
import image
import lcd
import time
import gc

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(0,0,0)

gc.enable()
gc.collect()
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_colorbar(False)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.set_auto_whitebal(False)
sensor.run(1)
sensor.skip_frames()

state = 1
qrRead = "nothing"

while True:
    gc.collect()
    # clock.tick()
    img = sensor.snapshot()
    img_cover_cut = img.cut(62,62,100,100) 
    # a = img_cover_cut.to_grayscale()  
    a = img_cover_cut.ai_to_pix()

    res = img_cover_cut.find_qrcodes()
    # fps =clock.fps()

    if len(res) > 0:
        # img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)
        print(res[0].payload())
        qrRead = res[0].payload()
    elif len(res) <= 0:
    	qrRead = ""

    img.draw_rectangle(0,0,240,25,color=(0,0,0),fill=True)
    img.draw_string(2,2,qrRead,color=(255,255,255),mono_space=False,scale=2)

    img.draw_rectangle(62,62,100,100,color=(255,255,255),fill=False, thickness=2)

    '''
    if qrRead == "CocoRobo_A":
        img.draw_rectangle(0,0,80,80,color=(0,255,255),fill=True)
        img.draw_string(14,8,"A",color=(0,0,0),monospace=True,scale=6)
    '''

    lcd.display(img,oft=(8,8))
