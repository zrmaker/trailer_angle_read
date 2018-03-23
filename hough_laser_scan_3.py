import rosbag
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import cv2
#from PIL import Image

def weighted_average(adata, window_length):
	if len(adata)<window_length:
		window_length=len(adata)
	weight=1.
	wsum=0.
	tsum=0.
	for i in range(window_length):
		tsum=tsum+adata[i]*weight
		wsum=wsum+weight
		#weight=math.exp(math.log(weight)+1)
		weight=(math.sqrt(weight)+.001)**2
		#weight=weight+1
	return tsum/wsum

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
	#plt.imshow(image,cmap='Reds')
	#theta = hough_transform_find_theta(image)
	img=np.uint8(image/np.max(image)*255)
	#print(edges.dtype)
	lines = cv2.HoughLines(img,1,np.pi/1800,1)
	
	k=[]
	theta_a=[]
	try:
		for rho,theta in lines[0]:
			theta_a=np.append(theta_a,theta)
		print(theta_a.shape)
		theta_h=np.mean(theta_a)
	except:
	#if theta-last_theta > 60:
	#	theta = theta-90
	#elif last_theta-theta > 60:
	#	theta = theta+90
	#last_theta = theta
	#print("{0:.4f}, {1:.4f}".format(t, np.rad2deg(theta)))
		plt.imshow(img,cmap='Reds')
		break
	print("{0:.4f}".format(np.rad2deg(theta_h)))
	theta_all=np.append(theta_all,theta_h)
	#break
plt.show()
bag.close()