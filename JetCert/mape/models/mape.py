import datetime
from peewee import *


def create_MAPE_model(base_model):
    try:

        class MAPEModel(base_model):
            monitor_execution_time = FloatField()
            analyse_execution_time = FloatField()
            plan_execution_time = FloatField()
            execute_execution_time = FloatField()
            overall_execution_time = FloatField()
            created_date = DateTimeField(default=datetime.datetime.now)

        db = base_model._meta.database
        db.create_tables([MAPEModel])

        return MAPEModel

    except:
        raise ValueError(f"The MAPEModel was not created!")
