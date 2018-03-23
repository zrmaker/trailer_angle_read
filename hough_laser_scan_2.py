import rosbag
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import cv2
#from PIL import Image

bag = rosbag.Bag('road_test_1.bag')
angle_increment = 0.00613592332229
angle_min = -0.521553456783
topics = bag.get_type_and_topic_info()

theta_all=[]
for msg in bag.read_messages(topics=['/scan']):
	nsecs = msg.message.header.stamp.nsecs
	secs = msg.message.header.stamp.secs
	t = secs-1.509412921e9 + nsecs/1000000000.0
	ranges = msg.message.ranges
	angle = angle_min
	image = np.zeros((180,200))
	for i in range(len(ranges)):
		x=ranges[i]*np.cos(angle)
		y=ranges[i]*np.sin(angle)
		if (x>=.2 and x<2):
			image[int(round((x-.2)*100)),int(round((y+1)*100))]+=1
		angle=angle+angle_increment

	img=np.uint8(image/np.max(image)*255)

	# 

	lines = cv2.HoughLinesP(img,1,np.pi/180,1,5,3)
	
	line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
	k=[]
	try:
		for line in lines:
			for x1,y1,x2,y2 in line:
				k=np.append(k,(y2.astype(np.float32)-y1.astype(np.float32))/(x2.astype(np.float32)-x1.astype(np.float32)))
				cv2.line(line_img, (x1, y1), (x2, y2), [0,255,255], 1)
		theta_h=np.arctan(np.mean(k))
		#theta_h=np.arctan(np.max(y2a)-np.max(y1a))/(np.max(x2a)-np.max(x1a))
		plt.imshow(line_img)
		#plt.imshow(img,cmap='Reds')
		plt.pause(0.001)
	except:
		plt.imshow(img,cmap='Reds')
		break
	print("{0:.4f}".format(np.rad2deg(theta_h)))
	theta_all=np.append(theta_all,theta_h)
	#break
plt.show()
bag.close()