""" Module with classes and functions to analyse gait signals. """

# load modules
import os
import json
import math
import numpy as np
import scipy.ndimage
import pandas as pd


def get_angle(pair_1: np.array, pair_2: np.array, pair_3: np.array, 
        which_part: str)-> float:
    """Check for angles and calculate angles using direction vectors found
    with the keypoints provided by the arrays that store the pairs of positions.
    
    Parameters
    ----------
    pair_1 : array
        Upper ordered pairs extracted from .json files

    pair_2 : array
        Central ordered pairs extracted from .json files

    pair_3 : array
        Lower ordered pairs extracted from .json files

    which_part : str
        The body part under analysis

    Returns
    -------
    angle : float
        Calculated angle

    """
    # todo: translate variable names to english

    if pair_1[0] == None or pair_1[1] == None or pair_2[0] == None or pair_2[1] == None or pair_3[0] == None or pair_3[
        1] == None:
        angle = None
    else:
        v1 = pair_1 - pair_2
        v2 = pair_3 - pair_2

        if which_part == 'knee':
            reference = (-v1 / np.linalg.norm(v1)) * np.linalg.norm(v2)
            
            dot_product = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[1] > reference[1]:
                angle = np.rad2deg(dot_product - np.pi)

            else:
                angle = np.rad2deg(math.pi - dot_product)

        if which_part == 'hip':
            reference = (-v1 / np.linalg.norm(v1)) * np.linalg.norm(v2)

            
            dot_product = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[0] > reference[0]:
                angle = np.rad2deg(dot_product - np.pi)

            else:
                angle = np.rad2deg(math.pi - dot_product)

        if which_part == 'ankle':
            reference = v1[1], -v1[0]
            reference = (reference / np.linalg.norm(v1)) * np.linalg.norm(v2)


            dot_product = np.arccos(np.dot(reference, v2) / (np.linalg.norm(reference) * np.linalg.norm(v2)))

            if v2[1] < reference[1]:
                angle = -np.rad2deg(dot_product)
            else:
                angle = np.rad2deg(dot_product)
    return angle

def detect_segment(data):
    """ Find begining and ending points of gait cycles in angle signals
    by using derivatives.

    Parameters
    ----------
    data : list or array
        Joint angle signal

    Returns
    -------
    indexes: list
        Indexes indicating the gait cycles limits in data
 
    """

    a = 0
    indexes = []

    grad = np.gradient(data)
    for index, js in enumerate(grad):
        if grad[index] > 0:
            a = index
        if a != 0 and grad[index] < 0:
            indexes.insert(index, a + 1)
            a = 0

    return indexes


def segment(data: list, indexes: list) -> list:
    """ Segment complete joint angle signals according to gait cycles. 

    Parameters
    ----------
    data : list
        Joint angle signal

    indexes: list
        Indexes indicating the gait cycles limits in data

    Returns
    -------
    segments: dict
        A dictionary of lists containing the segments of joint angles
    """
    
    segments = []
    for index, js in enumerate(indexes[:-1]):
        start = indexes[index]
        finish = indexes[index + 1]
        segdata = data[start:finish]
        segments.append(segdata)

    return segments


def read_data( path_to_data_files: str ) -> list:
    """ Read openpose data, and select anatomical points of interest for 
    futher analysis and processing.     

    Parameters
    ----------
    path_to_data_files : str
        The file location of the data file

    Returns
    -------
    anatomical_points: pd.DataFrame
        a dataframe of lists containing the selected anatomical points

    joint_angles: pd.DataFrame
        a dataframe of arrays containing the calculated joit angles
    """

    json_files = [pos_json for pos_json in sorted(os.listdir(
        path_to_data_files)) if pos_json.endswith('.json')]

    # initialization of vectors that store important data
    head_pos = []

    left_hip_angle = []
    left_knee_angle = []
    left_ankle_angle = []

    right_hip_angle = []
    right_knee_angle = []
    right_ankle_angle = []

    h = []
    t = []
    mh = []
    lk = []
    lh = []
    la = []
    lf = []
    lhe = []
    rk = []
    rh = []
    ra = []
    rf = []
    rhe = []

    # read the json files
    # --- rfz: deve haver uma maneira mais fácil de fazer ---
    for index,js in enumerate(json_files):
        f = open(os.path.join(path_to_data_files,js),'r')
        data = f.read()
        jsondata=json.loads(data)
        
        # middle parts
        head_x = jsondata["part_candidates"][0]["0"][0] \
            if len(jsondata["part_candidates"][0]["0"]) > 1 else None
        head_y = jsondata["part_candidates"][0]["0"][1] \
            if len(jsondata["part_candidates"][0]["0"]) > 1 else None

        trunk_x = jsondata["part_candidates"][0]["1"][0] \
            if len(jsondata["part_candidates"][0]["1"]) > 1 else None
        trunk_y = jsondata["part_candidates"][0]["1"][1] \
            if len(jsondata["part_candidates"][0]["1"]) > 1 else None

        mid_hip_x = jsondata["part_candidates"][0]["8"][0] \
            if len(jsondata["part_candidates"][0]["8"]) > 1 else None
        mid_hip_y = jsondata["part_candidates"][0]["8"][1] \
            if len(jsondata["part_candidates"][0]["8"]) > 1 else None
    
        # left part
        left_hip_x = jsondata["part_candidates"][0]["12"][0] \
            if len(jsondata["part_candidates"][0]["12"]) > 1 else None
        left_hip_y = jsondata["part_candidates"][0]["12"][1] \
            if len(jsondata["part_candidates"][0]["12"]) > 1 else None

        left_knee_x = jsondata["part_candidates"][0]["13"][0] \
            if len(jsondata["part_candidates"][0]["13"]) > 1 else None
        left_knee_y = jsondata["part_candidates"][0]["13"][1] \
            if len(jsondata["part_candidates"][0]["13"]) > 1 else None

        left_ankle_x = jsondata["part_candidates"][0]["14"][0] \
            if len(jsondata["part_candidates"][0]["14"]) > 1 else None
        left_ankle_y = jsondata["part_candidates"][0]["14"][1] \
            if len(jsondata["part_candidates"][0]["14"]) > 1 else None

        left_toe_x = jsondata["part_candidates"][0]["20"][0] \
            if len(jsondata["part_candidates"][0]["20"]) > 1 else None
        left_toe_y = jsondata["part_candidates"][0]["20"][1] \
            if len(jsondata["part_candidates"][0]["20"]) > 1 else None

        left_heel_x = jsondata["part_candidates"][0]["21"][0] \
            if len(jsondata["part_candidates"][0]["21"]) > 1 else None
        left_heel_y = jsondata["part_candidates"][0]["21"][1] \
            if len(jsondata["part_candidates"][0]["21"]) > 1 else None

        # right part
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

        right_toe_x = jsondata["part_candidates"][0]["22"][0] \
            if len(jsondata["part_candidates"][0]["22"]) > 1 else None
        right_toe_y = jsondata["part_candidates"][0]["22"][1] \
            if len(jsondata["part_candidates"][0]["22"]) > 1 else None

        right_heel_x = jsondata["part_candidates"][0]["24"][0] \
            if len(jsondata["part_candidates"][0]["24"]) > 1 else None
        right_heel_y = jsondata["part_candidates"][0]["24"][1] \
            if len(jsondata["part_candidates"][0]["24"]) > 1 else None

        # create arrays to store pairs of positions and then add to lists
        head = np.array([head_x, head_y])
        h.insert(index, head)
        trunk = np.array([trunk_x, trunk_y])
        t.insert(index, trunk)
        mid_hip = np.array([mid_hip_x, mid_hip_y])
        mh.insert(index, mid_hip)

        left_knee = np.array([left_knee_x, left_knee_y])
        lk.insert(index, left_knee)
        left_hip = np.array([left_hip_x, left_hip_y])
        lh.insert(index, left_hip)
        left_ankle = np.array([left_ankle_x, left_ankle_y])
        la.insert(index, left_ankle)
        left_foot = np.array([left_toe_x, left_toe_y])
        lf.insert(index, left_foot)
        left_heel = np.array([left_heel_x, left_heel_y])
        lhe.insert(index, left_heel)

        right_knee = np.array([right_knee_x, right_knee_y])
        rk.insert(index, right_knee)
        right_hip = np.array([right_hip_x, right_hip_y])
        rh.insert(index, right_hip)
        right_ankle = np.array([right_ankle_x, right_ankle_y])
        ra.insert(index, right_ankle)
        right_foot = np.array([right_toe_x, right_toe_y])
        rf.insert(index, right_foot)
        right_heel = np.array([right_heel_x, right_heel_y])
        rhe.insert(index, right_heel)

        # calculam-se os angulos
        if get_angle(trunk, mid_hip, left_knee, 'hip') != None:
            lha = get_angle(trunk, mid_hip, left_knee, 'hip')
            left_hip_angle.insert(index, lha)

        if get_angle(left_hip, left_knee, left_ankle, 'knee') != None:
            lka = get_angle(left_hip, left_knee, left_ankle, 'knee')
            left_knee_angle.insert(index, lka)

        if get_angle(left_knee, left_ankle, left_foot, 'ankle') != None:
            laa = get_angle(left_knee, left_ankle, left_foot, 'ankle')
            left_ankle_angle.insert(index, laa)

        if head[1] != None:
            head_pos.insert(index, head[1])

        if get_angle(trunk, right_hip, right_knee, 'hip') != None:
            rha = 180 - get_angle(trunk, right_hip, right_knee, 'hip')
            right_hip_angle.insert(index, rha)

        if get_angle(right_hip, right_knee, right_ankle, 'knee') != None:
            rka = 180 - get_angle(right_hip, right_knee, right_ankle, 'knee')
            right_knee_angle.insert(index, rka)

        if get_angle(right_knee, right_ankle, right_foot, 'ankle') != None:
            raa = 90 - get_angle(right_knee, right_ankle, right_foot, 'ankle')
            right_ankle_angle.insert(index, raa)


    # passes the angles through a Gaussian filter (standard deviation = sigma)
    head_pos = scipy.ndimage.gaussian_filter(head_pos, sigma=2)

    left_knee_angle = scipy.ndimage.gaussian_filter(left_knee_angle, sigma=3)
    left_hip_angle = scipy.ndimage.gaussian_filter(left_hip_angle, sigma=5)
    left_ankle_angle = scipy.ndimage.gaussian_filter(left_ankle_angle, sigma=5)

    right_knee_angle = scipy.ndimage.gaussian_filter(right_knee_angle, sigma=5)
    right_hip_angle = scipy.ndimage.gaussian_filter(right_hip_angle, sigma=5)
    right_ankle_angle = scipy.ndimage.gaussian_filter(right_ankle_angle, sigma=2)

    # adds the lists in dataframes
    anatomicals = [h, t, mh, lk, lh, la, lf, lhe, rk, rh, ra, rf, rhe]
    anatomical_points = pd.DataFrame(anatomicals).transpose()
    anatomical_points.columns = ['head', 'trunk', 'midhip', 'left_knee', 'left_hip', 'left_ankle', 'left_foot',
                                 'left_heel', 'right_knee', 'right_hip', 'right_ankle', 'right_foot', 'right_heel']

    angles = [head_pos, left_knee_angle, left_hip_angle, left_ankle_angle, right_knee_angle,
              right_hip_angle, right_ankle_angle]
    joint_angles = pd.DataFrame(angles).transpose()
    joint_angles.columns = ['head', 'left_knee', 'left_hip', 'left_ankle', 'right_knee', 'right_hip', 'right_ankle']

    return anatomical_points, joint_angles


def segmented(joint_angles: pd.DataFrame ) -> dict :
    """ Segment data by gait cycles

    Parameters
    ----------
    joint_angles: pd.DataFrame
        Dataframe of lists containing joint angles

    Returns
    -------
    segmented_angles: dict
        A dictionary of lists containing segmented joint angles
    """
    # Este trecho foi colocado para criar o módulo mais rapidamente
    # Substituir por estratégias mais eficientes em versões futuras
    head_pos = joint_angles['head']
    left_knee_angle = joint_angles['left_knee']
    left_hip_angle = joint_angles['left_hip']  
    left_ankle_angle = joint_angles['left_ankle']  
    right_knee_angle = joint_angles['right_knee']  
    right_hip_angle = joint_angles['right_hip']  
    right_ankle_angle = joint_angles['right_ankle']

    leftcycles = detect_segment(left_hip_angle)
    rightcycles = detect_segment(right_hip_angle)

    segmented_angles = {}
    segmented_angles['left_knee'] = segment(left_knee_angle, leftcycles)
    segmented_angles['left_hip'] = segment(left_hip_angle, leftcycles)
    segmented_angles['left_ankle'] = segment(left_ankle_angle, leftcycles)
    segmented_angles['right_knee'] = segment(right_knee_angle, rightcycles)
    segmented_angles['right_hip'] = segment(right_hip_angle, rightcycles)
    segmented_angles['right_ankle'] = segment(right_ankle_angle, rightcycles)

    return segmented_angles


def segments2matrix(segs: list, method: str = 'cut') -> np.array:
    """ Convert a colection of joint segments into a single matrix.

    Parameters
    ----------
    segs: list
        List of arrays, each one of which containing a joint signal segment

    method: string
        Method used to reshape segments:
            'zeros': segments are filled with zeros until the size of the 
                    largest segment; 
            'cut': segments are cropped to match the size of the smallest
                    segment

    Returns
    -------
    matrix_of_segments: array
        Matrix with all segments reshaped. Each line contains a segment.
    """

    # converts arrays into lists
    lst_arrays = []
    # calculates the size of the largest segment
    max_length = 0
    for item in segs:
        if len(item) > max_length:
            max_length = len(item)
        lst_arrays.append(list(item))

    # print('Max length: ', max_length)

    # calculates the size of the smallest segment
    min_length = max_length
    for item in segs:
        if len(item) < min_length:
            min_length = len(item)

    # vefifica o método (por enquanto, preenche de zeros)
    if method == 'zeros':
        for item in lst_arrays:
            # print(item)
            if len(item) < max_length:
                diff = max_length - len(item)
                for new in range(diff):
                    item.append(0)
            # print(item)

    # cuts excess elements
    if method == 'cut':
        for item in lst_arrays:
            if len(item) > min_length:
                diff = len(item) - min_length
                for cut in range(diff):
                    item.pop()

    matrix_of_segments = np.array(lst_arrays)
    # print( matrix_of_segments.shape)

    return matrix_of_segments


def stats( segments: dict ) -> dict: #old medias  
    """ Calculate the average and the standard deviation of joint 
        angle segments.

    Parameters
    ----------
    segments: array
        Matrix containing segments (each line) of a joint angle signals

    Returns
    -------
    avg_signal: dictionaty of list
        A dictionary of lists with the average of the input segments

    std_signal: dictionaty of list
        A dictionary of lists with the standard deviation of the input segments
    """

    avg_signal = {}
    std_signal = {}
    for joint_angle in segments:
        # convert segments[joint_angle] into matrix
        seg_matrix = segments2matrix(segments[joint_angle])
        # calculate average and standard deviation 
        avg_signal[joint_angle] = np.mean(seg_matrix, axis = 0)
        std_signal[joint_angle] = np.std(seg_matrix, axis = 0)

    return avg_signal, std_signal
