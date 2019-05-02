from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_admin import Admin
from passlib.hash import bcrypt

from .models import Post, PostAdmin, User, UserAdmin

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
CORS(app, resources={r"/post": {"origins": "http://localhost:3000"}})

# Admin setup
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='blog', template_mode='bootstrap3')
admin.add_view(PostAdmin(Post))
admin.add_view(UserAdmin(User))

# Routes
@app.route('/post', methods=['GET'])
def get_all_posts():
    query = Post.select().order_by(-Post.date)
    output = []

    for post in query:
        output.append({
            "title": post.title,
            "author": post.author,
            "body": post.body,
            "date": post.date
        })

    return jsonify({
        "posts": output
    }), 200

@app.route('/post', methods=['POST'])
def create_post():
    try:
        json = request.get_json()

        title = json['title']
        body = json['body']
        author = json['author']

        # Post title must be unique
        existingPost = Post.get_or_none(Post.title == title)

        if existingPost != None:
            return jsonify({
                "statusCode": 409,
                "message": "A post with that title already exists."
            }), 409

        Post.create(title=title, body=body, author=author)

        return jsonify({
            "statusCode": 201,
            "message": "Success! Post created."
        }), 201

    except:
        message = (
            "Invalid request. Request must be valid JSON and must contain"
            "the required fields"
        )

        return jsonify({
            "statusCode": 400,
            "message": message
        }), 400

@app.route('/register', methods=['POST'])
def register():
    try:
        json = request.get_json()

        username = json['username']
        password = json['password']
        email = json['email']

        if len(password) < 12:
            return jsonify({
                'statusCode': 400,
                'message': 'Password must be at least 12 characters'
            }), 400

        password_hash = bcrypt.hash(password)

        User.create(
            username=username,
            password_hash=password_hash,
            email=email
        )

        return jsonify({
            'statusCode': 201,
            'message': 'Success! New user registered.'
        })

    except:
        message = (
            "Invalid request. Request must be valid JSON and must contain"
            "the required fields"
        )

        return jsonify({
            'statusCode': 400,
            'message': message
        })
