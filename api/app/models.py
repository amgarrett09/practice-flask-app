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
    body = peewee.TextField(null=False)
    date = peewee.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

class PostAdmin(ModelView):
    column_exclude_list = ['body']

    column_sortable_list = ('title', 'date')