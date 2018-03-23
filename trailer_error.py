import rospy
import os 
import numpy as np
import matplotlib.pyplot as plt
import rosbag
 
class trailer_analyser:

    def __init__(self, bag_file_trailer, bag_file_truck):
        self.bag_trailer = rosbag.Bag(bag_file_trailer)
        self.bag_truck = rosbag.Bag(bag_file_truck)
        self.truck_list = []
        self.trailer_list = []
        self.compare()
        self.plotter()

    def compare(self):
        for angle_msg in self.bag_truck.read_messages(topics=['/error_monitor/error_info']):
            self.truck_list.append(angle_msg.message.crosstrack_error)
        for angle_msg in self.bag_trailer.read_messages(topics=['/error_monitor/trailer_error_info']):
            self.trailer_list.append(angle_msg.message.crosstrack_error)
        for i in range(len(self.truck_list)-len(self.trailer_list)-115):
            self.truck_list.pop(0)
        self.truck_list = np.array(self.truck_list)
        self.trailer_list = np.array(self.trailer_list)+.2

    def plotter(self):
        # fig = plt.figure(figsize=(40,16))
        # ax1 = fig.add_subplot(311)
        plt.figure(figsize=(24,3))
        plt.plot(self.truck_list, 'r')
        plt.plot(self.trailer_list, 'b')
        plt.legend(['truck', 'trailer'])
        plt.title('truck trailer error monitor')
        plt.xlabel('time')
        plt.ylabel('deviation from center line (m)')
        # ax1.plot(self.truck_list, 'r')
        # ax1.plot(self.trailer_list, 'b')
        plt.grid(which="both")
        # ax1.legend(['truck', 'trailer'])
        # ax2 = fig.add_subplot(312)
        # ax2.plot(self.truck_list, 'r')
        # ax2.legend(['truck'])
        # plt.grid(which="both")
        # ax3 = fig.add_subplot(313)
        # ax3.plot(self.trailer_list, 'b')
        # ax3.legend(['trailer'])
        # plt.grid(which="both")
        plt.show()

if __name__ == "__main__":
    trailer_analyser('20180124_2.bag','2018-01-24-15-30-27.bag')

