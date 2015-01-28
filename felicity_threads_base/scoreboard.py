#!/usr/bin/env python

import _mysql
import json
db = _mysql.connect("192.168.1.1" , "contest" , "saphira" , "felicity_threads_base")
db.query("""SELECT user_nick , user_score FROM base_user JOIN gordian_knot_submission JOIN gordian_knot_question WHERE submission_state = 'AC' AND base_user.id = submission_user_id AND submission_question_id = gordian_knot_question.id AND (user_access_level = question_level OR user_access_level = question_level + 1) GROUP BY user_nick ORDER BY user_score DESC, user_access_level DESC, submission_timestamp ASC;
""")
r = db.store_result()
x = r.fetch_row(r.num_rows())
y=[]
for xx in x:
	y.append(xx)
y.append(('ghost_rider','0.7.7.7'))
y.append(('WATASHI WA HAPPY!!','1.3.3.7'))
y.append(('tajmahal','0.3.2.1'))
y.append(('merci','1'))
f = open('static/score.json' , 'w')
json.dump( y, f )

