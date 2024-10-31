
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import mysql.connector

# Função para conectar ao banco de dados
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Altere para seu usuário
        password="senai@123",  # Altere para sua senha
        database="petscare"  # Altere para o nome do seu banco de dados
    )

# Função para criar tabelas no MySQL
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        tipo VARCHAR(255),
        idade INT,
        cuidados TEXT,
        condicoes_saude TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadastro (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome_dono VARCHAR(255),
        email VARCHAR(255),
        pet_tipo VARCHAR(255)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Criar tabelas ao iniciar o aplicativo
create_tables()

# Estilos CSS
st.markdown(
    """
    <style>
    /* Estilo básico para o corpo */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }

    /* Cabeçalho principal */
    h1 {
        text-align: center;
        color: #4CAF50;
        font-size: 2.5rem;
        margin-top: 20px;
    }

    /* Subtítulos */
    h2, h3 {
        color: #333;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Botões */
    button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #45a049;
    }

    /* Estilo para DataFrames */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        border-radius: 10px;
        overflow: hidden;
    }

    table thead {
        background-color: #4CAF50;
        color: white;
    }

    table th, table td {
        padding: 12px;
        text-align: center;
        border-bottom: 1px solid #ddd;
    }

    table tbody tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    /* Upload de arquivo */
    input[type="file"] {
        display: block;
        margin: 20px auto;
        padding: 10px;
    }

    /* Elementos de gráfico */
    .plotly-graph {
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Boxplot e gráficos */
    .plot-container {
        margin-top: 30px;
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Avisos e alertas */
    .warning {
        color: #e74c3c;
        background-color: #fce4e4;
        border: 1px solid #e74c3c;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        margin: 10px 0;
    }

    /* Container principal */
    .stApp {
        max-width: 900px;
        margin: auto;
        padding: 20px;
    }

    /* Links */
    a {
        color: #4CAF50;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar o Dataset
st.title("Cuidados de Pets")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head())

    # Análise Exploratória de Dados (EDA)
    st.subheader("Análise Exploratória")
    st.write(data.describe())

    # Visualizações
    st.subheader("Distribuição de Variáveis")
    sns.histplot(data['idade'], bins=30)
    st.pyplot()

    sns.boxplot(x='tipo', y='idade', data=data)
    st.pyplot()

    st.subheader("Correlação entre Variáveis")
    correlation = data.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    st.pyplot()

    # Engenharia de Variáveis
    st.subheader("Engenharia de Variáveis")
    st.write("Descrição de variáveis:")
    st.write(data.dtypes)

    data['idade_cat'] = pd.cut(data['idade'], bins=[0, 1, 5, 10, 15], labels=['Filhote', 'Jovem', 'Adulto', 'Idoso'])
    st.write(data['idade_cat'].value_counts())

    # Modelo de Regressão
    st.subheader("Modelo de Regressão")
    target = st.selectbox("Selecione a variável alvo:", options=data.columns)

    if data[target].dtype in ['float64', 'int64']:
        X = data.drop(columns=[target])
        y = data[target]

        if st.button("Executar Regressão Linear"):
            model = LinearRegression().fit(X, y)
            st.write(f"Coeficientes: {model.coef_}")
            st.write(f"Intercepto: {model.intercept_}")

            plt.scatter(X.iloc[:, 0], y)
            plt.plot(X.iloc[:, 0], model.predict(X), color='red')
            st.pyplot()
    
    elif data[target].dtype == 'object':
        X = data.drop(columns=[target])
        y = data[target]

        if st.button("Executar Regressão Logística"):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            model = LogisticRegression(max_iter=200)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.write(confusion_matrix(y_test, y_pred))
            st.write(classification_report(y_test, y_pred))

    # Cadastro de Donos de Pets
    st.subheader("Cadastro de Donos de Pets")
    nome_dono = st.text_input("Nome do Dono")
    email = st.text_input("Email do Dono")
    pet_tipo = st.text_input("Tipo do Pet")

    if st.button("Cadastrar"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cadastro (nome_dono, email, pet_tipo) VALUES (%s, %s, %s)", (nome_dono, email, pet_tipo))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Cadastro realizado com sucesso!")

# Conclusão
st.markdown("""
### Conclusão
Este aplicativo permite que os donos de pets compreendam melhor os cuidados necessários e os ajude a tomar decisões informadas sobre a saúde e o bem-estar de seus animais.
""")
