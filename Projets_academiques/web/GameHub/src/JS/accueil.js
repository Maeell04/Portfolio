document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const nom = document.getElementById("nom").value;
        const commentaire = document.getElementById("commentaire").value;
  
        if (nom && commentaire) {
          alert(`Merci ${nom} pour votre avis !`);
          form.reset();
        } else {
          alert("Veuillez remplir tous les champs.");
        }
      });
    }
  
    const loginBtn = document.querySelector(".login-btn");
    if (loginBtn) {
      loginBtn.addEventListener("click", () => {
        alert("Redirection vers la page de connexion...");
        window.location.href = "login.html"; 
      });
    }
  });
  