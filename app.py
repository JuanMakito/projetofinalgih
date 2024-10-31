import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import mysql.connector

# Configuração inicial
st.set_page_config(page_title="Cuidados Pet", layout="centered")

# Estilo CSS Customizado
def apply_custom_css():
    st.markdown("""
    <style>
        /* Estilo Global */
        body {
            background-color: #f8f9fa;
            color: #212529;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Estilo para títulos */
        h1, h2, h3 {
            color: #2d6a4f;
            font-weight: 700;
            margin-top: 1rem;
        }
        /* Estilo para botões */
        .stButton button {
            background-color: #52b788;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #40916c;
        }
        /* Estilo de cards para as seções */
        .section-card {
            padding: 2rem;
            margin: 1rem 0;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fff;
        }
        /* Caixa de busca e formulário de contato */
        .stTextInput, .stTextArea {
            margin-top: 1rem;
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        /* Footer */
        footer {
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# Funções para conectar ao banco de dados e realizar o cadastro
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai@123",
        database="petscare"
    )

def register_owner(name, email, pet_type):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cadastro (nome_dono, email, pet_tipo) VALUES (%s, %s, %s)", (name, email, pet_type))
            conn.commit()

# Função de Análise de Dados
def data_analysis():
    st.title("Análise de Dados")
    csv_file_path = r'C:\Users\ead\Desktop\projetinhomanha\animais.csv'
    
    @st.cache_data
    def load_data():
        data = pd.read_csv(csv_file_path)
        return data

    data = load_data()
    
    st.subheader("Visualização das Primeiras Linhas dos Dados")
    st.write(data.head())
    
    st.subheader("Estatísticas Descritivas")
    st.write(data.describe())
    
    st.subheader("Informações do Dataset")
    buffer = data.info(buf=None)
    st.text(buffer)

# Funções de Conteúdo do Site
def homepage():
    st.image("https://www.jornalspnorte.com.br/wp-content/uploads/2015/12/1812_jornal-do-futuro-animais-domesticos.jpg", use_column_width=True)
    st.title("Bem-vindo ao Cuidados Pet!")
    st.write("Descubra dicas essenciais e serviços para melhorar o bem-estar dos seus pets.")
    st.markdown("### Destaques Recentes")

def care_section():
    st.title("Seção de Cuidados")
    st.write("Artigos e dicas sobre cuidados essenciais para diferentes animais.")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def health_section():
    st.title("Saúde e Bem-Estar")
    st.write("Informações e recomendações sobre a saúde dos pets.")

def adopt_section():
    st.title("Adote um Pet")
    st.write("Animais disponíveis para adoção e histórias de sucesso.")

def community_section():
    st.title("Comunidade")
    st.write("Espaço para troca de experiências entre donos de pets.")

def shop_section():
    st.title("Loja de Produtos")
    products = pd.DataFrame({
        "Produto": ["Ração", "Brinquedo", "Cama"],
        "Preço": ["R$50", "R$20", "R$100"]
    })
    st.table(products)

def blog_section():
    st.title("Blog")
    st.write("Artigos regulares sobre o mundo pet.")

def contact_section():
    st.title("Contato")
    st.write("Entre em contato conosco.")
    with st.form("contact_form"):
        name = st.text_input("Nome")
        email = st.text_input("Email")
        message = st.text_area("Mensagem")
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success("Mensagem enviada com sucesso!")

def pet_registration():
    st.title("Cadastro de Donos de Pets")
    nome_dono = st.text_input("Nome do Dono")
    email = st.text_input("Email do Dono")
    pet_tipo = st.text_input("Tipo do Pet")
    if st.button("Cadastrar"):
        if nome_dono and email and pet_tipo:
            register_owner(nome_dono, email, pet_tipo)
            st.success("Cadastro realizado com sucesso!")

# Navegação por Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Página Inicial", "Cuidados", "Saúde", "Adoção", 
    "Comunidade", "Loja", "Blog", "Análise de Dados", "Cadastro de Pets"
])

# Conteúdo de cada Tab
with tab1:
    homepage()
with tab2:
    care_section()
with tab3:
    health_section()
with tab4:
    adopt_section()
with tab5:
    community_section()
with tab6:
    shop_section()
with tab7:
    blog_section()
with tab8:
    data_analysis()
with tab9:
    pet_registration()

# Rodapé
st.markdown("<footer>&copy; 2023 Cuidados Pet - Todos os direitos reservados.</footer>", unsafe_allow_html=True)
