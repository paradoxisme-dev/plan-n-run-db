from peewee import *
import os


option_db = SqliteDatabase('options.db')


class OptionValue(Model):
    key = CharField(unique=True)
    value = TextField()

    class Meta:
        database = option_db


def init_option_database():
    global option_db
    if os.path.exists('options.db'):
        option_db.connect()
    else:
        option_db.init('options.db')
        option_db.connect()
        option_db.create_tables([OptionValue], safe=True)

        # option for OBS WebSocket connection
        OptionValue.create(key='obs_ws_host', value='localhost')
        OptionValue.create(key='obs_ws_port', value='4455')

        # option for open database history
        OptionValue.create(key='open_db_history_size_max', value='5')
        OptionValue.create(key='open_db_history', value='[]')
