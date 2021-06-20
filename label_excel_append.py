import pandas as pd
import numpy as np
import os

dfLabelAll = pd.DataFrame()
filepath = r'./LabelWithFile'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfLabel = pd.read_excel(filename)
            dfLabelAll = dfLabelAll.append(dfLabel)
            print(filename + ' done!')

dfLabelAll = dfLabelAll.reset_index(drop=True)
dfLabelAll.to_excel('dfLabelAll.xlsx')
