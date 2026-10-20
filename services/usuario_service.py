import hashlib
import secrets
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importa a classe Usuario definida no pacote model
from model.usuario import Usuario


class UsuarioService:
    def __init__(self, db_session: Session):
        """Recebe a sessão ativa do SQLAlchemy para efetuar as operações na BD."""
        self.db = db_session

    # =========================================================================
    # Métodos Auxiliares de Segurança
    # =========================================================================
    @staticmethod
    def _gerar_hash_senha(senha_plana: str) -> str:
        """Gera o hash SHA-256 da palavra-passe."""
        return hashlib.sha256(senha_plana.encode("utf-8")).hexdigest()

    @staticmethod
    def _gerar_senha_aleatoria(tamanho: int = 10) -> str:
        """Gera uma palavra-passe aleatória segura para redefinição por parte do administrador."""
        caracteres = string.ascii_letters + string.digits + "!@#$%&*"
        return "".join(secrets.choice(caracteres) for _ in range(tamanho))

    # =========================================================================
    # Regras do Módulo / Utilizador Comum
    # =========================================================================
    def cadastrar_usuario(
        self, nome: str, email: str, senha: str, perfil: str = "COMUM"
    ) -> Usuario:
        """Registo inicial: guarda com hash e com bloqueado='N'."""
        email_normalizado = email.strip().lower()

        if self.buscar_por_email(email_normalizado):
            raise ValueError(f"O e-mail '{email_normalizado}' já se encontra registado.")

        novo_usuario = Usuario(
            nome=nome.strip(),
            email=email_normalizado,
            senha=self._gerar_hash_senha(senha),
            perfil=perfil.upper(),
            bloqueado="N",
        )

        try:
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
            return novo_usuario
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro de integridade ao registar o utilizador.")

    def autenticar(self, email: str, senha: str) -> Usuario:
        """Validação de login: confere e-mail, se está bloqueado e a hash da palavra-passe."""
        usuario = self.buscar_por_email(email.strip().lower())

        if not usuario:
            raise ValueError("Credenciais inválidas.")

        if usuario.bloqueado == "S":
            raise PermissionError("Utilizador bloqueado. Contacte o administrador.")

        if usuario.senha != self._gerar_hash_senha(senha):
            raise ValueError("Credenciais inválidas.")

        return usuario

    def alterar_propria_senha(
        self, id_usuario: int, senha_atual: str, nova_senha: str
    ) -> bool:
        """Regra 3.2.3: O utilizador comum altera a sua própria palavra-passe."""
        usuario = self.buscar_por_id(id_usuario)

        if not usuario:
            raise ValueError("Utilizador não encontrado.")

        if usuario.senha != self._gerar_hash_senha(senha_atual):
            raise ValueError("A palavra-passe atual está incorreta.")

        if len(nova_senha) < 6:
            raise ValueError("A nova palavra-passe deve ter pelo menos 6 caracteres.")

        usuario.senha = self._gerar_hash_senha(nova_senha)
        self.db.commit()
        return True

    # =========================================================================
    # Regras do Administrador
    # =========================================================================
    def alterar_status_bloqueio(self, id_usuario: int, bloquear: bool) -> Usuario:
        """Regra 3.1.2: Administrador bloqueia ('S') ou desbloqueia ('N') um utilizador."""
        usuario = self.buscar_por_id(id_usuario)

        if not usuario:
            raise ValueError("Utilizador não encontrado.")

        usuario.bloqueado = "S" if bloquear else "N"
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def redefinir_senha_aleatoria(self, id_usuario: int) -> str:
        """
        Regra 3.1.4: Redefine a palavra-passe do utilizador para um valor aleatório.
        Retorna a palavra-passe em texto limpo para ser fornecida ao utilizador.
        """
        usuario = self.buscar_por_id(id_usuario)

        if not usuario:
            raise ValueError("Utilizador não encontrado.")

        senha_temporaria = self._gerar_senha_aleatoria(10)
        usuario.senha = self._gerar_hash_senha(senha_temporaria)

        self.db.commit()
        return senha_temporaria

    # =========================================================================
    # Consultas
    # =========================================================================
    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == id_usuario).first()

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email.strip().lower()).first()

    def listar_todos(self) -> List[Usuario]:
        """Lista todos os utilizadores (usado no painel administrativo)."""
        return self.db.query(Usuario).order_by(Usuario.nome).all()