import requests
import re
import csv

url = 'https://genshin.honeyhunterworld.com/db/char/characters/?lang=EN'
strhtml = requests.get(url) #get方式获取网页数据
strhtml.encoding='utf-8'
pattern1 = re.compile(r"(?<=sea_charname>)\w*\s*\w*")
names = pattern1.findall(strhtml.text)
print(names)
char_table = [['cid', 'cname', 'elements', 'rarity', 'weapon_type', 'birthday', 'base_hp', 'base_attack', 'base_defence',
               'nation_id']]
wierd_webs = {'Kamisato Ayaka':'ayaka', 'Yanfei':'feiyan', 'Kaedehara Kazuha':'kazuha',
              'Raiden Shogun':'shougun', 'Sangonomiya Kokomi':'kokomi', 'Kujou Sara':'sara'}
t_type = ['_boy_anemo', '_boy_geo', '_girl_anemo', '_girl_geo', '_boy_electro', '_girl_electro']
t_count = 0
i = 1
for name in names:
    if name == 'Traveler':
        no_space = name + t_type[t_count]
        t_count +=1
    elif name not in wierd_webs:
        tmp = list(name)
        no_space = ''
        for char in tmp:
            if char!=' ':
                no_space += char
    else:
        no_space = wierd_webs[name]
    url_cha = 'https://genshin.honeyhunterworld.com/db/char/{}/?lang=EN'.format(no_space)
    char_web = requests.get(url_cha)
    char_web.encoding = 'utf-8'
    pattern = re.compile(r'Rarity(.*?)Weapon Type.*?">(\w*).*?'
                         r'data-src=/img/icons/element/(\w*)_35'
                         r".*?Birthday</td><td>(\d*\s+\w*)"
                         r'.*?<tr><td>1</td><td>(\d*)</td><td>(\d*)</td><td>(\d*)')
    row = pattern.findall(char_web.text)[0]
    get_rarity = re.compile(r'sea_char_stars_wrap(.*?)svg class')
    rarity = len(get_rarity.findall(row[0]))
    print(name, rarity, row[1:])
    complet_row = [i, name, row[2], rarity, row[1]] + list(row[3:])
    print(complet_row)
    i += 1
    char_table.append(complet_row)
with open('./Characters.csv', 'a', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerows(char_table)
    f.close()


