""" Assess joint angles from json files
"""

# path to .json files
path_to_json = './keypoints/'

# read .json data
anatomical_points, joint_angles = read_data(path_to_json) # implemented, need test

# signal segmentation
segmented_angles =  segment(joint_angles)

# ploting

