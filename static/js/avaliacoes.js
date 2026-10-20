document.addEventListener("DOMContentLoaded", () => {
    // Sinalizar comentário como potencialmente ofensivo (Utilizador Comum)
    const botoesSinalizar = document.querySelectorAll(".btn-sinalizar-ofensivo");
    botoesSinalizar.forEach((botao) => {
        botao.addEventListener("click", async () => {
            const idAvaliacao = botao.getAttribute("data-id");

            if (!confirm("Deseja denunciar este comentário como potencialmente ofensivo?")) {
                return;
            }

            try {
                const resposta = await fetch(`/avaliacoes/${idAvaliacao}/sinalizar`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                if (resposta.ok) {
                    alert("Comentário sinalizado para moderação.");
                    botao.disabled = true;
                    botao.innerText = "Sinalizado";
                } else {
                    alert("Não foi possível sinalizar o comentário.");
                }
            } catch (erro) {
                console.error("Erro:", erro);
            }
        });
    });

    // Moderação de Comentários Ofensivos (Painel Admin: Confirmar ou Rejeitar)
    const botoesModerar = document.querySelectorAll(".btn-moderar-avaliacao");
    botoesModerar.forEach((botao) => {
        botao.addEventListener("click", async () => {
            const idAvaliacao = botao.getAttribute("data-id");
            const decisao = botao.getAttribute("data-decisao"); // 'S' para confirmar ofensivo, 'N' para rejeitar

            try {
                const resposta = await fetch(`/admin/avaliacoes/${idAvaliacao}/moderar`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ confirmacao: decisao })
                });

                if (resposta.ok) {
                    alert("Decisão de moderação registada com sucesso!");
                    window.location.reload();
                } else {
                    alert("Erro ao moderar avaliação.");
                }
            } catch (erro) {
                console.error("Erro na moderação:", erro);
            }
        });
    });
});