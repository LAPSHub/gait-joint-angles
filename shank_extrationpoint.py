# load modules
import os
import numpy as np
import json
import pandas as pd

# path to .json files
path_to_data_files = 'C:/Users/lpinh/Downloads/projeto/lemoh012'
#path_to_data_files = 'C:/Users/Clebson/Downloads/lemoh012'


#name for the csv that will be created
file_name_csv = '012.csv'

rhx = []
rhy = []
rkx = []
rky = []
rax = []
ray = []
ra = []
rk = []
rsx = []
rsy = []
rs = []
rs_list = []

#function that calculates the x and y points of the shin
def get_pointshin(pair_10: np.array, pair_11: np.array):
    t = np.array(pair_10)
    m = np.array(pair_11)
    v = m - t
    magv = v / 3
    par_shin = pair_10 + magv
    return par_shin

# read the json files and stores all x and y points of interest
json_files = [pos_json for pos_json in sorted(os.listdir(
    path_to_data_files)) if pos_json.endswith('.json')]

for index, js in enumerate(json_files):
    f = open(os.path.join(path_to_data_files, js), 'r')
    data = f.read()
    jsondata = json.loads(data)

    right_hip_x = jsondata["part_candidates"][0]["9"][0] \
        if len(jsondata["part_candidates"][0]["9"]) > 1 else None
    right_hip_y = jsondata["part_candidates"][0]["9"][1] \
        if len(jsondata["part_candidates"][0]["9"]) > 1 else None
    right_knee_x = jsondata["part_candidates"][0]["10"][0] \
        if len(jsondata["part_candidates"][0]["10"]) > 1 else None
    right_knee_y = jsondata["part_candidates"][0]["10"][1] \
        if len(jsondata["part_candidates"][0]["10"]) > 1 else None
    right_ankle_x = jsondata["part_candidates"][0]["11"][0] \
        if len(jsondata["part_candidates"][0]["11"]) > 1 else None
    right_ankle_y = jsondata["part_candidates"][0]["11"][1] \
        if len(jsondata["part_candidates"][0]["11"]) > 1 else None

    right_ankle = np.array([right_ankle_x, right_ankle_y])
    ra.insert(index, right_ankle)
    right_knee = np.array([right_knee_x, right_knee_y])
    rk.insert(index, right_knee)

    rhy.insert(index, right_hip_y)
    rhx.insert(index, right_hip_x)
    rky.insert(index, right_knee_y)
    rkx.insert(index, right_knee_x)
    ray.insert(index, right_ankle_y)
    rax.insert(index, right_ankle_x)

par = get_pointshin(rk, ra)
rs.insert(index, par)

for item in rs[0]:
    rs_list.append(item)
L_rs = len(rs_list)

for k in range(L_rs):
    if len(rs[0][k]) <= L_rs:
        x_item = rs[0][k][0]
        y_item = rs[0][k][1]
        x_item = round(x_item, 3)
        y_item = round(y_item, 3)
        rsx.insert(k, x_item)
        rsy.insert(k, y_item)

# dataframe and csv file
anatomicals = [rhx, rhy, rkx, rky, rsx, rsy]
anatomical_points = pd.DataFrame(anatomicals).transpose()
anatomical_points.columns = ['right_hip_x', 'right_hip_y', 'right_knee_x', 'right_knee_y', 'right_shank_x', 'right_shank_y']
anatomical_points.to_csv(file_name_csv, index=False)