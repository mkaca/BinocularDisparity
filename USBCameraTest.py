from imutils.video import VideoStream
import time
import cv2
import numpy as numpy

#webcam1 = VideoStream(src=0).start()
#time.sleep(1)
#print(webcam1.read())
#cv2.imshow(webcam1.read(),'gray')

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
time.sleep(1)
#rval, frame = vc.read()
#cv2.imshow('fd',frame)
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
print(rval)
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
vc.release()
cv2.destroyWindow("preview")
