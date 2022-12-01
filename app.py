import re

from GraphHandler import GraphHandler
from TwitterUser import TwitterUser

import streamlit as st


def __main__():
    st.write("""
        # Rede de Notícias Falsas
        Digite abaixo seu usuário do twitter
    """)

    username = st.text_input('Digite seu @ do twitter')

    if not re.search(r'^(@)(\w{1,15})$', username):
        if username:
            st.error('Por favor preencha um usuário válido')

    print(username)

    # try:
    graph = GraphHandler()
    graph.add_user(TwitterUser(username=username))
    st.write(graph.get_pagerank())
    graph.draw()
    # except Exception as error:
    #     if error:
    #         st.error(str(error))


__main__()
