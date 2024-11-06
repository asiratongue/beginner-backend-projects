#TODO temporary tokens

from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime, jwt, os
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta


os.chdir(r'G:\01101000111101\Programming\Projects\Backend Projects\RESTful API - To Do List')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fyle.db'
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

db = SQLAlchemy(app)
SECRET_KEY = "herro_chitty_wok"

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "The requested resource was not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "an internal server error occurred"}), 500

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "You don't have permission to access this resource"})

class ToDoObj(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Userid = db.Column(db.String(399), unique=False, nullable = False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(600), unique=False, nullable=False)
    CreatedAt = db.Column(db.DateTime, default = datetime.datetime.now)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), unique=False, nullable = False)
    email = db.Column(db.String(250), unique=True, nullable = False)
    password = db.Column(db.String(250), unique=False, nullable = False)
    token = db.Column(db.String(245), unique=True) 

with app.app_context():
    try:
        db.create_all()
        print('success!')
    except Exception as e:
        print(f'an error occured {e}')


@app.route('/register', methods = ['POST'])
def register():


    NewUserData = request.get_json(force=True)
    NewUser = User(username = NewUserData['username'], email = NewUserData['email'], password = NewUserData['password'])
    db.session.add(NewUser)
    db.session.commit()

    Token = jwt.encode({'username': NewUser.username, 
                    'exp': datetime.datetime.now()+ timedelta(hours=1)},
                    SECRET_KEY, algorithm="HS256")
    
    NewUser.token = Token 
    db.session.commit()
    
    return jsonify({'token': NewUser.token, 'keep your token safe!' : 'youll need it to login'})


@app.route('/login', methods = ['POST'])
def login():

    if request.method == 'POST':
        auth_get = request.get_json(force=True)
        UserEmail = User.query.filter(User.email == auth_get['email']).first()
        UserPassword = User.query.filter(User.password == auth_get['password']).first()

        if UserEmail and UserPassword != None:

            Token = jwt.encode({'username': UserEmail.username, 
                'exp': datetime.datetime.now()+ timedelta(hours=1)},
                SECRET_KEY, algorithm="HS256")
            UserEmail.token = Token
            db.session.commit()
            
            return jsonify({'login successful -- token': UserEmail.token, 'keep your token safe!' : 'youll need it to authorise'})

        return jsonify({'error':'invalid credentials'}), 401
    
def Token_check(Token):
    if 'Bearer ' in Token:
        Token = Token.replace('Bearer ', '')

    CheckTokenValidity = User.query.filter(User.token == Token).first()
    print(CheckTokenValidity)

    if CheckTokenValidity == None:
        return jsonify({'message':'Token is missing or expired, please login again.'}), 403
    elif CheckTokenValidity != []:
        return Token


@app.route('/todos', methods = ['GET', 'POST'])
def todo():

    Token = request.headers.get('Authorization')
    blud = Token_check(Token)
    
    if isinstance(blud, tuple):
        return blud 
    
    if blud in Token:   
        if request.method == 'POST':

            try:
                TodoData = request.get_json(force=True)
                data = jwt.decode(blud, SECRET_KEY, algorithms=["HS256"])
                ToDoTable = ToDoObj(Userid = data["username"], title = TodoData['title'], description = TodoData['description'])
                db.session.add(ToDoTable)
                db.session.commit()

                return jsonify({"message" : "welcome " + data["username"], 
                                "id" : f"{ToDoTable.id}", 
                                "title" : f"{ToDoTable.title}",
                                "description": f"{ToDoTable.description}"}
                            ), 200

            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid or Expired token!'}), 401
        
        elif request.method == "GET":
            jsonqueryreturn = {}
            metadataDict = {}

            data = jwt.decode(blud, SECRET_KEY, algorithms=["HS256"])
            page = request.args.get('page', default=1, type=int)
            limit = request.args.get('limit', default=10, type=int)
            TodoPosts = ToDoObj.query.filter(ToDoObj.Userid == data["username"]).offset(page-1).limit(limit).all()


            
            for posts in TodoPosts:
                jsondata = {"id" : posts.id, "title" : posts.title, "description" : posts.description}
                jsonqueryreturn[posts.id] = jsondata

            metadataDict["total"] = str(len(jsonqueryreturn))
            metadataDict["page"] = str(page)
            metadataDict["limit"] = str(limit)

            jsonqueryreturn[1337] = metadataDict

            return jsonify(jsonqueryreturn)
    else:
        return(blud)


@app.route('/todos/<int:idx>', methods = ['DELETE', 'PUT'])  # use
def todoedit(idx):

    Token = request.headers.get('Authorization')
    blud = Token_check(Token)
    idCheck = ToDoObj.query.filter(ToDoObj.id == idx).first()
    Tokencheck = User.query.filter(User.token == blud).first()
    if idCheck.Userid != Tokencheck.username:
        return "Invalid Token! Try again.", 401

    if blud in Token:   

        if request.method == 'PUT':
            TodoData = request.get_json(force=True)
            GrabPost = ToDoObj.query.filter(ToDoObj.id == int(idx)).first()                         
            GrabPost.title = TodoData['title'] 
            GrabPost.description = TodoData['description']
            db.session.commit()

            return jsonify({"id" : GrabPost.id, "title" : GrabPost.title, "description" : GrabPost.description})
            
        if request.method == 'DELETE': 
            
            GrabPost = ToDoObj.query.filter(ToDoObj.id == idx).delete() 
            db.session.commit()
            return "message deleted!", 204
    else:
        return(blud)


if __name__ == '__main__':
    app.run(debug=True)