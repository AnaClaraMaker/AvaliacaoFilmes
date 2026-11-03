from flask import session
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from conn import BD_Session
from model.avaliacao import Avaliacao

def avaliacao_listar_alerta():
    avaliacoes = []

    with BD_Session() as bd_sessao:
        dados = bd_sessao.query(Avaliacao).filter(Avaliacao.alerta_ofensivo == "S", Avaliacao.check_ofensivo == "N").order_by(Avaliacao.data_avaliacao).all()
        if dados:
            avaliacoes = [avaliacao.to_print() for avaliacao in dados]

    return avaliacoes

def avaliacao_listar_filme(filme_id):
    avaliacoes = []

    with BD_Session() as bd_sessao:
        dados = bd_sessao.query(Avaliacao).filter(Avaliacao.filme_id == filme_id, Avaliacao.check_ofensivo == "N").order_by(Avaliacao.data_avaliacao.desc()).all()
        if dados:
            avaliacoes = [avaliacao.to_print() for avaliacao in dados]

    return avaliacoes

def avaliacao_listar_alerta():
    avaliacoes = []

    with BD_Session() as bd_sessao:
        dados = bd_sessao.query(Avaliacao).filter(Avaliacao.alerta_ofensivo == "S", Avaliacao.check_ofensivo == "N").order_by(Avaliacao.data_avaliacao).all()
        if dados:
            avaliacoes = [avaliacao.to_print(True) for avaliacao in dados]

    return avaliacoes

def avaliacao_detalhe(id):
    avaliacao = None
    with BD_Session() as bd_sessao:
        avaliacao = bd_sessao.get(Avaliacao, id)
        if avaliacao:
            avaliacao = avaliacao.to_print()
    return avaliacao

def avaliacao_nova(filme_id, usuario_id, comentario, nota):
    resultado = False
    data_avaliacao = datetime.now()
    alerta_ofensivo='N'
    check_ofensivo='N'

    with BD_Session() as bd_sessao:
        avaliacao = Avaliacao(filme_id=filme_id,
                              usuario_id=usuario_id,
                              data_avaliacao=data_avaliacao,
                              comentario=comentario,
                              nota=nota,
                              alerta_ofensivo=alerta_ofensivo,
                              check_ofensivo=check_ofensivo)
        bd_sessao.add(avaliacao)
        bd_sessao.commit()
        resultado = True

    return resultado

def avaliacao_alertar(id):
    resultado = False

    with BD_Session() as bd_sessao:
        avaliacao = bd_sessao.get(Avaliacao, id)
        if(avaliacao):
            avaliacao.alerta_ofensivo = "S"
            bd_sessao.commit()
            resultado = True

    return resultado

def avaliacao_ofensiva(id):
    resultado = False
    
    with BD_Session() as bd_sessao:
        avaliacao = bd_sessao.get(Avaliacao, id)
        if(avaliacao):
            avaliacao.alerta_ofensivo = "S"
            avaliacao.check_ofensivo = "S"
            bd_sessao.commit()
            resultado = True

    return resultado

def avaliacao_inofensiva(id):
    resultado = False
    
    with BD_Session() as bd_sessao:
        avaliacao = bd_sessao.get(Avaliacao, id)
        if(avaliacao):
            avaliacao.alerta_ofensivo = "N"
            avaliacao.check_ofensivo = "N"
            bd_sessao.commit()
            resultado = True

    return resultado

def avaliacao_excluir(id):
    resultado = False

    with BD_Session() as bd_sessao:
        avaliacao = bd_sessao.get(Avaliacao, id)
        if(avaliacao):
            bd_sessao.delete(avaliacao)
            bd_sessao.commit()
            resultado = True

    return resultado