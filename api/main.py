from app import app, Post

DEBUG = True

if __name__ == '__main__':
    try:
        Post.create_table()
    except:
        pass

    app.run(debug=DEBUG)

