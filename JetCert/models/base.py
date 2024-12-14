from peewee import *


def create_base_model(db):
    try:

        class BaseModel(Model):
            class Meta:
                database = db

        return BaseModel

    except:
        raise ValueError(f"The BaseModel was not created!")
