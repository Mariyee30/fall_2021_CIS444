from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import json

def handle_request():
	logger.debug("Get Books Handle Request")

	cursor = g.db.cursor()

	try :
		user_id = g.jwt_data['user_id']
		#string = " ".join(("SELECT * FROM books WHERE NOT EXISTS","(SELECT FROM purchased WHERE books.id = purchased.book_id AND",str(user_id),"= purchased.user_id);"))
		#cursor.execute(string, user_id)
		cursor.execute("select * from books;", user_id)
		print("Got Books")

	except:
		print("Did not get the books!?")
		return json_response(data={"message": "Did not get books."}, status=500)


	message = "{\"books\":["
	count = 0

	while 1:
		database_row = cursor.fetchone() 
		if database_row is None: 
			print("No more books.")
			break;
		else: 
			print("Adding books")
			if count > 0: 
				message += ","
			message += "{\"title\": \"%s\", \"author\": \"%s\", \"price\": %s, \"book_id\": %s}" % (database_row[2], database_row[1], str(database_row[3]), str(database_row[0]))
			count += 1 
	message += "]}"

	print("Adding books")

	return json_response(data = json.loads(message))
