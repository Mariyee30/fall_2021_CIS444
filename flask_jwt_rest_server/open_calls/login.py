from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import jwt

def handle_request():
	logger.debug("Login Handle Request")
	#use data here to auth the user

	username_from_user_form = request.form['username']
	password_from_user_form = request.form['password']

	cursor = g.db.cursor()

	cursor.execute("SELECT * FROM users WHERE username = '%s';" % (username_from_user_form))
	row = cursor.fetchone()

	if row is None:
		return json_response(data={"message": "The username '" + username_from_user_form + "' does not exist."}, status=404)

	else:
		if password_from_user_form == row[2]:
			user = {"user_id": row[0]}
			return json_response(data={"jwt": create_token(user)})
		else:
			return json_response(data={"message": "The password for '" + username_from_user_form + "' is incorrect."}, status=404)
