import os
import base64
import re
from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='user')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs.get('password', ''))

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'first_name', 'last_name', 'email', 'username', 'password'}

        def camel_to_snake(camel_string):
            return re.sub('([A-Z][A-Za-z]*)', '_\1', camel_string).lower()
        
        for key, value in kwargs.items():
            snake_key = camel_to_snake(key)
            if snake_key in allowed_fields:
                if snake_key == 'password':
                    self.set_password(value)
                else:
                    setattr(self, snake_key, value)
        
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'username': self.username,
        }
    
    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(hours=1)
        db.session.commit()
        return self.token


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # author = db.relationship('User',back_populates='posts')
    comments = db.relationship('Comment', backref='post')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'title', 'body'}

        # def camel_to_snake(camel_string):
        #     return re.sub('([A-Z][A-Za-z]*)', '_\1', camel_string).lower()

        for key, value in kwargs.items():
            # snake_key = camel_to_snake(key)
            if key in allowed_fields:
                setattr(self, key, value)

        self.save()

    def delete(self):
        db.session.delete(self) # deleting THIS object from the database
        db.session.commit() # commiting our changes

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'dateCreated': self.date_created,
            'userId': self.user_id,
            'author': self.author.to_dict(),
            'comments': [comment.to_dict() for comment in self.comments]
        }
    
    
# Create our Comment class/table
class Comment(db.Model):
    # CREATE TABLE
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # user = db.relationship('User',back_populates='comments')
    
    
    # INSERT INTO
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()
        
    def __repr__(self):
        return f"<Comment {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'dateCreated': self.date_created,
            'post_id': self.post_id,
            'user': self.user.to_dict()
        }



