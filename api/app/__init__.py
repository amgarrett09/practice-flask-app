from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_admin import Admin
from passlib.hash import bcrypt
from functools import wraps
import jwt
import datetime

from .models import Post, PostAdmin, User, UserAdmin

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:3000'}})

# Admin setup
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='blog', template_mode='bootstrap3')
admin.add_view(PostAdmin(Post))
admin.add_view(UserAdmin(User))


# JWT decorator
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return f(None, *args, **kwargs)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.get_or_none(User.username == data['username'])
        except:
            return f(None, *args, **kwargs)
        return f(user, *args, **kwargs)
    return decorated


# Routes
@app.route('/api/post', methods=['GET'])
def get_all_posts():
    query = Post.select().order_by(-Post.date)
    output = []

    for post in query:
        output.append({
            'title': post.title,
            'author': post.author,
            'body': post.body,
            'date': post.date
        })

    return jsonify({
        'posts': output
    }), 200


@app.route('/api/post', methods=['POST'])
@auth_required
def create_post(user):
    if user is None:
        return jsonify({
            'statusCode': 401,
            'message': 'Login required.'
        }), 401

    try:
        json = request.get_json()

        title = json['title']
        body = json['body']
        author = user.username

        # Post title must be unique
        existingPost = Post.get_or_none(Post.title == title)

        if existingPost is not None:
            return jsonify({
                'statusCode': 409,
                'message': 'A post with that title already exists.'
            }), 409

        Post.create(title=title, body=body, author=author)

        return jsonify({
            'statusCode': 201,
            'message': 'Success! Post created.'
        }), 201

    except:
        message = (
            'Invalid request. Request must be valid JSON and must contain'
            'the required fields'
        )

        return jsonify({
            'statusCode': 400,
            'message': message
        }), 400


@app.route('/api/register', methods=['POST'])
def register():
    try:
        json = request.get_json()

        username = json['username']
        password = json['password']
        email = json['email']

        # Data validation
        if len(password) < 12:
            return jsonify({
                'statusCode': 400,
                'message': 'Password must be at least 12 characters'
            }), 400

        user_with_name = User.get_or_none(User.username == username)
        user_with_email = User.get_or_none(User.email == email)

        if user_with_name is not None or user_with_email is not None:
            return jsonify({
                'statusCode': 409,
                'message': 'User with that username or email already exists.'
            }), 409

        password_hash = bcrypt.hash(password)

        User.create(
            username=username,
            password_hash=password_hash,
            email=email
        )

        return jsonify({
            'statusCode': 201,
            'message': 'Success! New user registered.'
        }), 201
    except:
        message = (
            'Invalid request. Request must be valid JSON and must contain'
            'the required fields'
        )

        return jsonify({
            'statusCode': 400,
            'message': message
        }), 400


@app.route('/api/login', methods=['POST'])
def login():
    try:
        json = request.get_json()

        username = json['username']
        password = json['password']

        user = User.get_or_none(User.username == username)

        # If user exists, verify password. If no user, default to False
        authenticated = bcrypt.verify(password, user.password_hash) \
            if user is not None else False

        if authenticated:
            expiration = datetime.datetime.utcnow() \
                    + datetime.timedelta(minutes=30)

            token = jwt.encode({
                'username': username,
                'exp': expiration
            }, app.config['SECRET_KEY'])

            return jsonify({
                'username': username,
                'token': token.decode('UTF-8')
            })
        else:
            return jsonify({
                'statusCode': 401,
                'message': 'Invalid username or password'
            }), 401

    except:
        return jsonify({
            'statusCode': 400,
            'message': 'Bad request'
        }), 400


@app.route('/api/check-auth', methods=['POST'])
def check_auth():
    try:
        json = request.get_json()
        token = json['token']

        auth_data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.get_or_none(User.username == auth_data['username'])

        if user is not None:
            return jsonify({
                'username': user.username
            }), 200
        else:
            return jsonify({
                'statusCode': 401,
                'message': 'Login required'
            }), 401

    except jwt.ExpiredSignatureError:
        return jsonify({
            'statusCode': 401,
            'message': 'Token expired. Login required.'
        }), 401

    except jwt.InvalidTokenError:
        return jsonify({
            'statusCode': 401,
            'message': 'Invalid token. Login required.'
        }), 401

    except:
        return jsonify({
            'statusCode': 400,
            'message': 'Bad request'
        }), 400
