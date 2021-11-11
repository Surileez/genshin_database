 Genshin database web application
 ==================================================
 ### By: Siyu Li(sl4826), Zhibo Dai(zd2263)
 ### PostgreSQL account: zd2263
 ### url: http://34.75.164.72:8111/
 
 ### Original proposal :
 In part 1, we proposed that: using this application, visitors can not only find the basic information of the game but also the users, which is not common in other sites. They can check how many users have one specific character or who is the character that users owe most. Those parts have all been implemented in our application. </br>
The basic game-related information can be found on webpage Users: game players, Characters basic information, Weapons basic information, and Local materials and talent_level_up materials. For more information related to the user owning characters, Owning: users' characters page has that information.  </br>
The most interesting parts are on Other special requests page. On this page, visitors can see not only who are the popular characters that users owe most, but also who are top users who own most characters or have the highest average character level. Visitors can choose the criteria to get the top users and popular characters they want. For more specific descriptions, please check the special page part. </br>
In a word, we have implemented all features we proposed in part 1. </br>
 
 ### Data sources:
 For basic game information, including characters, weapons, materials, nations, and so on, we collect information from the website https://genshin.honeyhunterworld.com/?lang=EN by request library in Python. After we receive the information from the website, we use Regular expressions to catch the information we need.  </br>
	For user information, we used a script from https://github.com/babalae/genshin-info to collect. It can get user information by searching user id. However, the result is in image format so we used Tencent OCR to get the text from images. After collecting text information, we transform them into CSV files and insert commands to add data into the database.  </br>
	Now all the characters, weapons, materials related information is in our database. For the user information, we only got 60 users. Because the OCR took a lot of time to process and there may be some fault in recognizing text so we have to double-check the result. It took us quite a lot of time. As a result, we decided to use 60 users' information first. The code for collecting and processing data is in the folder data processing. </br>
 
 ### Web pages and how to use:
 ##### Login in:
 This application only allows users in our database to login in. If you don't type UID and name completely or you input wrong type of UID(must be integer) or the UID and name do not match our database, you will get a message to notice that you have made something wrong. </br>
 NOTICE: For log in, please try UID:45, Name:MHY.(one user in our database)</br>
 After login in successfully, you will reach search page including different link of pages to do search. </br>
 NOTICE: Each page we will show 5 rows on the top, and you can know what you can search for and which format you should input. On each page except special requests page, if you input nothing and click search, you will get the whole table. If you input wrong type of text, we will notice you(for example: You must input integer).

 ##### Local materials and talent level up materials(Interesting web pages!)
 Description: This page is for users to search local materials and talent level up materials to find basic information about the materials such as location, name and open day, as well as level up information about materials used by characters. </br>
 It combines table Materials, Loc_materials, Talent_level_up_materials, Level_up, Nations, Characters in our database. Notice that open_day is the attribute only for talent_level_up materials in our database, because these materials can only be gained in domain having specific open days in a week, while local materials can just be picked up any time you want, also you can regard its open_day as from Mon to Sun. And we use type to clearly show users the kind of materials.</br>
 Users can input name of materials, location, name of nation, type of materials, open day, and name of character to search what they need. After receiving those parameters, we ask the cursor to execute SQL we wrote before.</br>
 If users input character's name, we will show users the information of the materials used by the character. 
 ```
 SELECT mname,location,nation_name,'Loc_materials' AS type, %s AS used_by_characters
 from Materials M, Nations N, Locate L,Loc_materials Loc,Characters C, Level_up U
 where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid and (cname=%s,...)
 ```
You can also do multiple search, and (...) will change according to your requirements.</br>
</br>
If users do not input character's name, we will instead show all characters who use the materials using 'string_agg' and 'group by' in SQL.
 ```
 SELECT mname,location,nation_name,'Talent_level_up_materials' AS type,open_day, string_agg(cname,',') AS used_by_characters
 from Materials M, Nations N, Locate L,Talent_level_up_materials Loc,Characters C, Level_up U 
 where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid (...)
 Group by Loc.mid,mname,location,nation_name,open_day 
 ```
 (...) will change according to your requirements.</br>
 Notice that we avoid SQL injection by always using format like 'column name'=%s, only %s is what we get from users' input. And we use some select boxes to let users select rather than input, it is both safe for our database and convenient for users.</br>
 
 Why do we think this page is interesting? :</br>
 Because this page combines information of different kinds of materials and information about level up, it is covenient for users to quickly find which materials the character required as well as well and when to get those materials. Thus, users can level up their characters easily.
  
 
 ##### Other special requests(Interesting web pages!)
 Description: On the special search page, users can see top users and popular characters ordered by their needs. The order types unique for users include User Level, Activate Day, Number of Achievements. For both users and characters, types include Owning Number, Average Character Level, Average Character Friendship.  </br>
	Users can choose what they want to see, how to order the result, and the number of rows by clicking corresponding checkboxes. After choosing what he or she needs, click the search bottom and the application will show the result. </br>
	In our application, the user must choose to see the top users, popular characters, and both of them by choosing the bottom in Order Target. We only accept one order type used to order the result. If we receive more than one, we will show an alert to ask the user to choose only one. </br>
	The user can choose to see the result in the top 5, top 10, or all the results. If the user doesn't choose anyone, the application will return the top 5 as default.
	The order type inputs are used to decide the SQL order by which attribute. The order target inputs are used to decide which SQL to use order type value. For example, if order target = User, only sql_1, which queries user info more, will use the order type value to order the SQL result. </br>
	After receiving those parameters, we ask the cursor to execute SQL we wrote before, something like:  
 ```
"SELECT cname, C.elements, C.character_rarity, COUNT(*) AS number_of_user_owing, AVG(O.clevel) AS average_character_level,  AVG(O.friendship) AS average_character_friendship
from Owning O, Users U, Characters C 
where O.uid=U.uid and O.cid=C.cid 
GROUP BY O.cid, cname, C.elements, C.character_rarity ORDER BY {} DESC".format(c_order)
+ " limit {}".format(num_row)
```
Why do we think this page is interesting? :</br>
 Because this page provides a unique way for visitors to see the users' and characters' ranking in their need ways. They can find which character is most loved by all other users and who is the player with the highest average character levels. Those things are hard to get from other normal game database websites. And that's what we hoped to achieve in part 1.

 ##### Users: game players
 This page is information about game players, including uid, user_name, level, activate_day, number_of_achievements, deep_spiral.  
 ##### Owning: users' characters
 This page is for users to search users' owning characters, including uid, user_name, character_name, character_element, character_rarity, character_level, friendliness and constellation.
 ##### Characters basic information
 This page is for users to search basic information about characters, including name, element, rarity, weapon_type, birthday, base_attack, base_hp, base_defence and nation_name. 
 ##### Weapons basic information
 This page is for users to search basic information about weapons, including name, rarity, weapon_type, base_attack, extra_attribute and its value. 



