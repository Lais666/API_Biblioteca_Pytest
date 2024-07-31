import os

# Define se as chaves JSON devem ser ordenadas
JSON_SORT_KEYS = True

# Define a chave secreta
SECRET_KEY = 'sua_chave_aqui'

# Define o caminho do banco de dados principal
DATABASE_PATH = 'mysql://root:12345678@localhost/biblioteca'

# Verifica se estamos no ambiente de teste
if os.environ.get('FLASK_ENV') == 'testing':
    # Se estivermos no ambiente de teste, usa um banco de dados de teste
    DATABASE_PATH = 'mysql://root:12345678@localhost/teste_db'

# Define o URI do banco de dados com base no caminho definido acima
SQLALCHEMY_DATABASE_URI = DATABASE_PATH