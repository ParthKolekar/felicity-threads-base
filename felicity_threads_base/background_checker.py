import _mysql
import json
db = _mysql.connect("10.4.8.62" , "contest" , "saphira" , "felicity_threads_base")
db.query("""SELECT user_nick , user_score, user_username FROM base_user JOIN cache_in_submission JOIN cache_in_question WHERE submission_state = 'AC' AND base_user.id = submission_user_id AND submission_question_id = cache_in_question.id AND user_access_level = question_level + 1 GROUP BY user_nick ORDER BY user_score DESC, submission_timestamp ASC LIMIT 20;
""")
r = db.store_result()
x = r.fetch_row( r.num_rows() )

st = ""

for xx in x:
	print "%-30s\t%-30s\t%-30s" % xx

