from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils import APIException
from models import db, Consultants, logintokens, interviews, websitemessages
from flask_jwt_simple import JWTManager, jwt_required, create_jwt
import os
from flask_mail import Mail, Message

# loginEmail = os.environ.get('LOGIN_EMAIL')
# loginPassword = os.environ.get('LOGIN_PASSWORD')

app = Flask(__name__)
app.config.from_object("config")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

# app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
jwt = JWTManager(app)

mail = Mail(app)

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

@app.route('/checkToken', methods=['GET'])
def check_token():
    if request.method == 'GET':
        CheckToken = logintokens.query.filter_by(id=1).first()
        return jsonify(CheckToken.serialize()), 200 

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

@app.route('/newInterview', methods=['POST'])
def new_interview():

    if request.method == 'POST':
        form_body = request.get_json()

        # send email (need to replace recipient by the real consultant email)
        msg = Message(
            'Interview',
            sender='headquarter@datavault.com',
            recipients=['samirbenzada@gmail.com'],
            html=render_template(
                "email.html", 
                firstname=form_body['c_firstname'], 
                lastname=form_body['c_lastname'], 
                time=form_body['Time'],
                client = form_body['Client'],
                vendor = form_body['Vendor'],
                implementationpartner = form_body['ImplementationPartner'],
                mode = form_body['Mode'],
                calltype = form_body['Type'],
                assist1 = form_body['assist1'],
                assist2 = form_body['assist2'],
                saleassociate = form_body['SA'],
                manager = form_body['Manager'],
                livecoding = form_body['LiveCoding'],
                positiontitle = form_body['PositionTitle'],
                jobdescription = form_body['JD'],
                projectduration = form_body['ProjectDuration'],
                projectlocation = form_body['ProjectLocation'],
                clientwebsite = form_body['ClientWebsite'],
                vendorwebsite = form_body['VendorWebsite'],
                interviewername = form_body['InterviewerName'],
                interviewerlinkedIn = form_body['InterviewerLinkedIn'],
                vendornotes = form_body['VendorNotes']
                )
        )
        mail.send(msg)

        # insert to Database
        db.session.add(interviews(
            firstname = body['c_firstname'],
            lastname = body['c_lastname'],
            email = body['c_email'],
            time = body['Time'],
            client = body['Client'],
            vendor = body['Vendor'],
            implementationpartner = body['ImplementationPartner'],
            mode = body['Mode'],
            calltype = body['Type'],
            assist1 = body['assist1'],
            assist2 = body['assist2'],
            saleassociate = body['SA'],
            manager = body['Manager'],
            livecoding = body['LiveCoding'],
            positiontitle = body['PositionTitle'],
            jobdescription = body['JD'],
            projectduration = body['ProjectDuration'],
            projectlocation = body['ProjectLocation'],
            clientwebsite = body['ClientWebsite'],
            vendorwebsite = body['VendorWebsite'],
            interviewername = body['InterviewerName'],
            interviewerlinkedIn = body['InterviewerLinkedIn'],
            vendornotes = body['VendorNotes']
        ))
        db.session.commit()
        
        return jsonify({
            'created': 'success',
            'msg': 'Successfully Saved and Email sent'
        })

    return "Invalid Method", 404

@app.route('/interviews', methods=['GET'])
def list_interviews():

    if request.method == 'GET':
        allInterviews = interviews.query.all()

        if not allInterviews:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in allInterviews] ), 200

    return "Invalid Method", 404

@app.route('/newMessage', methods=['POST'])
def new_message():
    
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            return jsonify({
                'msg': 'empty',
                'txt': 'Form cannot be empty!'
                })
        else:
            db.session.add(websitemessages(
                full_name = body['name'],
                email_address = body['email'],
                contact_message = body['message']
            ))

            db.session.commit()
            return jsonify({
                'msg': 'success',
                'txt': 'message sent successfully'
            })

    return jsonify({
        "msg": "error",
        "txt": "Invalid Method"
    }), 404

@app.route('/allWebsiteMessages', methods=['GET'])
def list_messages():

    if request.method == 'GET':
        allMessages = websitemessages.query.all()

        if not allMessages:
            return jsonify({'msg':'Messages not found'}), 404

        return jsonify( [x.serialize() for x in allMessages] ), 200

    return "Invalid Method", 404

@app.route('/countMessage', methods=['GET'])
def count_messages():

    if request.method == 'GET':
        countMessages = websitemessages.query(read_flag=0).count()

        if not countMessages:
            return jsonify({'msg':'Count Messages not found'}), 404

        return jsonify(countMessages.serialize()), 200

    return "Invalid Method", 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)