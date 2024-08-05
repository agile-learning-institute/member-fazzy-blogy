from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(50), default='author')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    # Relationships
    posts = db.relationship('BlogPost', back_populates='author', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    author = db.relationship('User', back_populates='posts', lazy=True)
    comments = db.relationship('Comment', back_populates='blog_post', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blog_post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('blog_posts.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    blog_post = db.relationship('BlogPost', back_populates='comments', lazy=True)
    user = db.relationship('User', back_populates='comments', lazy=True)