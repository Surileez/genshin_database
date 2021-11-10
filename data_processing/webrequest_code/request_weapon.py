# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 21:29:45 2021

@author: admin123
"""
import requests
import re
import csv
import pandas as pd
names=['sword','claymore','polearm','bow','catalyst']
char_table = [['wid','wname','rarity','type','base_attack','extra_attribute','value']]
id=0
name='sword'
for name in names:
  url_cha='https://genshin.honeyhunterworld.com/db/weapon/{}/?lang=EN'.format(name)
  char_web = requests.get(url_cha)
  char_web.encoding = 'utf-8' 
  pattern = re.compile(r'data-src=/img/weapon/.*?></div></div></td><td>.*?lang=EN">(.*?)</a></td><td><div class=stars_wrap>(.*?)/></svg></div></td><td>(\d*)</td><td>(\w*\s*\w*\s*\w*\s*\w*)</td><td>(\d*)')
  row= pattern.findall(char_web.text)
  pattern1=re.compile(r'Unreleased, Incomplete or Upcoming Weapons(.*?)textwidget custom-html-widget')
  row1= pattern1.findall(char_web.text) 
  pattern2=re.compile(r'data-src=/img/weapon/.*?lang=EN">(.*?)</a></td><td>')
  rownew=pattern2.findall(row1[0])
  row=row[0:-len(rownew)]
  i=0
  for i in range(len(row)):
      pat=re.compile(r'fill=yellow')
      star=len(pat.findall(row[i][1]))
      id+=1
      char_table.append([id,row[i][0],star,name,row[i][2],row[i][3],row[i][4]])
      

with open('D://DS/4111/scrapy/Weapons.csv', 'a', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerows(char_table)
    f.close()
    

