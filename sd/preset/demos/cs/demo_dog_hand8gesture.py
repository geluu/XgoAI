import sensor
import image
import lcd
import KPU as kpu

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_hmirror(0)
sensor.run(1)
task = kpu.load("/sd/yolov2.kmodel")
anchor=(3.8144, 4.0599, 4.4811, 4.5793, 5.2525, 5.0046, 5.5361, 5.7905, 6.3127, 6.1317)
a = kpu.init_yolo2(task, 0.65, 0, 5, anchor)
labels = ['fist', ' five', ' left', ' right', ' loveyou', ' ok', ' thumbup', ' yearh']
while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
    	print(code)
        for i in code:
            a=img.draw_rectangle(i.rect(),(0,255,0),2)
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(i.x()+45, i.y()-5, labels[i.classid()], lcd.WHITE,lcd.RED)
    else:
        a = lcd.display(img)
a = kpu.deinit(task)