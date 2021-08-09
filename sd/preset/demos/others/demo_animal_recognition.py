from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time
from Maix import FPIOA, GPIO
import KPU as kpu

gc.enable()

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(0,0,0)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)
sensor.skip_frames()

# 飛機、單車、鳥、船、水瓶、巴士、汽車、貓、椅子、牛、餐桌、狗、馬、摩托車、人、盆栽、羊、沙發、火車、顯示器
gc.collect()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load("/sd/preset/models/tinyyolo_v2_20class.kmodel") 
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
gc.collect()

class_name = 'null'

img_block = image.Image("/sd/preset/images/default_block.jpg")

while(True):
    gc.collect()
    
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)

    img_screen = img.resize(224,168)
    a = img_screen.ai_to_pix
    a = img.draw_circle(120, 90, 1, fill=True)

    if code:
        for i in code:
            a = img_screen.draw_rectangle(int(i.x()/1.42),int(i.y()/1.42),int(i.w()/1.42),int(i.h()/1.42),color=(255,255,255),fill=False, thickness=2)
            print(i)
            for i in code:
                class_name = classes[i.classid()]
                img_screen.draw_rectangle(int(i.x()/1.42), int(i.y()/1.42)-22,int(i.w()/1.42),22,color=(255,0,0),fill=True)
                img_screen.draw_string(int(i.x()/1.42), int(i.y()/1.42)-22, classes[i.classid()], color=(255,255,255),scale=2)
    
    a = lcd.display(img_screen, oft=(8,38))
    lcd.draw_string(8, 8,"Object Detection Demo", lcd.WHITE)

a = kpu.deinit(task)