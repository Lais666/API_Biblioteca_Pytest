import json
import os
import sys
import pytest

# Configura a variável de ambiente para o ambiente de teste
os.environ['FLASK_ENV'] = 'testing'

# Adiciona o diretório raiz do projeto ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, db
from models import Livro, Usuario
# Define um fixture do pytest para configurar o cliente de teste
@pytest.fixture
def client():

    # Configurações específicas para o modo de teste
    app.config['TESTING'] = True
    # Define o banco de dados a ser usado durante os testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/teste_db'

    # Cria um cliente de teste para a aplicação Flask
    with app.test_client() as client:
        # Cria um contexto da aplicação para que operações como db.create_all() possam ser executadas
        with app.app_context():
            # Cria todas as tabelas definidas nos modelos SQLAlchemy
            db.create_all()

            # Retorna o cliente de teste para ser usado nos testes
            yield client

            # Reverte todas as mudanças feitas durante os testes
            db.session.rollback()

            # (Opcional) Dropa todas as tabelas para limpar o ambiente de teste
            db.drop_all()

# Testa a rota GET /livro
def test_get_livro(client):
    print("Running test_get_livro")
    # Faz uma requisição GET para a rota /livro
    response = client.get('/livro')
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém a palavra 'Lista'
    assert b'Lista' in response.data

# Testa a rota POST /livro
def test_post_livro(client):
    print("Running test_post_livro")
    # Cria uma sessão de transação para simular o login do usuário
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    # Faz uma requisição POST para a rota /livro com os dados do livro no formato JSON
    response = client.post('/livro', json={
        'id_livro': 1,
        'titulo': 'Python Testing',
        'autor': 'Author Name',
        'ano_publicacao': 2021
    })
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém a mensagem de sucesso
    assert b'Livro Cadastrado com Sucesso' in response.data

# Testa a rota POST /login
def test_login(client):
    print("Running test_login")
    # Cria um contexto da aplicação para adicionar um usuário ao banco de dados
    with app.app_context():
        usuario = Usuario(id_usuario=1, email='test@example.com', senha='123456')
        db.session.add(usuario)
        db.session.commit()

    # Faz uma requisição POST para a rota /login com os dados de login no formato JSON
    response = client.post('/login', json={
        'email': 'test@example.com',
        'senha': '123456'
    })
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém a mensagem de sucesso no login
    assert b'Login com sucesso' in response.data

# Testa a rota POST /logout
def test_logout(client):
    print("Running test_logout")
    # Cria uma sessão de transação para simular o login do usuário
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    # Faz uma requisição POST para a rota /logout
    response = client.post('/logout')
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém a mensagem de sucesso no logout
    assert b'Logout bem Sucedido' in response.data

# Testa a rota PUT /livro/<id_livro>
def test_put_livro(client):
    print("Running test_put_livro")
    # Cria uma sessão de transação para simular o login do usuário
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    # Cria um contexto da aplicação para adicionar um livro ao banco de dados
    with app.app_context():
        livro = Livro(id_livro=2, titulo='Old Title', autor='Old Author', ano_publicacao=2020)
        db.session.add(livro)
        db.session.commit()

    # Faz uma requisição PUT para a rota /livro/2 com os novos dados do livro no formato JSON
    response = client.put('/livro/2', json={
        'titulo': 'New Title',
        'autor': 'New Author',
        'ano_publicacao': 2022
    })
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém a mensagem de sucesso na atualização do livro
    assert b'Livro atualizado com sucesso' in response.data

# Testa a rota DELETE /livro/<id_livro>
def test_delete_livro(client):
    print("Running test_delete_livro")
    # Cria uma sessão de transação para simular o login do usuário
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    # Cria um contexto da aplicação para adicionar um livro ao banco de dados
    with app.app_context():
        livro = Livro(id_livro=3, titulo='Title', autor='Author', ano_publicacao=2020)
        db.session.add(livro)
        db.session.commit()

    # Faz uma requisição DELETE para a rota /livro/3
    response = client.delete('/livro/3')
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200

    # Decodifica a resposta JSON
    response_data = json.loads(response.data.decode('utf-8'))
    # Verifica se a mensagem de sucesso na exclusão do livro está presente na resposta
    assert 'Livro excluído com sucesso' in response_data['mensagem']
