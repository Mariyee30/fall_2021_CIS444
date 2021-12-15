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

		user_id = g.jwt_data['user_id']

		#string = " ".join(("SELECT name FROM items WHERE", "(SELECT FROM purchased WHERE items.item_id = purchased.item_id AND", str(user_id), "= purchased.user_id);"))
		string = "SELECT name FROM items WHERE item_id = 1"
		cursor.execute(string, user_id)
		message = "{\"items\":["
		count = 0

		while 1:
			database_row = cursor.fetchone()
			if database_row is None:
				print("No more items in the inventory.")
				break;
			else:
				print("Adding items from inventory")
				if count > 0:
					message += ","
				message += "{\"name\": \"%s\"}" % (database_row[0])
				count += 1
		message += "]}"

		print("Added inventory items")
		return json_response(data = json.loads(message))
		#return json_response(data={"message": "Item was crafted."})
	except:
		print("Item was not crafted.")
		return json_response(data={"message": "Item was not crafted."}, status=500)

