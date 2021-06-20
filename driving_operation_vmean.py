import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import copy


def insertDfTrans_kineFrag(micrFrag, dfTransUpdt):
    for ii in range(len(micrFrag)):
        if 0.15 > micrFrag.loc[ii, 'acc'] > -0.15:
            micrFrag.loc[ii, 'cru'] = 1
        else:
            micrFrag.loc[ii, 'cru'] = 0

    startIndex = 0
    crntAcc = 1
    dfCutAll = []
    dfSimp = pd.DataFrame()
    for ii in range(1, len(micrFrag)):
        if micrFrag.loc[ii, 'acc'] * crntAcc < 0 or (micrFrag.loc[ii, 'cru'] * micrFrag.loc[ii - 1, 'cru']):
            dfCut = micrFrag.iloc[startIndex:ii, :]
            dfCut = dfCut.reset_index(drop=True)
            dfCut.loc[0, 'start_loc'] = int(startIndex)
            startIndex = ii - 1
            crntAcc = micrFrag.loc[ii, 'acc']
            dfCutAll.append(dfCut)

    for ii in range(len(dfCutAll)):
        dfSimp.loc[ii, 'vel_mean'] = dfCutAll[ii]['vel'].mean()
        tmp = int(int(dfSimp.loc[ii, 'vel_mean'] / 10) * 10)
        if tmp < 80:
            dfSimp.loc[ii, 'label_detail'] = '[{0}, {1})'.format(str(tmp), str(tmp + 10))
        elif tmp == 80:
            dfSimp.loc[ii, 'label_detail'] = '[80, 120)'
        else:
            dfSimp.loc[ii, 'label_detail'] = '> 120'
        # dfSimp.loc[ii, 'label'] = indexDict[dfSimp.loc[ii, 'label_detail']]
        dfSimp.loc[ii, 'start_loc'] = dfCutAll[ii].loc[0, 'start_loc']
        dfSimp.loc[ii, 'start_value'] = dfCutAll[ii].loc[0, 'vel']
        dfSimp.loc[ii, 'filename'] = filename

    for ii in range(1, len(dfSimp)):
        dfTransUpdt.loc[dfSimp.loc[ii, 'label_detail'], dfSimp.loc[ii - 1, 'label_detail']] += 1  # 行：子代，列：父代

    dfSimpOut = dfSimp[['vel_mean', 'label_detail', 'start_loc', 'start_value', 'filename']]
    return dfTransUpdt, dfSimpOut


def MonteCarlo():
    pass


matRange = 10
dfTrans = pd.DataFrame(np.zeros((matRange, matRange)))
indexList = ['[0, 10)', '[10, 20)', '[30, 40)', '[20, 30)', '[40, 50)', '[50, 60)', '[60, 70)', '[70, 80)', '[80, 120)',
             '> 120']
'''indexDict = {}
for i in range(len(indexList)):
    indexDict[str(indexList[i])] = i'''
dfTrans.columns = indexList
dfTrans.index = indexList

fo = open('log_20210311_vmean.txt', 'a')
filepath = r'./片段汇总'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfExl = pd.read_excel(filename, header=None)
            dfExl.columns = ['vel', 'acc']
            try:
                dfTrans, dfLabel = insertDfTrans_kineFrag(dfExl, dfTrans)
                dfLabel.to_excel(os.path.join(root, 'LabelWithFile', name))
            except:
                print(filename + ' error!')
                fo.write(filename + ' error!' + '\n')
                continue
            print(filename + ' done!')
            fo.write(filename + ' done!' + '\n')

# heatmap_plot = sns.heatmap(dfTrans, center=0, cmap='gist_ncar')
# plt.show()
fo.close()
dfTrans.to_excel('trans_result_vmean.xlsx')
