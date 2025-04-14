require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const { Pool } = require("pg");

const app = express();
app.set("trust proxy", 1);

// CORS deve vir logo no topo
const allowedOrigins = ["http://localhost:5173", "https://gravta.com"];
app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        return callback(null, true);
      } else {
        return callback(
          new Error("The CORS policy does not allow this origin."),
          false
        );
      }
    },
    methods: ["GET", "POST", "OPTIONS"],
    credentials: true,
  })
);

// Responde às preflight requests
app.options("*", cors());

// Segurança e parseamento
app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Limite de requisições
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many requests from this IP, please try again later.",
});
app.use(limiter);

// Banco de dados
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// POST /contact
app.post("/contact", async (req, res) => {
  const { fullName, companyName, jobTitle, workEmail } = req.body;

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

// GET /
app.get("/", (req, res) => {
  res.send("Express backend with PostgreSQL is running!");
});

// Start server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
