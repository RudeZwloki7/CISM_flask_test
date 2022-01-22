from blog import db, login_manager
from blog import bcrypt
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return BlogUser.query.get(int(user_id))


class BlogUser(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    login = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, unencrypted_pass):
        self.password_hash = bcrypt.generate_password_hash(unencrypted_pass).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    content = db.Column(db.String(), nullable=False)
    post_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    is_presented = db.Column(db.Boolean(), nullable=False, default=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('blog_user.id'), nullable=False)

    def soft_delete(self):
        self.is_presented = False
        db.session.commit()

    def recover(self):
        self.is_presented = True
        db.session.commit()
