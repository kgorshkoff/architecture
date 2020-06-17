from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    lists = db.relationship('ItemList', backref='owner', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)    


class ItemList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    items = db.relationship('Item', backref='items', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # subscribers = db.Column(db.Integer, )
    
    def __repr__(self):
        return '<List {}>'.format(self.name)
         

# class BaseItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False, unique=True)
    
#     def create_item(self):
#         pass
    
#     def delete_item(self, id):
#         pass
    
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False, unique=True)
    
#     def create_item(self):
#         pass
    
#     def delete_item(self, id):
#         pass


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('item_list.id'))

    def create_item(self):
        pass
    
    def delete_item(self, id):
        pass
    
    def __repr__(self):
        return '<Item {}>'.format(self.name)