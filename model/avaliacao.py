from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Avaliacao(Base):

    __tablename__ = "AVALIACAO"
    
    id = Column("IDAVALIACAO", Integer, primary_key=True)
    data_avaliacao = Column("DATA_AVALIACAO", DateTime)
    comentario = Column("COMENTARIO", String(100))
    nota = Column("NOTA", Integer)
    alerta_ofensivo = Column("ALERTA_OFENSIVO", String(1))
    check_ofensivo = Column("CHECK_OFENSIVO", String(1))

#relacionamento

    idfilme = Column("IDFILME", Integer, ForeignKey("FILME.IDFILME"))
    idusuario = Column("IDUSUARIO", Integer, ForeignKey("USUARIO.IDUSUARIO"))

# dados do relacionamento

    filme = relationship("Filme", back_populates="avaliacoes")
    usuario = relationship("Usuario")

    def to_print(self, hierarquia=False):

        if hierarquia:
            filme = self.filme.to_print()
            usuario = self.usuario.to_print()

        else: 
            filme = self.idfilme
            usuario = self.idusuario

        avaliacao2 = (self.data_avaliacao.strftime("%d/%m/%Y %H:%M:%S") if self.data_avaliacao else None)

        return {"id": self.id
                , "idfilme": self.idfilme
                , "idusuario": self.idusuario
                , "data_avaliacao": self.data_avaliacao
                , "data_avaliacao2": avaliacao2
                , "comentario": self.comentario
                , "nota": self.nota
                , "alerta_ofensivo": self.alerta_ofensivo
                , "check_ofensivo": self.check_ofensivo
                , "filme": filme
                , "usuario": usuario
                }