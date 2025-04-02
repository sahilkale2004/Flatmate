const express = require("express");
const router = express.Router();
const db = require("../config/db");

// Endpoint to get roommate recommendations based on cluster
router.get("/recommend-roommates/:studentId", async (req, res) => {
    const { studentId } = req.params;

    try {
        // Get the cluster of the given student
        const student = await db.query("SELECT cluster FROM Student_Preferences WHERE student_id = ?", [studentId]);

        if (!student || student.length === 0) {
            return res.status(404).json({ message: "Student not found" });
        }

        const cluster = student[0].cluster;

        if (cluster === undefined || cluster === null) {
            return res.status(500).json({ message: "Cluster data is missing for this student" });
        }

        // Get all students in the same cluster, excluding the input student
        const recommendations = await db.query(
            "SELECT * FROM Student_Preferences WHERE cluster = ? AND student_id != ?",
            [cluster, studentId]
        );

        res.json({ recommendations });
    } catch (error) {
        console.error("Error details:", error);
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;