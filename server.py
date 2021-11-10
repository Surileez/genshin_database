#!/usr/bin/env python
# coding=utf-8
"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
PIC_FOLDER = os.path.join('static','pic')
app = Flask(__name__, template_folder=tmpl_dir)
app.config ['UPLOAD_FOLDER'] = PIC_FOLDER
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://zd2263:123456@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/',methods=['GET', 'POST'])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  # DEBUG: this is debugging code to see what request looks like
  print (request.args)
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'genshin.jpg')
  if request.method == 'GET':
    return render_template('index.html', Login_image=full_filename)
  else:
    uid = request.form.get('uid')
    uname = request.form.get('uname')
    submit = request.form.get('login')
    if submit == 'login':
      if uid == '' or uname == '':
        return render_template('index.html', Login_image=full_filename, wrong='Please input both uid and uname')
      if not uid.isdigit():
        return render_template('index.html', Login_image=full_filename, wrong='UID must be integer')
      cursor = g.conn.execute("SELECT * from Users where uid=%s and uname=%s", (uid, uname))
      check = cursor.fetchall()
      cursor.close()
      if len(check) == 1:
        return redirect('/search')
      else:
        return render_template('index.html', Login_image=full_filename, wrong='Wrong login information')


@app.route('/search',methods=['GET', 'POST'])
def search():
  print(request.args)
  full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'Liyue.jpg')
  return render_template('search.html',Liyue_image = full_filename)

@app.route('/characters',methods=['GET', 'POST'])
def characters():
  print (request.args)
  if request.method == 'GET':
    cursor = g.conn.execute("SELECT * from Characters C INNER JOIN Nations N on C.nid=N.nid limit 5")
    characters = []
    for result in cursor:
      characters.append(result)  # can also be accessed using result
    context = dict(data=characters)
    cursor.close()
    return render_template("characters.html",**context)
  else:
    getcol=[]
    getcol.append(request.form.get('cname'))
    getcol.append(request.form.getlist('elements'))
    getcol.append(request.form.getlist('character_rarity'))
    getcol.append(request.form.getlist('weapon_type'))
    getcol.append(request.form.get('birthday'))
    getcol.append(request.form.getlist('nid'))
    submit = request.form.get('search')
    if submit == 'search':
      cols = ['cname', 'elements','character_rarity','weapon_type','birthday','nation_name']
      dic = {}
      i=1
      for col in cols:
        if getcol[i-1]!='' and getcol[i-1]!=[]:
          dic[col]=getcol[i-1]
        i+=1
      sql = 'SELECT * from Characters C INNER JOIN Nations N on C.nid=N.nid'
      if len(dic) > 0:
        sql = sql + ' where '
      data = []
      para = []
      for col in dic:
        if (col=='cname' or col=='birthday'):
           data.append(col + '=' + '%s')
           para.append(dic[col])
        else:
           part= []
           for n in dic[col]:
              part.append(col + '=' + '%s')
              para.append(n)
           data.append('(' + ' or '.join(part) + ')')
      sql = sql + ' and '.join(data)
      cursor = g.conn.execute(sql,para)
      characters = []
      for result in cursor:
        characters.append(result)  # can also be accessed using result[0]
      context = dict(data=characters)
      cursor.close()
      return render_template('characters.html',**context)

@app.route('/weapons',methods=['GET', 'POST'])
def weapons():
  print(request.args)
  if request.method == 'GET':
    sql="SELECT wname,weapon_rarity,type,weapon_base_attack,extra_attribute,value,"+\
      "case when extra_attribute='Elemental Mastery' or cast(value as varchar)='0' then cast(value as varchar) else (cast(value as varchar)||'%%') end AS valuenew "+\
      "from Weapons W limit 5"
    cursor = g.conn.execute(sql)
    characters = []
    for result in cursor:
      characters.append(result)  # can also be accessed using result
    context = dict(data=characters)
    cursor.close()
    return render_template("weapons.html", **context)
  else:
    getcol = []
    getcol.append(request.form.get('wname'))
    getcol.append(request.form.getlist('rarity'))
    getcol.append(request.form.getlist('weapon_type'))
    getcol.append(request.form.getlist('extra_attribute'))
    submit = request.form.get('search')
    if submit == 'search':
      cols = ['wname', 'weapon_rarity', 'type', 'extra_attribute']
      dic = {}
      i = 1
      for col in cols:
        if getcol[i - 1] != '' and getcol[i - 1] != []:
          dic[col] = getcol[i - 1]
        i += 1
      sql = "SELECT wname,weapon_rarity,type,weapon_base_attack,extra_attribute,value," + \
            "case when extra_attribute='Elemental Mastery' or cast(value as varchar)='0' then cast(value as varchar) else (cast(value as varchar)||'%%') end AS valuenew " + \
            "from Weapons W "
      if len(dic) > 0:
        sql = sql + ' where '
      data = []
      para = []
      for col in dic:
        if (col == 'wname'):
          data.append(col + '=' + '%s')
          para.append(dic[col])
        else:
          part = []
          for n in dic[col]:
            part.append(col + '=' + '%s')
            para.append(n)
          data.append('(' + ' or '.join(part) + ')')
      sql = sql + ' and '.join(data)
      cursor = g.conn.execute(sql, para)
      weapons = []
      for result in cursor:
        weapons.append(result)
      context = dict(data=weapons)
      cursor.close()
      return render_template('weapons.html', **context)

@app.route('/users',methods=['GET', 'POST'])
def users():
  print(request.args)
  if request.method == 'GET':
    cursor = g.conn.execute("SELECT * from Users limit 5")
    users = []
    for result in cursor:
      users.append(result)  # can also be accessed using result
    context = dict(data=users)
    cursor.close()
    return render_template("users.html", **context)
  else:
    getcol = []
    inuid=request.form.get('uid')
    getcol.append(inuid)
    getcol.append(request.form.get('uname'))
    inulevel=request.form.get('ulevel')
    getcol.append(inulevel)
    inday=request.form.get('activate_day')
    getcol.append(inday)
    inachievements=request.form.get('number_of_achievements')
    getcol.append(inachievements)
    getcol.append(request.form.get('deep_spiral'))
    submit = request.form.get('search')
    if submit == 'search':
      if not (inuid.isdigit() or inuid==''):
        context = dict(data=[])
        return render_template('users.html', **context,wrongu='must input integer')
      if not (inulevel.isdigit() or inulevel==''):
        context = dict(data=[])
        return render_template('users.html', **context,wrongl='must input integer')
      if not (inday.isdigit() or inday==''):
        context = dict(data=[])
        return render_template('users.html', **context,wrongd='must input integer')
      if not (inachievements.isdigit() or inachievements==''):
        context = dict(data=[])
        return render_template('users.html', **context,wronga='must input integer')
      else:
        cols = ['uid','uname', 'ulevel', 'activate_day', 'number_of_achievements','deep_spiral']
        dic = {}
        i = 1
        for col in cols:
          if getcol[i - 1] != '':
            dic[col] = getcol[i - 1]
          i += 1
        sql = 'SELECT * from Users'
        if len(dic) > 0:
          sql = sql + ' where '
        data = []
        para = []
        for col in dic:
            data.append(col + '=' + '%s')
            if col!='deep_spiral':
               para.append(dic[col])
            else:
               para.append(' '+dic[col])
        sql = sql + ' and '.join(data)
        cursor = g.conn.execute(sql, para)
        weapons = []
        for result in cursor:
          weapons.append(result)
        context = dict(data=weapons)
        cursor.close()
        return render_template('users.html', **context)

@app.route('/owning',methods=['GET', 'POST'])
def owning():
  print(request.args)
  if request.method == 'GET':
    cursor = g.conn.execute("SELECT O.uid,uname,cname,elements,character_rarity,clevel,friendship,constellation from Owning O, Users U, Characters C where O.uid=U.uid and O.cid=C.cid limit 5")
    characters = []
    for result in cursor:
      characters.append(result)  # can also be accessed using result
    context = dict(data=characters)
    cursor.close()
    return render_template("owning.html", **context)
  else:
    getcol = []
    inuid = request.form.get('uid')
    #getcol.append(request.form.get('uid'))
    getcol.append(inuid)
    getcol.append(request.form.get('uname'))
    getcol.append(request.form.get('cname'))
    getcol.append(request.form.getlist('elements'))
    getcol.append(request.form.getlist('character_rarity'))
    inclevel = request.form.get('clevel')
    getcol.append(inclevel)
    infrd = request.form.get('friendship')
    getcol.append(infrd)
    incon = request.form.get('constellation')
    getcol.append(incon)
    submit = request.form.get('search')
    if submit == 'search':
      if not (inuid.isdigit() or inuid == ''):
        context = dict(data=[])
        return render_template('owning.html', **context,wrongu='must input integer')
      if not (inclevel.isdigit() or inclevel == ''):
        context = dict(data=[])
        return render_template('owning.html', **context,wrongl='must input integer')
      if not (infrd.isdigit() or infrd == ''):
        context = dict(data=[])
        return render_template('owning.html', **context,wrongf='must input integer')
      if not (incon.isdigit() or incon == ''):
        context = dict(data=[])
        return render_template('owning.html', **context,wrongc='must input integer')
      else:
        cols = ['O.uid', 'uname', 'cname', 'elements','character_rarity','clevel', 'friendship', 'constellation']
        dic = {}
        i = 1
        for col in cols:
          if getcol[i - 1] != '' and getcol[i - 1] != []:
            dic[col] = getcol[i - 1]
          i += 1
        sql = 'SELECT O.uid,uname,cname,elements,character_rarity,clevel,friendship,constellation'\
              +' from Owning O, Users U, Characters C where O.uid=U.uid and O.cid=C.cid'
        if len(dic) > 0:
          sql = sql + ' and '
        data = []
        para = []
        for col in dic:
          if (col == 'elements' or col == 'character_rarity'):
            part = []
            for n in dic[col]:
              part.append(col + '=' + '%s')
              para.append(n)
            data.append('(' + ' or '.join(part) + ')')
          else:
            data.append(col + '=' + '%s')
            para.append(dic[col])
        sql = sql + ' and '.join(data)
        cursor = g.conn.execute(sql, para)
        users = []
        for result in cursor:
          users.append(result)
        context = dict(data=users)
        cursor.close()
        return render_template('owning.html', **context)

@app.route('/materials',methods=['GET', 'POST'])
def materials():
  print(request.args)
  if request.method == 'GET':
    sql="SELECT mname,location,nation_name,'Loc_materials' AS type "+\
      ",string_agg(cname,',') AS used_by_characters "+\
        "from Materials M, Nations N, Locate L,Loc_materials Loc,Characters C, Level_up U "+\
        "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "+\
        "Group by Loc.mid,mname,location,nation_name "+\
        "limit 5"
    cursor = g.conn.execute(sql)
    characters = []
    for result in cursor:
      characters.append(result)
    context_l = dict(data_l=characters)
    cursor.close()
    sql = "SELECT mname,location,nation_name,'Talent_level_up_materials' AS type,open_day "+\
      ",string_agg(cname,',') AS used_by_characters "+\
        "from Materials M, Nations N, Locate L,Talent_level_up_materials Loc,Characters C, Level_up U "+\
        "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "+\
        "Group by Loc.mid,mname,location,nation_name,open_day "+\
        "limit 5"
    cursor = g.conn.execute(sql)
    characters = []
    for result in cursor:
      characters.append(result)
    context_t= dict(data_t=characters)
    cursor.close()
    return render_template("materials.html", **context_l,**context_t)
  else:
    getcol = []
    getcol.append(request.form.get('mname'))
    getcol.append(request.form.get('location'))
    getcol.append(request.form.getlist('nid'))
    intype = request.form.getlist('type')
    days=request.form.getlist('open_day')
    getcol.append(days)
    getcol.append(request.form.get('cname'))
    submit = request.form.get('search')
    if submit == 'search':
      cols = ['mname','location','nation_name', 'open_day','cname']
      dic = {}
      i = 1
      for col in cols:
        if getcol[i - 1] != '' and getcol[i - 1] != []:
          dic[col] = getcol[i - 1]
        i += 1
      if (intype == []) or ('Loc_materials' in intype):
        if 'cname' not in dic:
          sql1 = "SELECT mname,location,nation_name,'Loc_materials' AS type " + \
            ",string_agg(cname,',') AS used_by_characters " + \
            "from Materials M, Nations N, Locate L,Loc_materials Loc,Characters C, Level_up U " + \
            "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "
          para = []
        else:
          sql1 ="SELECT mname,location,nation_name,'Loc_materials' AS type " + \
            ",%s AS used_by_characters " + \
            "from Materials M, Nations N, Locate L,Loc_materials Loc,Characters C, Level_up U " + \
            "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "
          para = [dic['cname']]
        if (len(dic) > 1) or (('open_day' not in dic) and len(dic) > 0):
           sql1 = sql1 + ' and '
        data = []
        for col in dic:
          if (col!='open_day'):
            if (col == 'nation_name'):
              part = []
              for n in dic[col]:
                part.append(col + '=' + '%s')
                para.append(n)
              data.append('(' + ' or '.join(part) + ')')
            else:
              data.append(col + '=' + '%s')
              para.append(dic[col])
        sql1 = sql1 + ' and '.join(data)+ 'Group by Loc.mid,mname,location,nation_name'
        cursor1 = g.conn.execute(sql1, para)
        Loc = []
        for result in cursor1:
          Loc.append(result)
        context_l = dict(data_l=Loc)
        cursor1.close()
      if (intype != []) and ('Loc_materials' not in intype):
        context_l = dict(data_l=[])
      if (intype == []) or ('Talent_level_up_materials' in intype):
        if 'cname' not in dic:
          sql2 = "SELECT mname,location,nation_name,'Talent_level_up_materials' AS type,open_day " + \
            ",string_agg(cname,',') AS used_by_characters " + \
            "from Materials M, Nations N, Locate L,Talent_level_up_materials Loc,Characters C, Level_up U " + \
            "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "
          para = []
        else:
          sql2 ="SELECT mname,location,nation_name,'Talent_level_up_materials' AS type,open_day " + \
            ",%s AS used_by_characters " + \
            "from Materials M, Nations N, Locate L,Talent_level_up_materials Loc,Characters C, Level_up U " + \
            "where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid "
          para = [dic['cname']]
        if (len(dic) > 0):
          sql2 = sql2 + ' and '
        data = []
        for col in dic:
          if (col == 'nation_name'):
            part = []
            for n in dic[col]:
              part.append(col + '=' + '%s')
              para.append(n)
            data.append('(' + ' or '.join(part) + ')')
          elif (col == 'open_day'):
            part = []
            if '1' in dic[col]:
              part.append(col + " like '%%1%%' ")
            if '2' in dic[col]:
              part.append(col + " like '%%2%%' ")
            if '3' in dic[col]:
              part.append(col + " like '%%3%%' ")
            if '4' in dic[col]:
              part.append(col + " like '%%4%%' ")
            if '5' in dic[col]:
              part.append(col + " like '%%5%%' ")
            if '6' in dic[col]:
              part.append(col + " like '%%6%%' ")
            if '7' in dic[col]:
              part.append(col + " like '%%7%%' ")
            data.append('(' + ' and '.join(part) + ')')
          else:
            data.append(col + '=' + '%s')
            para.append(dic[col])
        sql2 = sql2 + ' and '.join(data) + ' Group by Loc.mid,mname,location,nation_name,open_day'
        cursor2 = g.conn.execute(sql2, para)
        Talent= []
        for result in cursor2:
          Talent.append(result)
        context_t = dict(data_t=Talent)
        cursor2.close()
      if (intype != []) and ('Talent_level_up_materials' not in intype):
        context_t = dict(data_t=[])
      return render_template('materials.html', **context_l,**context_t)

@app.route('/special',methods=['GET', 'POST'])
def special():
    def type_get(u_order, c_order, num_row=5):
      sql_1 = "SELECT O.uid, uname, ulevel, activate_day, number_of_achievements, COUNT(*) AS owning_character_number, " \
              "AVG(O.clevel) AS average_character_level, AVG(O.friendship) AS average_character_friendship "+\
              "from Owning O, Users U, Characters C where O.uid=U.uid and O.cid=C.cid " \
              "GROUP BY O.uid, uname, ulevel, activate_day, number_of_achievements" \
              +" ORDER BY {} DESC".format(u_order)
      if num_row != 'All':
        sql_1 += " limit {}".format(num_row)
      cursor_u = g.conn.execute(sql_1)
      users = []
      for result in cursor_u:
        users.append(result)  # can also be accessed using result
      context_1 = dict(data_u=users)
      cursor_u.close()
      sql_2 = "SELECT cname, C.elements, C.character_rarity, COUNT(*) AS number_of_user_owing, " \
              " AVG(O.clevel) AS average_character_level, AVG(O.friendship) AS average_character_friendship " + \
              "from Owning O, Users U, Characters C where O.uid=U.uid and O.cid=C.cid " \
              "GROUP BY O.cid, cname, C.elements, C.character_rarity" \
              + " ORDER BY {} DESC".format(c_order)
      if num_row != 'All':
        sql_2 += " limit {}".format(num_row)
      cursor_c = g.conn.execute(sql_2)
      characters = []
      for result in cursor_c:
        characters.append(result)  # can also be accessed using result
      context_2 = dict(data_c=characters)
      cursor_u.close()
      return context_1, context_2

    if request.method == 'GET':
      context_1, context_2 = type_get(u_order='O.uid', c_order='cname')
      return render_template('special.html', **context_1, **context_2)
    else:
      number_rows = request.form.getlist('num_row')
      print("number_rows", number_rows)
      if 'All' in number_rows:
        num_rows = 'All'
      elif '10' in number_rows:
        num_rows = 10
      else:
        num_rows = 5
      order_target = request.form.getlist('order')
      print("order_target", order_target)
      if 'Both' in order_target:
        order = 'All'
      elif 'User' in order_target:
        order = 'User'
      else:
        order = 'Character'
      print("order", order)
      order_type = []
      ulevel = request.form.get('ulevel')
      order_type.append(ulevel)
      activate_day = request.form.get('activate_day')
      order_type.append(activate_day)
      number_of_achievements = request.form.get('number_of_achievements')
      order_type.append(number_of_achievements)
      owning_number = request.form.get('owning_number')
      order_type.append(owning_number)
      average_clevel = request.form.get('average_clevel')
      order_type.append(average_clevel)
      average_friendship = request.form.get('average_friendship')
      order_type.append(average_friendship)
      submit = request.form.get('search')
      print("order_type", order_type)
      cols_user = ['ulevel', 'activate_day', 'number_of_achievements']
      cols_char = ['owning_number', 'average_character_level', 'average_character_friendship']
      if submit == 'search':
        if order == 'User':
          cols = cols_user
        elif order == 'Character':
          cols = ['', '', '']+cols_char
        else:
          cols = cols_user + cols_char
        tmp = []
        print('cols', cols)
        for i in range(len(cols)):
          if order_type[i] != '' and order_type[i] != None:
            tmp.append(cols[i])
        print("tmp", tmp)
        def get_two_order(order_type, order):
          if order_type == 'owning_number':
            if order == 'All':
              return 'owning_character_number', 'number_of_user_owing'
            elif order == 'User':
              return 'owning_character_number', 'cname'
            else:
              return 'O.uid', 'number_of_user_owing'
        if len(tmp) > 1:
          c1, c2 = type_get(u_order='O.uid', c_order='cname')
          return render_template('special.html', **c1, **c2, wrong='Please ONLY choose one order type!')
        elif len(tmp) == 1:
          if order == 'All':
            if tmp[0] in cols_char:
              if tmp[0] == 'owning_number':
                u_order, c_order = get_two_order(tmp[0], order)
              else:
                u_order, c_order = tmp[0], tmp[0]
              context_1, context_2 = type_get(u_order=u_order, c_order=c_order, num_row=num_rows)
            else:
              context_1, context_2 = type_get(u_order=tmp[0], c_order='cname', num_row=num_rows)
          elif order == 'User':
            if tmp[0] == 'owning_number':
              u_order, c_order = get_two_order(tmp[0], order)
            else:
              u_order, c_order = tmp[0], 'cname'
            context_1, context_2 = type_get(u_order=u_order, c_order=c_order, num_row=num_rows)
          else:
            if tmp[0] in cols_char:
              if tmp[0] == 'owning_number':
                u_order, c_order = get_two_order(tmp[0], order)
              else:
                u_order, c_order = 'O.uid', tmp[0]
              context_1, context_2 = type_get(u_order=u_order, c_order=c_order, num_row=num_rows)
            else:
              context_1, context_2 = type_get(u_order='O.uid', c_order='cname', num_row=num_rows)
        else:
          context_1, context_2 = type_get(u_order='O.uid', c_order='cname', num_row=num_rows)
        return render_template('special.html', **context_1, **context_2)

    #return render_template('special.html')

def this_is_never_executed():
  print('***')
  pass


@app.route('/login')
def login():
    os.abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d"% (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
