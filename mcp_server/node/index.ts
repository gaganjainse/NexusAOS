import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BASE_DIR = path.resolve(__dirname, "../../");

const server = new Server(
  {
    name: "SeshaAOS",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// --- Resources ---
const RESOURCES = {
  "Sesha://core/handbook": "archives/core/foundation/corporate_os_handbook.md",
  "Sesha://core/constitution": "archives/core/foundation/Sesha_corporate_constitution.md",
  "Sesha://core/rules": "archives/core/rules/operating_rules.md",
  "Sesha://core/matrix": "archives/core/foundation/job_matrix.md",
  "Sesha://core/logic": "core/exports/Sesha_logic_export.json",
  "Sesha://core/index": "core/exports/Sesha_file_index.json",
};

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: Object.entries(RESOURCES).map(([uri, filePath]) => ({
    uri,
    name: path.basename(filePath),
    mimeType: filePath.endsWith(".json") ? "application/json" : "text/markdown",
  })),
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const filePath = RESOURCES[request.params.uri as keyof typeof RESOURCES];
  if (!filePath) throw new Error("Resource not found");

  const fullPath = path.join(BASE_DIR, filePath);
  const content = fs.readFileSync(fullPath, "utf-8");

  return {
    contents: [{
      uri: request.params.uri,
      mimeType: filePath.endsWith(".json") ? "application/json" : "text/markdown",
      text: content,
    }],
  };
});

// --- Tools ---
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "boot_Sesha",
      description: "Initialize and specialize the OS (Bridges to Python Engine).",
      inputSchema: {
        type: "object",
        properties: {
          domain: { type: "string" },
          platform: { "type": "string" },
        },
        required: ["domain", "platform"],
      },
    },
    {
      name: "search_Sesha",
      description: "Performs a global search across all SeshaAOS files using the index.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search term for roles, branches, or purpose." },
        },
        required: ["query"],
      },
    },
    {
      name: "refresh_index",
      description: "Triggers the Python-based full file indexer.",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "run_python_tool",
      description: "Executes a specialized Python-based role tool.",
      inputSchema: {
        type: "object",
        properties: {
          tool_name: { type: "string", description: "Name of the script in mcp_server/python/" },
          args: { type: "array", items: { type: "string" } },
        },
        required: ["tool_name"],
      },
    },
    {
      name: "stream_pulse",
      description: "Requests a high-density Agentic Logic Pulse (.nxp) for a specific branch or role ID.",
      inputSchema: {
        type: "object",
        properties: {
          target: { type: "string", description: "Branch name (e.g., 'ai') or specific Role ID (e.g., 'CAO')." },
        },
        required: ["target"],
      },
    },
    {
      name: "reforge_pulses",
      description: "Triggers a full rebuild of the Sesha Logic Pulse (.nxp) library.",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "query_logic_graph",
      description: "Performs a SQL query against the Sesha Logic Graph (Sesha_aos.db).",
      inputSchema: {
        type: "object",
        properties: {
          sql: { type: "string", description: "The SQL SELECT statement (e.g., 'SELECT * FROM artifacts WHERE branch=\"AI\"')" },
        },
        required: ["sql"],
      },
    },
    {
      name: "sync_markdown_views",
      description: "Re-generates human-readable .md files from the master YAML logic.",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "create_checkpoint",
      description: "Saves the current mission status and next intended step to the Operational Ledger.",
      inputSchema: {
        type: "object",
        properties: {
          status: { type: "string", description: "Description of the work completed so far." },
          next_step: { type: "string", description: "What the Firmware intends to do next." },
        },
        required: ["status", "next_step"],
      },
    },
    {
      name: "forge_tool",
      description: "Constructs a new native Python tool to bridge an Agentic capability gap.",
      inputSchema: {
        type: "object",
        properties: {
          tool_name: { type: "string", description: "Name of the new tool (e.g., 'image_optimizer')." },
          code: { type: "string", description: "The full Python source code for the tool." },
        },
        required: ["tool_name", "code"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "forge_tool") {
    const { tool_name, code } = args as { tool_name: string; code: string };
    const toolDir = path.join(BASE_DIR, "mcp_server/python/foundry");
    if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });

    const filePath = path.join(toolDir, `${tool_name}.py`);
    fs.writeFileSync(filePath, code);

    return {
      content: [{ type: "text", text: `Tool [${tool_name}] forged successfully in the Foundry. It is now available for execution via run_python_tool.` }],
    };
  }

  if (name === "create_checkpoint") {
    const { status, next_step } = args as { status: string; next_step: string };
    const ledgerPath = path.join(BASE_DIR, "core/monitoring/Sesha_operational_ledger.md");
    const timestamp = new Date().toISOString();
    const checkpointEntry = `\n- **[CHECKPOINT: ${timestamp}]:** ${status}\n- **[PENDING: NEXT_STEP]:** ${next_step}\n`;

    // Append to the file (simplified for this bridge)
    fs.appendFileSync(ledgerPath, checkpointEntry);
    return {
      content: [{ type: "text", text: `Checkpoint created at ${timestamp}. Session continuity secured.` }],
    };
  }

  if (name === "search_Sesha") {
    const { query } = args as { query: string };
    const indexPath = path.join(BASE_DIR, "core/exports/Sesha_file_index.json");
    const index = JSON.parse(fs.readFileSync(indexPath, "utf-8"));
    const results = index.filter((f: any) =>
      f.title.toLowerCase().includes(query.toLowerCase()) ||
      f.branch.toLowerCase().includes(query.toLowerCase()) ||
      f.purpose.toLowerCase().includes(query.toLowerCase()) ||
      f.keywords.some((k: string) => k.includes(query.toLowerCase()))
    ).slice(0, 10);

    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }

  if (name === "stream_pulse") {
    const { target } = args as { target: string };
    const pulseDir = path.join(BASE_DIR, "core/pulses");
    const indexPath = path.join(pulseDir, "master.nxi");

    // 1. Check if target is a specific Role ID in the index
    const index = JSON.parse(fs.readFileSync(indexPath, "utf-8"));
    if (index[target]) {
      const entry = index[target];
      const pulseFile = path.join(pulseDir, entry.file);
      const content = fs.readFileSync(pulseFile, "utf-8");
      // Find the specific pulse in the file
      const pulse = content.split("---Pulse-Break---").find(p => p.includes(`[[ID]] ${target}`));
      return { content: [{ type: "text", text: pulse || "Pulse ID not found in file." }] };
    }

    // 2. Check if target is a branch name (.nxp file)
    const branchFile = path.join(pulseDir, `${target.toLowerCase()}.nxp`);
    if (fs.existsSync(branchFile)) {
      const content = fs.readFileSync(branchFile, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    return { content: [{ type: "text", text: `Target [${target}] not found in Pulse Index or Branch library.` }], isError: true };
  }

  if (name === "reforge_pulses") {
    try {
      const forgeScript = path.join(BASE_DIR, "mcp_server/python/nxp_forge.py");
      const indexScript = path.join(BASE_DIR, "mcp_server/python/nxp_indexer.py");
      execSync(`python "${forgeScript}"`);
      execSync(`python "${indexScript}"`);
      return { content: [{ type: "text", text: "Sesha Logic Pulse (.nxp) library and index rebuilt successfully." }] };
    } catch (error: any) {
      return { content: [{ type: "text", text: error.message }], isError: true };
    }
  }

  if (name === "refresh_index") {
    const pythonScript = path.join(BASE_DIR, "mcp_server", "python", "Sesha_indexer.py");
    try {
      const output = execSync(`python "${pythonScript}"`, { encoding: "utf-8" });
      return { content: [{ type: "text", text: output }] };
    } catch (error: any) {
      return { content: [{ type: "text", text: error.message }], isError: true };
    }
  }

  if (name === "query_logic_graph") {
    const { sql } = args as { sql: string };
    const pythonScript = path.join(BASE_DIR, "mcp_server", "python", "logic_query.py");
    try {
      const output = execSync(`python "${pythonScript}" "${sql.replace(/"/g, '\\"')}"`, { encoding: "utf-8" });
      return { content: [{ type: "text", text: output }] };
    } catch (error: any) {
      return { content: [{ type: "text", text: error.message }], isError: true };
    }
  }

  if (name === "sync_markdown_views") {
    const pythonScript = path.join(BASE_DIR, "mcp_server", "python", "nlg_renderer.py");
    try {
      const output = execSync(`python "${pythonScript}"`, { encoding: "utf-8" });
      return { content: [{ type: "text", text: output }] };
    } catch (error: any) {
      return { content: [{ type: "text", text: error.message }], isError: true };
    }
  }

  if (name === "run_python_tool") {
    const { tool_name, args: toolArgs } = args as { tool_name: string, args?: string[] };

    // Check main python directory first, then foundry
    let pythonScript = path.join(BASE_DIR, "mcp_server", "python", `${tool_name}.py`);
    if (!fs.existsSync(pythonScript)) {
        pythonScript = path.join(BASE_DIR, "mcp_server", "python", "foundry", `${tool_name}.py`);
    }

    if (!fs.existsSync(pythonScript)) {
        return {
            content: [{ type: "text", text: `Error: Tool [${tool_name}] not found in python or foundry directories.` }],
            isError: true,
        };
    }

    try {
      const output = execSync(`python "${pythonScript}" ${(toolArgs || []).join(" ")}`, { encoding: "utf-8" });
      return {
        content: [{ type: "text", text: output }],
      };
    } catch (error: any) {
      return {
        content: [{ type: "text", text: `Python Execution Error: ${error.message}` }],
        isError: true,
      };
    }
  }

  throw new Error("Tool not found");
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);

