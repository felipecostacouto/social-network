import pickledb
import json
from datetime import datetime, timedelta

from SingletonMeta import SingletonMeta


class TwitterUserDAO(metaclass=SingletonMeta):

    def __init__(self):
        self.database = pickledb.load('database_twitter.pickle', False)

    def get_user(self, username):
        response = self.database.get(username)
        if not response:
            return False

        data = json.loads(response)

        user = data['user']
        metadata = data['metadata']

        updated_at = datetime.strptime(metadata['updated_at'], '%Y-%m-%d %H:%M:%S.%f')

        if updated_at < (datetime.now() - timedelta(days=1)):
            return False

        return user

    def set_user(self, user):

        data = dict()
        data['user'] = user
        data['metadata'] = {'updated_at': str(datetime.now())}

        self.database.set(user['username'], json.dumps(data))
        self.database.dump()
