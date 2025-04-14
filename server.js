// server.js
require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const { Pool } = require("pg");

const app = express();
// Setup for CORS and security headers
app.set("trust proxy", 1);
// Setup security headers with Helmet
app.use(helmet());

// Middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure CORS - adjust origin to your frontend domain
const allowedOrigins = [
  "http://localhost:5173",
  "https://gravta.com",
  "https://adneura-backend-uchgev-f09b61-194-195-86-246.traefik.me",
];

app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin) return callback(null, true);
      if (allowedOrigins.indexOf(origin) === -1) {
        const msg =
          "The CORS policy for this site does not allow access from the specified Origin.";
        return callback(new Error(msg), false);
      }
      return callback(null, true);
    },
  })
);

// Rate limiter to prevent abuse
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Maximum 100 requests per IP per 15 minutes
  message: "Too many requests from this IP, please try again later.",
});
app.use(limiter);

// Create a PostgreSQL connection pool using the connection string from .env
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// // Function to create the "contacts" table if it doesn't exist
// async function createContactsTable() {
//   const createTableQuery = `
//     CREATE TABLE IF NOT EXISTS contacts (
//       id SERIAL PRIMARY KEY,
//       fullName TEXT NOT NULL,
//       companyName TEXT,
//       jobTitle TEXT,
//       workEmail TEXT NOT NULL,
//       createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
//     );
//   `;
//   try {
//     await pool.query(createTableQuery);
//     console.log("Contacts table is ready!");
//   } catch (error) {
//     console.error("Error creating contacts table:", error);
//   }
// }

// // Call the function to create the table on server startup
// createContactsTable();

// POST endpoint to handle contact form submissions
app.post("/contact", async (req, res) => {
  const { fullName, companyName, jobTitle, workEmail } = req.body;

  // Basic validation for required fields
  if (!fullName || !workEmail) {
    return res
      .status(400)
      .json({ message: "Full name and work email are required." });
  }

  try {
    const insertQuery = `
      INSERT INTO contacts (fullName, companyName, jobTitle, workEmail)
      VALUES ($1, $2, $3, $4)
      RETURNING id, createdAt;
    `;
    const result = await pool.query(insertQuery, [
      fullName,
      companyName,
      jobTitle,
      workEmail,
    ]);

    return res.status(201).json({
      message: "Contact saved successfully!",
      contactId: result.rows[0].id,
      createdAt: result.rows[0].createdat,
    });
  } catch (error) {
    console.error("Error saving contact:", error);
    return res.status(500).json({ message: "Internal server error." });
  }
});

// Root endpoint for status check
app.get("/", (req, res) => {
  res.send("Express backend with PostgreSQL is running!");
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
