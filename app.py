from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessoes_filmes"

# Configuração da conexão com o banco MySQL
# Ajuste o usuário e senha conforme o seu ambiente local (ex: root:sua_senha)
USUARIO_BANCO = os.getenv("DB_USER", "root")
SENHA_BANCO = os.getenv("DB_PASS", "")
HOST_BANCO = os.getenv("DB_HOST", "localhost")
PORTA_BANCO = os.getenv("DB_PORT", "3306")
NOME_BANCO = os.getenv("DB_NAME", "DBEXERCICIO40")

DATABASE_URL = f"mysql+pymysql://{USUARIO_BANCO}:{SENHA_BANCO}@{HOST_BANCO}:{PORTA_BANCO}/{NOME_BANCO}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Função utilitária para abrir uma sessão com o banco de dados."""
    db = SessionLocal()
    return db

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Fecha as conexões ao final de cada requisição."""
    pass

# Rota inicial básica de teste
@app.route("/")
def index():
    return "Aplicação de Avaliação de Filmes rodando com sucesso!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
