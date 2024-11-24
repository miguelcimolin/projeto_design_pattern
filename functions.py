import sqlite3
from faker import Faker

faker = Faker()

def initialize_db(db_path="bd/banco.db"):
    """Cria o banco de dados e a tabela 'ordem' se ainda não existirem."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordem (
            id TEXT PRIMARY KEY,
            sequencial INTEGER,
            nome_cliente TEXT,
            cpf_cliente TEXT,
            data_compra DATE,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")


def generate_client_data():
    """Gera dados fictícios para o cliente."""
    nome_cliente = faker.name()
    cpf_cliente = faker.ssn()
    return nome_cliente, cpf_cliente

def get_next_sequencial(db_path="db/banco.db"):
    """Obtém o próximo número sequencial com base no banco."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(sequencial) FROM ordem")
    result = cursor.fetchone()[0]

    conn.close()
    return (result or 0) + 1

def consultarBanco(db_path="db/banco.db"):
    """Obtém os últimos 10 registros criados no BD"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ordem ORDER BY sequencial DESC LIMIT 10")
    result = cursor.fetchall()

    conn.close()
    return result