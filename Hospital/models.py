from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(100))
    created_at= db.Column(db.DateTime,default=datetime.utcnow)


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100),unique=True,nullable=False)
    location = db.Column(db.String(200),nullable=False)
    specialized = db.Column(db.String(100),nullable=False)
    doctor = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'location':self.location,
            'specialized':self.specialized,
            'doctor' : self.doctor
        }

class BookAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    hospital_id = db.Column(db.Integer,db.ForeignKey('hospital.id'))
    start_time= db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)

class DoctorReview(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    review = db.Column(db.String(100),nullable=False)
    drugs = db.Column(db.String(200),nullable = False)
    injections = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

