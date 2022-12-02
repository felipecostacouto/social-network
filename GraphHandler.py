from matplotlib import pyplot as plt
import networkx as nx
import pickle

from TwitterUser import TwitterUser


class GraphHandler:

    def __init__(self):
        self.pagerank = None
        try:
            self.DiGraph = pickle.load(open('digraph_twitter.pickle', 'rb'))
        except (OSError, IOError):
            self.DiGraph = nx.DiGraph()
            self.DiGraph

    def save_graph(self):
        pickle.dump(self.DiGraph, open("digraph_twitter.pickle", "wb"))

    def add_user(self, new_user: TwitterUser):
        self.DiGraph.add_weighted_edges_from(map(lambda user: (
            new_user.username, user.username, new_user.prestige
        ), new_user.get_users_following()))
        self.save_graph()
        self.update_pagerank()

    def update_pagerank(self):
        self.pagerank = dict(sorted(nx.pagerank(self.DiGraph).items(), key=lambda item: item[1], reverse=True))

    def get_figure(self):
        nx.draw(self.DiGraph)
        return plt.gcf()

    def draw(self):
        nx.draw(self.DiGraph, with_labels=True)
        plt.savefig('graph.png')
