from scipy import signal
import os
import pandas as pd
from array import array

# wn=2*400/1000=0.8 , 400为低通滤波频率400Hz,1000为采样频率1000Hz
# 当前尝试，wn取0.2

filepath = r'./片段汇总'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfExl = pd.read_excel(filename, header=None)
            dfExl.columns = ['vel', 'acc']
            data = array('d', dfExl['vel'])
            b, a = signal.butter(8, 0.2, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
            filtedData = signal.filtfilt(b, a, data, padlen=0)  # data为要过滤的信号
            dfData = pd.DataFrame()
            dfData['vel'] = filtedData
            dfData.loc[0, 'acc'] = 0
            for i in range(1, len(filtedData)):
                dfData.loc[i, 'acc'] = (dfData.loc[i, 'vel'] - dfData.loc[i - 1, 'vel']) * 10 / 3.6  # 10Hz #unit:m/s/s
            fdataFilename = os.path.join(r'./FilteringTry/Filtered片段 仅vel滤波', name)
            dfData.to_excel(fdataFilename)
