from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import json

def handle_request():
	logger.debug("Get Books Handle Request")
	cursor = g.db.cursor()
	try:
		cursor.execute("INSERT INTO purchased (user_id, book_id) VALUES (%s, %s);" % (str(g.jwt_data['user_id']), str(request.form['book_id']))) 
		g.db.commit()
		print("Book purchased.")
		return json_response(data={"message": "Book purchased."})
	except:
		print("Book was not purchased.")
		return json_response(data={"message": "Book was not purchased."}, status=500)
