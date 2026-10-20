from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# NOTA: Caso já tenha a Base criada num ficheiro de ligação à base de dados (ex: database.py),
# prefira importar de lá: from database import Base
Base = declarative_base()


class Usuario(Base):
  __tablename__ = "USUARIO"

  id = Column("IDUSUARIO", Integer, primary_key=True, autoincrement=True)
  nome = Column("NOME", String(100), nullable=False)
  email = Column("EMAIL", String(200), nullable=False, unique=True, index=True)
  senha = Column("SENHA", String(255), nullable=False)
  perfil = Column("PERFIL", String(20), nullable=False, default="COMUM")
  bloqueado = Column("BLOQUEADO", String(1), nullable=False, default="N")

  def to_dict(self):
    """Retorna uma representação em dicionário sem expor a senha."""
    return {
        "id": self.id,
        "nome": self.nome,
        "email": self.email,
        "perfil": self.perfil,
        "bloqueado": self.bloqueado,
    }

  def __repr__(self):
    return (
        f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    )