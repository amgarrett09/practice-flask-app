from app import app, Post, User

DEBUG = True

if __name__ == '__main__':
    Post.create_table(fail_silently=True)
    User.create_table(fail_silently=True)

    app.run(debug=DEBUG)

