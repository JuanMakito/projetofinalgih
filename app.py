import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from PIL import Image

# Configuração Inicial
st.set_page_config(page_title="Cuidados Pet", layout="wide")

# CSS Customizado
import streamlit as st

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

    # Gráfico de Dispersão (Scatter Plot)
    st.subheader("Gráfico de Dispersão")
    if 'column1' in data.columns and 'column2' in data.columns:  # Substitua column1 e column2 pelos nomes reais das colunas
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x='column1', y='column2', hue='pet_tipo', style='pet_tipo', s=100)
        plt.title('Relação entre Column1 e Column2')
        plt.xlabel('Column1')
        plt.ylabel('Column2')
        plt.legend(title='Tipo de Pet')
        st.pyplot(plt)
    else:
        st.warning("As colunas especificadas para o gráfico de dispersão não estão disponíveis.")

    # Histograma
    st.subheader("Histograma")
    if 'column3' in data.columns:  # Substitua column3 pelo nome real da coluna
        plt.figure(figsize=(10, 6))
        sns.histplot(data['column3'], bins=20, kde=True)  # KDE para adicionar a curva de densidade
        plt.title('Distribuição de Column3')
        plt.xlabel('Column3')
        plt.ylabel('Frequência')
        st.pyplot(plt)
    else:
        st.warning("A coluna especificada para o histograma não está disponível.")


# Funções de Conteúdo do Site
def homepage():
    # Exibindo a imagem de fundo
    st.image("https://seubeneficiodigital.com.br/wp-content/uploads/2017/03/pets-capa-para-twitter-gato-preto.jpg", use_column_width=True)
    # Título
    st.title("Bem-vindo ao Cuidados Pet!")
    
    # Descrição
    st.write("Descubra dicas essenciais e serviços para melhorar o bem-estar dos seus pets.")

    # Seção de Destaques Recentes
    st.subheader("Destaques Recentes")
    st.write("🐾 Dicas para a saúde do seu pet")
    st.write("🏆 Serviços de grooming e estética")
    st.write("📅 Agendamento de consultas veterinárias")

    # Seção de Serviços
    st.subheader("Nossos Serviços")
    st.write("- Consultas Veterinárias")
    st.write("- Banho e Tosa")
    st.write("- Treinamento de Comportamento")
    st.write("- Produtos para Pets")

    # Seção de Dicas
    st.subheader("Dicas Importantes")
    st.write("1. Mantenha a vacinação em dia.")
    st.write("2. Alimente seu pet com ração de qualidade.")
    st.write("3. Proporcione exercícios regulares.")
    st.write("4. Esteja atento a sinais de doenças.")

    # Rodapé
    st.markdown("---")
    st.write("Para mais informações, entre em contato conosco.")

def care_section():
    st.title("Seção de Cuidados para Pets")
    st.write("Aqui você encontra artigos e dicas sobre cuidados essenciais para diferentes tipos de animais. Mantenha seu pet saudável e feliz com as nossas orientações!")
    
    # Sugestões de cuidados
    st.subheader("Dicas de Cuidados")
    st.markdown("""
    - **Alimentação Balanceada:** Ofereça ração de qualidade, adequada à idade e ao tipo do seu pet.
    - **Exercícios Regulares:** Promova atividade física com passeios e brincadeiras.
    - **Higiene:** Mantenha a higiene do seu animal com banhos regulares e cuidados com os dentes.
    - **Visitas ao Veterinário:** Realize check-ups anuais para prevenir doenças.
    - **Socialização:** Exponha seu pet a diferentes ambientes e interações com outros animais.
    """)

    # Vídeo informativo
    st.subheader("Assista ao Nosso Vídeo")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Links úteis
    st.subheader("Links Úteis")
    st.markdown("""
    - [Dicas de Alimentação](https://www.petshopcontrol.com.br/blog/alimentacao-saudavel-para-pets-o-que-voce-precisa-saber/?gad_source=1&gclid=CjwKCAjw-JG5BhBZEiwAt7JR62sV-Ljrus7RLOW3PN1MnT8XSiTfrNuKmeCGIje9U1f20E2eiwYMCRoCj0QQAvD_BwE)
    - [Importância do Exercício](https://novadiagnostico.com.br/2023/08/07/atividade-fisica-com-pets-conheca-os-beneficios-e-os-cuidados/#:~:text=a%20sa%C3%BAde%20psicol%C3%B3gica.-,O%20que%20muitas%20pessoas%20ainda%20n%C3%A3o%20sabem%20%C3%A9%20que%20praticar,e%20o%20v%C3%ADnculo%20entre%20ambos.)
    - [Higiene e Cuidados](https://vetysdobrasil.com.br/blog/como-a-higiene-impacta-na-qualidade-de-vida-dos-pets/#:~:text=A%20higiene%20dos%20pets%20%C3%A9,f%C3%ADsico%20e%20evitar%20problemas%20comportamentais.)
    - [Consultas Veterinárias](https://www.hospitalpopularveterinario.com.br/2020/09/02/por-que-e-tao-importante-manter-a-vacinacao-do-seu-pet-em-dia)
    """)

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

    st.header("Consultas com Especialistas")
    st.write("Para cuidados mais específicos, entre em contato com um especialista:")
    st.markdown("- **Veterinários locais:** Confira nossa lista de veterinários recomendados.")
    st.markdown("- **Comportamentalistas:** Consulte especialistas para lidar com comportamentos problemáticos.")
    st.markdown("- **Clínicas de emergência:** Saiba onde encontrar atendimento em situações urgentes.")

    st.header("Espaço para Dúvidas")
    st.write("Tem alguma dúvida sobre a saúde do seu pet? Confira nossa seção de perguntas frequentes ou envie suas perguntas!")
    st.text_input("Digite sua dúvida aqui:")

def adopt_section():
    st.title("Adote um Pet")
    st.write("Adotar é um ato de amor! Descubra como você pode fazer a diferença na vida de um animal.")

    st.header("Benefícios da Adoção")
    st.write("Adotar um pet traz muitos benefícios, tanto para o animal quanto para você:")
    st.markdown("- **Salvamento de vidas:** A adoção reduz a superpopulação de animais em abrigos.")
    st.markdown("- **Amor incondicional:** Pets adotados são gratos e formam laços especiais com suas famílias.")
    st.markdown("- **Custo reduzido:** Adoções geralmente incluem vacinação e castração, economizando dinheiro.")

    st.header("Como Adotar")
    st.write("O processo de adoção é simples. Siga estes passos:")
    st.markdown("1. **Pesquise:** Conheça os abrigos e as opções de adoção disponíveis na sua região.")
    st.markdown("2. **Preencha um formulário:** A maioria dos abrigos exige um formulário de pré-adopção.")
    st.markdown("3. **Entrevista:** Alguns abrigos realizam entrevistas para garantir que você está preparado.")
    st.markdown("4. **Visita:** Conheça o pet que você deseja adotar e veja se há conexão.")
    st.markdown("5. **Taxas:** Esteja ciente de que pode haver taxas de adoção que ajudam a cobrir custos de cuidados.")

    st.header("Onde Adotar")
    st.write("Considere estas opções para encontrar seu novo amigo:")
    st.markdown("- **Abrigos locais:** Pesquise abrigos em sua área.")
    st.markdown("- **ONGs de proteção animal:** Muitas organizações têm pets para adoção.")
    st.markdown("- **Eventos de adoção:** Fique atento a feiras de adoção que ocorrem em sua cidade.")

    st.header("Preparação para a Adoção")
    st.write("Antes de trazer um pet para casa, considere:")
    st.markdown("- **Espaço:** Certifique-se de que sua casa é adequada para o tipo de animal que você deseja adotar.")
    st.markdown("- **Família:** Converse com todos os membros da família sobre a adoção e o novo pet.")
    st.markdown("- **Materiais:** Adquira os itens essenciais, como ração, cama, brinquedos e caixa de transporte.")

    st.header("Cuidados Após a Adoção")
    st.write("Dicas para ajudar seu novo amigo a se adaptar ao novo lar:")
    st.markdown("- **Tempo de adaptação:** Dê ao seu pet tempo para se ajustar ao novo ambiente.")
    st.markdown("- **Veterinário:** Marque uma consulta para verificar a saúde do seu novo animal.")
    st.markdown("- **Treinamento:** Considere aulas de adestramento para facilitar a adaptação.")

    st.header("Eventos de Adoção")
    st.write("Participe de eventos e faça a diferença:")
    st.markdown("- **Feira de Adoção:** Evento no Parque Central, dia 15 de novembro, das 10h às 16h.")
    st.markdown("- **Voluntariado:** Muitas ONGs precisam de ajuda para organizar eventos de adoção.")

    st.header("Voluntariado e Apoio")
    st.write("Você pode ajudar de várias formas:")
    st.markdown("- **Voluntariado:** Ofereça seu tempo em abrigos e ONGs.")
    st.markdown("- **Doações:** Contribua com ração, brinquedos ou produtos de higiene.")
    st.markdown("- **Espalhe a palavra:** Compartilhe informações sobre adoção nas redes sociais.")

    st.header("FAQ sobre Adoção")
    st.write("Tem alguma dúvida? Confira nossas perguntas frequentes:")
    st.markdown("- **Qual é a idade mínima para adotar?** Normalmente, você deve ter pelo menos 18 anos.")
    st.markdown("- **Posso adotar se já tenho outros pets?** Sim, mas é importante fazer a introdução com cuidado.")
    st.markdown("- **O que fazer se não puder mais cuidar do animal?** Entre em contato com o abrigo ou ONG onde adotou.")

def community_section():
    st.header("Comunidade")
    st.write("Participe da nossa comunidade e compartilhe suas experiências!")
    st.text_area("Conte-nos sua história ou dicas sobre cuidados com pets:")

    st.header("Histórias de Sucesso")
    st.write("Inspire-se com histórias de donos que melhoraram a saúde de seus pets. Veja como eles fizeram isso!")
    st.markdown("- **Caso 1:** O João transformou a dieta da sua gata e ela perdeu peso e ganhou energia.")
    st.markdown("- **Caso 2:** A Maria implementou uma rotina de exercícios para seu cachorro e agora eles têm passeios diários juntos.")

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Página Inicial", "Cuidados", "Saúde", "Adoção", 
    "Comunidade", "Análise de Dados", "Cadastro de Pets"
])

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
    data_analysis()
with tab7:
    pet_registration()

# Rodapé
st.markdown("<footer>&copy; 2023 Cuidados Pet - Todos os direitos reservados.</footer>", unsafe_allow_html=True)
