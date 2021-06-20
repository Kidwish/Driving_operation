import pandas as pd
import numpy as np
import os
import random


def findDC(label):
    # targetIndex = -1
    # randomIndex = int(random.random()*dfLabelAll.shape[0])
    count = []
    for ii in range(dfLabelAll.shape[0]):
        if (dfLabelAll['label_detail'][ii] == label) and dfLabelAll['length'][ii] > 30:
            count.append(ii)

    '''while len(count) < 50:
        if dfLabelAll['label_detail'][randomIndex] != label or (dfLabelAll['start_value'][randomIndex+1] - dfLabelAll['start_value'][randomIndex]) < 20:
            randomIndex = int(random.random()*dfLabelAll.shape[0])
            continue
        else:
            count.append(randomIndex)'''
    tmpmin = 1000
    targetIndex = count[0]
    for ii in count:
        if tmpmin > (dfLabelAll['start_value'][ii] - DC[-1]):
            tmpmin = dfLabelAll['start_value'][ii] - DC[-1]
            targetIndex = ii

    '''    
    for ii in range(dfLabelAll.shape[0]):
        if (dfLabelAll['label_detail'][ii] == label) and (dfLabelAll['start_value'][ii] - DC[-1] < 1):
            targetIndex = ii
            break

    if targetIndex == -1:
        print('no match frag!')
        targetIndex = dfLabelAll[dfLabelAll['label_detail'] == label]['start_value'].idxmin(axis=0)
    '''
    filename = dfLabelAll['filename'][targetIndex]
    filename = filename.replace('\\', '/')
    insertDC = pd.read_excel(filename, index_col=0)
    # insertDC.columns = ['vel', 'acc']
    for ii in range(dfLabelAll['start_loc'][targetIndex], dfLabelAll['start_loc'][targetIndex + 1]):
        DC.append(insertDC['vel'][ii])


print(1)
dfTrans = pd.read_excel('trans_result_vmean.xlsx', index_col=0)
# 转为累计概率矩阵
for i in range(10):
    dfTrans.iloc[i] = dfTrans.iloc[i] / dfTrans.iloc[i].sum()
# dfTrans = pd.DataFrame(dfTrans.values.T, index=dfTrans.columns, columns=dfTrans.index)
for i in range(1, 10):
    dfTrans.iloc[:, i] = dfTrans.iloc[:, i] + dfTrans.iloc[:, i - 1]

print(2)
'''
dfLabelAll = pd.DataFrame()
# filepath = r'./LabelWithFile'
filepath = r'./LabelWithFile'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfLabel = pd.read_excel(filename)
            dfLabelAll = dfLabelAll.append(dfLabel)
            print(filename + ' done!')
dfLabelAll = dfLabelAll.reset_index(drop=True)
'''
dfLabelAll = pd.read_excel('dfLabelAll.xlsx', index_col=0)


print(3)
startLabel = dfLabelAll['label_detail'][0]
DCtime = 1500  # unit:s
DC = []

# 初始化DC
startNum = 1
filename = dfLabelAll['filename'][1]
filename = filename.replace('\\', '/')
tmpDC = pd.read_excel(filename, index_col=0)
# print(tmpDC)
# tmpDC.columns = ['vel', 'acc']
# print(dfLabelAll['start_loc'][startNum])
# print(dfLabelAll['start_loc'][startNum + 1])
for i in range(dfLabelAll['start_loc'][startNum], dfLabelAll['start_loc'][startNum + 1]):
    DC.append(tmpDC['vel'][i])
# print('DC:', DC)

print(4)
# 根据转移矩阵补全DC
while len(DC) < DCtime * 10:
    print(len(DC)/10)
    p = random.random()
    for j in dfTrans.columns:
        if p < dfTrans.loc[startLabel][j]:
            startLabel = j
            findDC(startLabel)
            break

dfDC = pd.DataFrame(DC)
dfDC.to_excel('DC.xlsx')
