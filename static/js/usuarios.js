document.addEventListener("DOMContentLoaded", () => {
    // Validação básica do formulário de registo/alteração de palavra-passe
    const formUsuario = document.querySelector("#formUsuario");
    if (formUsuario) {
        formUsuario.addEventListener("submit", (e) => {
            const senhaInput = document.querySelector("#senha");
            if (senhaInput && senhaInput.value.length < 6) {
                e.preventDefault();
                alert("A palavra-passe deve conter pelo menos 6 caracteres.");
            }
        });
    }

    // Ação de Bloqueio/Desbloqueio de Utilizador (Painel Admin)
    const botoesBloqueio = document.querySelectorAll(".btn-bloquear-usuario");
    botoesBloqueio.forEach((botao) => {
        botao.addEventListener("click", async () => {
            const idUsuario = botao.getAttribute("data-id");
            if (!confirm("Tem a certeza de que deseja alterar o estado de bloqueio deste utilizador?")) {
                return;
            }

            try {
                const resposta = await fetch(`/admin/usuarios/${idUsuario}/bloquear`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                if (resposta.ok) {
                    alert("Estado do utilizador atualizado com sucesso!");
                    window.location.reload();
                } else {
                    alert("Erro ao alterar o estado do utilizador.");
                }
            } catch (erro) {
                console.error("Erro na requisição:", erro);
            }
        });
    });

    // Ação de Redefinir Senha para Aleatória (Painel Admin)
    const botoesRedefinir = document.querySelectorAll(".btn-redefinir-senha");
    botoesRedefinir.forEach((botao) => {
        botao.addEventListener("click", async () => {
            const idUsuario = botao.getAttribute("data-id");
            if (!confirm("Deseja redefinir a palavra-passe deste utilizador para uma senha aleatória?")) {
                return;
            }

            try {
                const resposta = await fetch(`/admin/usuarios/${idUsuario}/redefinir-senha`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                const dados = await resposta.json();
                if (resposta.ok) {
                    alert(`Nova palavra-passe gerada com sucesso: ${dados.nova_senha}`);
                } else {
                    alert("Erro ao redefinir a palavra-passe.");
                }
            } catch (erro) {
                console.error("Erro na requisição:", erro);
            }
        });
    });
});