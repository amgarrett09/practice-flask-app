from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_admin import Admin
import peewee
from flask_admin.contrib.peewee import ModelView
import datetime

DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
CORS(app, resources={r"/post": {"origins": "http://localhost:3000"}})

# Database setup
db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

# Models
class BaseModel(peewee.Model):
    class Meta:
        database = db

class Post(BaseModel):
    title = peewee.CharField()
    author = peewee.CharField()
    body = peewee.TextField(null=False)
    date = peewee.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

class PostAdmin(ModelView):
    column_exclude_list = ['body']

    column_sortable_list = ('title', 'date')

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



if __name__ == '__main__':
    try:
        Post.create_table()
    except:
        pass

    app.run(debug=DEBUG)

