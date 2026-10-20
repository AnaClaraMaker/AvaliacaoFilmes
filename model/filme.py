from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Filme(Base):
    __tablename__ = "FILME"

    id = Column("IDFILME", Integer, primary_key=True, autoincrement=True)
    titulo = Column("TITULO", String(100), nullable=False)
    descricao = Column("DESCRICAO", String(200))
    descricao_breve = Column("DESCRICAO_BREVE", String(100))
    data_estreia = Column("DATA_ESTREIA", Date)
    url_poster = Column("URL_POSTER", String(200))

    def to_print(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "descricao_breve": self.descricao_breve,
            "data_estreia": self.data_estreia.strftime("%Y-%m-%d") if self.data_estreia else None,
            "url_poster": self.url_poster
        }