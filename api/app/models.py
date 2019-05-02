import peewee
import datetime
from flask_admin.contrib.peewee import ModelView

# Database setup
db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

# Models
class BaseModel(peewee.Model):
    class Meta:
        database = db

class Post(BaseModel):
    title = peewee.CharField()
    author = peewee.CharField()
    body = peewee.TextField()
    date = peewee.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.title

class PostAdmin(ModelView):
    column_exclude_list = ['body']
    column_sortable_list = ('title', 'date')

class User(BaseModel):
    username = peewee.CharField(unique=True)
    password_hash = peewee.CharField()
    email = peewee.CharField()
    join_date = peewee.DateTimeField(default=datetime.datetime.now())
    is_admin = peewee.BooleanField(default=False)

class UserAdmin(ModelView):
    column_exclude_list = ['password_hash']
    column_sortable_list = ['username', 'join_date']
