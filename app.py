import sqlite3
import streamlit as st
import pandas as pd
import csv
import re
import base64


# Função para validar o formato do email
def validar_respostas(pergunta1, pergunta2, pergunta3, pergunta4, pergunta5,
                      pergunta6, pergunta7):

    if pergunta1 == '':
        st.warning('Você não respondeu a pergunta 1.')
        return False
    if pergunta2 == '':
        st.warning('Você não respondeu a pergunta 2.')
        return False
    if pergunta3 == '':
        st.warning('Você não respondeu a pergunta 3.')
        return False
    if pergunta4 == '':
        st.warning('Você não respondeu a pergunta 4.')
        return False
    if pergunta5 == '':
        st.warning('Você não respondeu a pergunta 5.')
        return False
    if pergunta6 == '':
        st.warning('Você não respondeu a pergunta 6.')
        return False
    if pergunta7  == '':
       st.warning('Você não respondeu a pergunta 7.')
       return False

    return True

# Cria uma conexão com o banco de dados
conn = sqlite3.connect('respostas.db')

# Cria uma tabela para armazenar os dados do usuário
conn.execute('''CREATE TABLE IF NOT EXISTS respostas
                (pergunta1 TEXT, pergunta2 TEXT, pergunta3 TEXT, pergunta4 TEXT,
                pergunta5 TEXT, pergunta6 TEXT, pergunta7 TEXT )''')

col1, col2 = st.columns([1, 0.4,])
with col1:
    st.title('Consulta: Trilhas do Conhecimento Ciências Naturais')
    st.subheader('Colégio Estadual Cora Coralina')
with col2:
    st.image('logo_cora.png', width=190)

# Campos para entrada de dados
with st.form('my_form'):
    pergunta1 = st.text_input('Quais dejetos que produzidos em nossas casas \
                  são considerados como esgoto?')

    pergunta2 = st.text_input('Cite a diferença entre esgoto doméstico e \
                                  esgoto industrial.')

    pergunta3 = st.text_input('Por que devemos tratar os esgotos domésticos \
                                  e industriais?')

    pergunta4 = st.text_input('Quais fenômenos estão associados ao processo \
                                  de decantação utilizado no tratamento de esgoto?')

    st.write('Você já realizou experimentos de fitragem \
                                  durante seu período escolar:')
    pergunta5_selecionada = ['Sim', 'Não']
    pergunta5 = st.radio('Selecione um item', pergunta5_selecionada, label_visibility="collapsed",)

    st.write('Existe um processo biológico muito utilizado no tratamento \
                      de esgoto, denominando de anaeróbico. Dentre os Gases listados \
                      abaixo, qual não faz parte desse processo?')

    opcoes_gases = ['Gás nitrogênio (N2)', 'Gás Oxigênio (O2)',
                    'Gás Carbônico (CO2)', 'Monóxido de Carbono (CO)',
                    'Vapor de Água', 'Metano (CH4)']

    pergunta6 = st.radio('Selecione um Gás', opcoes_gases, label_visibility="collapsed")

    pergunta7 = st.text_input('Em sua visão de mundo o que é uma cidade planejada?')

    st.markdown(
         """
         <style>
         input {
               font-size: 1rem !important;
         }
         </style>
         """,
         unsafe_allow_html = True
    )

    # Botão de envio
    submit_button = st.form_submit_button(label='Enviar')

# Insere os dados do usuário no banco de dados
if submit_button:
    if validar_respostas(pergunta1, pergunta2, pergunta3, pergunta4, pergunta5,
                         pergunta6, pergunta7):
        conn.execute("INSERT INTO respostas VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (pergunta1, pergunta2, pergunta3, pergunta4, pergunta5,
                     pergunta6, pergunta7))
        conn.commit()
        st.success('Dados enviados com sucesso!')

        # Ler os dados do banco de dados usando pandas
        df = pd.read_sql_query("SELECT * from respostas", conn)

        # Exibir os dados em uma tabela
        #st.write(df)

        # Botão para baixar os dados como um arquivo CSV
        def download_csv(df):
            csvfile = df.to_csv(index=False)
            b64 = base64.b64encode(csvfile.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="respostas.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        download_csv(df)

        # Fecha a conexão com o banco de dados
        conn.close()
