import os, json
import math
import matplotlib.pyplot as plt
import numpy as np

# path dos arquivos
path = './angles/'


def medias(string):
    a_t = []
    med = []
    s = []
    std = []
    data_files = [files for files in sorted(os.listdir(path)) if files.endswith(string)]
    for index, af in enumerate(data_files):
        a_t = np.load(os.path.join(path, af), 'r')

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
    x = len(data)
    #plt.text(0,line2,"IC",fontsize=15)                   #initial contact
    plt.axvline(0, color='gray', linewidth=3.0)
    #plt.text(x*0.1,line2,"LR",fontsize=15)               #loanding response
    plt.axvline(x*0.1, color='gray', linewidth=3.0)
    #plt.text(x*0.3,line2,"MS",fontsize=15)               #mid stance
    plt.axvline(x*0.3, color='gray', linewidth=3.0)
    #plt.text(x*0.5,line2,"TS",fontsize=15)               #terminal stance
    plt.axvline(x*0.5, color='gray', linewidth=3.0)
    #plt.text(x*0.6,line2,"PS",fontsize=15)               #pre swing
    plt.axvline(x*0.6, color='gray', linewidth=3.0)
    #plt.text(x*0.7,line2,"IS",fontsize=15)               #initial swing
    plt.axvline(x*0.7, color='gray', linewidth=3.0)
    #plt.text(x*0.85,line2,"MS",fontsize=15)              #mid swing
    plt.axvline(x*0.85, color='gray', linewidth=3.0)
    #plt.text(x,line2,"TS",fontsize=15)                   #terminal swing
    plt.axvline(x, color='gray', linewidth=3.0)
    plt.text(x*0.05, line, "Stance phase", fontsize=20)
    plt.axhline(line, xmin=0., xmax=0.6, color='g', linewidth=3.0)
    plt.text(x*0.65, line, "Swing phase", fontsize=20)
    plt.axhline(line, xmin=0.6, xmax=1, color='r', linewidth=3.0)
    ax1 = plt.subplot(111)
    ax1.set_xlim(x)
    ax1.set_xticks([0, x*0.1, x*0.3, x*0.5, x*0.6, x*0.7, x*0.85, x])
    ax1.set_xticklabels(['0', '10', '30', '50', '60', '70', '85', '100'])
    plt.plot(data, linewidth=6.0)
    plt.title(string)
    plt.xlabel('% do ciclo')
    plt.ylabel('extension<-angle(degrees)->flexion')
    plt.show()


left_hip = medias('left_hip_angles.npy')
left_knee = medias('left_knee_angles.npy')
left_ankle = medias('left_ankle_angles.npy')
right_hip = medias('right_hip_angles.npy')
right_knee = medias('right_knee_angles.npy')
right_ankle = medias('right_ankle_angles.npy')
#head = medias('_cabec.npy')

left_hip_med = left_hip[0]
left_knee_med = left_knee[0]
left_ankle_med = left_ankle[0]
right_hip_med = right_hip[0]
right_knee_med = right_knee[0]
right_ankle_med = right_ankle[0]
#head_med = head[0]

left_hip_std = left_hip[1]
left_knee_std = left_knee[1]
left_ankle_std = left_ankle[1]
right_hip_std = right_hip[1]
right_knee_std = right_knee[1]
right_ankle_std = right_ankle[1]
#head_std = head[1]

plot(left_hip_med, "quadril esquerdo medio")
plot(left_knee_med, "joelho esquerdo medio")
plot(left_ankle_med, "tornozelo esquerdo medio")
plot(right_hip_med, "quadril direito medio")
plot(right_knee_med, "joelho direito medio")
plot(right_ankle_med, "tornozelo direito medio")
#plot(head_med, "posicao da cabeca")

#np.save('medhip_angle', hip_med)
#np.save('medknee_angle', knee_med)
#np.save('medankle_angle', ankle_med)
