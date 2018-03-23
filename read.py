import rosbag
import numpy as np
import matplotlib.pyplot as plt
import math

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

bag =rosbag.Bag('2017-10-26-13-45-51.bag')
topics = bag.get_type_and_topic_info()
#print(topics)
t=[]
angle=[]
angle_speed=[]
for msg in bag.read_messages(topics=['/trailer_angle']):
	#print (msg.message.header.stamp.nsecs)
	nsecs=msg.message.header.stamp.nsecs
	secs=msg.message.header.stamp.secs
	t=np.append(t,secs-1.507336751e9+nsecs/1000000000.0)
	angle=np.append(angle,msg.message.angle)
	#angle_speed=np.append(angle_speed,msg.message.angle_velocity)
angle_filtered=angle[1]
window_length=40
for i in range(1,len(angle)):
	if i<window_length:
		tmp=angle[0:i]
	else:
		tmp=angle[i-window_length:i]
	angle_filtered=np.append(angle_filtered,weighted_average(tmp,window_length))
angle_filtered2=angle_filtered[1]
window_length=100
for i in range(1,len(angle_filtered)):
	if i<window_length:
		tmp=angle_filtered[0:i]
	else:
		tmp=angle_filtered[i-window_length:i]
	angle_filtered2=np.append(angle_filtered2,weighted_average(tmp,window_length))

angle_speed_cal=[]
window_length=1
print(len(t),len(angle),len(angle_filtered),len(angle_filtered2))
for i in range(2,len(t)):
	tmp=[]
	if i<=window_length:
		for j in range(1,i):
			tmp=np.append(tmp,(angle_filtered2[i]-angle_filtered2[j-1])/(t[i]-t[j-1]))
	else:
		for j in range(i-window_length,i):
			tmp=np.append(tmp,(angle_filtered2[i]-angle_filtered2[j-1])/(t[i]-t[j-1]))
	angle_speed_cal=np.append(angle_speed_cal,weighted_average(tmp,window_length))

plt.plot(t,angle_filtered2/math.pi*180)
plt.plot(t[1:len(t)-1],angle_speed_cal/math.pi*180)
plt.show()
bag.close()
