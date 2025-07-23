const mariadb = require("mariadb");

const pool = mariadb.createPool({
  host: "localhost",
  user: "root",
  password: "toor",
  database: "ecommerce_db",
});

module.exports = pool;
