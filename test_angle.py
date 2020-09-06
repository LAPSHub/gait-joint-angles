""" Example script that demonstrates how to use lapsgait module
"""
import lapsgait as lg  # loading lapsgait
import matplotlib.pyplot as plt

# path to .json files
path_to_json = './keypoints/'

# read .json data and calculate joint angles
anatomical_points, joint_angles = lg.read_data(path_to_json) # implemented, need test

# signal segmentation
segmented_angles =  lg.segment(joint_angles)

# ploting joint angles
plt.figure(1)
plt.plot(joint_angles['left_hip'], 'r')
plt.grid(True)

# ploting segmentes joint angles
plt.figure(2)
plt.hold(True)
plt.grid(True)
for item in segmented_angles['left_hip']:
    plt.plot(item, 'r')

plt.show()
