from imutils.video import VideoStream
import time
import cv2
import numpy
from matplotlib import pyplot as plt


numpy.core.arrayprint._line_width = 1100
numpy.set_printoptions(edgeitems=300)
webcamSize = 300

vc = cv2.VideoCapture(0) # pc webcam

vc2 = cv2.VideoCapture(1) #usb 1
vc2.set(3,webcamSize)
vc2.set(4,webcamSize)

vc3 = cv2.VideoCapture(2) #usb 2
vc3.set(3,webcamSize)
vc3.set(4,webcamSize)

time.sleep(2)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
print(rval)

if vc3.isOpened(): # try to get the first frame
    rval3, frame3 = vc3.read()
else:
    rval3 = False
print(rval3)

if vc2.isOpened(): # try to get the first frame
    rval2, frame2 = vc2.read()
else:
    rval2 = False
print(rval2)

cv2.imwrite('Left.png',frame3)
cv2.imwrite('Right.png',frame2)

stereo = cv2.createStereoBM(numDisparities=64, blockSize=25)
#stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
frame2_new=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
frame3_new=cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)



#print(frame2_new)
#print('')
#print(frame3_new)
disparity = stereo.compute(frame3_new,frame2_new)
plt.imshow(disparity,'gray')
plt.show()

## GOt my left and right frame......

## TRY APPLYING PIXEL SHIFTING COMPARISON....# geometry for left and right image pixel difference which will give depth
	# Larger pixel shift == object is closer 
	##### NEed to have larger resolution for this.... try maxing it out. like 450 or something

""" NOw need to apply :
     Monocular:
      1. SHadows
      2. Relative Size
      3. Blurry = further away
     Binocular:
      4. Occlusion (object hidden behind another)
      5. Pattern in image A that is missing in image B
   While moving :
            get rate of deletion and accretion
   For best results, get something in the image of known size"""


