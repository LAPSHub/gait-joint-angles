""" Module with classes and functions to analyse gait signals. """

# load modules
import os
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage


def get_angle(upper, central, lower, which_part):
    """ Calculate angles:

               a (ax,ay)

                  /
                 /
              ba/
               /
              /
    b(bx,by) /)-> @
             -------- c(cx,cy)
          bc
                           ba.bc
             @ = arccos(-----------) -> dot product of two vectors
                 |ba|*|bx|
    """
    # todo: translate variable names to english

    if upper[0] == 0 or upper[1] == 0 or central[0] == 0 or central[1] == 0 or lower[0] == 0 or lower[
        1] == 0:
        angle = 0
    else:
        v1 = upper - central
        v2 = lower - central

        if which_part == 'knee':
            reference = (-v1 / np.linalg.norm(v1)) * np.linalg.norm(v2)
            # prod_vetorial não é usado por se tratar de aplicação em 2d
            # prod_vetorial = np.linalg.norm(np.cross(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
            dot_product = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[1] > reference[1]:
                angle = np.rad2deg(dot_product - np.pi)

            else:
                angle = np.rad2deg(math.pi - dot_product)

        if which_part == 'hip':
            reference = (-v1 / np.linalg.norm(v1)) * np.linalg.norm(v2)

            # prod_vetorial não é usado por se tratar de aplicação em 2d
            # prod_vetorial = np.linalg.norm(np.cross(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
            dot_product = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[0] > reference[0]:
                angle = np.rad2deg(dot_product - np.pi)

            else:
                angle = np.rad2deg(math.pi - dot_product)

        if which_part == 'ankle':
            reference = v1[1], -v1[0]
            reference = (reference / np.linalg.norm(v1)) * np.linalg.norm(v2)

            # prod_vetorial não é usado por se tratar de aplicação em 2d
            # prod_vetorial = np.linalg.norm(np.cross(referencia, v2)) / (np.linalg.norm(referencia) * np.linalg.norm(v2))
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

def segment(data: list, indexes: list) -> list: #, string, n):
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
        # sugestão: eliminar todo o bloco
        # justificativa: não há necessidade de armazenar os segmentos !
        #
        # bloco comentado por rfz
        ## -- inserção feita pelo Clebson
        ##Necessário criar pasta angles no diretório
        ##Direciona uma pasta de destino para salvar os arquivos: Medankle_angle.npy,
        ## medhip_angle.npy e medknee_angle.npy.
        #path_name = './angles/' + str(n) + '_' + string
        #np.save(path_name, segdata)
        ## -- fim da inserção
        # 
        #x = list(range(start, finish))
        #plt.title('segmentos de um ciclo')
        #plt.plot(x, segdata, 'r')
        #plt.xlabel('frames')
        #plt.show()
        # fim de bloco comentado por rfz

    return segments



def plot(data, string, n): # is this function really necessary ?
    """ Plot data.

    Parameters
    ----------
    data : ???
        The file location of the data file
    string: str
        Description
    n: ???
        Description

    Returns
    -------
        0
    """

    x = range(len(data))
    plt.figure(n)
    plt.subplot(212)
    plt.plot(x, data)
    plt.title(string)
    plt.xlabel('frames')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()

    return 0

def read_data( path_to_data_files: str ) -> list:
    """ Read openpose data, and select anatomical points of interest for 
    futher analysis and processing.     

    Parameters
    ----------
    path_to_data_files : str
        The file location of the data file

    Returns
    -------
    anatomical_points: dict
        a dictionary of lists containing the selected anatomical points

    joint_angles: dict
        a dictionary of arrays containing the calculated joit angles
    """

    json_files = [pos_json for pos_json in sorted(os.listdir(
        path_to_data_files)) if pos_json.endswith('.json')]

    # --- rfz: traduzir comentários
    #inicializacao dos vetores que armazenam dados importantes
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

    #leitura dos dados na pasta selecionada
    # --- rfz: deve haver uma maneira mais fácil de fazer ---
    for index,js in enumerate(json_files):
        f = open(os.path.join(path_to_data_files,js),'r')
        data = f.read()
        jsondata=json.loads(data)
        
        #partes medianas
        head_x = jsondata["part_candidates"][0]["0"][0] \
            if len(jsondata["part_candidates"][0]["0"]) > 1 else 0
        head_y = jsondata["part_candidates"][0]["0"][1] \
            if len(jsondata["part_candidates"][0]["0"]) > 1 else 0

        trunk_x = jsondata["part_candidates"][0]["1"][0] \
            if len(jsondata["part_candidates"][0]["1"]) > 1 else 0
        trunk_y = jsondata["part_candidates"][0]["1"][1] \
            if len(jsondata["part_candidates"][0]["1"]) > 1 else 0

        mid_hip_x = jsondata["part_candidates"][0]["8"][0] \
            if len(jsondata["part_candidates"][0]["8"]) > 1 else 0
        mid_hip_y = jsondata["part_candidates"][0]["8"][1] \
            if len(jsondata["part_candidates"][0]["8"]) > 1 else 0
    
        #parte esquerda
        left_hip_x = jsondata["part_candidates"][0]["12"][0] \
            if len(jsondata["part_candidates"][0]["12"]) > 1 else 0
        left_hip_y = jsondata["part_candidates"][0]["12"][1] \
            if len(jsondata["part_candidates"][0]["12"]) > 1 else 0

        left_knee_x = jsondata["part_candidates"][0]["13"][0] \
            if len(jsondata["part_candidates"][0]["13"]) > 1 else 0
        left_knee_y = jsondata["part_candidates"][0]["13"][1] \
            if len(jsondata["part_candidates"][0]["13"]) > 1 else 0

        left_ankle_x = jsondata["part_candidates"][0]["14"][0] \
            if len(jsondata["part_candidates"][0]["14"]) > 1 else 0
        left_ankle_y = jsondata["part_candidates"][0]["14"][1] \
            if len(jsondata["part_candidates"][0]["14"]) > 1 else 0

        left_toe_x = jsondata["part_candidates"][0]["20"][0] \
            if len(jsondata["part_candidates"][0]["20"]) > 1 else 0
        left_toe_y = jsondata["part_candidates"][0]["20"][1] \
            if len(jsondata["part_candidates"][0]["20"]) > 1 else 0

        left_heel_x = jsondata["part_candidates"][0]["21"][0] \
            if len(jsondata["part_candidates"][0]["21"]) > 1 else 0
        left_heel_y = jsondata["part_candidates"][0]["21"][1] \
            if len(jsondata["part_candidates"][0]["21"]) > 1 else 0

        #parte direita
        right_hip_x = jsondata["part_candidates"][0]["9"][0] \
            if len(jsondata["part_candidates"][0]["9"]) > 1 else 0
        right_hip_y = jsondata["part_candidates"][0]["9"][1] \
            if len(jsondata["part_candidates"][0]["9"]) > 1 else 0

        right_knee_x = jsondata["part_candidates"][0]["10"][0] \
            if len(jsondata["part_candidates"][0]["10"]) > 1 else 0
        right_knee_y = jsondata["part_candidates"][0]["10"][1] \
            if len(jsondata["part_candidates"][0]["10"]) > 1 else 0

        right_ankle_x = jsondata["part_candidates"][0]["11"][0] \
            if len(jsondata["part_candidates"][0]["11"]) > 1 else 0
        right_ankle_y = jsondata["part_candidates"][0]["11"][1] \
            if len(jsondata["part_candidates"][0]["11"]) > 1 else 0

        right_toe_x = jsondata["part_candidates"][0]["22"][0] \
            if len(jsondata["part_candidates"][0]["22"]) > 1 else 0
        right_toe_y = jsondata["part_candidates"][0]["22"][1] \
            if len(jsondata["part_candidates"][0]["22"]) > 1 else 0

        right_heel_x = jsondata["part_candidates"][0]["24"][0] \
            if len(jsondata["part_candidates"][0]["24"]) > 1 else 0
        right_heel_y = jsondata["part_candidates"][0]["24"][1] \
            if len(jsondata["part_candidates"][0]["24"]) > 1 else 0

        #criam-se arrays para armazenar os pares de posicoes
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
        lha = get_angle(trunk, mid_hip, left_knee, 'hip')
        left_hip_angle.insert(index, lha)

        lka = get_angle(left_hip, left_knee, left_ankle, 'knee')
        left_knee_angle.insert(index, lka)

        laa = get_angle(left_knee, left_ankle, left_foot, 'ankle')
        left_ankle_angle.insert(index, laa)

        head_pos.insert(index, head[1])

        rha = 180 - get_angle(trunk, right_hip, right_knee, 'hip')
        right_hip_angle.insert(index, rha)

        rka = 180 - get_angle(right_hip, right_knee, right_ankle, 'knee')
        right_knee_angle.insert(index, rka)

        raa = 90 - get_angle(right_knee, right_ankle, right_foot, 'ankle')
        right_ankle_angle.insert(index, raa)


    # função implementa um filtro gaussiano 1-D. O desvio padrão do filtro
    # gaussiano é passado pelo parâmetro sigma]
    # rfz: Por que é feita uma filtragem aqui? Como são determinados os sigmas?
    head_pos = scipy.ndimage.gaussian_filter(head_pos, sigma=2)

    left_knee_angle = scipy.ndimage.gaussian_filter(left_knee_angle, sigma=3)
    left_hip_angle = scipy.ndimage.gaussian_filter(left_hip_angle, sigma=5)
    left_ankle_angle = scipy.ndimage.gaussian_filter(left_ankle_angle, sigma=5)

    right_knee_angle  = scipy.ndimage.gaussian_filter(right_knee_angle, sigma=5)
    right_hip_angle   = scipy.ndimage.gaussian_filter(right_hip_angle, sigma=5)
    right_ankle_angle = scipy.ndimage.gaussian_filter(right_ankle_angle, sigma=2)

    anatomical_points = {}
    anatomical_points['head'] = h
    anatomical_points['trunk'] = t
    anatomical_points['mid_hip'] = mh
    anatomical_points['left_knee'] = lk
    anatomical_points['left_hip'] = lh
    anatomical_points['left_ankle'] = la
    anatomical_points['left_foot'] = lf
    anatomical_points['left_heel'] = lh
    anatomical_points['right_knee'] = rk
    anatomical_points['right_hip'] = rh
    anatomical_points['right_ankle'] = ra
    anatomical_points['right_foot'] = rf
    anatomical_points['right_heel'] = rhe

    joint_angles = {}
    joint_angles['head'] = head_pos 
    joint_angles['left_knee'] = left_knee_angle 
    joint_angles['left_hip'] = left_hip_angle 
    joint_angles['left_ankle'] = left_ankle_angle 
    joint_angles['right_knee'] = right_knee_angle 
    joint_angles['right_hip'] = right_hip_angle 
    joint_angles['right_ankle'] = right_ankle_angle 

    return anatomical_points, joint_angles

def segmented(joint_angles: dict) -> dict :
    # avaliar melhor essas funções que usam plot associados
    # tirar o plot delas
    """ Segment data by gait cycles

    Parameters
    ----------
    joint_angles: dict
        Dictionary of lists containing joint angles

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
    # plot(left_knee_angle, "angulo do joelho esquerdo", 0)

    segmented_angles['left_hip'] = segment(left_hip_angle, leftcycles)
    # plot(left_hip_angle, "angulo do quadril esquerdo", 1)

    segmented_angles['left_ankle'] = segment(left_ankle_angle, leftcycles)
    # plot(left_ankle_angle, "angulo do tornozelo esquerdo", 2)

    segmented_angles['right_knee'] = segment(right_knee_angle, rightcycles)
    # plot(right_knee_angle,"angulo do joelho direito", 3)

    segmented_angles['right_hip'] = segment(right_hip_angle, rightcycles)
    # plot(right_hip_angle,"angulo do quadril direito", 4)

    segmented_angles['right_ankle'] = segment(right_ankle_angle, rightcycles)
    # plot(right_ankle_angle,"angulo do tornozelo direito", 5)

    return segmented_angles

def segments2matrix(segs: list, method: str = 'zeros' ) -> np.array :
    """ Convert a colection of joint segments into a single matrix.

    Parameters
    ----------
    segs: list
        List of arrays, each one of which containing a joint signal segment

    method: string
        Method used to reshape smaller segments (default=zeros: smaller 
        signals are simply filled with zeros)

    Returns
    -------
    matrix_of_segments: array
        Matrix with all segments reshaped. Each line contains a segment.
    """

    # converte arrays em lista de listas
    lst_arrays = []
    # calcula o tamanho do maior segmento
    max_length = 0
    for item in segs:
        if len(item) > max_length:
            max_length = len(item)
        lst_arrays.append(list(item))

    #print('Max length: ', max_length)

    # vefifica o método (por enquanto, preenche de zeros)
    if method == 'zeros':
        for item in lst_arrays:
            #print(item)
            if len(item) < max_length:
                diff = max_length - len(item)
                for new in range(diff):
                    item.append(0)
            #print(item)

    matrix_of_segments = np.array(lst_arrays)
    #print( matrix_of_segments.shape)
    
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
