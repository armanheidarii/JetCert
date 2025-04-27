from peewee import *

from main.db import db


class Base(Model):
    class Meta:
        database = db
