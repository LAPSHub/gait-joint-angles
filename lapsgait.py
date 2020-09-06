""" Module with classes and functions to analyse gait signals. """

# load modules
import os,json
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

def get_angle(superior,central,inferior,qual_parte):
    """ Funcao para calcular angulos:
    
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
	         @ = arccos(-----------) -> produto escalar de dois vetores
			     |ba|*|bx|
    """

    if superior[0] == 0 or superior[1]==0 or central[0] == 0 or central[1]==0 or inferior[0]==0 or inferior[1] == 0:
        angulo = 0
    else:
        v1 = superior - central
        v2 = inferior - central

        if qual_parte == 'joelho':
            referencia = (-v1/np.linalg.norm(v1))*np.linalg.norm(v2)
            # prod_vetorial não é usado por se tratar de aplicação em 2d
            #prod_vetorial = np.linalg.norm(np.cross(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
            prod_escalar = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            
            if v2[1]>referencia[1]:
                angulo = np.rad2deg(prod_escalar - np.pi)

            else:
                angulo = np.rad2deg(math.pi - prod_escalar)

        if qual_parte == 'quadril':
            referencia = (-v1/np.linalg.norm(v1))*np.linalg.norm(v2)

            #prod_vetorial não é usado por se tratar de aplicação em 2d
            #prod_vetorial = np.linalg.norm(np.cross(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
            prod_escalar = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[0]>referencia[0]:
                angulo = np.rad2deg(prod_escalar - np.pi)

            else:
                angulo =  np.rad2deg(math.pi - prod_escalar)

        if qual_parte == 'tornozelo':
            referencia = v1[1],-v1[0]
            referencia = (referencia/np.linalg.norm(v1))*np.linalg.norm(v2)

            # prod_vetorial não é usado por se tratar de aplicação em 2d
            prod_vetorial = np.linalg.norm(np.cross(referencia,v2))/(np.linalg.norm(referencia)*np.linalg.norm(v2))
            prod_escalar = np.arccos(np.dot(referencia, v2) / (np.linalg.norm(referencia) * np.linalg.norm(v2)))

            if v2[1]<referencia[1]:
                angulo = -np.rad2deg(prod_escalar)
            else:
                angulo = np.rad2deg(prod_escalar)
    return angulo

def detecta_segmento(data):
    """ Funcao que pega os dados dos angulos e tenta segmenta-los por meio de 
    relacoes de derivadas, ele retorna os indices para inicio/fim de cada ciclo
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
    #print(len(indexes) - 1)
    return indexes

def segmenta(data: list, indexes: list) -> list: #, string, n):
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
        a list of lists containing the segments of joint angles
    """
    
    segments = []
    for index, js in enumerate(indexes[:-1]):
        start = indexes[index]
        finish = indexes[index + 1]
        #print(start, finish)
        segdata = data[start:finish]

        segments.append(segdata)
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
        a dictionary of lists containing the calculated joit angles
    """

    json_files = [pos_json for pos_json in sorted(os.listdir(
        path_to_data_files)) if pos_json.endswith('.json')]

    #inicializacao dos vetores que armazenam dados importantes
    head_pos = []
    
    left_hip_angle = []
    left_knee_angle = []
    left_ankle_angle = []

    right_hip_angle = []
    right_knee_angle = []
    right_ankle_angle = []

    #leitura dos dados na pasta selecionada
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

        mid_hip_x = jsondata["part_candidates"][0]["8"][0]\
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
        left_ankle_y = jsondata["part_candidates"][0]["14"][1]\
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
        head = np.array([head_x,head_y])
        trunk = np.array([trunk_x,trunk_y])
        mid_hip = np.array([mid_hip_x,mid_hip_y])

        left_knee = np.array([left_knee_x,left_knee_y])
        left_hip = np.array([left_hip_x,left_hip_y])
        left_ankle = np.array([left_ankle_x,left_ankle_y])
        left_foot = np.array([left_toe_x,left_toe_y])
        left_heel = np.array([left_heel_x,left_heel_y])

        right_knee = np.array([right_knee_x,right_knee_y])
        right_hip = np.array([right_hip_x,right_hip_y])
        right_ankle = np.array([right_ankle_x,right_ankle_y])
        right_foot = np.array([right_toe_x,right_toe_y])
        right_heel = np.array([right_heel_x,right_heel_y])

        #calculam-se os angulos
        lha = get_angle(trunk,mid_hip,left_knee,'quadril')
        left_hip_angle.insert(index,lha)

        lka = get_angle(left_hip,left_knee,left_ankle,'joelho')
        left_knee_angle.insert(index,lka)

        laa = get_angle(left_knee,left_ankle,left_foot,'tornozelo')
        left_ankle_angle.insert(index,laa)

        #rka = 180 - get_angle(right_hip,right_knee,right_ankle)
        #right_knee_angle.insert(index,rka)

        head_pos.insert(index,head[1])

        rha = 180 - get_angle(trunk, right_hip, right_knee, 'quadril')
        right_hip_angle.insert(index, rha)

        rka = 180 - get_angle(right_hip, right_knee, right_ankle, 'joelho')
        right_knee_angle.insert(index, rka)

        raa = 90 - get_angle(right_knee, right_ankle, right_foot, 'tornozelo')
        right_ankle_angle.insert(index, raa)

    left_knee_angle  = scipy.ndimage.gaussian_filter(left_knee_angle,sigma = 3)
    left_hip_angle   = scipy.ndimage.gaussian_filter(left_hip_angle,sigma = 5)
    left_ankle_angle = scipy.ndimage.gaussian_filter(left_ankle_angle,sigma = 5)


    head_pos=  scipy.ndimage.gaussian_filter(head_pos,sigma = 2)

    # função implementa um filtro gaussiano 1-D. O desvio padrão do filtro 
    # gaussiano é passado pelo parâmetro sigma
    left_knee_angle = scipy.ndimage.gaussian_filter(left_knee_angle, sigma=3)
    left_hip_angle = scipy.ndimage.gaussian_filter(left_hip_angle, sigma=5)
    left_ankle_angle = scipy.ndimage.gaussian_filter(left_ankle_angle, sigma=5)

    right_knee_angle  = scipy.ndimage.gaussian_filter(right_knee_angle, sigma=5)
    right_hip_angle   = scipy.ndimage.gaussian_filter(right_hip_angle, sigma=5)
    right_ankle_angle = scipy.ndimage.gaussian_filter(right_ankle_angle,sigma=2)

    anatomical_points = {}
    anatomical_points['head'] = head
    anatomical_points['trunck'] = trunk
    anatomical_points['mid_hip'] = mid_hip
    anatomical_points['left_knee'] = left_knee
    anatomical_points['left_hip'] = left_hip
    anatomical_points['left_ankle'] = left_ankle
    anatomical_points['left_foot'] = left_foot
    anatomical_points['left_heel'] = left_heel
    anatomical_points['right_knee'] = right_knee
    anatomical_points['right_hip'] = right_hip
    anatomical_points['right_ankle'] = right_ankle
    anatomical_points['right_foot'] = right_foot
    anatomical_points['right_heel'] = right_heel

    joint_angles = {}
    joint_angles['head'] = head_pos 
    joint_angles['left_knee'] = left_knee_angle 
    joint_angles['left_hip'] = left_hip_angle 
    joint_angles['left_ankle'] = left_ankle_angle 
    joint_angles['right_knee'] = right_knee_angle 
    joint_angles['right_hip'] = right_hip_angle 
    joint_angles['right_ankle'] = right_ankle_angle 

    return anatomical_points, joint_angles

def segment(joint_angles: dict) -> dict : 
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
    
    
    leftciclos = detecta_segmento(left_hip_angle)
    rightciclos = detecta_segmento(right_hip_angle)

    segmented_angles = {}
    segmented_angles['left_knee'] = segmenta(left_knee_angle, leftciclos)
    #plot(left_knee_angle, "angulo do joelho esquerdo", 0)

    segmented_angles['left_hip'] = segmenta(left_hip_angle, leftciclos)
    #plot(left_hip_angle, "angulo do quadril esquerdo", 1)

    segmented_angles['left_ankle'] = segmenta(left_ankle_angle, leftciclos)
    #plot(left_ankle_angle, "angulo do tornozelo esquerdo", 2)

    segmented_angles['right_knee'] = segmenta(right_knee_angle, rightciclos)
    #plot(right_knee_angle,"angulo do joelho direito", 3)

    segmented_angles['right_hip'] = segmenta(right_hip_angle, rightciclos)
    #plot(right_hip_angle,"angulo do quadril direito", 4)

    segmented_angles['right_ankle'] = segmenta(right_ankle_angle, rightciclos)
    #plot(right_ankle_angle,"angulo do tornozelo direito", 5)

    return segmented_angles

def segments2matrix(segs: list, method: str = 'zeros' ) -> np.array :
    """ Todo

    Parameters
    ----------
    segs: list
        Todo

    method: string
        Todo

    Returns
    -------
    matrix_of_segments: array
        Todo
    """

    # converte arrays em lista de listas
    lst_arrays = []
    # calcula o tamanho do maior segmento
    max_length = 0
    for item in segs:
        if len(item) > max_length:
            max_length = len(item)
        lst_arrays.append(list(item))

    # vefifica o método (por enquanto, preenche de zeros)
    if method == 'zeros':
        for item in lst_arrays:
            #print(item)
            if len(item) < max_length:
                diff = max_length - len(item)
                for new in range(diff):
                    item.append(0)

    matrix_of_segments = np.array(segs)
    print( matrix_of_segments.shape)
    
    return matrix_of_segments

def average( segments: dict ) -> dict: #old medias  
    """ Calculate the average of joint angle segments

    Parameters
    ----------
    segments: dict
        Dictionary of lists containing segments of a joint angle signals

    Returns
    -------
    avg_signal: dictionaty of list
        A dictionary of lists with the average of the input segments
    """

    avg_signal = {} 
    for joint_angle in segments:
        # converte segments[joint_angle] em matriz
        seg_matrix = segments2matrix(segments[joint_angle])
        # calcula a média 
        avg_signal[joint_angle] = np.mean(seg_matrix)

    print(avg_signal)

    #a = []


    #a_t = []
    #med = []
    #s = []
    #std = []
    #data_files = [files for files in sorted(os.listdir(path)) if files.endswith(string)]
    #for index, af in enumerate(data_files):
    #    f = np.load(os.path.join(path, af), 'r')
    #    # inserindo os dados numa lista temporaria
    #    a.insert(index, f)
    #    # transpondo a lista temp
    #    a_t = list(map(list, zip(*a)))

    ## calculando as medias
    #for i1 in range(len(list(a_t))):
    #    i = []
    #    for i2 in range(len(list(a_t[i1]))):
    #        i.insert(i1, a_t[i1][i2])
    #        media = np.mean(i)
    #    # inserindo as medias numa lista nova
    #    med.insert(i1, media)

    #for i1 in range(len(list(a_t))):
    #    for i2 in range(len(list(a_t[i1]))):
    #        a1 = a_t[i1][i2] - med[i2]
    #        a1 = math.pow(a1, 2)
    #        s.insert(i1, a1)
    #    b = len(s)
    #    s = sum(s)
    #    s = s / b
    #    s = math.sqrt(s)
    #    std.insert(i1, s)
    #    s = []
    return 0 #(med, std)


