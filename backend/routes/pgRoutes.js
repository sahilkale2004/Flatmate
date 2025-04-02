const express = require("express");
const router = express.Router();
const db = require("../config/db");

// Endpoint to get PG recommendations based on cluster
router.get("/recommend-pg/:pgId", async (req, res) => {
    const pgId = parseInt(req.params.pgId, 10);

    if (isNaN(pgId)) {
        return res.status(400).json({ message: "Invalid PG ID" });
    }

    try {
        const rows = await db.query("SELECT cluster FROM PG_Details WHERE pg_id = ?", [pgId]);

        if (!rows || rows.length === 0) {
            return res.status(404).json({ message: "No PG found with the specified ID" });
        }

        const cluster = rows[0].cluster;

        if (cluster === undefined || cluster === null) {
            return res.status(500).json({ message: "Cluster data is missing for this PG" });
        }

        const recommendations = await db.query("SELECT * FROM PG_Details WHERE cluster = ?", [cluster]);

        res.json({ recommendations });
    } catch (error) {
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;