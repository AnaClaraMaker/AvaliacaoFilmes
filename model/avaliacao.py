from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Avaliacao(Base):
    __tablename__ = "AVALIACAO"
    id = Column("IDAVALIACAO", Integer, primary_key=True)
    idfilme = Column("IDFILME", Integer, ForeignKey("FILME.IDFILME"))
    idusuario = Column("IDUSUARIO", Integer, ForeignKey("USUARIO.IDUSUARIO"))
    data_avaliacao = Column("DATA_AVALIACAO",)