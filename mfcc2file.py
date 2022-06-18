import numpy as np
import matplotlib.pyplot as plt
import librosa as lib
import librosa.display as dis
from io import BytesIO
import os

folder = os.path.normpath('raw_samples/')
for filename in os.listdir(folder):
    base = os.path.splitext(filename)
    if base[1] == '.wav':
        print(base[0])
        svgfile = str(base[0]) + '.svg'
        snd, rate = lib.load(os.path.join(folder,filename), res_type='kaiser_fast')
        mfccs = lib.feature.mfcc(y=snd, sr=rate,hop_length=256, n_mfcc=64,fmin=20,fmax=8000)
        axis = dis.specshow(mfccs,cmap='gray_r',x_axis='time',y_axis='log')
        plt.tight_layout()
        plt.axis('off')
        plt.gca().set_position([0, 0, 1, 1])
        plt.savefig(os.path.join(folder,svgfile))
        plt.clf()

print("Conversion Complete")
