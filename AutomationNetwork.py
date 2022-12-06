import re
import time

from tweepy import TooManyRequests

from GraphHandler import GraphHandler
from TwitterUser import TwitterUser

# time.sleep(900)

# Usuário zero
username = ''

if re.search(r'^(@)(\w{1,15})$', username):

    graph = GraphHandler()

    user_queue = [TwitterUser(username=username)]

    while graph.DiGraph.number_of_nodes() < 10000:
        print('nodes', graph.DiGraph.number_of_nodes())
        print('edges', graph.DiGraph.number_of_edges())

        user = user_queue.pop(0)
        print('Add', user.username)

        success = False

        while not success:
            try:
                graph.add_user(user)
                most_prestige = sorted(user.get_users_following(), key=lambda u: u.prestige, reverse=True)[:10]
                user_queue.extend(most_prestige)
                success = True
            except TooManyRequests as e:
                print(e)
                time.sleep(60)
                print('Tentando de novo')
            except Exception as e:
                print(e, 'Pulando usuario')
                break

else:
    print('Por favor preencha um usuário válido')
