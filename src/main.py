from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils import APIException, sha256
from models import db, Consultants, logintokens, interviews, websitemessages, datavaultusers, usersmessageslivechat
from flask_jwt_simple import JWTManager, jwt_required, create_jwt
import os
from flask_mail import Mail, Message
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

loginEmail = os.environ.get('LOGIN_EMAIL')
loginPassword = os.environ.get('LOGIN_PASSWORD')
# TEST sending email from rackspace
emailSenderTest = os.environ.get('EMAIL_SENDER')
passwordSenderTest = os.environ.get('PASSWORD_SENDER')

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
            firstname = form_body['c_firstname'],
            lastname = form_body['c_lastname'],
            email = form_body['c_email'],
            time = form_body['Time'],
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
        countMessages = websitemessages.query.filter_by(read_flag=0).count()

        if not countMessages:
            return jsonify({'msg':'Count Messages not found'}), 404

        return jsonify(countMessages), 200

    return "Invalid Method", 404

@app.route('/messageProcessed', methods=['PUT', 'POST'])
def processed_message():

    body = request.get_json()

    if request.method == 'PUT':
        updateMessage = websitemessages.query.get(body['id'])

        if updateMessage is None:
            raise APIException('Message not found', status_code=404)

        if "read" in body:
            updateMessage.read_flag = body["read"]

            db.session.commit()
            return jsonify({
                'updated': 'success',
                'msg': 'Successfully Updated'
            })
    
    if request.method == 'POST':
        deleteMessage = websitemessages.query.get(body['id'])
        db.session.delete(deleteMessage)
        db.session.commit()
        return jsonify({
            'updated': 'success',
            'msg': 'Successfully Deleted'
        })

    return "Invalid Method, try again", 404

@app.route('/updatePasswordDatavault', methods=['PUT'])
def update_password():

    body = request.get_json()

    if request.method == 'PUT':
        user = datavaultusers.query.filter_by(email=body['email'], password=sha256(body['oldpassword'])).first()

        if not user:
            return 'User not found', 404

        if "oldpassword" in body:
            user.password = sha256(body['newpassword'])

            db.session.commit()
            return jsonify({
                'updated': 'success',
                'msg': 'Successfully Updated'
            })

    return "Invalid Method, try again", 404

@app.route('/loginDatavaultCourses', methods=['POST'])
def handle_loginDatavault():

    body = request.get_json()

    user = datavaultusers.query.filter_by(email=body['email'], password=sha256(body['password'])).first()

    if not user:
        return 'Wrong Password or Email', 404

    return jsonify({
              'token': create_jwt(identity=1),
              'id': user.id,
              'email': user.email,
              'firstname': user.firstname,
              'lastname': user.lastname,
              'courses': user.courses
              })

@app.route('/registerDatavaultCourses', methods=['POST'])
def handle_registerDatavault():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'firstname' not in body and 'lastname' not in body:
        raise APIException("You need to specify the first name and last name", status_code=400)
    if 'password' not in body and 'email' not in body:
        raise APIException("You need to specify the password and email", status_code=400)
    if 'firstname' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'lastname' not in body:
        raise APIException('You need to specify the last name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)

    db.session.add(datavaultusers(
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        password = sha256(body['password'])
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'Successfully Registered'
    })

@app.route('/students', methods=['GET'])
def list_students():

    if request.method == 'GET':
        allStudents = datavaultusers.query.all()

        if not allStudents:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in allStudents] ), 200

    return "Invalid Method", 404

@app.route('/updateCourses', methods=['PUT'])
def update_courses():

    body = request.get_json()

    if request.method == 'PUT':
        updateCourses = datavaultusers.query.get(body['id'])

        if updateCourses is None:
            raise APIException('Message not found', status_code=404)

        if "course" in body:
            updateCourses.courses = body["course"]

            db.session.commit()
            return jsonify({
                'updated': 'success',
                'msg': 'Successfully Updated'
            })

@app.route('/saveMessagesFromLiveChat', methods=['POST'])
def liveChat_messages_save():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)

    db.session.add(usersmessageslivechat(
        username = body['username'],
        country = body['country'],
        state = body['state'],
        city = body['city'],
        latitude = body['latitude'],
        longitude = body['longitude'],
        ip = body['ip'],
        message = body['message'],
        saveddate = body['saveddate']
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'message saved'
    })

@app.route('/sendEmailTest', methods=['POST'])
def sendEmailTest():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)

    sender_email = emailSenderTest
    password = passwordSenderTest
    receiver_email = body["email_receiver"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
    Hi,
    How are you? It's a message from Samir using Python program
    """
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("secure.emailsrvr.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


######################################################
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)