document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const toast = document.getElementById("toast");

  function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 3000);
  }

  loginForm?.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    fetch("../PHP/login.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          showToast("Connexion réussie !", "success");
          setTimeout(() => {
            window.location.href = data.role === "admin"
              ? "admin.html"
              : "accueil.html";
          }, 1000);
        } else {
          showToast(data.error || "Erreur de connexion", "error");
        }
      })
      .catch(() => showToast("Erreur serveur", "error"));
  });

  registerForm?.addEventListener("submit", (e) => {
    e.preventDefault();

    const nom = document.getElementById("register-nom").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const confirm = document.getElementById("register-confirm").value;

    if (password !== confirm) {
      showToast("Les mots de passe ne correspondent pas", "error");
      return;
    }

    fetch("../PHP/register.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nom, email, password })
    })
      .then(res => res.json())
      .then(data => {
        showToast(data.message || data.error, data.success ? "success" : "error");
        if (data.success) registerForm.reset();
      })
      .catch(() => showToast("Erreur lors de l'inscription", "error"));
  });
});
