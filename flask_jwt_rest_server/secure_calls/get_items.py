from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import json

def handle_request():
	logger.debug("Get Items Handle Request")

	cursor = g.db.cursor()

	try :
		user_id = g.jwt_data['user_id']
		#string = " ".join(("SELECT * FROM items WHERE NOT EXISTS","(SELECT FROM purchased WHERE items.id = purchased.item_id AND",str(user_id),"= purchased.user_id);"))
		#cursor.execute(string, user_id)
		cursor.execute("select * from items;", user_id)
		print("Got Items")

	except:
		print("Did not get the items.")
		return json_response(data={"message": "Did not get the items."}, status=500)


	message = "{\"items\":["
	count = 0

	while 1:
		database_row = cursor.fetchone() 
		if database_row is None: 
			print("No more items.")
			break;
		else: 
			print("Adding items")
			if count > 0: 
				message += ","
			message += "{\"type\": \"%s\", \"name\": \"%s\", \"cost\": \"%s\", \"id\": %s}" % (database_row[1], database_row[2], (database_row[3]), str(database_row[0]))
			count += 1 
	message += "]}"

	print("Added items")

	return json_response(data = json.loads(message))
