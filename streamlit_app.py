import re
import pandas as pd
from itertools import islice

from GraphHandler import GraphHandler
from TwitterUser import TwitterUser

import streamlit as st

st.write("""
    # Rede de Notícias Falsas
    Digite abaixo seu usuário do twitter
""")



username = st.text_input('Digite seu @ do twitter')

if re.search(r'^(@)(\w{1,15})$', username):

    try:

        graph = GraphHandler()

        num_nodes = graph.DiGraph.number_of_nodes()
        num_edges = graph.DiGraph.number_of_edges()

        user = TwitterUser(username=username)

        graph.add_user(user)

        new_num_nodes = graph.DiGraph.number_of_nodes()
        new_num_edges = graph.DiGraph.number_of_edges()

        col1, col2 = st.columns(2)
        col1.metric("Usuários Totais da Rede", new_num_nodes, "+ " + str(new_num_nodes - num_nodes))
        col2.metric("Conexões Totais da Rede", new_num_edges, "+ " + str(new_num_edges - num_edges))

        ranking = list(islice((user for user in user.following if user.username in graph.pagerank.keys()), 10))
        data = [(rank.name, rank.username, rank.prestige, graph.pagerank[rank.username]) for rank in ranking]
        st.dataframe(pd.DataFrame(data, columns=['Nome', 'Usuário', 'Prestigio Individual', 'Pagerank']))

    except Exception as error:
        if error:
            st.error(error)

else:
    if username:
        st.error('Por favor preencha um usuário válido')
