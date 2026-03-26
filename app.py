from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, init_db
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Inicializar banco de dados
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes ORDER BY data_cadastro DESC').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, telefone, endereco, cidade, estado, cep))
            conn.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Erro: Email já cadastrado!', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('cadastrar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']
        
        try:
            conn.execute('''
                UPDATE clientes 
                SET nome = ?, email = ?, telefone = ?, endereco = ?, 
                    cidade = ?, estado = ?, cep = ?
                WHERE id = ?
            ''', (nome, email, telefone, endereco, cidade, estado, cep, id))
            conn.commit()
            flash('Cliente atualizado com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Erro: Email já cadastrado!', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar.html', cliente=cliente)

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)