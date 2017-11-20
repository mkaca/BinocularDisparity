from imutils.video import VideoStream
import time
import cv2
import numpy
import copy
from matplotlib import pyplot as plt

class ImageComparison(object):
	def __init__(self, leftImage, rightImage):
		self.leftImage = leftImage
		self.rightImage = rightImage

	def convertToGray(self, image):
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Returns array, and then size of total array
	def getPatternArray(self, img, blockSize):
		#########NOTE THAT IN THE IMG, the HEIGHT IS FIRST..... so img[Y][X]
		img = self.convertToGray(img)
		##checks if blockSize fits arraySize
		if (len(img)%blockSize != 0 or len(img[0])%blockSize != 0):
			raise AssertionError("The image size must be perfectly divisible by the blockSize...ImageSize: %i by %i" %(len(img),len(img[0])))

		completeArray = []
		
		# SOMETHING IS REVERESED YOU DUMBASS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!......last part of subArray is defs reveresed, rest of matrices might be too!
		#print ('height',len(img)) # == 480
		# width == 640
		for height in range(0,len(img),blockSize):
			for width in range(0,len(img[0]),blockSize):
				subArray = [[0 for _ in range(blockSize)] for _ in range(blockSize)]
				#print('height:',height)
				#print('width:',width)
				for blockHeight in range (blockSize):
					for blockWidth in range(blockSize):
						#print('bwidth',blockWidth)
						#print('bheight',blockHeight)
						subArray[blockHeight][blockWidth] = img[height+blockHeight][width+blockWidth]

				subArray.append([height,width])   ### This is our position coordinate
				completeArray.append(subArray)
		print (len(completeArray[0]))
		#time.sleep(1)
		#print completeArray
		#print(completeArray[1199])
		return completeArray, blockSize


	##### THIS IS THE DISPARITY CODE (NEED BETTER IMAGES FOR BETTER TESTING)
	def comparePatternToImg(self, completeArray, img, blockSize, tolerance = 3, viewRange = 15, CameraDistanceX = 0,CameraDistanceY = 0):
		img = self.convertToGray(img)
		imgForDrawing = copy.copy(img)
		if (len(img)%blockSize != 0 or len(img[0])%blockSize != 0):
			raise AssertionError("The image size must be perfectly divisible by the blockSize")
		count = 0 
		for i in range(len(completeArray)):
			#Set search boundaries
			startingPoint = copy.copy(completeArray[i][blockSize])
			startingPoint[0] = startingPoint[0] - viewRange + CameraDistanceY
			startingPoint[1] = startingPoint[1] - viewRange + CameraDistanceX
			#print ('orgBeg',startingPoint)
			if startingPoint[0] < 0:  startingPoint[0] = 0
			if startingPoint [1] < 0: startingPoint[1] = 0
			endingPoint = copy.copy(completeArray[i][blockSize])
			endingPoint[0] = endingPoint[0] + viewRange + blockSize + CameraDistanceY
			endingPoint[1] = endingPoint[1] + viewRange + blockSize + CameraDistanceX
			#print ('orgEnding',endingPoint)
			if endingPoint[0] > len(img): endingPoint[0] = len(img)
			if endingPoint[1] > len(img[0]): endingPoint[1] = len(img[0])
			#print('finalStart',startingPoint)
			#print('finalEnd',endingPoint)

			superBroken = False
			for sHeight in range(startingPoint[0],endingPoint[0]-blockSize,1):
				for sWidth in range(startingPoint[1],endingPoint[1]-blockSize,1):
					broken = False
					if superBroken:
						break
					if (abs(completeArray[i][0][0] - img[sHeight][sWidth]) < tolerance):
						#print('completearray',completeArray[i][0][0])
						#print('img',img[sHeight,sWidth])
						#print('very nice')
						successCount = 0
						#happy...keep going
						for blockWidth in range(blockSize):
							if broken or superBroken:
								break
							for blockHeight in range(blockSize):
								if (abs(completeArray[i][blockHeight][blockWidth] - img[sHeight+blockHeight][sWidth+blockWidth]) < tolerance):
									successCount = successCount +1 
									#print('very nicex 2',successCount)
								else:
									#go back to forLoop sWidth.
									broken = True
									#print ('i broke oh no')
									break
								if (successCount == blockSize*blockSize):
									count = count + 1         ### THis tells us the pattern matches!!
									superBroken = True
									cv2.rectangle(imgForDrawing,(sWidth,sHeight),(sWidth+blockSize,sHeight+blockSize),(0,255,0),3)
					#else:
						#print("what the fuck")
						#print('image value at height %i and width %i:'%(sHeight,sWidth), img[sHeight][sWidth], "complete array value at same point, height:",completeArray[i][c][d])
				if superBroken:
					break
			#print ('count:', count)
		cv2.imshow("imgForDrawing",imgForDrawing)
		cv2.waitKey(0)

								




					
				





	#def 

				



"""
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
"""
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


