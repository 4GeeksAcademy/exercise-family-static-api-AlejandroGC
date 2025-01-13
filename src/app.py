"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_members():
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except:
        return "An error has occurred", 400

@app.route('/members/<int:id>', methods=['GET'])
def handle_get_member(id):
    # this is how you can use the Family datastructure by calling its methods
    try:
        member = jackson_family.get_member(id)
        if len(member) == 0:
            return "Id of the member not found", 400
        return jsonify(member), 200
    except:
        return "An error has occurred", 400

@app.route('/members', methods=['POST'])
def handle_create_member():
    # this is how you can use the Family datastructure by calling its methods
    try:
        request_body = request.get_json(force=True)
        keys = request_body.keys()
        if len(keys) != 3 or "first_name" not in keys or "age" not in keys or "lucky_numbers" not in keys:
            return "You must enter the keys 'last_name', 'age' and 'lucky numbers'", 400
        elif type(request_body['first_name']) != str:
            return "The key 'first_name' must be a str", 400
        elif type(request_body['age']) != int:
            return "The key 'age' must be an int", 400
        elif type(request_body['lucky_numbers']) != list:
            return "The key 'lucky_numbers' must be a list", 400
        
        members = jackson_family.add_member(request_body)
        return jsonify(members), 200
    except:
        return "An error has occurred", 400

@app.route('/members/<int:position>', methods=['DELETE'])
def handle_delete_member(position):
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.delete_member(position)
        if members == False:
            return "Id of the member not found", 400
        return jsonify(members), 200
    except:
        return "An error has occurred", 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
