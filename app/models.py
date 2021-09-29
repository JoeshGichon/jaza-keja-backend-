from . import db
from datetime import datetime

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'User {self.name}'

class UserPayment(db.Model):

    __tablename__ = 'payments'

    payment_id=db.Column(db.Integer,primary_key=True)
    payment_type=db.Column(db.String(length=50),nullable=False)
    account_no=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'UserPayment {self.account_no}-{self.payment_type}'

class Product(db.Model):

    __tablename__="products"

    product_id=db.Column(db.Integer,primary_key=True,nullable=False)
    product_name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer,nullable=False)
    desc=db.Column(db.String(length=1024),nullable=False,unique=True)

    def __repr__(self):
        return f'Product {self.name}-{self.price}'

class ProductCategory(db.Model):

    __tablename__="categories"

    category_id=db.Column(db.Integer,primary_key=True,nullable=False)
    category_name=db.Column(db.String(length=100),nullable=False)
    category_desc=db.Column(db.String(length=1025),nullable=False)

class Order(db.Model):

    __tablename__="orders"

    order_id=db.Column(db.Integer,primary_key=True,nullable=False)
    status=db.Column(db.String(length=1025))
    created_at=db.Column(db.DateTime, default=datetime)

    user_id=db.Column(db.Integer,db.ForeignKey("user_id"))

    def __repr__(self):
        return f"{self.status}"

class OrderItems(db.Model):

    __tablename__="items"

    item_id=db.Column(db.Integer,primary_key=True)
    quantity = db.Column(db.Integer)

    order_id=db.Column(db.Integer,db.ForeignKey("order_id"))
    product_id=db.Column(db.Integer,db.ForeignKey("product_id"))
    
    def __repr__(self):
        return f"{self.quantity}"


