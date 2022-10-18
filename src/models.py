from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class logintokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<logintokens %r>' % self.token

    def serialize(self):
        return {
            "id": self.id,
            "token": self.token
        }

class Consultants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    birthdate = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zipCode = db.Column(db.String(120))
    emailPerso = db.Column(db.String(120))
    emailWork = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    skype = db.Column(db.String(120))
    last4ssn = db.Column(db.String(12))
    trainingstart = db.Column(db.String(12))
    cohort = db.Column(db.String(12))

    def __repr__(self):
        return '<Consultants %r>' % self.firstname

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "emailPerso": self.emailPerso,
            "emailWork": self.emailWork,
            "phone": self.phone,
            "skype": self.skype,
            "last4ssn": self.last4ssn,
            "trainingstart": self.trainingstart,
            "cohort": self.cohort
        }

class interviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(120))
    client = db.Column(db.String(120))
    vendor = db.Column(db.String(120))
    implementationpartner = db.Column(db.String(120))
    mode = db.Column(db.String(120))
    calltype = db.Column(db.String(120))
    assist1 = db.Column(db.String(120))
    assist2 = db.Column(db.String(120))
    saleassociate = db.Column(db.String(120))
    manager = db.Column(db.String(120))
    livecoding = db.Column(db.String(120))
    positiontitle = db.Column(db.String(120))
    jobdescription = db.Column(db.Text, nullable=False)
    projectduration = db.Column(db.String(120))
    projectlocation = db.Column(db.String(120))
    clientwebsite = db.Column(db.String(120))
    vendorwebsite = db.Column(db.String(120))
    interviewername = db.Column(db.String(120))
    interviewerlinkedIn = db.Column(db.String(120))
    vendornotes = db.Column(db.String(120))

    def __repr__(self):
        return '<interviews %r>' % self.firstname

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "time": self.time,
            "client": self.client,
            "vendor": self.vendor,
            "implementationpartner": self.implementationpartner,
            "mode": self.mode,
            "calltype": self.calltype,
            "assist1": self.assist1,
            "assist2": self.assist2,
            "saleassociate": self.saleassociate,
            "manager": self.manager,
            "livecoding": self.livecoding,
            "positiontitle": self.positiontitle,
            "jobdescription": self.jobdescription,
            "projectduration": self.projectduration,
            "projectlocation": self.projectlocation,
            "clientwebsite": self.clientwebsite,
            "vendorwebsite": self.vendorwebsite,
            "interviewername": self.interviewername,
            "interviewerlinkedIn": self.interviewerlinkedIn,
            "vendornotes": self.vendornotes
        }

class websitemessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    contact_message = db.Column(db.Text, nullable=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read_flag = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<websitemessages %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email_address": self.email_address,
            "contact_message": self.contact_message,
            "dt": self.dt,
            "read_flag": self.read_flag
        }

class datavaultusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120),  nullable=False )
    password = db.Column(db.String(80), nullable=False)
    courses = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<datavaultusers %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "courses": self.courses
        }

class usersmessageslivechat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.String(120), nullable=False)
    longitude = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    saveddate = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<usersmessageslivechat %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "ip": self.ip,
            "message": self.message,
            "saveddate": self.saveddate
        }

class pythonusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120),  nullable=False )
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<pythonusers %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

class questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(100), nullable=False)
    questionID = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<questions %r>' % self.question

    def serialize(self):
        return {
            "id": self.id,
            "cat": self.cat,
            "questionID": self.questionID,
            "question": self.question,
            "answer": self.answer
        }