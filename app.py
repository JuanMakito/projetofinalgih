import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import pymysql
import pickle  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password = ('senai@123'),
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
    except mysql.connector.IntegrityError:
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
    email = st.text_input("Email", placeholder="Digite seu email", key="email")
    
    if choice == "Cadastro":
        name = st.text_input("Nome", placeholder="Digite seu nome", key="name")
    
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

abas = st.tabs(["Introdução", "Lista de Espécies", "Causas da Extinção", "Quiz", "Conservação"])
le = LabelEncoder()
@st.cache_data
def load_animais_data():
    df = pd.read_csv("animais.csv", on_bad_lines='skip')
    # Carregar os dados dos animais
    animais_df = load_animais_data()
    animais_df = _animais_df()
    _animais_df = animais_df() 

    # Exibir a quantidade de espécies após o filtro
    st.write(f"Mostrando {len(animais_df)} espécies.")

    st.write(df.head())
    st.write(df.isnull().sum())
    required_columns = ['Motivo', 'Região', 'Ano', 'Status de Extinção']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Faltam as seguintes colunas: {', '.join(missing_columns)}")
    return df

# Função para carregar dados dos animais
@st.cache_data
def load_animais_data():
    df = pd.read_csv("animais.csv", on_bad_lines='skip')
    st.write(f"Mostrando {len(df)} espécies.")  # Mostra a quantidade de espécies carregadas
    st.write(df.head())  # Exibe as primeiras linhas do DataFrame
    animais_df = _animais_df()
    _animais_df = animais_df() 
    return df

# Função de preprocessamento (apenas exemplo)
def preprocess_data(df):
    le_motivo = LabelEncoder()
    le_regiao = LabelEncoder()
    if df['Motivo'].isnull().any() or df['Região'].isnull().any():
        st.error("Há valores nulos em 'Motivo' ou 'Região'.")
    df['Motivo'] = le_motivo.fit_transform(df['Motivo'])
    df['Região'] = le_regiao.fit_transform(df['Região'])
    animais_df = _animais_df()
    _animais_df = animais_df() 
    return df, le_motivo, le_regiao

# Agora, para carregar os dados e aplicar o filtro
animais_df = load_animais_data()  # Carrega os dados uma vez

def train_model(df):
    df, le_motivo, le_regiao = preprocess_data(df)
    X = df[['Motivo', 'Região', 'Ano']]
    y = df['Status de Extinção']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Acurácia do modelo: {accuracy:.2f}")
    animais_df = _animais_df()
    _animais_df = animais_df() 
    with open("modelo_extincao.pkl", "wb") as f:
        pickle.dump(model, f)
    return model, le_motivo, le_regiao

def fazer_previsao(motivo, regiao, ano, le_motivo, le_regiao, modelo):
    motivo_codificado = le_motivo.transform([motivo])[0]
    regiao_codificada = le_regiao.transform([regiao])[0]
    nova_entrada = pd.DataFrame({'Motivo': [motivo_codificado], 'Região': [regiao_codificada], 'Ano': [ano]})
    animais_df = _animais_df()
    _animais_df = animais_df() 
    return modelo.predict(nova_entrada)[0]

@st.cache_data
def load_causas_extincao(_animais_df):
    animais_df = _animais_df["Motivo"].value_counts().reset_index()
    animais_df.columns = ["Causa", "Contagem"]
    animais_df = _animais_df()
    _animais_df = animais_df() 
    return animais_df

# Introdução
with abas[0]:
    st.title("A Crise da Extinção: Nosso Planeta em Perigo")
    st.markdown("""
    *Junte-se a nós na preservação da vida selvagem!* 

    A perda acelerada de espécies ameaça o equilíbrio ecológico e a qualidade de vida humana. As principais causas dessa crise incluem:

    - *Desmatamento*: Perda de habitat.
    - *Caça ilegal*: Tráfico de animais.
    - *Mudanças climáticas*: Ameaça à sobrevivência de várias espécies.

    *Como você pode ajudar?*
    - Opte por produtos sustentáveis.
    - Apoie projetos de conservação.
    - Compartilhe a causa.

    *Explore mais e descubra como fazer a diferença!*
    """)


# Nova Aba para Previsões
with abas[1]:
    st.header("🌍 Previsão do Status de Extinção")
    
    # Coletar dados do usuário para a previsão
    motivo = st.selectbox('Causa da Ameaça', ["Perda de habitat", "Caça ilegal", "Mudanças climáticas", "Poluição", "Outros"])
    regiao = st.selectbox('Região', ["Africa", "Asia", "América do Sul", "Europa", "Oceania"])
    ano = st.number_input('Ano de Avaliação', min_value=2000, max_value=2024, value=2024)

    if st.button("Prever Status de Extinção"):
        # Fazer a previsão
        status_previsto = fazer_previsao(motivo, regiao, ano, le)
        st.write(f"O Status de Extinção previsto para esta espécie é: {status_previsto}")


    # Filtros de Busca
    st.subheader("🔎 Filtre as Espécies")
    col1, col2 = st.columns(2)

    # Filtro por nível de ameaça
    with col2:
        nivel_ameaca = st.selectbox(
            "Status de Ameaça", ["Todos", "Vulnerável", "Em perigo", "Crítico", "Menos preocupante", "Quase ameaçado"]
        )
    # Filtro por tipo de ameaça
    with col1:
        tipo_ameaca = st.selectbox(
            "Causa da Extinção", ["Todas", "Perda de Habitat", "Caça Ilegal", "Mudanças Climáticas", "Poluição", "Outros"]
        )
    

# Inicializa _animais_df com os dados originais
animais_df = _animais_df()

# Aplicar filtros aos dados
if tipo_ameaca != "Todas":
    _animais_df = _animais_df[_animais_df["Motivo"] == tipo_ameaca]
    
if nivel_ameaca != "Todos":
    _animais_df = _animais_df[_animais_df["Status de Extinção"] == nivel_ameaca]
    
# Exibir a quantidade de espécies após filtro
st.write(f"Mostrando {len(_animais_df)} espécies.")

# Exibir tabela de espécies
st.write(_animais_df)  # Usar st.write() para exibir o dataframe completo


    # Complemento informativo
st.markdown("""
    As espécies listadas estão em risco devido a diversas ameaças ambientais. Explore os dados para entender melhor os fatores que contribuem para sua extinção.
    """) 

    # Função para carregar e preparar os dados das causas de extinção

    # Exibir gráfico de causas de extinção
st.subheader("📊 Causas de Extinção")
causas_df = load_causas_extincao(_animais_df)
st.bar_chart(causas_df.set_index("Causa")["Contagem"])

# Aba 3 - Causas da Extinção
with abas[2]:
    st.header("Principais Causas da Extinção")

    # Carrega os dados das causas de extinção a partir do DataFrame 'animais_df'
    causas_df = load_causas_extincao(_animais_df)

    # Cria um gráfico de pizza interativo
    fig = px.pie(
        causas_df,
        values="Contagem",  # Coluna com os valores (número de animais por causa)
        names="Causa",      # Coluna com os nomes das causas
        title="Distribuição das Causas da Extinção",
        color_discrete_sequence=px.colors.sequential.RdBu  # Cor do gráfico
    )

    # Adiciona um hover_data para mostrar a contagem exata ao passar o mouse sobre cada fatia
    fig.update_traces(hovertemplate='%{label}: %{value} animais')

    # Personaliza o layout do gráfico (opcional, mas pode ser feito aqui)
    fig.update_layout(
        title_font=dict(size=20),
        margin=dict(t=30, b=30, l=30, r=30)
    )

    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

# Aba 4 - Ecossistema
with abas[3]:
    st.markdown("""
    Teste seus conhecimentos sobre as consequências da extinção de espécies para o ecossistema! 
    Responda às perguntas abaixo.
    """)

    # Definir perguntas e opções
    perguntas = [
        {
            "pergunta": "Qual é um dos principais processos afetados pela perda de biodiversidade?",
            "opcoes": ["Ciclo do carbono", "Ciclo da água", "Ciclo do oxigênio"],
            "resposta": "Ciclo do carbono"
        },
        {
            "pergunta": "O que pode acontecer quando uma espécie é extinta?",
            "opcoes": ["Desestabilização das redes alimentares", "Aumento da biodiversidade", "Redução da poluição"],
            "resposta": "Desestabilização das redes alimentares"
        },
        {
            "pergunta": "Como a perda de biodiversidade impacta a qualidade de vida humana?",
            "opcoes": ["Melhorando os recursos naturais", "Aumentando os desastres naturais", "Impactando recursos como agricultura e pesca"],
            "resposta": "Impactando recursos como agricultura e pesca"
        }
    ]

    # Criação de abas
    tabs = ["Pergunta 1", "Pergunta 2", "Pergunta 3"]
    tab_selecionada = st.selectbox("Escolha uma pergunta:", tabs)

    # Variáveis para armazenar as respostas
    respostas = []

    # Exibir as perguntas e opções dentro de cada aba
    if tab_selecionada == "Pergunta 1":
        resposta = st.radio(perguntas[0]["pergunta"], perguntas[0]["opcoes"], key="pergunta_1")
        respostas.append(resposta)
    elif tab_selecionada == "Pergunta 2":
        resposta = st.radio(perguntas[1]["pergunta"], perguntas[1]["opcoes"], key="pergunta_2")
        respostas.append(resposta)
    elif tab_selecionada == "Pergunta 3":
        resposta = st.radio(perguntas[2]["pergunta"], perguntas[2]["opcoes"], key="pergunta_3")
        respostas.append(resposta)

    # Botão para mostrar o resultado
    if st.button("Verificar Respostas"):
        pontos = 0
        for i, pergunta in enumerate(perguntas):
            if respostas[i] == pergunta["resposta"]:
                pontos += 1
        
        # Exibir o resultado
        st.markdown(f"Você acertou {pontos} de {len(perguntas)} perguntas.")
        
        if pontos == len(perguntas):
            st.success("Parabéns! Você tem um ótimo conhecimento sobre o ecossistema e extinção!")
        else:
            st.warning("Você tem um bom conhecimento, mas ainda há espaço para aprender mais!")
# Aba 5 - Iniciativas Globais de Conservação
with abas[4]:
    st.header("Iniciativas Globais de Conservação")
    st.markdown("""
                Muitas organizações internacionais estão trabalhando incansavelmente para proteger nosso planeta. Conheça algumas das principais iniciativas:
                """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://www.worldwildlife.org/media/images/panda_thumb_16x9.jpg")
        st.subheader("WWF")
        st.write("O WWF trabalha para construir um futuro em que as pessoas vivam em harmonia com a natureza. Descubra seus projetos em [link para o site do WWF](https://www.worldwildlife.org/).")
    
    with col2:
        st.image("https://www.conservation.org/content/dam/conservation/images/about-us/our-work/conservation-international-logo-horizontal.jpg")
        st.subheader("Conservation International")
        st.write("A Conservation International protege a natureza para que a natureza possa proteger as pessoas. Saiba mais em [link para o site da Conservation International](https://www.conservation.org/).")
    
    with col3:
        st.image("https://www.iucn.org/sites/dev/files/styles/large/public/design/logos/iucn_logo_red.svg")
        st.subheader("IUCN")
        st.write("A IUCN avalia o estado de conservação das espécies e inspira soluções para conservação e uso sustentável da natureza. Acesse a Lista Vermelha em [link para a Lista Vermelha da IUCN](https://www.iucnredlist.org/).")
    
    st.write("*Explore os hotspots de biodiversidade no mundo:*")
    st.markdown("""
                *Faça a sua parte!*
                * *Compartilhe este conteúdo* nas redes sociais e ajude a espalhar a mensagem.
                * *Doe* para as organizações que você admira.
                * *Reduza seu impacto* no meio ambiente, adotando hábitos mais sustentáveis.
                * *Voluntarie-se* em projetos de conservação.
                *Juntos, podemos fazer a diferença!*
                """)