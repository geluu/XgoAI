#by jd3096 20210808
import sensor
import image
import lcd
import KPU as kpu
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_hmirror(True)
sensor.run(1)
task = kpu.load("/sd/preset/models/rpsyolov2.kmodel")
anchor=[1.9551, 4.6866, 2.3092, 5.4064, 2.7024, 5.7547, 3.2026, 4.4318, 3.3322, 5.6523]
a = kpu.init_yolo2(task, 0.65, 0.1, 5, anchor)
labels = ['scissors', 'paper', 'rock']
while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        print(code)
        for i in code:
            a=img.draw_rectangle(i.rect(),(0,255,0),0)
            a = lcd.display(img)
            for i in code:
    			 lcd.draw_string(10,10, labels[i.classid()], lcd.WHITE,lcd.RED)
                #lcd.draw_string(i.x()+45, i.y()-5, labels[i.classid()], lcd.WHITE,lcd.RED)
    else:
        a = lcd.display(img)
a = kpu.deinit(task)