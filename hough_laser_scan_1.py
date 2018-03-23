import rosbag
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

def hough_transform(img):
	thetas = np.deg2rad(np.arange(30.0, 150.0, 1))
	width, height = img.shape
	diag_len = np.ceil(np.sqrt(width * width + height * height))
	rhos = np.linspace(-diag_len, diag_len, diag_len * 2.0)

	cos_t = np.cos(thetas)
	sin_t = np.sin(thetas)
	num_thetas = len(thetas)

	accumulator = np.zeros((int(2 * diag_len), num_thetas), dtype=np.uint64)
	y_idxs, x_idxs = np.nonzero(img)

	for i in range(len(x_idxs)):
		x = x_idxs[i]
		y = y_idxs[i]
		for t_idx in range(num_thetas):
			rho = int(round(x * cos_t[t_idx] + y * sin_t[t_idx]) + diag_len)
			accumulator[rho, t_idx] += 1

	return accumulator, thetas, rhos


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

bag =rosbag.Bag('road_test_1.bag')
angle_increment=0.00613592332229
angle_min=-0.521553456783
topics = bag.get_type_and_topic_info()

image=np.zeros((180,200))
for msg in bag.read_messages(topics=['/scan']):
	nsecs=msg.message.header.stamp.nsecs
	secs=msg.message.header.stamp.secs
	t=secs-1.509412921e9+nsecs/1000000000.0
	ranges=msg.message.ranges
	angle=angle_min
	for i in range(len(ranges)):
		x=ranges[i]*np.cos(angle)
		y=ranges[i]*np.sin(angle)
		if (x>=.2 and x<2):
			image[int(round((x-.2)*100)),int(round((y+1)*100))]+=1
		angle=angle+angle_increment
	#plt.imshow(image,cmap='Reds')
	accumulator, thetas, rhos = hough_transform(image)
	idx = np.argmax(accumulator)
	rho = rhos[idx / accumulator.shape[1]] / 100
	theta = thetas[idx % accumulator.shape[1]] - np.deg2rad(90.)
	print("{0:.4f}, {1:.4f}".format(t, theta))
	#plt.imshow(accumulator,cmap='Reds')
	#angle_accumulator=np.sum(accumulator,axis=1)
	#plt.plot(rhos,angle_accumulator)
	#break
plt.show()
bag.close()