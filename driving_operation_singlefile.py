#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df_csv = pd.read_csv('20200720_002.csv')
#print(df)


# In[5]:


df_csv.head(10)


# In[6]:


df = pd.DataFrame(df_csv.iloc[11:,2])
df.columns = ['vel'] #unit:km/h
df = df.reset_index(drop = True)
df['vel'] = pd.to_numeric(df['vel'])
for i in range(1,len(df)):
    df.loc[i,'acc'] = (df.loc[i,'vel'] - df.loc[i-1,'vel'])*10/3.6 #10Hz #unit:m/s/s
df.drop([0], axis = 0, inplace = True)
df = df.reset_index(drop = True)
#df.info()
df.describe()


# In[24]:


vel=df['vel']
acc=df['acc']
plt.scatter(vel,acc)
plt.ylim(-5, 5)
plt.show()


# In[47]:


timeGap=2*60 #unit:s
df_simp=pd.DataFrame()
for i in range(0,len(df),timeGap*10): #10Hz
    df_simp.loc[i,'vel_mean']=np.mean(df.loc[i:i+timeGap*10-1,'vel'])
    df_simp.loc[i,'vel_std']=np.std(df.loc[i:i+timeGap*10-1,'vel'])
df_simp = df_simp.reset_index(drop = True)
df_simp


# In[48]:


vMeanRange=150
vMeanGap=30 #0~vMeanRange
vStdRange=50
vStdGap=5 #0~vStdRange
matRange=int((vMeanRange/vMeanGap)*(vStdRange/vStdGap))
df_trans=pd.DataFrame(np.zeros((matRange,matRange)))
indexList=[]
for i in range(0,vMeanRange,vMeanGap):
    for j in range(0,vStdRange,vStdGap):
        indexList.append(str([i,j]))
df_trans.columns=indexList
df_trans.index=indexList

for i in range(1,len(df_simp)):
    if df_simp.loc[i,'vel_mean']==0 and df_simp.loc[i-1,'vel_mean']==0:
        continue
    else:
        loci=[int(df_simp.loc[i,'vel_mean']/vMeanGap)*vMeanGap,int(df_simp.loc[i,'vel_std']/vStdGap)*vStdGap]
        loci=str(loci)
        locj=[int(df_simp.loc[i-1,'vel_mean']/vMeanGap)*vMeanGap,int(df_simp.loc[i-1,'vel_std']/vStdGap)*vStdGap]
        locj=str(locj)
        df_trans.loc[loci,locj] += 1  #行：子代，列：父代


# In[49]:


heatmap_plot=sns.heatmap(df_trans, center=0, cmap='gist_ncar')
plt.show()


# In[40]:


get_ipython().system('jupyter nbconvert --to python driving_operation_singlefile.ipynb')


# In[ ]:




