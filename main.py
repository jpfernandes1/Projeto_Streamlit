#################################################
# Projeto Final Análise de Dados com streamlit  #
#                                               #
# instalação: pip install streamlit             #
#                                               #
# executar: streamlit run main.py               #
#                                               #
# Prof: Tiago Dias                              #
#################################################


#Construir uma aplicação web utilizando o streamlit para análise de dados de um dataset qualquer em formato csv. A aplicação deve atender todos os requisitos listados na especificação.

#Em seguida, criar um repositório público no GitHub e publicar o código python da aplicação, enviando o link do repositório para o Formulário (https://docs.google.com/forms/d/e/1FAIpQLSeahbxqxAmgtt2p_gB9V64XbPnScFoCIYzt3dGFj6uZ5MoW4Q/viewform).

#1 - Receber um arquivo csv via upload.
#2 - Exibir as informações básicas da base de dados
#	2.1 - Tamanho do dados
#	2.2 - Dados nulos (soma, percentual e gráfico) 
#	2.3 - Uma amostra dos dados
#	2.4 - Outras informações que julgar inportantes para a análise de um terceiro
#3 - Opção para usuário exibir um gráfico para contagem de dados categóricos, lembrando de disponibilizar a(s) coluna(s) para escolha da exibição do usuário.
#4 - Opção para usuário exibir um gráfico que analisa a relação entre duas variáveis, lembrando de disponibilizar a(s) coluna(s) para escolha da exibição do usuário.
#5 - Opção para usuário exibir um gráfico que analisa a correlação entre as variáveis.
#6 - Opção para usuário exibir um gráfico que analisa o percentual da contagem de dados categóricos em relação ao todo, lembrando de disponibilizar a(s) coluna(s) para escolha da exibição do usuário.

# Importar bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import statistics as sts

# Função principal:

def app():
    st.title('Projeto Final - Tecnicas de programação II - Python')
    # Sub - Título da aplicação
    st.subheader('Análise de Dados com streamlit')
    arquivo = st.file_uploader("Escolha um arquivo")
    # Exibir informações básicas:
    if arquivo is not None:
        df = pd.read_csv(arquivo)
        shape = df.shape
        st.write(f'o Tamanho do arquivo é: {shape[0]} linhas e {shape[1]} colunas')
        analise = st.radio("Qual visualização você quer?", ('info', 'head', 'Describe'))
        if analise == 'info':
            st.dataframe({'columns': list(df.dtypes.index), 'Dtype': list(map(str, df.dtypes.values)), 'Valores não nulos': list(df.count().values)})
        if analise == 'head':
            st.write(df.head())
        if analise == 'Describe':
            st.write(df.describe())
        if st.checkbox('Valores Nulos'):
            nulos =  df.isna().sum()[df.isna().sum()>0]
            nulos_per = df.isna().sum()[df.isna().sum()>0]/len(df)*100
            df_null = st.dataframe({'Contagem de nulos': nulos, 'Percentual de nulos': round(nulos_per,2)})
            fig, ax = plt.subplots()
            ax.bar(x=nulos.index, height = nulos.values)
            st.pyplot(fig)
            
        if st.checkbox('Verificar medidas de tendencia central'):
            coluna = st.selectbox('Selecione uma coluna', list(df.select_dtypes(include='number').columns))
            media = df[coluna].mean()
            mediana = df[coluna].median()
            moda = df[coluna].mode().max()
            st.dataframe({'valor':{'Média': round(media,2), 'mediana': mediana, 'moda': moda}})
        if st.checkbox('Contagem dos dados categóricos'):
            coluna = st.selectbox('Selecione uma coluna',list(df.select_dtypes(include='object').columns))
            fig, ax = plt.subplots()
            ax.bar(x = df[coluna].value_counts().index, height = df[coluna].value_counts().values)
            st.pyplot(fig)
        if st.checkbox('Verificar relação entre duas variáveis:'):
            st.markdown('1ª Coluna - Eixo x')
            coluna1 = st.selectbox('Selecione a primeira coluna', list(df.select_dtypes(include='number').columns))
            st.markdown('2ª Coluna - Eixo y')
            coluna2 = st.selectbox('Selecione a segunda coluna', list(df.select_dtypes(include='number').columns))
            fig = px.scatter(data_frame=df, x=df[coluna1], y=df[coluna2])
            st.plotly_chart(fig)
        if st.checkbox('Verificar a corrrelação entre as variáveis'):
            correl = round(df.corr(),2)
            fig = px.imshow(correl, text_auto = True)
            st.plotly_chart(fig)
        if st.checkbox('Percentual relativo de dados categóricos'):
            coluna = st.selectbox('Selecione a Coluna', list(df.select_dtypes(include='object')))
            fig = px.pie(df, values=df[coluna].index, names=df[coluna].values)
            st.plotly_chart(fig)


if __name__ == '__main__':
    app()