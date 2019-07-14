import sensor, image, time

from pid import PID
from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

red_threshold  = (34, 8, -21, 20, 21, -28)

pan_pid = PID(p=0.20, i=0, d=0.01,imax=90) #脱机运行或者禁用图像传输，使用这个PID
tilt_pid = PID(p=0.20, i=0, d=0.01,imax=90) #脱机运行或者禁用图像传输，使用这个PID
#pan_pid = PID(p=0.2, i=0.03, imax=90)#在线调试使用这个PID
#tilt_pid = PID(p=0.2, i=0.03, imax=90)#在线调试使用这个PID

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.set_windowing((195,195))
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([red_threshold])
    if blobs:
        max_blob = find_max(blobs)
       # pan_error = max_blob.cx()-img.width()/2
        #tilt_error = max_blob.cy()-img.height()/2
        pan_error = max_blob.cx()-97
        tilt_error = max_blob.cy()-97
        print("pan_error: ", pan_error)
        print("tilt_error: ", tilt_error)
        print(max_blob.cx(),max_blob.cy())
        img.draw_rectangle(max_blob.rect()) # rect
        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
        img.draw_cross(97,97)
        pan_output=pan_pid.get_pid(pan_error,1)
        tilt_output=tilt_pid.get_pid(tilt_error,1)
        print("pan_output",pan_output)
        #pan_servo.angle(-pan_output)
        #pan_servo.angle(pan_servo.angle()+pan_output)
        #tilt_servo.angle(tilt_servo.angle()-tilt_output)
        if pan_output<-40:
                        pan_output=-40
        elif pan_output>40:
                        pan_output=40

        if tilt_output<-40:
                        tilt_output=-40
        if tilt_output>40:
                        tilt_output=40

        pan_servo.angle(-pan_output-1)
        tilt_servo.angle(-tilt_output-3)

