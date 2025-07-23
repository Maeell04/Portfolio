document.addEventListener("DOMContentLoaded", () => {
    fetch("../api/get_jeux.php")
        .then(res => res.json())
        .then(jeux => {
            const container = document.getElementById("jeux-container");

            jeux.forEach(jeu => {
                const card = document.createElement("div");
                card.className = "jeu-card";

                card.innerHTML = `
                    <img src="${jeu.thumbnail}" alt="${jeu.nom}" class="jeu-image">
                    <h3>${jeu.nom}</h3>
                    <p>${jeu.description}</p>
                    <p><strong>Durée :</strong> ${jeu.duree} min</p>
                    <p><strong>Âge :</strong> ${jeu.min_age}+ ans</p>
                    <p><strong>Joueurs :</strong> ${jeu.min_joueurs} à ${jeu.max_joueurs}</p>
                `;

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Erreur lors du chargement des jeux :", err);
        });
});

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (!toast) return;
  
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove("hidden");
  
    setTimeout(() => toast.classList.add("hidden"), 3000);
  }
  