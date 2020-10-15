""" Example script that demonstrates how to use lapsgait module
"""
import lapsgait as lg  # loading lapsgait
import matplotlib.pyplot as plt

# path to .json files
path_to_json = './keypoints/v03'

# read .json data and calculate joint angles
anatomical_points, joint_angles = lg.read_data(path_to_json) #implemented, need test

# signal segmentation
segmented_angles =  lg.segmented(joint_angles)

# average signals
averaged_signals, standard_deviation_signals = lg.stats(segmented_angles)

joint = 'left_hip'
# ploting joint angles
plt.figure(1)
plt.plot(joint_angles[joint], 'r')
plt.grid(True)
plt.title('Complete '+ joint)
plt.xlabel('Samples')
plt.ylabel('Angles')

# ploting segmented joint angles
plt.figure(2)
#plt.hold(True)
plt.grid(True)
for item in segmented_angles[joint]:
    plt.plot(item, 'r')
plt.title('Segments of '+ joint)
plt.xlabel('Samples')
plt.ylabel('Angles')

plt.figure(3)
#plt.hold(True)
plt.grid(True)
plt.plot(averaged_signals[joint],'b')
plt.title('Average of '+ joint)
plt.xlabel('Samples')
plt.ylabel('Angles')

plt.show()
