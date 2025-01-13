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
    except:
        return "Ha ocurrido un error", 400
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def handle_get_member(id):
    # this is how you can use the Family datastructure by calling its methods
    try:
        member = jackson_family.get_member(id)
    except:
        return "Ha ocurrido un error", 400
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def handle_create_member():
    # this is how you can use the Family datastructure by calling its methods
    request_body = request.get_json(force=True)
    try:
        members = jackson_family.add_member(request_body)
    except:
        return "Ha ocurrido un error", 400
    return jsonify(members), 200

@app.route('/members/<int:position>', methods=['DELETE'])
def handle_delete_member(position):
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.delete_member(position)
    except:
        return "Ha ocurrido un error", 400
    return jsonify(members), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
