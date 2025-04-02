const mysql = require("mysql");

const pool = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "123456",
  database: "KMEANS",
  connectionLimit: 10,
});

// Promisify the query method
pool.query = function (sql, params) {
  return new Promise((resolve, reject) => {
    this.getConnection((err, connection) => {
      if (err) {
        return reject(err);
      }
      connection.query(sql, params, (error, results) => {
        connection.release();
        if (error) {
          return reject(error);
        }
        resolve(results);
      });
    });
  });
};

module.exports = pool;