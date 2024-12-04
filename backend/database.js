const { createPool } = require('mysql');

const pool = createPool({
  host: "localhost",
  user: "root",
  password: "123456",
  database: "FLATMATES",
  connectionLimit: 10
});

module.exports = pool;
