print("Clearing Cached Variables...", end="")
for name in dir(): 
    if not name.startswith('_'): 
        del globals()[name]
print(" Done\n")
import KPU as kpu
from Maix import utils
import gc
print("gc.mem_free():\t" + str(gc.mem_free()))
print("kpu.memtest():")
kpu.memtest()
utils.gc_heap_size(524288)
print("GC Heap Size set to 524288")
print("utils.gc_heap_size():\t" + str(utils.gc_heap_size()))

################# Done Init #################

import sensor
import image
import lcd
import time
from Maix import FPIOA, GPIO
import gc
from fpioa_manager import fm
from board import board_info

gc.enable()
def set_key_state(*_):
    global start_processing
    start_processing = True
gc.collect()

kpu.memtest()
task_fd = kpu.load("/sd/preset/models/face_reocgnition/FD.emodel")
task_ld = kpu.load("/sd/preset/models/face_reocgnition/KP_chwise.emodel")
task_fe = kpu.load("/sd/preset/models/face_reocgnition/FE_mbv1_0.5.emodel")
kpu.memtest()

fm.register(10, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)
start_processing = False

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

lcd.init(type=2)
lcd.rotation(1)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437,6.92275, 6.718375, 9.01025)  # anchor for face detect
dst_point = [(44, 59), (84, 59), (64, 82), (47, 105),(81, 105)]  # standard face key point position
a = kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)
img_lcd = image.Image()
img_face = image.Image(size=(128, 128))
index = -1
a = img_face.pix_to_ai()
record_ftr = []
record_ftrs = []
names = ["1", "2", "3"]

gc.collect()

while True:
    img = sensor.snapshot()
    code = kpu.run_yolo2(task_fd, img)
    kpu.memtest()
    if code:
        for i in code:
            # Cut face and resize to 128x128
            a = img.draw_rectangle(i.rect())
            face_cut_128 = img.cut(i.x(), i.y(), i.w(), i.h())
            face_cut_128 = face_cut_128.resize(128, 128)
            face_cut_128.pix_to_ai()
            #a = img.draw_image(face_cut_128, (0,0))
            # Landmark for face 5 points
            #.............
            fmap = kpu.forward(task_ld, face_cut_128)
            del face_cut_128
            plist = fmap[:]
            le = (i.x()+int(plist[0]*i.w() - 10), i.y()+int(plist[1]*i.h()))
            re = (i.x()+int(plist[2]*i.w()), i.y()+int(plist[3]*i.h()))
            nose = (i.x()+int(plist[4]*i.w()), i.y()+int(plist[5]*i.h()))
            lm = (i.x()+int(plist[6]*i.w()), i.y()+int(plist[7]*i.h()))
            rm = (i.x()+int(plist[8]*i.w()), i.y()+int(plist[9]*i.h()))
            a = img.draw_circle(le[0], le[1], 4)
            a = img.draw_circle(re[0], re[1], 4)
            a = img.draw_circle(nose[0], nose[1], 4)
            a = img.draw_circle(lm[0], lm[1], 4)
            a = img.draw_circle(rm[0], rm[1], 4)
            # align face to standard position
            src_point = [le, re, nose, lm, rm]
            T = image.get_affine_transform(src_point, dst_point)
            a = image.warp_affine_ai(img, img_face, T)
            # a = img_face.ai_to_pix()
            #a = img.draw_image(img_face, (128,0))
            # calculate face feature vector
            fmap = kpu.forward(task_fe, img_face)
            feature = kpu.face_encode(fmap[:])
            reg_flag = False
            scores = []
            for j in range(len(record_ftrs)):
                score = kpu.face_compare(record_ftrs[j], feature)
                scores.append(score)
            max_score = 0
            index = -1
            for k in range(len(scores)):
                if max_score < scores[k]:
                    max_score = scores[k]
                    index = k
            if(len(names) > index):
                if max_score > 85:
                    a = img.draw_string(i.x(), i.y(), ("%s :%2.1f" % (names[index], max_score)), color=(0, 255, 0), scale=2)
                else:
                    a = img.draw_string(i.x(), i.y(), ("X :%2.1f" % (max_score)), color=(255, 0, 0), scale=2)
                if start_processing:
                    record_ftr = feature
                    record_ftrs.append(record_ftr)
                    start_processing = False
            break
    gc.collect()
    kpu.memtest()
    img = img.cut(40,0,240,240)
    kpu.memtest()
    lcd.display(img, oft=(0,0))
    del img
    gc.collect()