from flask import jsonify,request,make_response
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt
import uuid
from functools import wraps
from .. import db
from ..models import User
from . import auth

# auth.config["SECRET_KEY"]="jwtsecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message":"Token is missing"}),401
        try:
            data = jwt.decode(token,auth.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"])
        except:
            return jsonify({"message":"Token is invalid"}),401
        return f(current_user,*args,**kwargs)
    return decorated


@auth.route("/users",methods=["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data["public_id"] = user.public_id
        user_data["name"] = user.name
        user_data["password"] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)

    return jsonify({"users":output})

@auth.route("/users/<public_id>",methods=["GET"])
@token_required
def get_one_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"no user found!"})

    user_data = {}
    user_data["public_id"] = user.public_id
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["admin"] = user.admin

    return jsonify({"user":user_data})

@auth.route("/users",methods=["POST"])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"],method="sha256")

    new_user = User(public_id=str(uuid.uuid4()),name=data["name"],password=hashed_password,admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message":"new_user created"})

@auth.route("/users/<public_id>",methods=["PUT"])
@token_required
def promote_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"no user found!"})

    user.admin = True
    db.session.commit()
    return jsonify({"message":"The user has been promoted"})

@auth.route("/users/<public_id>",methods=["DELETE"])
@token_required
def delete_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"no user found!"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"user has been deleted"})

@auth.route("/login")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify",401,{"www-Authenticate":"Basic realm ='Login required!'"})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response("Could not verify",401,{"www-Authenticate":"Basic realm ='Login required!'"})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({"public_id":user.public_id,"exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},auth.config["SECRET_KEY"])

        return jsonify({"token":token.decode("UTF-8")})

    return make_response("Could not verify",401,{"www-Authenticate":"Basic realm ='Login required!'"})