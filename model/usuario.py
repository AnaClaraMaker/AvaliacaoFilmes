from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# criando o elemento que vai mapear a classe com a tabela do banco
Base = declarative_base()

class Usuario(Base):

    __tablename__ = "USUARIO"

    id = Column("IDUSUARIO", Integer, primary_key=True)
    nome = Column("NOME", String(100))
    email = Column("EMAIL", String(200))
    senha = Column("SENHA", String(200))
    perfil = Column("PERFIL", String(10))
    bloqueado = Column("BLOQUEADO", String(1))

    def to_print(self):
        return {"id": self.id
                , "nome": self.nome
                , "email": self.email
                , "perfil": self.perfil
                , "bloqueado": self.bloqueado
                }