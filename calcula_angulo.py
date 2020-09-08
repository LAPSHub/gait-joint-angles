#codigo para extacao de angulos a partir de arquivos do tipo .json armazenados pelo openpose
#------------------------------------------------------------------------------------
#bibliotecas
import os,json
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

#------------------------------------------------------------------------------------
#funcao para calcular angulos seguindo:
#
# 					   a (ax,ay)
#                  /
#                 /
#              ba/
#               /
#              /
#    b(bx,by) /)-> @
#             -------- c(cx,cy)
# 					  bc
#
# 				        (ba.bc)
#		 @ = arccos(-----------) -> produto escalar de dois vetores
#						(|ba|*|bx|)
#------------------------------------------------------------------------------------
#a seguinte funcao pega 3 pontos p(x,y),o primeiro corresponde ao membro mais alto,o segundo e o medio e o terceiro o mais baixo
def get_angle(superior,central,inferior,qual_parte):
    if superior[0] == 0 or superior[1] == 0 or central[0] == 0 or central[1] == 0 or inferior[0] == 0 or inferior[1] == 0:
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

            # prod_vetorial não é usado por se tratar de aplicação em 2d
            #prod_vetorial = np.linalg.norm(np.cross(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
            prod_escalar = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            if v2[0]>referencia[0]:
                angulo = np.rad2deg(prod_escalar - np.pi)

            else:
                angulo = np.rad2deg(math.pi - prod_escalar)

        if qual_parte == 'tornozelo':
            referencia = v1[1],-v1[0]
            referencia = (referencia/np.linalg.norm(v1))*np.linalg.norm(v2)

            # prod_vetorial não é usado por se tratar de aplicação em 2d
            #prod_vetorial = np.linalg.norm(np.cross(referencia,v2))/(np.linalg.norm(referencia)*np.linalg.norm(v2))
            prod_escalar = np.arccos(np.dot(referencia, v2) / (np.linalg.norm(referencia) * np.linalg.norm(v2)))

            if v2[1]<referencia[1]:
                angulo = -np.rad2deg(prod_escalar)
            else:
                angulo = np.rad2deg(prod_escalar)
    return angulo
#------------------------------------------------------------------------------------
#funcao que pega os dados dos angulos e tenta segmenta-los por meio de relacoes de derivadas, ele retorna os indices para inicio/fim de cada ciclo
def detecta_segmento(data):
    a = 0
    indexes = []

    grad = np.gradient(data)
    for index, js in enumerate(grad):
        if grad[index] > 0:
            a = index
        if a != 0 and grad[index] < 0:
            indexes.insert(index, a + 1)
            a = 0
    print(len(indexes) - 1)
    return indexes


# ------------------------------------------------------------------------------------
# funcao que pega os dados dos angulos e da segmentacao para retornar as listas segmentadas
def segmenta(data, indexes, string, n):
    arrayT = []
    for index, js in enumerate(indexes[:-1]):
        start = indexes[index]
        finish = indexes[index + 1]
        print(start, finish)
        segdata = data[start:finish]

        # -- inserção feita pelo Clebson
        #Necessário criar pasta angles no diretório
        #Direciona uma pasta de destino para salvar os arquivos
        path_name = './angles/' + string
        arrayT.append(segdata)
        a_t = list(map(list, zip(*arrayT)))
        np.save(path_name, a_t)
        # -- fim da inserção

        x = list(range(start, finish))
        plt.title('segmentos de um ciclo')
        plt.plot(x, segdata, 'r')
        plt.xlabel('frames')
        plt.show()


# ------------------------------------------------------------------------------------
# funcao para plotagem
def plot(data, string, n):
    x = range(len(data))
    plt.figure(n)
    plt.subplot(212)
    plt.plot(x, data)
    plt.title(string)
    plt.xlabel('frames')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()


# ------------------------------------------------------------------------------------
# leitura dos arquivos .json na pasta indicada
path_to_json = './keypoints/'
json_files = [pos_json for pos_json in sorted(os.listdir(path_to_json)) if pos_json.endswith('.json')]

#------------------------------------------------------------------------------------
#inicializacao dos vetores que armazenam dados importantes
head_pos = []

left_hip_angle = []
left_knee_angle = []
left_ankle_angle = []

right_hip_angle = []
right_knee_angle = []
right_ankle_angle = []
#------------------------------------------------------------------------------------
#incializacao das variaveis que armazenarao os angulos dos membros inferiores

#------------------------------------------------------------------------------------
#leitura dos dados na pasta selecionada
for index,js in enumerate(json_files):
    f = open(os.path.join(path_to_json,js),'r')
    data = f.read()
    jsondata=json.loads(data)
    #-----------------------------------------------------------------------------------
    #partes medianas
    head_x = jsondata["part_candidates"][0]["0"][0] if len(jsondata["part_candidates"][0]["0"]) > 1 else 0
    head_y = jsondata["part_candidates"][0]["0"][1] if len(jsondata["part_candidates"][0]["0"]) > 1 else 0

    trunk_x = jsondata["part_candidates"][0]["1"][0] if len(jsondata["part_candidates"][0]["1"]) > 1 else 0
    trunk_y = jsondata["part_candidates"][0]["1"][1] if len(jsondata["part_candidates"][0]["1"]) > 1 else 0

    mid_hip_x = jsondata["part_candidates"][0]["8"][0] if len(jsondata["part_candidates"][0]["8"]) > 1 else 0
    mid_hip_y = jsondata["part_candidates"][0]["8"][1] if len(jsondata["part_candidates"][0]["8"]) > 1 else 0
    #-----------------------------------------------------------------------------------
    #parte esquerda
    left_hip_x = jsondata["part_candidates"][0]["12"][0] if len(jsondata["part_candidates"][0]["12"]) > 1 else 0
    left_hip_y = jsondata["part_candidates"][0]["12"][1] if len(jsondata["part_candidates"][0]["12"]) > 1 else 0

    left_knee_x = jsondata["part_candidates"][0]["13"][0] if len(jsondata["part_candidates"][0]["13"]) > 1 else 0
    left_knee_y = jsondata["part_candidates"][0]["13"][1] if len(jsondata["part_candidates"][0]["13"]) > 1 else 0

    left_ankle_x = jsondata["part_candidates"][0]["14"][0] if len(jsondata["part_candidates"][0]["14"]) > 1 else 0
    left_ankle_y = jsondata["part_candidates"][0]["14"][1] if len(jsondata["part_candidates"][0]["14"]) > 1 else 0

    left_toe_x = jsondata["part_candidates"][0]["20"][0] if len(jsondata["part_candidates"][0]["20"]) > 1 else 0
    left_toe_y = jsondata["part_candidates"][0]["20"][1] if len(jsondata["part_candidates"][0]["20"]) > 1 else 0

    left_heel_x = jsondata["part_candidates"][0]["21"][0] if len(jsondata["part_candidates"][0]["21"]) > 1 else 0
    left_heel_y = jsondata["part_candidates"][0]["21"][1] if len(jsondata["part_candidates"][0]["21"]) > 1 else 0
    #-----------------------------------------------------------------------------------
    #parte direita
    right_hip_x = jsondata["part_candidates"][0]["9"][0] if len(jsondata["part_candidates"][0]["9"]) > 1 else 0
    right_hip_y = jsondata["part_candidates"][0]["9"][1] if len(jsondata["part_candidates"][0]["9"]) > 1 else 0

    right_knee_x = jsondata["part_candidates"][0]["10"][0] if len(jsondata["part_candidates"][0]["10"]) > 1 else 0
    right_knee_y = jsondata["part_candidates"][0]["10"][1] if len(jsondata["part_candidates"][0]["10"]) > 1 else 0

    right_ankle_x = jsondata["part_candidates"][0]["11"][0] if len(jsondata["part_candidates"][0]["11"]) > 1 else 0
    right_ankle_y = jsondata["part_candidates"][0]["11"][1] if len(jsondata["part_candidates"][0]["11"]) > 1 else 0

    right_toe_x = jsondata["part_candidates"][0]["22"][0] if len(jsondata["part_candidates"][0]["22"]) > 1 else 0
    right_toe_y = jsondata["part_candidates"][0]["22"][1] if len(jsondata["part_candidates"][0]["22"]) > 1 else 0

    right_heel_x = jsondata["part_candidates"][0]["24"][0] if len(jsondata["part_candidates"][0]["24"]) > 1 else 0
    right_heel_y = jsondata["part_candidates"][0]["24"][1] if len(jsondata["part_candidates"][0]["24"]) > 1 else 0
    #-----------------------------------------------------------------------------------
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

    #-----------------------------------------------------------------------------------
    #calculam-se os angulos
    lha = get_angle(trunk,mid_hip,left_knee,'quadril')
    left_hip_angle.insert(index,lha)

    lka = get_angle(left_hip,left_knee,left_ankle,'joelho')
    left_knee_angle.insert(index,lka)

    laa = get_angle(left_knee,left_ankle,left_foot,'tornozelo')
    left_ankle_angle.insert(index,laa)

    head_pos.insert(index,head[1])

    rha = 180 - get_angle(trunk,right_hip,right_knee,'quadril')
    right_hip_angle.insert(index,rha)

    rka = 180 - get_angle(right_hip,right_knee,right_ankle,'joelho')
    right_knee_angle.insert(index,rka)

    raa = 90 - get_angle(right_knee,right_ankle,right_foot,'tornozelo')
    right_ankle_angle.insert(index,raa)

# função implementa um filtro gaussiano 1-D. O desvio padrão do filtro gaussiano é passado pelo parâmetro sigma
left_knee_angle = scipy.ndimage.gaussian_filter(left_knee_angle, sigma=3)
left_hip_angle = scipy.ndimage.gaussian_filter(left_hip_angle, sigma=5)
left_ankle_angle = scipy.ndimage.gaussian_filter(left_ankle_angle, sigma=5)

right_knee_angle = scipy.ndimage.gaussian_filter(right_knee_angle, sigma=5)
right_hip_angle = scipy.ndimage.gaussian_filter(right_hip_angle, sigma=5)
right_ankle_angle = scipy.ndimage.gaussian_filter(right_ankle_angle, sigma=2)

head_pos = scipy.ndimage.gaussian_filter(head_pos, sigma=2)

leftciclos = detecta_segmento(left_hip_angle)
rightciclos = detecta_segmento(right_hip_angle)

segmenta(left_knee_angle, leftciclos, 'left_knee_angles.npy', 0)
plot(left_knee_angle, "angulo do joelho esquerdo", 0)

segmenta(left_hip_angle, leftciclos, 'left_hip_angles.npy', 1)
plot(left_hip_angle, "angulo do quadril esquerdo", 1)

segmenta(left_ankle_angle, leftciclos, 'left_ankle_angles.npy', 2)
plot(left_ankle_angle, "angulo do tornozelo esquerdo", 2)

segmenta(right_knee_angle, rightciclos, 'right_knee_angles.npy', 3)
plot(right_knee_angle, "angulo do joelho direito", 3)

segmenta(right_hip_angle, rightciclos, 'right_hip_angles.npy', 4)
plot(right_hip_angle, "angulo do quadril direito", 4)

segmenta(right_ankle_angle, rightciclos, 'right_ankle_angles.npy', 5)
plot(right_ankle_angle, "angulo do tornozelo direito", 5)
