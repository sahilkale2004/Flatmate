const express = require("express");
const app = express();
const pgRoutes = require("./routes/pgRoutes");
const studentRoutes = require("./routes/studentRoutes");
const vacancyRoutes = require("./routes/vacancyRoutes");

// Middleware to parse JSON
app.use(express.json());

// Use all the routes for the '/pg'; '/student' & /update-vacancy path
app.use("/pg", pgRoutes);
app.use("/student", studentRoutes);
app.use("/api/vacancy", vacancyRoutes);

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});