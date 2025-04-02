const express = require("express");
const router = express.Router();
const db = require("../config/db");

// Endpoint to update PG availability
router.post("/update-vacancy", async (req, res) => {
    const { pgId, status } = req.body;

    try {
        await db.query("UPDATE PG_Vacancy SET status = ? WHERE pg_id = ?", [status, pgId]);
        res.json({ message: "Vacancy status updated successfully" });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Server error" });
    }
});

// Endpoint to get vacancy alerts for students
router.get("/vacancy-alerts/:studentId", async (req, res) => {
    const { studentId } = req.params;

    try {
        const [student] = await db.query("SELECT preferred_location FROM Student_Preferences WHERE student_id = ?", [studentId]);

        if (!student.length) {
            return res.status(404).json({ message: "Student not found" });
        }

        const preferredLocation = student[0].preferred_location;

        // Fetch available PGs in the student's preferred location
        const vacancies = await db.query(`
            SELECT PG_Details.pg_id, PG_Details.name, PG_Details.location, PG_Vacancy.status 
            FROM PG_Details 
            JOIN PG_Vacancy ON PG_Details.pg_id = PG_Vacancy.pg_id 
            WHERE PG_Details.location = ? AND PG_Vacancy.status = 'Available'
        `, [preferredLocation]);

        res.json({ vacancies });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
