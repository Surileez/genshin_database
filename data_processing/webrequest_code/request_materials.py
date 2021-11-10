# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 05:03:34 2021

@author: admin123
"""
import requests
import re
import csv
import pandas as pd


def gettable(url_char,i):
    char_web = requests.get(url_char)
    char_web.encoding = 'utf-8'
    pattern = re.compile(r'(<span class=itemname>.*?</div></div></div>)')
    row= pattern.findall(char_web.text)
    char_table=[['mid','mname','cid']]
    df = pd.read_csv("D:/DS/4111/scrapy/Characters_all.csv")
    wierd_webs = {'ayaka':'Kamisato Ayaka', 'feiyan':'Yanfei', 'kazuha':'Kaedehara Kazuha',
              'shougun':'Raiden Shogun','kokomi':'Sangonomiya Kokomi', 'sara':'Kujou Sara',
              'hutao':'Hu Tao'}
    for n in row:
      pattern = re.compile(r'<span class=itemname>(.*?)</span></a><div class=sea_item_used_by_char>')
      mname=pattern.findall(n)
      pattern = re.compile(r'<a href="/db/char/(\w*\s*\w*\s*\w*\s*\w*)')
      cname=pattern.findall(n)
      for name in cname:
        if (re.match('traveler',name)):
          break
        elif name in wierd_webs:
          name = wierd_webs[name]
        else:  
          name=name.capitalize()
        if(df[df.cname==name].empty):
          break
        else:
          cid=df[df.cname==name]['cid'].item()
          char_table.append([i,mname[0],cid])  
      i+=1
    return(char_table)
    
url1='https://genshin.honeyhunterworld.com/db/item/character-ascension-material-local-material/?lang=EN'
char_table1=gettable(url1,1)
i=len(char_table1)
i=char_table1[i-1][0]
url2='https://genshin.honeyhunterworld.com/db/item/character-ascension-material-elemental-stone/?lang=EN'
char_table2=gettable(url2,i+1)
del(char_table2[0])
char_table1.extend(char_table2)
url_char='https://genshin.honeyhunterworld.com/db/item/talent-level-up-material/?lang=EN'
char_table=gettable(url_char,1000)
del(char_table[0])
char_table1.extend(char_table)
with open('D://DS/4111/scrapy/Level_up.csv', 'a', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerows(char_table1)
    f.close()
      
newdf=pd.DataFrame(char_table1[1:],columns=char_table1[0])
df=newdf.iloc[:,0:2]
df=df.drop_duplicates(keep='first')
df.to_csv('D://DS/4111/scrapy/Materials.csv',index=False)


