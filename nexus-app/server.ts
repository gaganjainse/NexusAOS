import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json({ limit: "10mb" }));

const PORT = 3000;

// Initialize Google GenAI client lazily or when GEMINI_API_KEY is present
let aiClient: GoogleGenAI | null = null;
function getGenAIClient(): GoogleGenAI | null {
  if (!aiClient && process.env.GEMINI_API_KEY) {
    aiClient = new GoogleGenAI({
      apiKey: process.env.GEMINI_API_KEY,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
  }
  return aiClient;
}

// In-memory / persisted state simulation
let vitalsData = {
  energy: 78,
  ischemia: 79.1, // Disk C usage %
  hypoxia: 0,    // CPU distress %
  fever: 37.2,   // Temperature °C
  vibe: 0.34,    // Endocrine positive
  status: "Homeostatic",
  lastTick: new Date().toISOString(),
};

let directivesList = [
  {
    id: "DIR-101",
    text: "Design and implement the Sesha App dual-interface specification",
    status: "Completed",
    timestamp: "10 minutes ago",
    priority: "High",
    subtasks: [
      { text: "Architect L1-L4 Sovereign Terminal layout", done: true },
      { text: "Implement Pet companion dynamic states & animations", done: true },
      { text: "Build System Monitor dashboard with Host Vitals", done: true },
      { text: "Integrate Sesha Core LLM workspace view", done: true },
    ],
    agentBids: ["Orchestrator-01 (100% match)", "Immune-03 (Security check)"],
    outcome: "Sesha App initialized successfully across Sovereign Terminal & Core.",
  },
  {
    id: "DIR-102",
    text: "/patrol Run immune check and verify disk C space",
    status: "Completed",
    timestamp: "4 minutes ago",
    priority: "Medium",
    subtasks: [
      { text: "Scan file tree for memory leaks", done: true },
      { text: "Check Disk C storage threshold (79.1%)", done: true },
    ],
    agentBids: ["Guardian-AOS"],
    outcome: "Disk C space within 80% tolerance threshold. System homeostatic.",
  },
];

// API Routes
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", app: "Sesha App AOS" });
});

app.get("/api/Sesha/vitals", (_req, res) => {
  // Add minor variance to metrics to simulate a living host
  const cpuUsage = Math.floor(15 + Math.random() * 45);
  const memUsage = (8.0 + Math.random() * 0.8).toFixed(1);
  res.json({
    ...vitalsData,
    cpuUsage,
    memUsage: `${memUsage}/16 GB`,
    diskC: vitalsData.ischemia,
    diskD: 34.2,
    netDown: (0.8 + Math.random() * 0.8).toFixed(1) + " MB/s",
    netUp: Math.floor(200 + Math.random() * 200) + " KB/s",
    lastUpdate: new Date().toLocaleTimeString(),
  });
});

app.post("/api/Sesha/action", (req, res) => {
  const { action } = req.body;
  if (action === "conservation") {
    vitalsData.status = "Conservation";
    vitalsData.energy = Math.min(100, vitalsData.energy + 10);
    return res.json({ success: true, message: "Triggered Conservation Mode. Energy conserving.", vitals: vitalsData });
  } else if (action === "immune") {
    vitalsData.fever = 36.6;
    vitalsData.hypoxia = 0;
    return res.json({ success: true, message: "Immune Patrol completed. All systems cleared.", vitals: vitalsData });
  } else if (action === "evolve") {
    vitalsData.vibe = Number((vitalsData.vibe + 0.15).toFixed(2));
    return res.json({ success: true, message: "Evolving skills... Hot-loaded optimization kernel v2.1.", vitals: vitalsData });
  }
  res.json({ success: true, message: `Executed action: ${action}` });
});

app.post("/api/Sesha/chat", async (req, res) => {
  try {
    const { message, contextFile, history } = req.body;
    const ai = getGenAIClient();

    if (!ai) {
      // Fallback AI simulation if GEMINI_API_KEY is not provided
      const responseText = `[Sesha Core System Response]\nI have received your query regarding "${message}".\n\nActive Context: ${contextFile || "main.py"}\n\nAll Vitals are currently Homeostatic (Energy: ${vitalsData.energy}%, Vibe: +${vitalsData.vibe}). I can assist with code editing, system diagnostics, executing directives, or managing database/git operations.`;
      return res.json({ text: responseText, status: "simulated" });
    }

    const systemInstruction = `You are Sesha (Sesha-α), an advanced AI Operating System companion and core intelligence for SeshaAOI.
You operate across the Sovereign Terminal IDE and Sesha Core LLM Workspace.
Keep your answers direct, technical, sharp, and helpful. Use markdown formatting and code blocks where relevant.
Current Host Vitals: Energy ${vitalsData.energy}%, Disk C ${vitalsData.ischemia}%, Vibe +${vitalsData.vibe}.`;

    const chatMessages = (history || []).map((h: any) => `${h.role === "user" ? "User" : "Sesha"}: ${h.text}`).join("\n");
    const fullPrompt = `${chatMessages}\nContext file: ${contextFile || "None"}\nUser: ${message}\nSesha:`;

    const response = await ai.models.generateContent({
      model: "gemini-3.6-flash",
      contents: fullPrompt,
      config: {
        systemInstruction,
        temperature: 0.7,
      },
    });

    res.json({ text: response.text || "Sesha generated response.", status: "live" });
  } catch (err: any) {
    console.error("Error in /api/Sesha/chat:", err);
    res.status(500).json({ error: err.message || "Failed to generate AI response" });
  }
});

app.post("/api/Sesha/directive", async (req, res) => {
  try {
    const { directiveText } = req.body;
    const dirId = `DIR-${103 + directivesList.length}`;
    
    let outcome = "Directive dispatched to Sesha Core orchestrator.";
    let subtasks = [
      { text: "Parse directive semantics and tool constraints", done: true },
      { text: "Dispatch agent sub-tasks", done: true },
      { text: "Execute code/tool actions", done: true },
    ];

    if (directiveText.startsWith("/")) {
      const parts = directiveText.split(" ");
      const cmd = parts[0].toLowerCase();
      if (cmd === "/vitals") {
        outcome = `Vitals Summary: Energy ${vitalsData.energy}%, Ischemia ${vitalsData.ischemia}%, Status ${vitalsData.status}`;
      } else if (cmd === "/patrol") {
        vitalsData.fever = 36.6;
        outcome = "Immune patrol finished. No anomalies detected in AOS runtime services.";
      } else if (cmd === "/evolve") {
        vitalsData.vibe += 0.1;
        outcome = "Mutation proposal generated and hot-loaded into active instinct stack.";
      } else if (cmd === "/edit" || cmd === "/explain") {
        outcome = `AI Command ${cmd} processed for context selection.`;
      }
    } else {
      const ai = getGenAIClient();
      if (ai) {
        try {
          const resp = await ai.models.generateContent({
            model: "gemini-3.6-flash",
            contents: `The user issued a Sovereign directive: "${directiveText}". Break this directive down into 3 short subtasks and 1 summary outcome in JSON format: {"subtasks": ["subtask1", "subtask2", "subtask3"], "outcome": "summary statement"}`,
            config: {
              responseMimeType: "application/json",
            },
          });
          const parsed = JSON.parse(resp.text || "{}");
          if (parsed.subtasks) {
            subtasks = parsed.subtasks.map((st: string) => ({ text: st, done: true }));
          }
          if (parsed.outcome) outcome = parsed.outcome;
        } catch (e) {
          console.warn("Gemini directive breakdown fallback:", e);
        }
      }
    }

    const newDirective = {
      id: dirId,
      text: directiveText,
      status: "Completed",
      timestamp: "Just now",
      priority: directiveText.startsWith("/") ? "High" : "Medium",
      subtasks,
      agentBids: ["Orchestrator-01", "Motor-AOS"],
      outcome,
    };

    directivesList.unshift(newDirective);
    res.json({ directive: newDirective, vitals: vitalsData });
  } catch (err: any) {
    res.status(500).json({ error: err.message || "Directive execution failed" });
  }
});

// Serve frontend in dev or prod
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (_req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`[Sesha Server] Running on http://localhost:${PORT}`);
  });
}

startServer();

