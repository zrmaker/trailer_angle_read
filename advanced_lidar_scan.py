import rosbag
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import least_squares

global angle_increment
angle_increment = 0.00613592332229
global angle_min
angle_min = -0.521553456783

def read_bag():
	return rosbag.Bag('road_test_13.bag')

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

def std_dev(adata, window_length):
	if len(adata)<window_length:
		window_length=len(adata)
	sum1=0.
	sum2=0.
	for i in range(window_length):
		sum1+=adata[i]
	mean=sum1/window_length;
	for i in range(window_length):
		sum2+=(adata[i]-mean)**2
	return np.sqrt(sum2/window_length)

def read_trailer_angle():
	bag = read_bag()
	topics = bag.get_type_and_topic_info()
	time_stamp=[]
	trailer_angle=[]
	angular_velocity=[]
	std_dev=[]
	trailer_angle_revised=[]
	for msg in bag.read_messages(topics=['/trailer_angle']):
		nsecs=msg.message.header.stamp.nsecs
		secs=msg.message.header.stamp.secs
		time_stamp=np.append(time_stamp,secs-1.507336751e9+nsecs/1000000000.0)
		trailer_angle=np.append(trailer_angle,msg.message.angle/math.pi*180)
		trailer_angle_revised=np.append(trailer_angle_revised,msg.message.angle_offset_compensation/math.pi*180)
		#angular_velocity=np.append(angular_velocity,msg.message.angular_velocity)
		std_dev=np.append(std_dev,msg.message.std_dev)
	return time_stamp,trailer_angle,std_dev,trailer_angle_revised

def least_squares_a(ranges,angle_min,angle_increment):
	x=[]
	y=[]
	x_sum=0
	y_sum=0
	xx_sum=0
	xy_sum=0
	points_count=0
	angle = angle_min
	for r in ranges:
		if np.isnan(r): 
			angle=angle+angle_increment
			continue
		x=r*np.cos(angle)
		y=r*np.sin(angle)
		x_sum+=x
		xx_sum+=x*x
		y_sum+=y
		xy_sum+=x*y
		points_count+=1
		angle=angle+angle_increment
	tmp=math.pi/2+np.arctan((points_count*xy_sum-x_sum*y_sum)/(points_count*xx_sum-x_sum*x_sum))
	if tmp>math.pi/2:
		tmp=tmp-math.pi
	return -tmp

def angle_10_degree(ranges, angle_10):
	ranges_filtered=ranges[56:112]
	angle_min_1=angle_min+56*angle_increment
	angle_f=least_squares_a(ranges_filtered,angle_min_1,angle_increment)
	angle_10=np.append(angle_10,angle_f)
	
	return angle_10

def angle_30_degree(ranges, angle_30):
	angle_f=least_squares_a(ranges,angle_min,angle_increment)
	angle_30=np.append(angle_30,angle_f)
	return angle_30

bag = read_bag()
topics = bag.get_type_and_topic_info()
'''
time_stamp=[]
angle_10=[]
angle_30=[]
for msg in bag.read_messages(topics=['/scan']):
	nsecs = msg.message.header.stamp.nsecs
	secs = msg.message.header.stamp.secs
	time_stamp = np.append(time_stamp,secs-1.507336751e9+nsecs/1000000000.0)
	ranges = msg.message.ranges
	#angle_10 = angle_10_degree(ranges,angle_10)
	angle_30 = angle_30_degree(ranges,angle_30)
	angle = angle_min
	x_all = []
	y_all = []
	image = np.zeros((180,200))
	for r in ranges:
		x_all=np.append(x_all,r*np.cos(angle))
		y_all=np.append(y_all,r*np.sin(angle))
		if (r*np.cos(angle)>=.2 and r*np.cos(angle)<2):
			image[int(round((r*np.cos(angle)-.2)*100)),int(round((r*np.sin(angle)+1)*100))]+=1
		angle=angle+angle_increment
	img=np.uint8(image/np.max(image)*255)
	#plt.imshow(image,cmap='Reds')

	#y_new=np.tan(angle_f/180*math.pi)*x_all+(y_all[0]-x_all[0]*np.tan(angle_f/180*math.pi))
	#plt.clf()
	#plt.plot(x_all,y_new,x_all,y_all)
	#plt.xlim((-1, 1))
	#plt.ylim((0, 2))
	#plt.plot(res_robust)
	#plt.pause(.001)
	#break
time_stamp = time_stamp - np.min(time_stamp)
angle_filtered=angle_30[0]

window_length=100

for i in range(1,len(angle_30)):
	if i<window_length:
		tmp=angle_30[0:i]
	else:
		tmp=angle_30[i-window_length+1:i]
	angle_filtered=np.append(angle_filtered,weighted_average(tmp, window_length))
	
	#if np.abs(angle_30[i]-angle_filtered[i])<5:
	#	if i<window_length:
	#		tmp=angle_30[0:i]-angle_filtered[0:i]
	#	else:
	#		tmp=angle_30[i-window_length+1:i]-angle_filtered[i-window_length+1:i]
	#	tmp2=weighted_average(tmp, window_length)
	#else:
	#	tmp2=angle_filtered[i]
'''
time_stamp,trailer_angle,std_dev,trailer_angle_revised=read_trailer_angle()

'''
offset_accu=[]
offset=0
angle_new=[]
window_length=100
for i in range(1,len(std_dev)):
	if std_dev[i]<.5:
		offset_accu=np.append(offset_accu,trailer_angle[i])
	if len(offset_accu)>100:
		offset_accu=offset_accu[2:101]
	offset=weighted_average(offset_accu,window_length)
	angle_new=np.append(angle_new,-offset+trailer_angle[i])
'''
'''
angle_new=[]

for i in range(1,len(trailer_angle_revised)):
	if i<100:
		tmp=trailer_angle_revised[0:i]
	else:
		tmp=trailer_angle_revised[i-100+1:i]
	angle_new=np.append(angle_new,weighted_average(tmp,100))
trailer_angle_revised=angle_new

print(np.mean(trailer_angle[5000:12000]),np.mean(trailer_angle[15000:21000]))
'''
#plt.plot(angle_10/math.pi*180)
#plt.plot(angle_filtered/math.pi*180, label="from scan")

# plt.plot(angle_new, label="new algorithm")
# plt.plot(trailer_angle_revised, label="trailer angle revised")
plt.plot(trailer_angle_revised, label="trailer angle revised")
plt.plot(trailer_angle, label="trailer angle")
#plt.plot(angle_filtered/math.pi*180, label="+-10")
#plt.plot(trailer_angle+2*std_dev, 'r--', label="Bollinger Upper Band")
#plt.plot(trailer_angle-2*std_dev, 'r--', label="Bollinger Lower Band")

# plt.plot(trailer_angle, label="+-30")

plt.plot(std_dev, label="std_dev")
# plt.figure()
# plt.plot(offset_accu)

plt.legend()
plt.show()
