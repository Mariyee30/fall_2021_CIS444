from flask import Flask, render_template, request
from flask_json import FlaskJSON, json_response
from dbA3_con import get_db, get_db_instance

import bcrypt
import datetime
import json
import jwt

app = Flask(__name__)
FlaskJSON(app)

# connect to the database
global_db_con = get_db()

TOKEN = None
SECRET = None

with open("secret", "r") as f:
	SECRET = f.read()

@app.route("/", methods=["GET"]) #default endpoint 
def index():
	return render_template("a3.html")

#User Verification

#authenticating user
@app.route("/userauth", methods=["POST"]) #endpoint
def userauth():
	cursor = global_db_con.cursor()

	#call database
	cursor.execute("select * from users where username = '" + request.form["username"] + "';")
	database_row = cursor.fetchone()

	if database_row is None:
		print("Username '" + request.form["username"] + "' is invalid.")
		return json_response(data = {"message" : "Username '" + request.form["username"] + "' does not exist."}, status = 404)
	else: 
#		if bcrypt.checkpw(bytes(request.form["password"], "utf-8"), bytes(database_row[2], "utf-8")) == True:
		if request.form['password'] == database_row[2]:
			global TOKEN, SECRET
			TOKEN = jwt.encode({"user_id": database_row[0]}, SECRET, algorithm="HS256")
			return json_response(data = {"jwt" : TOKEN})
		else:
			print("Incorrect password.")
			return json_response(data = {"message" : "Incorrect password."}, status = 404)

def validToken(token):
	if TOKEN is None:
		print("No token available.")
		return False
	else:
		server = jwt.decode(TOKEN, SECRET, algorithms=["HS256"])
		client = jwt.decode(token, SECRET, algorithms=["HS256"])

		if server == client:
			print("Token authorized.")
			return True
		else:
			print("Token not authorized.")
			return False

#creating user
#def signup():
#	cursor = global_db_con.cursor()
#	form = request.form

	#call database
#	cursor.execute("SELECT * FROM users WHERE username = '" + request.form["username"] + "';")

	#if username is available, allow for user creation
#	if cursor.fetchone() is None:
#		user = request.form["username"]
#		encrypt_password = bcrypt.hashpw(bytes(form['password'], 'utf-8'), bcrypt.gensalt(11))
#		cursor.execute("INSERT INTO users (id, username, password) values (3, '" + user + "', '" + encrypt_password + "');")
		#important commit created user to db
#		global_db_con.commit() 
#		print('User "' + form['username'] + '" created.')
#		return json_response(data = {"message" : "User account created."})
#	else:
#		print('Error: "' + form['username'] + '" already exists.')
#		return json_response(data = {"message" : "Username is already in use."}, status = 404)

#Getting Bookstore

#pulling the books from the database
@app.route("/getbooks", methods=["POST"]) #endpoint
def getbooks():
	if validToken(request.form["jwt"]) == True:
		print("Token is valid... pulling books")
		cursor = global_db_con.cursor()

		try:
			cursor.execute("select * from books;")
			print("Pulled Books.")

		except:
			print("Could not find books.")
			return json_response(data = {"message" : "Could not find books."}, status = 500)

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
	else:
		print("Invalid Token.")
		return json_response(data = {"message" : "Invalid Token."}, status = 404)

#TODO: DISPLAY PURCHASED BOOKS IN SEPERATE TABLE

#def getpurchasedbooks():
#	if validToken(request.form["jwt"]) == True:
#		cursor = global_db_con.cursor()

#		try:
#			print("Pulling Books")
#			cursor.execute("select * from purchased;")

#		except:
#			print("No purchased books.")
#			return json_response(data = {"message" : "No purchased books."}, status = 500)

#		message = "{\"books\":["
#		count = 0

#		while 1:
#			database_row = cursor.fetchone()
#			if database_row is None:
#				print("No more books.")
#				break;
#			else:
#				if count > 0:
#					message += ","
#				message += "{\"title\": \"%s\", \"author\": \"%s\", \"price\": %s, \"book_id\": %s}" % (database_row[1], database_row[2], str(database_row[3]), str(database_row[0]))
#				count += 1
#		message += "]}"
#		return json_response(data = json.loads(message))
#	else:
#		return json_response(data = {"message" : "Invalid Token."}, status = 404)

#buying books will add it into the purchased table, but the user can still buy multiple copies of one book
@app.route('/purchase', methods=["POST"]) #endpoint
def purchase():
	cursor = global_db_con.cursor()

	try:
		global SECRET
		decoded = jwt.decode(TOKEN, SECRET, algorithms=["HS256"])
		cursor.execute("INSERT INTO purchased (user_id, book_id) VALUES(%s, %s);" % (str(decoded['user_id']), str(request.form['book_id'])))
		global_db_con.commit()
		print("Book Purchased.")
		return json_response(data={"message": "Book purchased."})

	except:
		return json_response(data = {"message" : "Failed to write to database."}, status = 500)

app.run(host='0.0.0.0', port=80)
