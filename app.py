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
    st.title("Saúde e Bem-Estar dos Pets")
    st.write("Bem-vindo à seção de Saúde e Bem-Estar! Aqui você encontrará informações valiosas e recomendações para garantir que seus animais de estimação vivam de forma saudável e feliz.")

    st.header("Dicas de Nutrição")
    st.write("Uma alimentação equilibrada é essencial para a saúde do seu pet. Considere as seguintes orientações:")
    st.markdown("- **Ração de qualidade:** Escolha marcas reconhecidas e adequadas à idade e tamanho do seu animal.")
    st.markdown("- **Alimentos proibidos:** Evite dar chocolate, cebola, uvas e alimentos muito gordurosos.")
    st.markdown("- **Consulte um veterinário:** Para orientações específicas sobre a dieta do seu pet.")

    st.header("Exercícios e Atividades")
    st.write("A atividade física ajuda a manter seu pet saudável e feliz. Algumas sugestões incluem:")
    st.markdown("- **Caminhadas diárias:** Pelo menos 30 minutos de exercício para cães.")
    st.markdown("- **Brincadeiras interativas:** Use brinquedos que estimulem o raciocínio, como quebra-cabeças.")
    st.markdown("- **Atividades de agilidade:** Experimente cursos de obstáculos para cães.")

    st.header("Cuidados de Saúde")
    st.write("Manter a saúde do seu pet é crucial. Fique atento a:")
    st.markdown("- **Vacinas:** Mantenha a vacinação em dia para prevenir doenças.")
    st.markdown("- **Check-ups anuais:** Visitas regulares ao veterinário ajudam a detectar problemas precocemente.")
    st.markdown("- **Sinais de alerta:** Observe alterações no comportamento, apetite ou energia do seu pet.")

    st.header("Higiene e Cuidados Pessoais")
    st.write("A higiene adequada é fundamental. Considere estas práticas:")
    st.markdown("- **Banho regular:** A frequência depende da raça e estilo de vida do pet.")
    st.markdown("- **Escovação dos dentes:** Use escovas e pastas específicas para pets, pelo menos uma vez por semana.")
    st.markdown("- **Corte de unhas:** Verifique e corte as unhas regularmente para evitar desconforto.")

    st.header("Saúde Mental")
    st.write("Assim como nós, os pets também precisam de cuidados mentais. Algumas dicas incluem:")
    st.markdown("- **Enriquecimento ambiental:** Proporcione brinquedos variados e espaços para explorar.")
    st.markdown("- **Socialização:** Exponha seu pet a diferentes ambientes e outros animais.")
    st.markdown("- **Rotina:** Mantenha horários regulares para alimentação e passeios.")

    st.header("Espaço para Dúvidas")
    st.write("Tem alguma dúvida sobre a saúde do seu pet? Confira nossa seção de perguntas frequentes ou envie suas perguntas!")
    st.text_input("Digite sua dúvida aqui:")

    st.header("Artigos e Recursos")
    st.write("Aprofunde-se em temas de saúde animal com nossos recursos recomendados:")
    st.markdown("- **Artigos:** [Saúde Animal](https://exemplo.com/artigos) - Uma coleção de artigos sobre cuidados com pets.")
    st.markdown("- **Livros:** 'O que seu animal está tentando lhe dizer' - um guia prático para entender seu pet.")
    st.markdown("- **Vídeos:** [Canal do YouTube](https://youtube.com/exemplo) - Dicas de cuidados e treinamento.")

    st.header("Comunidade")
    st.write("Participe da nossa comunidade e compartilhe suas experiências!")
    st.text_area("Conte-nos sua história ou dicas sobre cuidados com pets:")

    st.header("Consultas com Especialistas")
    st.write("Para cuidados mais específicos, entre em contato com um especialista:")
    st.markdown("- **Veterinários locais:** Confira nossa lista de veterinários recomendados.")
    st.markdown("- **Comportamentalistas:** Consulte especialistas para lidar com comportamentos problemáticos.")
    st.markdown("- **Clínicas de emergência:** Saiba onde encontrar atendimento em situações urgentes.")

    st.header("Histórias de Sucesso")
    st.write("Inspire-se com histórias de donos que melhoraram a saúde de seus pets. Veja como eles fizeram isso!")
    st.markdown("- **Caso 1:** O João transformou a dieta da sua gata e ela perdeu peso e ganhou energia.")
    st.markdown("- **Caso 2:** A Maria implementou uma rotina de exercícios para seu cachorro e agora eles têm passeios diários juntos.")


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
