#!/usr/bin/env python

import ldap
import _mysql
import json
db = _mysql.connect("192.168.1.1" , "contest" , "saphira" , "felicity_threads_base")
con = ldap.initialize('ldap://192.168.1.3')
con.simple_bind_s( "uid=generic_portal,ou=services,dc=felicity,dc=iiit,dc=ac,dc=in" , "generic_pass" )
db.query("""SELECT user_nick , user_score , user_username FROM base_user JOIN cache_in_submission JOIN cache_in_question WHERE submission_state = 'AC' AND base_user.id = submission_user_id AND submission_question_id = cache_in_question.id AND user_access_level = question_level + 1 GROUP BY user_nick ORDER BY user_score DESC, submission_timestamp ASC;
""")
r = db.store_result()
x = r.fetch_row( r.num_rows() )
x = list(x)
y=[]
for xx in x:
        name = con.search_s( "ou=users,dc=felicity,dc=iiit,dc=ac,dc=in" , ldap.SCOPE_SUBTREE , 'uid='+xx[2] , ['displayName', 'sn' , 'givenName' , 'o'])[0][1]
	y.append(['','','','',''])
	y[-1][0]=name['displayName']
	y[-1][1]=''#str(name['givenName'][0])+' '+str(name['sn'][0])
	y[-1][3]=name['o']
	y[-1][4]=xx[1]

y.append(['ghost_rider','','','International Institute of Information Technology, Hyderabad','0.7.7.7'])
f = open('static/score2.json' , 'w')
json.dump( y, f )

