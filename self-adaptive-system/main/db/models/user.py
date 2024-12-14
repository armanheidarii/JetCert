import uuid
from peewee import *

from main.db import db
from main.db.models.base import BaseModel


class UserModel(BaseModel):
    public_id = UUIDField(default=uuid.uuid4, unique=True)
    name = CharField(max_length=256)
    email = CharField(max_length=128, unique=True)
    password = CharField(max_length=128)


db.create_tables([UserModel])
