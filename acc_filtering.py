from scipy import signal
import os
import pandas as pd
from array import array

# wn=2*400/1000=0.8 , 400为低通滤波频率400Hz,1000为采样频率1000Hz
# 当前尝试，wn取0.6

filepath = r'./Filtered片段 仅vel滤波'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfExl = pd.read_excel(filename, index_col=0)
            data = array('d', dfExl['acc'])
            b, a = signal.butter(8, 0.2, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
            filtedData = signal.filtfilt(b, a, data, padlen=0)  # data为要过滤的信号
            dfData = pd.DataFrame()
            dfData['vel'] = dfExl['vel']
            dfData['acc'] = filtedData
            fdataFilename = os.path.join(r'./Filtered片段', name)
            dfData.to_excel(fdataFilename)
