import pandas as pd
import numpy as np
import os
import random

filepath = r'./LabelWithFile'
for root, dirs, files in os.walk(filepath):
    for name in files:
        filename = os.path.join(root, name)
        if filename[-5:] == '.xlsx':
            dfLabel = pd.read_excel(filename)
            dfLabel['length'] = dfLabel['start_loc']
            for ii in range(len(dfLabel)-1):
                dfLabel['length'][ii] = dfLabel['start_loc'][ii+1]-dfLabel['start_loc'][ii]
            ii = len(dfLabel)-1
            tmpdf = pd.read_excel(dfLabel['filename'][ii], index_col=0)
            dfLabel['length'][ii] = len(tmpdf)-1 - dfLabel['start_loc'][ii-1]
            dfLabel.to_excel(filename)
            print(filename + ' done!')
