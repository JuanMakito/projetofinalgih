import mysql.connector
import pymysql

# Conexão com o banco de dados MySQL usando mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai@123",
        database="petscare"
    )

# Conexão com o banco de dados MySQL usando pymysql
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='seu_usuario',
        password='sua_senha',
        database='seu_banco_de_dados'
    )
    return connection

# Função para registrar um dono de pet
def register_owner(name, email, pet_type):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cadastro (nome_dono, email, pet_tipo) VALUES (%s, %s, %s)", (name, email, pet_type))
            conn.commit()

# Função para inserir um comentário
def insert_comment(comment):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO comentarios (texto) VALUES (%s)", (comment,))
        connection.commit()

# Função para buscar comentários
def fetch_comments():
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT texto FROM comentarios")
            result = cursor.fetchall()
    return [row[0] for row in result]
