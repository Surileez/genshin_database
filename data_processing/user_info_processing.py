import csv
names=['安柏','芭芭拉','北斗','班尼特','重云','迪卢克','菲谢尔','琴','凯亚','刻晴','可莉','丽莎','莫娜',
       '凝光','诺艾尔','七七','雷泽','砂糖','温迪','香菱','魈','行秋','达达利亚','钟离','迪奥娜','辛焱',
       '甘雨','阿贝多','罗莎莉亚','神里绫华','胡桃','烟绯','优菈','枫原万叶','宵宫','早柚','雷电将军',
       '珊瑚宫心海','埃洛伊','九条裟罗','托马']
def get_uname_info(input_path):
    with open(input_path, encoding='gbk') as f:
        csv_reader = csv.reader(f)
        uid_dict = {}
        i = 0
        for line in csv_reader:
            uid = line[0]
            uid_dict[uid] = line[1:]
        return uid_dict
uid_dict = get_uname_info('./part3/user.csv')
print(uid_dict)
#print(" ".isdigit())
def dic(names):
    i = 1
    dic = {}
    for name in names:
        dic[name] = i  # '%i'%i
        i += 1
    return dic
name_dict = dic(names)
def get_user_info(tokens, index, uid_dict):
    user_info = [index]
    for i in range(len(tokens)):
        if tokens[i] == '查询栏':
            uid = tokens[i+1][:-4]
            #user_info.append(str(uid))
            user_info += uid_dict[uid]
        elif tokens[i] == '数据总览':
            user_info.append(int(tokens[i + 5]))#activate_day
            user_info.append(int(tokens[i + 6]))#number_of_achievements
        elif tokens[i] == '深境螺旋':
            tmp = tokens[i + 4]
            if '-' in list(tmp):
                user_info.append(' '+tokens[i + 4])#deep_spiral
            else:
                user_info.append('None')
            return user_info
def get_digit(s, type):
    l = ""
    for char in s:
        if char.isdigit():
            l += char
        elif char == 'o' or 'O': #or (char == 'O'):
            l += '0'
    ans = int(l)
    if type == 'c':
        print("l, s", l, s)
        if int(l) > 6:
            for i in l:
                if i != '0':
                    ans = int(i)
                    break
    return ans
def get_owing_info(tokens, uid, owning, name_dict):
    start = tokens.index('角色列表')+1
    n = len(tokens)
    if '深境螺旋战绩' in tokens:
        end = tokens.index('深境螺旋战绩')+1
    else:
        end = n
    print(start, end, end-start)
    i = start
    #print(tokens[i])
    while i<end:
        #print("check name",tokens[i] in name_dict)
        if tokens[i] in name_dict or tokens[i] == '旅行者':
            span = 1
            while tokens[i+span] in name_dict or tokens[i+span] == '旅行者':
                span +=1
            #print("span", span)
            for j in range(span):
                index = i + j
                if index + 3*span < end and tokens[index] in name_dict:
                    line = [uid, name_dict[tokens[index]]]
                    #pattern = re.compile(r'(?<=:)\s*\d*')
                    #print("角色名", tokens[index])
                    clevel = get_digit(tokens[index+span], 'l')
                    friendliness = get_digit(tokens[index + span*2], 'f')
                    constellation = get_digit(tokens[index + span*3], 'c')
                    #print(clevel, friendliness, constellation)
                    line += [clevel, friendliness, constellation]
                    owning.append(line)
            i += span*4
        else:
            i += 1
        #print(i, tokens[i])
    return owning
user_pre = [['uid', 'uname', 'ulevel', 'activate_day', 'number_of_achievements', 'deep_spiral']]
owning = [['uid', 'cid', 'clevel', 'friendliness', 'constellation']]
def process_ocr_result(input_path, user_pre, owning, index):

    with open(input_path, encoding='utf-8') as f:
        txt = f.read()
        #print(txt)
        #print(len(txt))
        tokens = txt.split('\n')
        #print(tokens)
        user_info = get_user_info(tokens, index, uid_dict)
        print(user_info)
        if len(user_info) > 0:
            user_pre.append(user_info)
            owning = get_owing_info(tokens, user_info[0], owning, name_dict)
            #print(owning)
        f.close()

    return user_pre, owning
folder = './user(1)/'
fname = 'result.txt'
for i in range(5, 7):
    file_path = folder + '1 ({})/'.format(i) + fname
    user_pre, owning = process_ocr_result(file_path, user_pre, owning, i)
for line in user_pre:
    print(line)
for line in owning:
    print(line)
#print(user_pre)
#print(owning)
with open('./part3/Users_test.csv', 'a', encoding='gbk', newline='') as f:
    write = csv.writer(f)
    write.writerows(user_pre)
    f.close()
with open('./part3/owning_test.csv', 'a', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerows(owning)
    f.close()

