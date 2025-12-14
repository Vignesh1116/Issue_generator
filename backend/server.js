import express from "express";
import axios from "axios";
import cors from "cors";
import dotenv from "dotenv";

import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());
console.log("Current directory:", __dirname);
console.log("Frontend path:", path.join(__dirname, "../frontend"));
console.log("Index path:", path.join(__dirname, "../frontend/index.html"));

app.use(express.static(path.join(__dirname, "../frontend")));

app.get("/", (req, res) => {
    const indexPath = path.join(__dirname, "../frontend/index.html");
    res.sendFile(indexPath, (err) => {
        if (err) {
            console.error("Error serving index.html:", err);
            res.status(500).send("Error serving index.html: " + err.message);
        }
    });
});

app.post("/create-issue", async (req, res) => {
    const { issueText, pageUrl } = req.body;

    if (!issueText) {
        return res.status(400).json({ error: "Issue text required" });
    }

    try {
        const owner = process.env.GITHUB_OWNER;
        const repo = process.env.GITHUB_REPO;

        if (!owner || !repo) {
            throw new Error("GitHub configuration missing in .env");
        }

        const url = `https://api.github.com/repos/${owner}/${repo}/issues`;

        const response = await axios.post(
            url,
            {
                title: "Issue from Quiz App",
                body: `${issueText}\n\nPage URL: ${pageUrl}`
            },
            {
                headers: {
                    Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
                    Accept: "application/vnd.github+json"
                }
            }
        );

        res.json({
            success: true,
            issueUrl: response.data.html_url
        });
    } catch (error) {
        res.status(500).json({
            error: "Failed to create issue",
            details: error.response?.data || error.message
        });
    }
});

app.listen(5001, () => {
    console.log("Server running on http://localhost:5001");
});