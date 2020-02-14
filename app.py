from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
CORS(app)

def load_db():
	with open("database.JSON", "r") as f:
		database = json.load(f)
	return database
	# Look up and find the database file (database.JSON)
	# Save it as something or return it 

def save_db(database):
	with open("database.JSON", "w") as f:
		json.dump(database, f, indent=4)



@app.route("/diaryentry", methods=["GET"])
@cross_origin()
def get_all_diary_entries():
	db = load_db()
	n_entries = len(db)
	response = {
		'message': 'Successfully got all diary entries!',
		'entries': db,
		'count': n_entries 
	}
	return jsonify(response), 200
	# I need a function to load my database
	# Then I need to make my database be JSON 
	# Then I need to return the JSON to the user
	# Do I need to do anything else? 
@app.route("/diaryentry/<entryid>", methods=["GET"])
@cross_origin()
def get_diary_entry(entryid):
	db = load_db()
	data = db.get(entryid)
	success_response = {
		'message': 'Successfully found your entry id',
		'data': data,
		'entryid': entryid
	}

	if data is None:
		return jsonify({'message':f'Could not find your entry with id {entryid}'}), 404
	return jsonify(success_response), 200
	# We need to load our database 
	# We need to search the database for our entryid
	# We need to return the entry associated to the entryid
	# We want to return that entry to the user with a success message
	# If that id doesn't exist, let the user know their entry id wasn't available


@app.route("/diaryentry", methods=["POST"])
@cross_origin()
def create_diary_entry():
	
	data = json.loads(request.data)
	
	db = load_db()
	unique_id = str(uuid4())
	db[unique_id] = data

	db[unique_id]["createdat"] = str(datetime.now())

	save_db(db)

	response = {
		'message': 'New entry created',
		'data': data,
		'id': unique_id
	}
	return jsonify(response), 201

	# Get the data from the post request
	# Save the data into a variable 
	# Load the database 
	# Give the new entry an id 
	# Add the new entry to the database
	# Give the new entry a timestamp 
	# Return the new entry + a success message to the user 

@app.route("/diaryentry/<entryid>", methods=["PUT"])
@cross_origin()
def update_diary_entry(entryid):
	data = json.loads(request.data)

	db = load_db()
	db[entryid]['title'] = data['title']
	db[entryid]['description'] = data['description']

	save_db(db)

	response = {
		'message': 'Entry updated!',
		'data': db[entryid],
		'id': entryid
	}

	return jsonify(response), 201


@app.route("/diaryentry/<entryid>", methods=["DELETE"])
@cross_origin()
def delete_diary_entry(entryid):
	db = load_db()
	db.pop(entryid)

	save_db(db)

	response = {
		'message': 'Entry deleted',
	}

	return jsonify(response), 200










