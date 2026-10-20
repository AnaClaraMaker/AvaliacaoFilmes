document.addEventListener("DOMContentLoaded", () => {
    // Dispara a sincronização de filmes em cartaz via API TMDB (Admin)
    const btnSincronizarTMDB = document.querySelector("#btnSincronizarTMDB");
    if (btnSincronizarTMDB) {
        btnSincronizarTMDB.addEventListener("click", async () => {
            btnSincronizarTMDB.disabled = true;
            btnSincronizarTMDB.innerText = "A atualizar catálogo...";

            try {
                const resposta = await fetch("/admin/filmes/sincronizar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                const resultado = await resposta.json();
                if (resposta.ok) {
                    alert(`Catálogo atualizado! ${resultado.adicionados || 0} novos filmes inseridos.`);
                    window.location.reload();
                } else {
                    alert("Erro ao sincronizar filmes com o TMDB.");
                }
            } catch (erro) {
                console.error("Erro ao sincronizar:", erro);
                alert("Falha na ligação com o servidor.");
            } finally {
                btnSincronizarTMDB.disabled = false;
                btnSincronizarTMDB.innerText = "Atualizar Filmes do TMDB";
            }
        });
    }
});