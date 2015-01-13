import _mysql
import json
db = _mysql.connect("localhost" , "root" , "saphira" , "felicity_threads_base")
db.query("""SELECT user_nick , user_score FROM base_user ORDER BY user_score DESC , user_total_time ASC""")
r = db.store_result()
f = open('static/score.json' , 'w')
json.dump(r.fetch_row() , f)

