import requests
from datetime import datetime
from model.filme import Filme

class FilmeService:
    # Insira aqui a chave da API do TMDB quando for testar a sincronização
    TMDB_API_KEY = "SUA_API_KEY_DO_TMDB"
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    @staticmethod
    def listar_todos(db_session):
        """Lista todos os filmes cadastrados."""
        return db_session.query(Filme).all()

    @staticmethod
    def listar_por_data_estreia(db_session):
        """Requisito 3.3.1: Lista filmes ordenados pela data de estreia (mais recente para o mais antigo)."""
        return db_session.query(Filme).order_by(Filme.data_estreia.desc()).all()

    @staticmethod
    def obter_por_id(db_session, id_filme):
        """Busca um filme específico pelo ID."""
        return db_session.query(Filme).filter(Filme.id == id_filme).first()

    @staticmethod
    def cadastrar_filme(db_session, titulo, descricao, descricao_breve, data_estreia, url_poster):
        """Insere um novo filme no banco de dados."""
        if isinstance(data_estreia, str) and data_estreia:
            data_estreia = datetime.strptime(data_estreia, "%Y-%m-%d").date()

        novo_filme = Filme(
            titulo=titulo,
            descricao=descricao,
            descricao_breve=descricao_breve,
            data_estreia=data_estreia,
            url_poster=url_poster
        )
        db_session.add(novo_filme)
        db_session.commit()
        db_session.refresh(novo_filme)
        return novo_filme

    @classmethod
    def buscar_filmes_tmdb_em_cartaz(cls):
        """Requisito 1: Consulta a API do TMDB para obter os filmes em cartaz."""
        url = f"{cls.TMDB_BASE_URL}/movie/now_playing"
        params = {
            "api_key": cls.TMDB_API_KEY,
            "language": "pt-BR",
            "page": 1
        }
        try:
            resposta = requests.get(url, params=params)
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get("results", [])
            return []
        except Exception as e:
            print(f"Erro ao consultar TMDB: {e}")
            return []

    @classmethod
    def sincronizar_filmes_tmdb(cls, db_session):
        """Requisito 3.1.1: Permite ao administrador atualizar a lista com filmes do TMDB."""
        filmes_tmdb = cls.buscar_filmes_tmdb_em_cartaz()
        filmes_adicionados = 0

        for item in filmes_tmdb:
            titulo = item.get("title")
            
            # Evita duplicar se o filme já estiver no banco
            existe = db_session.query(Filme).filter(Filme.titulo == titulo).first()
            if not existe:
                descricao = item.get("overview", "")
                descricao_breve = (descricao[:97] + "...") if len(descricao) > 100 else descricao
                data_lancamento = item.get("release_date")
                poster_path = item.get("poster_path")
                url_poster = f"{cls.IMAGE_BASE_URL}{poster_path}" if poster_path else ""

                cls.cadastrar_filme(
                    db_session=db_session,
                    titulo=titulo,
                    descricao=descricao[:200] if descricao else "",
                    descricao_breve=descricao_breve,
                    data_estreia=data_lancamento,
                    url_poster=url_poster
                )
                filmes_adicionados += 1

        return filmes_adicionados