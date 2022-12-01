from tweepy import Client

from PrestigeHandler import PrestigeHandler
from SingletonMeta import SingletonMeta
from TwitterUserDAO import TwitterUserDAO


class ClientHandler(metaclass=SingletonMeta):

    def __init__(self):
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAJ1ggEAAAAA8X01El%2FEBkIBAJKlE8wJzT%2BrhfQ%3D7DD6tWwONqF6zDZRTga8H6PAiLWR8ksL7e8pmA4z6QVSJRxaLB'
        self.client = Client(bearer_token=bearer_token)

    def get_client(self):
        return self.client


class TweepyHandler:

    def __init__(self):
        clientHandler = ClientHandler()
        self.client = clientHandler.get_client()

    def get_user(self, username):
        print('request user twitter', username)
        response = self.client.get_user(username=username)

        if response.data is None:
            raise Exception('User not found')

        return response.data

    def get_users_following(self, user_id):
        print('request following twitter')
        return self.client.get_users_following(id=user_id).data

    def get_users_tweets(self, user_id):
        return self.client.get_users_tweets(id=user_id).data


class TwitterUser:

    def __init__(self, username=None, user=None):

        self.id = None
        self.name = None
        self.username = None
        self.prestige = None

        self.twitterUserDAO = TwitterUserDAO()

        username = user.username if user is not None else username[1:]
        print(username)
        response = self.twitterUserDAO.get_user(username)
        if response is not False:
            self.create_twitter_user(response)
            return

        if user is not None:
            self.constructor_by_user(user)
        else:
            self.constructor_by_username(username)

    def create_twitter_user(self, data):
        self.id = data['id']
        self.name = data['name']
        self.username = data['username']
        self.prestige = data['prestige']

    def constructor_by_username(self, username):
        tweepy_handler = TweepyHandler()
        user = tweepy_handler.get_user(username)

        self.constructor_by_user(user)

    def constructor_by_user(self, user):
        prestige_handler = PrestigeHandler()
        prestige = prestige_handler.get_user_prestige(user)

        user_data = dict()
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['prestige'] = prestige

        self.twitterUserDAO.set_user(user_data)
        self.create_twitter_user(user_data)

    def get_users_following(self):
        tweepy_handler = TweepyHandler()
        return [TwitterUser(user=user) for user in tweepy_handler.get_users_following(self.id)]

    def get_users_tweets(self):
        tweepy_handler = TweepyHandler()
        return tweepy_handler.get_users_tweets(self.id)

    def get_user_prestige(self):
        return self.prestige
