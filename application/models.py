from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    mobile = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    donor_user = db.relationship('Donor', backref='users')
    seeker_user = db.relationship('Seeker', backref = 'users')
class Blood(db.Model):
    __tablename__ = 'blood'
    __table_args__ = {'extend_existing': True}
    bid = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False)
    bgroup = db.Column(db.String, unique=True, nullable=False)
    donors = db.relationship('Donor', backref='blood')
    seekers = db.relationship('Seeker', backref='blood')
    inventories = db.relationship('Inventory', backref='blood')
    transfusions = db.relationship('Transfusion', backref= 'blood')
class Donor(db.Model):
    __tablename__ = 'donor'
    __table_args__ = {'extend_existing': True}
    did = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False)
    dname = db.Column(db.String(20), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey('blood.bid'), nullable=False)
    dold = db.Column(db.Date, nullable=False)
    mobile = db.Column(db.String(13), nullable=False)
    # blood = db.relationship("Blood", backref="donors")
class Seeker(db.Model):
    __tablename__ = 'seeker'
    __table_args__ = {'extend_existing': True}
    sid = db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey('blood.bid'), nullable=False)
    dolt = db.Column(db.Date,  nullable=False)
    mobile = db.Column(db.String(13))
    transfusions = db.relationship('Transfusion', backref= 'seeker')

    # blood = db.relationship("Blood", backref="seekers")
class Hospital(db.Model):
    __tablename__ = 'hospital'
    __table_args__ = {'extend_existing': True}
    hid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hname = db.Column(db.String(20), nullable=False)
    loc = db.Column(db.String(50), nullable=False)
    # inventories = db.relationship('Inventory', backref='hospital')

class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = {'extend_existing': True}
    hid = db.Column(db.Integer, db.ForeignKey('hospital.hid'), primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('blood.bid'), primary_key=True)
    stock = db.Column(db.Integer)
    hospital = db.relationship("Hospital", backref="inventories")

class Transfusion(db.Model):
    __tablename__ = 'transfusion'
    __table_args__ = {'extend_existing': True}

    sid = db.Column(db.Integer, db.ForeignKey('seeker.sid'), primary_key=True)
    bid = db.Column(db.Integer,db.ForeignKey('blood.bid'),  primary_key=True)
    dot = db.Column(db.Date, nullable=False)
