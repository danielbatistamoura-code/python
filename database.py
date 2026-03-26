import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            endereco TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Ativo'
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")