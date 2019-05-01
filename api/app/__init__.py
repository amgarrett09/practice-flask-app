from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_admin import Admin

from .models import Post, PostAdmin

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
CORS(app, resources={r"/post": {"origins": "http://localhost:3000"}})

# Admin setup
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='blog', template_mode='bootstrap3')
admin.add_view(PostAdmin(Post))

# Routes
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
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
    else:
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