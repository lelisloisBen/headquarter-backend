from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException
from models import db, Consultants, logintokens
from flask_jwt_simple import JWTManager, jwt_required, create_jwt
import os

loginEmail = os.environ.get('LOGIN_EMAIL')
loginPassword = os.environ.get('LOGIN_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

@app.route('/login', methods=['POST'])
def handle_login():
    body = request.get_json()

    if body is None:
        return jsonify({
                'msg': 'login cannot be empty'
                })
    else:
        if body['email'] != loginEmail:
            return jsonify({
                'msg': 'wrong email'
                })
        elif body['password'] != loginPassword:
                return jsonify({
                'msg': 'wrong password'
                })
        else:
            TheLoginToken = create_jwt(identity=1)

            saveToken = logintokens.query.filter_by(id=1).first()
            saveToken.token = TheLoginToken
            db.session.commit()

            return jsonify({
                'token': TheLoginToken,
                'email': body['email'],
                'name': "admin"
                })

    return "Invalid Method", 404


@app.route('/consultant', methods=['GET'])
def handle_consultant():

    if request.method == 'GET':
        consultant = Consultants.query.all()

        if not consultant:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in consultant] ), 200

    return "Invalid Method", 404

@app.route('/consultant/<int:id>', methods=['PUT', 'GET'])
def get_single_consultant(id):

    body = request.get_json() #{ 'username': 'new_username'}

    if request.method == 'PUT':
        user = Consultants.query.get(id)
        user.firstname = body.firstname
        db.session.commit()
        return jsonify(user.serialize()), 200

    if request.method == 'GET':
        user = Consultants.query.get(id)
        return jsonify(user.serialize()), 200

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