import _mysql
import json
db = _mysql.connect("10.4.8.62" , "contest" , "saphira" , "felicity_threads_base")
db.query("""SELECT user_nick , user_score, submission_timestamp FROM base_user JOIN cache_in_submission JOIN cache_in_question WHERE submission_state = 'AC' AND base_user.id = submission_user_id AND submission_question_id = cache_in_question.id AND user_access_level = question_level + 1 GROUP BY user_nick ORDER BY user_score DESC, submission_timestamp ASC;
""")
r = db.store_result()
f = open('static/score.json' , 'w')
json.dump( r.fetch_row( r.num_rows() ), f )

