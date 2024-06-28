import psycopg2
from dotenv import load_dotenv
import os

# Carregar variáveis .env
load_dotenv()

# Puxar das environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')  # Default 5432


#conectar
def connect():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Conexão ao banco de dados bem-sucedida!")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar:", error)
        return None

def create_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    #Criar os campos na tabela, o drop está apenas para testar a criação novamente
    #Se for inserir nova coluna é daqui pra baixo
    cursor.execute('''
                   DROP TABLE IF EXISTS apartmentos;
                   CREATE TABLE IF NOT EXISTS apartmentos (
                       id SERIAL PRIMARY KEY,
                       edificio TEXT,
                       endereco TEXT,
                       area FLOAT,
                       quartos INTEGER,
                       suite INTEGER,
                       banheiros INTEGER,
                       vagas INTEGER,
                       preco FLOAT,
                       imobiliaria TEXT
                   )
                ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(edificio, endereco, area, quartos, suite, banheiros, vagas, preco, imobiliaria):
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
     # Definindo valores padrão para campos vazios
    if quartos == "":
        quartos = 1
    if suite == "":
        suite = 1
    if banheiros == "":
         banheiros = 1
    if vagas == "":
        vagas = 1
    
    cursor.execute('''
                  INSERT INTO apartmentos (edificio, endereco, area, quartos, suite, banheiros, vagas, preco, imobiliaria)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ''', (edificio, endereco, area, quartos, suite, banheiros, vagas, preco, imobiliaria))
    conn.commit()
    cursor.close()
    conn.close()
    
def fetch_data():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()
    query = "SELECT edificio, endereco, area, quartos, suite, banheiros, vagas, preco, imobiliaria FROM apartmentos"
    cursor.execute(query)
    rows = cursor.fetchall()

    columns = ['edificio', 'endereco', 'area', 'quartos', 'suite', 'banheiros', 'vagas', 'preco', 'imobiliaria']
    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()
    return data