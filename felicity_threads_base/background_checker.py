#!/usr/bin/env python
import ldap
import _mysql
import json

# Connect To Data Sources
db = _mysql.connect("192.168.1.1" , "contest" , "saphira" , "felicity_threads_base")
con = ldap.initialize('ldap://192.168.1.3')
con.simple_bind_s( "uid=generic_portal,ou=services,dc=felicity,dc=iiit,dc=ac,dc=in" , "generic_pass" )

db.query("""SELECT user_nick , user_score, user_username FROM base_user JOIN cache_in_submission JOIN cache_in_question WHERE submission_state = 'AC' AND base_user.id = submission_user_id AND submission_question_id = cache_in_question.id AND user_access_level = question_level + 1 GROUP BY user_nick ORDER BY user_score DESC, submission_timestamp ASC LIMIT 25;
""")
r = db.store_result()
x = r.fetch_row( r.num_rows() )
x = list(x)

for xx in x:
	name = con.search_s( "ou=users,dc=felicity,dc=iiit,dc=ac,dc=in" , ldap.SCOPE_SUBTREE , 'uid='+xx[2] , ['sn' , 'givenName' , 'o'])[0][1]
	fn = name['givenName']
	sn = name['sn']
	o = name['o']

	kawaii = list(xx) + fn + sn + o
	print "%-20s %-5s %-40s %-15s %-15s %-30s" % tuple(kawaii)
