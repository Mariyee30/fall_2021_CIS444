from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import jwt

def handle_request():
	logger.debug("Sign Up Handle Request")

	username_from_user_form = request.form['username']
	password_from_user_form = request.form['password']

	cursor = g.db.cursor()

	cursor.execute("SELECT * FROM users WHERE username = '%s';" % (username_from_user_form))
	row = cursor.fetchone()

	if row is None:
		cursor.execute(f"INSERT INTO users (username, password) VALUES " f"('{username_from_user_form}', '{password_from_user_form}');")
		g.db.commit()
		cursor.execute(f"SELECT * FROM users " f"WHERE username = '{username_from_user_form}';")

		row = cursor.fetchone()
		user = {"user_id": row[0]}
		return json_response(data={"jwt": create_token(user)})

	else:
		return json_response(data={"message": "The username '" + username_from_user_form + "' is already taken."}, status=404)
