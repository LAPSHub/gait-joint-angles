import os, json
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

# path dos arquivos
path = './angles/'


def medias(string):
    a = []
    a_t = []
    med = []
    s = []
    std = []
    data_files = [files for files in sorted(os.listdir(path)) if files.endswith(string)]
    for index, af in enumerate(data_files):
        f = np.load(os.path.join(path, af), 'r')
        # inserindo os dados numa lista temporaria
        a.insert(index, f)
        # transpondo a lista temp
        a_t = list(map(list, zip(*a)))

    # calculando as medias
    for i1 in range(len(list(a_t))):
        i = []
        for i2 in range(len(list(a_t[i1]))):
            i.insert(i1, a_t[i1][i2])
            media = np.mean(i)
        # inserindo as medias numa lista nova
        med.insert(i1, media)

    for i1 in range(len(list(a_t))):
        for i2 in range(len(list(a_t[i1]))):
            a1 = a_t[i1][i2] - med[i2]
            a1 = math.pow(a1, 2)
            s.insert(i1, a1)
        b = len(s)
        s = sum(s)
        s = s / b
        s = math.sqrt(s)
        std.insert(i1, s)
        s = []
    return (med, std)


def plot(data, string):
    line = min(data)
    line2 = max(data)
    #plt.text(0,line2,"IC",fontsize=15)                           #initial contact
    plt.axvline(0, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.1,line2,"LR",fontsize=15)               #loanding response
    plt.axvline(len(data)*0.1, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.3,line2,"MS",fontsize=15)               #mid stance
    plt.axvline(len(data)*0.3, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.5,line2,"TS",fontsize=15)               #terminal stance
    plt.axvline(len(data)*0.5, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.6,line2,"PS",fontsize=15)               #pre swing
    plt.axvline(len(data)*0.6, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.7,line2,"IS",fontsize=15)               #initial swing
    plt.axvline(len(data)*0.7, color='gray', linewidth=3.0)
    #plt.text(len(data)*0.85,line2,"MS",fontsize=15)              #mid swing
    plt.axvline(len(data)*0.85, color='gray', linewidth=3.0)
    #plt.text(len(data),line2,"TS",fontsize=15)                   #terminal swing
    plt.axvline(len(data), color='gray', linewidth=3.0)
    plt.text(len(data)*0.05, line, "Stance phase", fontsize=20)
    plt.axhline(line, xmin=0., xmax=0.6, color='g', linewidth=3.0)
    #plt.text(60, line, "Swing phase", fontsize=20)
    plt.text(len(data)*0.65, line, "Swing phase", fontsize=20)
    plt.axhline(line, xmin=0.6, xmax=1, color='r', linewidth=3.0)
    ax1 = plt.subplot(111)
    ax1.set_xlim(len(data))
    ax1.set_xticks([0, len(data)*0.1, len(data)*0.3, len(data)*0.5, len(data)*0.6, len(data)*0.7, len(data)*0.85, len(data)])
    ax1.set_xticklabels(['0', '10', '30', '50', '60', '70', '85', '100'])
    plt.plot(data, linewidth=6.0)
    plt.title(string)
    plt.xlabel('% do ciclo')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()


hip = medias('hip_angle.npy')
knee = medias('knee_angle.npy')
ankle = medias('ankle_angle.npy')
#head = medias('_cabec.npy')

hip_med = hip[0]
knee_med = knee[0]
ankle_med = ankle[0]
#head_med = head[0]

hip_std = hip[1]
knee_std = knee[1]
ankle_std = ankle[1]
#head_std = head[1]

plot(hip_med, "quadril medio")
plot(knee_med, "joelho medio")
plot(ankle_med, "tornozelo medio")
#plot(head_med, "posicao da cabeca")

np.save('medhip_angle', hip_med)
np.save('medknee_angle', knee_med)
np.save('medankle_angle', ankle_med)
