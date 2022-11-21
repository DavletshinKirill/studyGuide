import uuid


from flask_admin.contrib.sqla import ModelView
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, admin
from sqlalchemy import Enum


class Permission(Enum):
    USER = 'USER'
    AVERAGE_USER = 'AVERAGE_USER'
    HIGH_USER = 'HIGH_USER'
    ADMIN = 'ADMIN'


class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(70), unique=True)
    user_name = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)
    permission = db.Column(db.Enum("USER", "AVERAGE_USER", "HIGH_USER", 'ADMIN', name="Permission"))
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, name, password, email, permission=Permission.USER):
        self.user_name = name
        self.hash_password(password)
        self.email = email
        self.permission = permission
        admin.add_view(ModelView(Users, db.session))

    def __repr__(self):
        return '<User %r>' % self.id

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def verify_permission(self, permission):
        return True if self.permission > permission else False

    def activate_user(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_email(email):
        email = Users.query.filter_by(email=email).first()
        if email:
            return False
        return True

    @staticmethod
    def check_name(name):
        name = Users.query.filter_by(user_name=name).first()
        if name:
            return False
        return True

    def create_user(self, form):
        if not self.check_email(form.email.data):
            return "You entered email which already exist"
        elif not self.check_name(form.user_name.data):
            return "You entered name which already exist"
        else:
            self.email = form.email.data
            self.user_name = form.user_name.data
            self.password = generate_password_hash(form.password.data)
            db.session.add(self)
            db.session.commit()
        return self


class Languages(db.Model):
    __tablename__ = 'languages'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language = db.Column(db.String(70), unique=True)
    topic_names = db.relationship("TopicNames", lazy=True)




class TopicNames(db.Model):
    __tablename__ = 'topic_names'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_name = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(70), unique=True)
    language = db.Column(UUID(as_uuid=True), db.ForeignKey('languages.id'))
    notes = db.relationship("Notes", lazy=True)




class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(70), unique=True)
    tutorial = db.Column(db.Text)
    task = db.Column(db.Text)
    permission = db.Column(db.Enum("USER", "AVERAGE_USER", "HIGH_USER", 'ADMIN', name="Permission"))
    topic_names = db.Column(UUID(as_uuid=True), db.ForeignKey('topic_names.id'))



admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Languages, db.session))
admin.add_view(ModelView(TopicNames, db.session))
admin.add_view(ModelView(Notes, db.session))
