from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import json

def handle_request():
	logger.debug("Get Items Handle Request")
	cursor = g.db.cursor()
	try:
		cursor.execute("INSERT INTO purchased (user_id, item_id) VALUES (%s, %s);" % (str(g.jwt_data['user_id']), str(request.form['item_id']))) 
		g.db.commit()
		print("Item was crafted.")
		return json_response(data={"message": "Item was crafted."})
	except:
		print("Item was not crafted.")
		return json_response(data={"message": "Item was not crafted."}, status=500)

