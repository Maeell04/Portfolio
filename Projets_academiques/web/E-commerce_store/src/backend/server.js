const express = require("express");
const bodyParser = require("body-parser");
const pool = require("./config/db"); // Importez la configuration de la base de données

const app = express();

app.use(bodyParser.json());

// Example route
app.get("/", (req, res) => {
  res.send("Backend is working!");
});

// Test API endpoint
app.get("/api/test", (req, res) => {
  res.json({ message: "API working!" });
});

// Test endpoint to check database connection
app.get("/api/test-db", async (req, res) => {
  try {
    const connection = await pool.getConnection(); // Récupère une connexion depuis le pool
    await connection.query("SELECT 1"); // Une requête simple pour tester la connexion
    connection.release(); // Libère la connexion
    res.status(200).json({ message: "Database connection is working!" });
  } catch (error) {
    console.error("Database connection error:", error);
    res.status(500).json({ message: "Database connection failed!", error });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
