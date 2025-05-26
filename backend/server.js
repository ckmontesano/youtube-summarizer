const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, "../frontend/dist")));

// Video summarization endpoint
app.post("/api/summarize", async (req, res) => {
  const { videoUrl } = req.body;

  if (!videoUrl) {
    return res.status(400).json({ error: "Video URL is required" });
  }

  try {
    // Get the path to the Python script and virtual environment
    const scriptPath = path.join(__dirname, "summarize_video.py");
    const pythonPath = path.join(__dirname, "venv/bin/python3");

    // Spawn Python process
    const pythonProcess = spawn(pythonPath, [scriptPath, videoUrl]);

    let summary = "";
    let error = "";

    // Collect data from Python script
    pythonProcess.stdout.on("data", (data) => {
      summary += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      error += data.toString();
    });

    // Handle process completion
    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        console.error("Python process error:", error);
        return res.status(500).json({
          error:
            "Failed to generate summary. Please check the video URL and try again.",
        });
      }

      if (!summary.trim()) {
        return res.status(500).json({
          error: "No summary was generated. Please try again.",
        });
      }

      // Parse the title and summary from the Python script output
      const titleMatch = summary.match(/=== (.*?) ===/);
      const title = titleMatch ? titleMatch[1] : "Untitled Video";
      const summaryText = summary.replace(/=== .*? ===\n/, "").trim();

      res.json({
        title: title,
        summary: summaryText,
      });
    });
  } catch (err) {
    console.error("Server error:", err);
    res.status(500).json({
      error: "An error occurred while processing your request.",
    });
  }
});

// Serve the frontend for any other routes
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/dist/index.html"));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
