import os, json
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

# path dos arquivos
path = r"\path\"


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
    x = range(len(data))
    # plt.text(0,line2,"IC",fontsize=30)
    # plt.text(8,line2,"OT",fontsize=30)
    plt.axvline(8, color='k', linewidth=3.0)
    # plt.text(33,line2,"HR",fontsize=30)
    plt.axvline(33, color='k', linewidth=3.0)
    # plt.text(50,line2,"OI",fontsize=30)
    plt.axvline(50, color='k', linewidth=3.0)
    # plt.text(58,line2,"TO",fontsize=30)
    plt.axvline(58, color='k', linewidth=3.0)
    # plt.text(78,line2,"FA",fontsize=30)
    plt.axvline(78, color='k', linewidth=3.0)
    # plt.text(85,line,"TV",fontsize=30)
    plt.axvline(85, color='k', linewidth=3.0)
    # plt.text(100,line,"IC",fontsize=30)
    plt.axvline(100, color='k', linewidth=3.0)
    plt.text(0, line, "Stance phase", fontsize=30)
    plt.axhline(line, xmin=0., xmax=0.4, color='g', linewidth=3.0)
    plt.text(40, line, "Swing phase", fontsize=30)
    plt.axhline(line, xmin=0.4, xmax=1, color='r', linewidth=3.0)
    plt.plot(x, data, linewidth=6.0)
    plt.title(string)
    plt.xlabel('% do cliclo')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()
    plt.close()


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
