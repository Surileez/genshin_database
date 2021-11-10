# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 05:51:40 2021

@author: admin123
"""
import csv
import pandas as pd
df1 = pd.read_csv("D:/DS/4111/scrapy/Characters_all.csv")    
df2 = pd.read_csv("D:/DS/4111/scrapy/Weapons.csv")
names={'sword':0,'claymore':1,'polearm':2,'bow':3,'catalyst':4}
i=0
wid=[]
equip=[['cid','mid']]
for name in names:
    wid.append(df2[df2.type==name]['wid'])
for i in range(df1.iloc[-1][0]):
    k=names[df1.iloc[i][4].lower()]
    for j in wid[k]:
        equip.append([df1.iloc[i][0],j])

df=pd.DataFrame(equip[1:],columns=equip[0])
df.to_csv('D://DS/4111/scrapy/Equip.csv',index=False)