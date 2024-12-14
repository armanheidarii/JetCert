from peewee import *

from main.db import db


class BaseModel(Model):
    class Meta:
        database = db
