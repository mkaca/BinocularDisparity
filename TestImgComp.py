from ImageComparison import ImageComparison as imgComp
import cv2
import time
from matplotlib import pyplot as plt

"""webcamSize = 300
vc = cv2.VideoCapture(0) # pc webcam
vc2 = cv2.VideoCapture(1) #usb 1
#vc2.set(3,webcamSize)
#vc2.set(4,webcamSize)
vc3 = cv2.VideoCapture(2) #usb 2
#vc3.set(3,webcamSize)
#vc3.set(4,webcamSize)
time.sleep(1)

print("Starting to take pictures")
frame2 = vc2.read()[1]
frame3 = vc3.read()[1]
print("Finishing taking pictures")
cv2.imwrite('LeftLarge.png',frame3)
cv2.imwrite('RightLarge.png',frame2)"""
start = time.time()
leftImg = cv2.imread("LeftLarge.png")
rightImg = cv2.imread("RightLarge.png")
blockSize = 2
leftImg = cv2.GaussianBlur(leftImg,(7,7),0)
rightImg = cv2.GaussianBlur(rightImg,(7,7),0)

comp = imgComp(leftImg, rightImg)
array = comp.getPatternArray(leftImg,blockSize)[0]
#print array
leftGrey = cv2.cvtColor(leftImg, cv2.COLOR_BGR2GRAY)
rightGrey = cv2.cvtColor(rightImg, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(leftGrey,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(leftImg, contours, -1, (0,255,0), 3)
#cv2.imshow('taa',leftGrey)
#cv2.imshow('taa',leftImg)
#cv2.waitKey(0)

#comp.comparePatternToImg(array,rightImg,blockSize, viewRange = 1, tolerance = 15, \
	#CameraDistanceX = -13, CameraDistanceY = 10)

stereo = cv2.createStereoBM(numDisparities=16, blockSize=5)
disparity = stereo.compute(leftGrey,rightGrey)
plt.imshow(disparity,'gray')
plt.show()


end = time.time()
print ("FINISHED: RUN TIME:", end-start)

### calculate proper cameraDistance and test with code 

### NEXT MAKE some equations for occlusion
    ## Group objects together by color i guess 
  ### segregate each contour, and then match contours of the exact same color to be one plane, 
  #####if plane is interrupted, then it means it's behind???? but by how much dafuq