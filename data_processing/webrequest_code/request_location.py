# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 23:41:14 2021

@author: admin123
"""

import requests
import re
import csv
import pandas as pd



def gettable(names,i):
  char_table=[['mid','location']]
  for name in names:
    url_char='https://genshin.honeyhunterworld.com/db/item/i_{}/?lang=EN'.format(name)
    char_web = requests.get(url_char)
    char_web.encoding = 'utf-8'
    pattern = re.compile(r'Recommendation: Found \w+ (.*?)</td></tr>')
    row= pattern.findall(char_web.text)
    if(row!=[]):
      char_table.append([i,row[0]])
    else:
      pattern = re.compile(r'Found \w+ (.*?)</td></tr>')
      row= pattern.findall(char_web.text)
      char_table.append([i,row[0]])
    i+=1
  return char_table
  
url='https://genshin.honeyhunterworld.com/db/item/character-ascension-material-local-material/?lang=EN'
char_web = requests.get(url)
char_web.encoding = 'utf-8'
pattern = re.compile(r'</div></a><a href="/db/item/i_(\d+)')
names= pattern.findall(char_web.text)  
char_table=gettable(names,1)
i=len(char_table)
i=char_table[i-1][0]

def gettable1(names,i):
  char_table=[['mid','location']]
  for name in names:
    url_char='https://genshin.honeyhunterworld.com/db/item/i_{}/?lang=EN'.format(name)
    char_web = requests.get(url_char)
    char_web.encoding = 'utf-8'
    pattern = re.compile(r'Dropped by Lv.\s*\d\d\+ (.*?)</td></tr></table>')
    row= pattern.findall(char_web.text)
    if(row!=[]):
      char_table.append([i,row[0]])
      i+=1
  return char_table
url1='https://genshin.honeyhunterworld.com/db/item/character-ascension-material-elemental-stone/?lang=EN'
char_web = requests.get(url1)
char_web.encoding = 'utf-8'
pattern = re.compile(r'</div></a><a href="/db/item/i_(\d+)')
names1= pattern.findall(char_web.text)  
char_table2=gettable1(names1,i+1)
del(char_table2[0])
char_table.extend(char_table2)

def gettable2(names,i):
  char_table=[['mid','location']]
  for name in names:
    url_char='https://genshin.honeyhunterworld.com/db/item/i_{}/?lang=EN'.format(name)
    char_web = requests.get(url_char)
    char_web.encoding = 'utf-8'
    pattern = re.compile(r'Obtained from Domain.*?</div><span class=asc_amount>\s*(.*?)</span></a></td></tr>')
    row= pattern.findall(char_web.text)
    if(row!=[]):
      char_table.append([i,row[0]])
      i+=1
    else:
      pattern = re.compile(r'Dropped by.*?</div><span class=asc_amount>.*?,\s(.*?)</span></a>')
      row= pattern.findall(char_web.text)
      char_table.append([i,row[0]])
      i+=1
  return char_table
url2='https://genshin.honeyhunterworld.com/db/item/talent-level-up-material/?lang=EN'
char_web = requests.get(url2)
char_web.encoding = 'utf-8'
pattern = re.compile(r'</div></a><a href="/db/item/i_(\d+)')
names2= pattern.findall(char_web.text) 
del(names2[-1])
char_table3=gettable2(names2,1000)
del(char_table3[0])
char_table.extend(char_table3)

with open('D://DS/4111/scrapy/Locate.csv', 'a', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerows(char_table)
    f.close()