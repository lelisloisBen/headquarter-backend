from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException
from models import db, Consultants
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

@app.route('/consultant', methods=['GET'])
def handle_consultant():

    if request.method == 'GET':
        consultant = Consultants.query.all()

        if not consultant:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in consultant] ), 200

    return "Invalid Method", 404

@app.route('/add-consultant', methods=['POST'])
def new_consultant():
    
    if request.method == 'POST':
        body = request.get_json()
        db.session.add(Consultants(
            firstname = body['firstname'],
            lastname = body['lastname'],
            birthdate = body['birthdate'],
            gender = body['gender'],
            address = body['address'],
            city = body['city'],
            state = body['state'],
            zipCode = body['zipCode'],
            emailPerso = body['emailPerso'],
            emailWork = body['emailWork'],
            phone = body['phone'],
            skype = body['skype'],
            bankName = body['bankName'],
            routing = body['routing'],
            account = body['account']
        ))

        db.session.commit()
        return jsonify({
            'created': 'success',
            'msg': 'Successfully Added'
        })

    return "Invalid Method", 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)