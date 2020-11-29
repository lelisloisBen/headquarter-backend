from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    bankName = db.Column(db.String(120))
    routing = db.Column(db.String(120))
    account = db.Column(db.String(120))

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
            "bankName": self.bankName,
            "routing": self.routing,
            "account": self.account
        }