document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.querySelector(".login-btn");
    if (loginBtn) {
      loginBtn.addEventListener("click", () => {
        alert("Redirection vers la page de connexion...");
      });
    }
  
    const searchInput = document.querySelector('input[type="text"]');
    const cards = document.querySelectorAll(".card");
  
    if (searchInput && cards.length > 0) {
      searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
  
        cards.forEach(card => {
          const title = card.querySelector("strong").textContent.toLowerCase();
          card.style.display = title.includes(query) ? "block" : "none";
        });
      });
    }
  });
  