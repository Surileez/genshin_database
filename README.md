 Genshin database web application
 ==================================================
 ### By: Siyu Li(sl4826), Zhibo Dai(zd2263)
 ### PostgreSQL account: zd2263
 ### url: 
 
 ### Original proposal :
 
 ### Data sources:
 
 
 
 
 
 ### How to use:
 ##### Login in:
 This application only allows users in our database to login in. If you don't type UID and name completely or you input wrong type of UID(must be integer) or the UID and name do not match our database, you will get a message to notice that you have made something wrong. </br>
 NOTICE: For log in, please try UID:45, Name:MHY.(one user in our database)</br>
 After login in successfully, you will reach search page including different link of pages to do search. </br>
 NOTICE: Each page we will show 5 rows on the top, and you can know what you can search for and which format you should input. On each page except special requests page, if you input nothing and click search, you will get the whole table. If you input wrong type of text, we will notice you(for example: You must input integer).
 ##### Users: game players
 This page is information about game players, including uid, user_name, level, activate_day, number_of_achievements, deep_spiral.  
 ##### Owning: users' characters
 This page is for users to search users' owning characters, including uid, user_name, character_name, character_element, character_rarity, character_level, friendliness and constellation.
 ##### Characters basic information
 This page is for users to search basic information about characters, including name, element, rarity, weapon_type, birthday, base_attack, base_hp, base_defence and nation_name. 
 ##### Weapons basic information
 This page is for users to search basic information about weapons, including name, rarity, weapon_type, base_attack, extra_attribute and its value. 
 ##### Local materials and talent level up materials(Interesting web pages!)
 Description: This page is for users to search local materials and talent level up materials to find basic information about the materials such as location, name and open day, as well as level up information about materials used by characters. </br>
 It combines table Materials, Loc_materials, Talent_level_up_materials, Level_up, Nations, Characters in our database. Notice that open_day is the attribute only for talent_level_up materials in our database, because these materials can only be gained in domain having specific open days in a week, while local materials can just be picked up any time you want, also you can regard its open_day as from Mon to Sun. 
 
 ```
 SELECT mname,location,nation_name,'Loc_materials' AS type, %s AS used_by_characters
 from Materials M, Nations N, Locate L,Loc_materials Loc,Characters C, Level_up U
 where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid and (cname=%s,....)
 ```
 
 ```
 SELECT mname,location,nation_name,'Talent_level_up_materials' AS type,open_day, string_agg(cname,',') AS used_by_characters
 from Materials M, Nations N, Locate L,Talent_level_up_materials Loc,Characters C, Level_up U 
 where N.nid=L.nid and Loc.mid=M.mid and Loc.mid=L.mid and C.cid=U.cid and Loc.mid=U.mid and(...)
 Group by Loc.mid,mname,location,nation_name,open_day 
 ```
