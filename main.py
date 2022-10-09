#################################################
# Projeto Final Análise de Dados com streamlit  #
#                                               #
# instalação: pip install streamlit             #
#                                               #
# executar: streamlit run main.py               #
#                                               #
# Prof: Tiago Dias                              #
#################################################


# Importar bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import statistics as sts

# Função principal:

def app():
    col1, col2 = st.columns((2,1))
    with col1:
        st.title('Projeto Final - Tecnicas de programação II - Python')
        
    with col2:
        st.image('Python.jpg')
    
    # Sub - Título da aplicação
    st.markdown("<h1 style='text-align: center;'>Análise de Dados com streamlit</h1>", unsafe_allow_html=True)
    arquivo = st.file_uploader("Escolha um arquivo")
    # Exibir informações básicas:
    if arquivo is not None:
        df = pd.read_csv(arquivo)
        shape = df.shape
        html_subtile = """
        <div style="background-color:tomato;"><p> Quantidade de linhas no arquivo:</p></div>   
        """
        st.markdown(html_subtile, unsafe_allow_html=True)
        st.write(shape[0])
        html_subtile1 = """
        <div style="background-color:tomato;"><p> Quantidade de Colunas no arquivo:</p></div>       
        """
        st.markdown(html_subtile1, unsafe_allow_html=True)
        st.write(shape[1])

        analise = st.radio("Escolha uma visão: ", ('info', 'head', 'Describe'))
        if analise == 'info':
            st.dataframe({'columns': list(df.dtypes.index), 'Dtype': list(map(str, df.dtypes.values)), 'Valores não nulos': list(df.count().values)})
        if analise == 'head':
            all_columns = df.columns.tolist()
            container = st.container()
                       
            if st.checkbox('Selecionar tudo'):
                selected_options = container.multiselect("Selecione as colunas que quer ver:",all_columns,all_columns)
            else:
                selected_options =  container.multiselect("Selecione as Colunas que quer ver:", all_columns)
    
            new_df = df[selected_options]
            st.dataframe(new_df)
            
        if analise == 'Describe':
            st.write(df.describe())

        if st.checkbox('Valores Nulos'):
            nulos =  df.isna().sum()[df.isna().sum()>0]
            nulos_per = df.isna().sum()[df.isna().sum()>0]/len(df)*100
            df_null = st.dataframe({'Contagem de nulos': nulos, 'Percentual de nulos': round(nulos_per,2)})
            fig = px.bar(nulos, x = nulos.index, y=nulos.values)
            fig.update_xaxes(title_text='Colunas')
            fig.update_yaxes(title_text='Contagem')
            st.plotly_chart(fig)
            
        if st.checkbox('Verificar medidas de tendencia central'):
            coluna = st.selectbox('Selecione uma coluna', list(df.select_dtypes(include='number').columns))
            media = df[coluna].mean()
            mediana = df[coluna].median()
            moda = df[coluna].mode().max()
            st.dataframe({'valor':{'Média': round(media,2), 'mediana': mediana, 'moda': moda}})
        if st.checkbox('Contagem dos dados categóricos'):
            coluna = st.selectbox('Selecione uma coluna',list(df.select_dtypes(include='object').columns))
            fig = px.bar(df, x = df[coluna].value_counts().index, y = df[coluna].value_counts().values)
            fig.update_xaxes(title_text='Colunas')
            fig.update_yaxes(title_text='Contagem')
            st.plotly_chart(fig)
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