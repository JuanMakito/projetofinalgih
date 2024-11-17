import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import pymysql
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="senai@123",
        database="extinsite"
    )

# Função para registrar um novo usuário
def register_user(nome, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nome, email) VALUES (%s, %s)", (nome, email))
        conn.commit()
        return True
    except pymysql.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

# Função para verificar se o usuário está registrado
@st.cache_data
def is_user_registered(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

# Controle de login na sessão
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Tela de Login ou Cadastro
if not st.session_state['logged_in']:
    st.title("Bem-vindo ao Sistema de Extinção das Espécies!")
    st.write("Por favor, faça o login ou registre-se para acessar o conteúdo.")
    
    choice = st.radio("Escolha uma opção", ["Login", "Cadastro"])
    email = st.text_input("Email", placeholder="Digite seu email")

    if choice == "Cadastro":
        name = st.text_input("Nome", placeholder="Digite seu nome")

    if choice == "Login" and st.button("Entrar"):
        if is_user_registered(email):
            st.session_state['logged_in'] = True
            st.success(f"Bem-vindo de volta, {email}!")
        else:
            st.error("Email não registrado. Por favor, registre-se primeiro.")
    
    elif choice == "Cadastro" and st.button("Cadastrar"):
        if name and email:
            if register_user(name, email):
                is_user_registered.clear()  # Limpa o cache após novo cadastro
                st.success("Cadastro realizado com sucesso! Faça login agora.")
            else:
                st.error("Email já registrado. Tente fazer login.")
        else:
            st.error("Por favor, preencha todos os campos.")
    
    st.stop()

# Função para exibir a introdução
def introducao():
    st.title("Introdução à Extinção de Espécies")
    st.markdown("""
    ### O que é a Extinção de Espécies?
    A extinção de espécies é o desaparecimento permanente de espécies na Terra, frequentemente acelerado por atividades humanas.
    
    ### Por que devemos nos preocupar?
    A perda de biodiversidade impacta ecossistemas, agricultura e o bem-estar humano.

    ### O que está sendo feito?
    - **Áreas protegidas**
    - **Legislação ambiental**
    - **Reprodução em cativeiro**
    """)

import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def grafico():
    try:
        df = pd.read_csv("animais.csv")  # Carregar o dataset
    except Exception as e:
        st.write(f"Erro ao carregar o arquivo CSV: {e}")
        return

    # Verificar se o CSV foi carregado corretamente
    if df.empty:
        st.write("Erro: O arquivo CSV está vazio.")
        return

    # Verificar se as colunas necessárias existem no CSV
    required_columns = ['Animal', 'Status de Extinção', 'Motivo', 'Consequência', 'Região', 'Ano']
    for col in required_columns:
        if col not in df.columns:
            st.write(f"Erro: A coluna '{col}' não foi encontrada no CSV.")
            return

    # Seleção do animal
    st.header("Simulação de Extinção de Animais")
    animal_selecionado = st.selectbox("Escolha um animal do dataset", df['Animal'].unique(), key="animal_selectbox")

    # Seleção da região
    regiao_selecionada = st.selectbox("Escolha uma região do mundo", df['Região'].unique(), key="regiao_selectbox")

    # Dados do animal e região selecionados
    dados_selecionados = df[(df['Animal'] == animal_selecionado) & (df['Região'] == regiao_selecionada)]

    if dados_selecionados.empty:
        st.error(f"Não foram encontrados dados para o animal: {animal_selecionado} na região: {regiao_selecionada}")
        return

    # Verificar se o animal está em extinção ou não na região
    status_extincao = dados_selecionados['Status de Extinção'].unique()

    if len(status_extincao) > 0:
        st.write(f"Status de Extinção do animal **{animal_selecionado}** na região **{regiao_selecionada}**: {status_extincao[0]}")
        
        if status_extincao[0] in ['Crítico', 'Em perigo', 'Vulnerável']:
            st.write(f"**{animal_selecionado}** está em risco de extinção nesta região!")
        else:
            st.write(f"**{animal_selecionado}** não está em risco de extinção nesta região.")
    else:
        st.write(f"Não foi possível determinar o status de extinção para **{animal_selecionado}** na região **{regiao_selecionada}**.")
        
    # Treinamento do modelo de previsão (se necessário)
    label_encoders = {}
    for col in ['Motivo', 'Consequência', 'Região', 'Status de Extinção']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Treinar modelo
    model = RandomForestClassifier()
    model.fit(df[['Motivo', 'Consequência', 'Região', 'Ano']], df['Status de Extinção'])


# Outras abas
def como_contribuir():
    st.title("Como Contribuir")
    st.write("Informações sobre como ajudar na preservação.")

def acoes_locais():
    st.title("Ações Locais")
    st.write("Iniciativas locais para a conservação de espécies.")

# Função principal
def main():
    pagina = st.sidebar.radio("Escolha uma página", ("Introdução", "Gráficos", "Como Contribuir", "Ações Locais"))
    if pagina == "Introdução":
        introducao()
    elif pagina == "Gráficos":
        grafico()
    elif pagina == "Como Contribuir":
        como_contribuir()
    elif pagina == "Ações Locais":
        acoes_locais()

if __name__ == "__main__":
    main()
