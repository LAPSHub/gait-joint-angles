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
    print(len(indexes) - 1)
    return indexes

def segmenta(data, indexes, string, n):
    """ Funcao que pega os dados dos angulos e da segmentacao para retornar as 
    listas segmentadas
    """

    for index, js in enumerate(indexes[:-1]):
        start = indexes[index]
        finish = indexes[index + 1]
        print(start, finish)
        segdata = data[start:finish]

        # -- inserção feita pelo Clebson
        #Necessário criar pasta angles no diretório
        #Direciona uma pasta de destino para salvar os arquivos: Medankle_angle.npy,
        # medhip_angle.npy e medknee_angle.npy.
        path_name = './angles/' + str(n) + '_' + string
        np.save(path_name, segdata)
        # -- fim da inserção
        
        x = list(range(start, finish))
        plt.title('segmentos de um ciclo')
        plt.plot(x, segdata, 'r')
        plt.xlabel('frames')
        plt.show()

def plot(data, string, n):
    """ Função para plotagem
    """

    x = range(len(data))
    plt.figure(n)
    plt.subplot(212)
    plt.plot(x, data)
    plt.title(string)
    plt.xlabel('frames')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()




