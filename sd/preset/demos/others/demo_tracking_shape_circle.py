import sensor, image, time, lcd

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(0,0,0)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_colorbar(False)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)
sensor.skip_frames()

# threshold_red1 = (45, 65, 40, 80, 40, 60)
# threshold_red2 = (45, 65, -20, 30, -60, -20)
# threshold_green1 = (0,   80,  -70,   -10,   -0,   30)
# threshold_green2 = (45, 65, -50, -30, 0, 40)
# threshold_blue = (0, 15, 0, 40, -80, -20)
fc_threshold_red = (30, 100, 15, 127, 15, 127)
fc_threshold_green = (30, 100, -64, -8, -32, 32)
fc_threshold_blue = (45, 65, -20, 30, -60, -20)

fc_color_threshold = fc_threshold_red
fc_bounding_box_color = (200,200,200)

def fc_expand_roi(roi):
    extra = 5
    win_size = (224, 224)
    (x, y, width, height) = roi
    fc_new_roi = [x-extra, y-extra, width+2*extra, height+2*extra]

    if fc_new_roi[0] < 0:
        fc_new_roi[0] = 0
    if fc_new_roi[1] < 0:
        fc_new_roi[1] = 0
    if fc_new_roi[2] > win_size[0]:
        fc_new_roi[2] = win_size[0]
    if fc_new_roi[3] > win_size[1]:
        fc_new_roi[3] = win_size[1]

    return tuple(fc_new_roi)

while(True):
    img = sensor.snapshot()

    fc_blobs = img.find_blobs([fc_color_threshold], area_threshold=150)
    if fc_blobs:
        for fc_blob in fc_blobs:
            fc_is_circle = False
            fc_max_circle = None
            fc_max_radius = -1
            fc_new_roi = fc_expand_roi(fc_blob.rect())

            for fc_c in img.find_circles(threshold = 2000, x_margin = 20, y_margin = 20, r_margin = 10, roi=fc_new_roi):
                fc_is_circle = True
                # img.draw_circle(c.x(), c.y(), c.r(), color = (255, 255, 255))
                if fc_c.r() > fc_max_radius:
                    fc_max_radius = fc_c.r()
                    fc_max_circle = fc_c

            if fc_is_circle:
                img.draw_rectangle(fc_new_roi, thickness=1)
                img.draw_rectangle(fc_new_roi[0], fc_new_roi[1]-20, fc_new_roi[2], 20, color=(255,255,255), fill=True)
                img.draw_string(fc_new_roi[0]+2, fc_new_roi[1]-20+2, "x:"+ str(fc_new_roi[0]) + ", y:"+ str(fc_new_roi[1]), mono_space=False, color=(0,0,0), scale=2)
                img.draw_cross(fc_blob[5], fc_blob[6])
                img.draw_circle(fc_max_circle.x(), fc_max_circle.y(), fc_max_circle.r(), color = fc_bounding_box_color)
                img.draw_circle(fc_max_circle.x(), fc_max_circle.y(), fc_max_circle.r() + 1, color = fc_bounding_box_color)

    lcd.display(img, oft=(8,8))


