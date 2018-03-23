import rosbag
import numpy as np
import matplotlib.pyplot as plt
import math

bag =rosbag.Bag('road_test_6.bag')
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
	angle=np.append(angle,msg.message.angle/math.pi*180)
	angle_speed=np.append(angle_speed,msg.message.angular_velocity)
angle_speed_cal=[]
for i in range(len(t)-1):
	angle_speed_cal=np.append(angle_speed_cal,(angle[i+1]-angle[i])/(t[i+1]-t[i]))

plt.plot(t,angle)
#plt.plot(t[1:len(t)],angle_speed_cal)
plt.show()
bag.close()
