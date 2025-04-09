const { createPool } = require('mysql');

const pool = createPool({
  host: process.env.host,
  user: process.env.user,
  password: process.env.password,
  database: process.env.database,
  connectionLimit: 10
});

module.exports = pool;
