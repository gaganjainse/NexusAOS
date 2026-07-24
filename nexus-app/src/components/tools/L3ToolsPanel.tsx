import React, { useState } from "react";
import {
  MCPTool,
  DBTable,
  GitCommit,
  ChatMessage,
} from "../../types/Sesha";
import {
  Wrench,
  Globe,
  Database,
  GitBranch,
  Play,
  Terminal,
  Search,
  Plus,
  Send,
  CheckCircle2,
  XCircle,
  Clock,
  Layers,
  ChevronDown,
  ChevronRight,
  Server,
  RefreshCw,
  X,
  Webhook,
  MessageSquare,
  GitCompare,
  FileText,
  Laptop,
  Tablet,
  Smartphone,
  ExternalLink,
  ChevronLeft,
  Sparkles,
  Bot,
  Square,
  Paperclip,
  Brain,
  Edit3,
  AlertCircle,
  FileCode,
  RotateCcw,
  AlertTriangle,
} from "lucide-react";

interface L3ToolsPanelProps {
  tools: MCPTool[];
  dbTables: DBTable[];
  gitCommits: GitCommit[];
  chatMessages?: ChatMessage[];
  onSendMessage?: (msg: string) => void;
  onExecuteTool: (toolId: string, params: Record<string, any>) => void;
  onClosePanel?: () => void;
  activeTab?: "tools" | "api" | "db" | "git" | "ci" | "browser" | "chat" | "diff" | "docs";
}

export const L3ToolsPanel: React.FC<L3ToolsPanelProps> = React.memo(({
  tools,
  dbTables,
  gitCommits,
  chatMessages = [],
  onSendMessage,
  onExecuteTool,
  onClosePanel,
  activeTab = "tools",
}) => {
  // Tool drawer state
  const [selectedTool, setSelectedTool] = useState<MCPTool>(tools[0]);
  const [toolParamValues, setToolParamValues] = useState<Record<string, string>>({});
  const [toolSearch, setToolSearch] = useState("");

  // API Playground state
  const [apiMethod, setApiMethod] = useState<"GET" | "POST" | "PUT" | "DELETE">("POST");
  const [apiUrl, setApiUrl] = useState("/api/Sesha/vitals");
  const [apiHeaders, setApiHeaders] = useState('{\n  "Content-Type": "application/json"\n}');
  const [apiBody, setApiBody] = useState('{\n  "action": "conservation"\n}');
  const [apiResponse, setApiResponse] = useState<string | null>(null);

  // DB Browser state
  const [selectedTable, setSelectedTable] = useState<DBTable>(dbTables[0]);
  const [sqlQuery, setSqlQuery] = useState(`SELECT * FROM ${dbTables[0]?.name || "Sesha_directives"} LIMIT 10;`);
  const [queryResult, setQueryResult] = useState<any[] | null>(null);

  // Inbuilt Browser State for Top Rightbar
  const [browserUrl, setBrowserUrl] = useState("http://localhost:3000/app");
  const [browserDevice, setBrowserDevice] = useState<"desktop" | "tablet" | "mobile">("desktop");
  const [chatInput, setChatInput] = useState("");

  const handleToolRun = (e: React.FormEvent) => {
    e.preventDefault();
    onExecuteTool(selectedTool.id, toolParamValues);
  };

  const handleApiSend = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      let options: RequestInit = { method: apiMethod };
      if (apiMethod !== "GET") {
        options.body = apiBody;
        options.headers = JSON.parse(apiHeaders || "{}");
      }
      const res = await fetch(apiUrl, options);
      const data = await res.json();
      setApiResponse(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setApiResponse(JSON.stringify({ error: err.message }, null, 2));
    }
  };

  const handleRunQuery = (e: React.FormEvent) => {
    e.preventDefault();
    setQueryResult(selectedTable.data);
  };

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    onSendMessage?.(chatInput.trim());
    setChatInput("");
  };

  return (
    <aside className="w-full h-full bg-[#120a06]/95 rounded-xl border-2 border-amber-800/60 flex flex-col select-none overflow-hidden font-mono text-xs shadow-2xl relative oil-lamp-glow shilpkari-concave ring-1 ring-amber-500/20 backdrop-blur-md">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-amber-800/60 bg-[#1f1712] px-3 py-2 text-xs font-mono shrink-0">
        <div className="flex items-center gap-2 font-bold text-amber-300 tracking-wider">
          {activeTab === "tools" && (
            <>
              <Wrench className="w-3.5 h-3.5 text-cyan-400" />
              <span>MCP TOOLS DRAWER</span>
            </>
          )}
          {activeTab === "api" && (
            <>
              <Webhook className="w-3.5 h-3.5 text-purple-400 animate-pulse" />
              <span>API CLIENT & INSPECTOR</span>
            </>
          )}
          {activeTab === "db" && (
            <>
              <Database className="w-3.5 h-3.5 text-amber-400" />
              <span>DATABASE MANAGER</span>
            </>
          )}
          {activeTab === "git" && (
            <>
              <GitBranch className="w-3.5 h-3.5 text-emerald-400" />
              <span>GIT GRAPH & REVISIONS</span>
            </>
          )}
          {activeTab === "ci" && (
            <>
              <Server className="w-3.5 h-3.5 text-sky-400" />
              <span>CI/CD BUILD PIPELINE</span>
            </>
          )}
          {activeTab === "browser" && (
            <>
              <Globe className="w-3.5 h-3.5 text-sky-400" />
              <span>INBUILT DEV BROWSER</span>
            </>
          )}
          {activeTab === "chat" && (
            <>
              <MessageSquare className="w-3.5 h-3.5 text-purple-400" />
              <span>Sesha AI CO-PILOT CHAT</span>
            </>
          )}
          {activeTab === "diff" && (
            <>
              <GitCompare className="w-3.5 h-3.5 text-amber-400" />
              <span>CODE REVISION & DIFF</span>
            </>
          )}
          {activeTab === "docs" && (
            <>
              <FileText className="w-3.5 h-3.5 text-emerald-400" />
              <span>SYSTEM DOCUMENTATION</span>
            </>
          )}
        </div>
        {onClosePanel && (
          <button
            onClick={onClosePanel}
            title="Hide Panel"
            className="p-0.5 hover:bg-zinc-800 rounded text-zinc-500 hover:text-zinc-200"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-3 font-mono text-xs">
        {/* TOP RIGHTBAR 1: INBUILT DEV BROWSER */}
        {activeTab === "browser" && (
          <div className="flex flex-col h-full gap-2">
            {/* Browser Control Toolbar */}
            <div className="flex items-center justify-between bg-zinc-900 border border-zinc-800 rounded-lg p-1.5 gap-2 shrink-0">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => {}}
                  title="Back"
                  className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-zinc-200 transition-colors"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => {}}
                  title="Forward"
                  className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-zinc-200 transition-colors"
                >
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => {
                    // Force reload iframe by re-evaluating URL
                    setBrowserUrl((prev) => (prev.endsWith("#") ? prev.slice(0, -1) : prev + "#"));
                  }}
                  title="Refresh Page"
                  className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-zinc-200 transition-colors"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* URL Address Bar */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                }}
                className="flex-1 flex items-center bg-zinc-950 border border-zinc-800 focus-within:border-cyan-500 rounded-md px-2.5 py-1 gap-1.5 text-xs text-zinc-200 shadow-inner"
              >
                <Globe className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                <input
                  type="text"
                  value={browserUrl}
                  onChange={(e) => setBrowserUrl(e.target.value)}
                  className="w-full bg-transparent focus:outline-none font-mono text-[11px]"
                  placeholder="https://localhost:3000..."
                />
                <span className="px-1.5 py-0.2 bg-emerald-950 text-emerald-400 border border-emerald-800/80 rounded text-[9px] font-bold">
                  200 OK
                </span>
              </form>

              {/* Device Mode Toggle & External Launch */}
              <div className="flex items-center gap-1 shrink-0">
                <button
                  onClick={() => setBrowserDevice("desktop")}
                  title="Desktop View (100%)"
                  className={`p-1.5 rounded-md transition-colors ${
                    browserDevice === "desktop"
                      ? "bg-cyan-950 text-cyan-300 border border-cyan-700/60"
                      : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800"
                  }`}
                >
                  <Laptop className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => setBrowserDevice("tablet")}
                  title="Tablet View (768px)"
                  className={`p-1.5 rounded-md transition-colors ${
                    browserDevice === "tablet"
                      ? "bg-cyan-950 text-cyan-300 border border-cyan-700/60"
                      : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800"
                  }`}
                >
                  <Tablet className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => setBrowserDevice("mobile")}
                  title="Mobile View (375px)"
                  className={`p-1.5 rounded-md transition-colors ${
                    browserDevice === "mobile"
                      ? "bg-cyan-950 text-cyan-300 border border-cyan-700/60"
                      : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800"
                  }`}
                >
                  <Smartphone className="w-3.5 h-3.5" />
                </button>
                <a
                  href={browserUrl}
                  target="_blank"
                  rel="noreferrer"
                  title="Open in external browser window"
                  className="p-1.5 text-zinc-400 hover:text-cyan-300 hover:bg-zinc-800 rounded-md transition-colors"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            {/* Inbuilt Live Web Page Viewport */}
            <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg p-2 flex flex-col items-center justify-center overflow-hidden relative shadow-inner min-h-[350px]">
              <div
                className={`transition-all duration-300 h-full flex flex-col ${
                  browserDevice === "mobile"
                    ? "w-[375px] max-w-full border-x-4 border-y-8 border-zinc-800 rounded-2xl shadow-2xl"
                    : browserDevice === "tablet"
                    ? "w-[720px] max-w-full border-4 border-zinc-800 rounded-xl shadow-2xl"
                    : "w-full"
                }`}
              >
                {/* Device Frame Header if simulated */}
                {browserDevice !== "desktop" && (
                  <div className="bg-zinc-900 px-3 py-1 text-[10px] text-zinc-400 flex items-center justify-between border-b border-zinc-800 rounded-t shrink-0">
                    <span className="font-mono">{browserDevice === "mobile" ? "iPhone 15 Pro Simulator" : "iPad Air Simulator"}</span>
                    <span className="text-emerald-400 font-bold">ONLINE</span>
                  </div>
                )}

                <iframe
                  src={browserUrl.startsWith("http") ? browserUrl : window.location.origin}
                  className="w-full flex-1 border-0 bg-white rounded-md"
                  title="Sesha Inbuilt Dev Browser Workspace"
                  sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
                />
              </div>

              <div className="absolute bottom-2 right-3 text-[9px] font-mono text-zinc-500 bg-zinc-900/90 px-2 py-0.5 rounded border border-zinc-800 pointer-events-none">
                Sesha Web Kernel v13.0 • HMR Live
              </div>
            </div>
          </div>
        )}

        {/* TOP RIGHTBAR 2: Sesha AI CHAT */}
        {activeTab === "chat" && (
          <div className="flex flex-col h-full gap-3">
            <div className="flex-1 overflow-y-auto space-y-3 pr-1">
              {chatMessages.length === 0 ? (
                <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl text-center text-zinc-400">
                  <Bot className="w-8 h-8 text-purple-400 mx-auto mb-2 animate-bounce" />
                  <p className="font-bold text-zinc-200">Sesha Sovereign Co-Pilot</p>
                  <p className="text-[11px] mt-1 text-zinc-500">Ask any code question or issue multi-file directives.</p>
                </div>
              ) : (
                chatMessages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`p-3 rounded-xl border text-xs leading-relaxed ${
                      msg.sender === "user"
                        ? "bg-cyan-950/60 border-cyan-800 text-cyan-200 ml-4"
                        : "bg-zinc-900 border-zinc-800 text-zinc-200 mr-4"
                    }`}
                  >
                    <div className="font-bold text-[10px] text-zinc-400 mb-1 flex justify-between">
                      <span>{msg.sender === "user" ? "You" : "Sesha Assistant"}</span>
                      <span>{msg.timestamp}</span>
                    </div>
                    <div>{msg.text}</div>
                  </div>
                ))
              )}
            </div>

            <form onSubmit={handleChatSubmit} className="flex gap-2 shrink-0">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask Sesha Assistant..."
                className="flex-1 bg-zinc-900 border border-zinc-800 focus:border-purple-500 rounded-lg px-3 py-2 text-xs text-zinc-200 focus:outline-none"
              />
              <button
                type="submit"
                className="px-3 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg flex items-center justify-center transition-colors"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </form>
          </div>
        )}

        {/* TOP RIGHTBAR 3: DIFF / REVIEW STREAM (JetBrains / Codex Style Agent Review) */}
        {activeTab === "diff" && (
          <div className="flex flex-col h-full gap-3 font-sans text-xs">
            {/* Top Workspace Tab Bar inside Card */}
            <div className="flex items-center justify-between border-b border-zinc-800 bg-zinc-925 pb-1 text-[11px]">
              <div className="flex items-center gap-1 overflow-x-auto">
                <div className="flex items-center gap-1 px-2 py-1 bg-zinc-850 text-zinc-200 border-t-2 border-purple-400 rounded-t font-medium">
                  <span className="truncate max-w-[130px]">User sends an initial...</span>
                  <X className="w-3 h-3 text-zinc-500 hover:text-zinc-300 cursor-pointer" />
                </div>
                <div className="flex items-center gap-1 px-2 py-1 bg-zinc-900 text-zinc-400 rounded-t hover:text-zinc-200">
                  <span className="truncate max-w-[120px]">Implement real-ti...</span>
                </div>
                <div className="flex items-center gap-1 px-2 py-1 bg-zinc-900 text-purple-400 rounded-t hover:text-purple-300 font-mono text-[10px]">
                  <span>NEURAL_13.0_SPEC.md</span>
                </div>
              </div>
              <div className="flex items-center gap-1 text-zinc-400">
                <button className="p-1 hover:bg-zinc-800 rounded"><Plus className="w-3.5 h-3.5" /></button>
                <button className="p-1 hover:bg-zinc-800 rounded"><MessageSquare className="w-3.5 h-3.5" /></button>
              </div>
            </div>

            {/* Agent Directive Title */}
            <div className="px-1 pt-1">
              <h2 className="font-semibold text-zinc-100 text-sm tracking-tight">
                User sends an initial greeting to Sesha.
              </h2>
            </div>

            {/* Steps & Execution Stream */}
            <div className="flex-1 overflow-y-auto space-y-2 pr-1 text-[11px] font-mono">
              {/* Step 1: Thought */}
              <div className="p-2 bg-zinc-900/80 border border-zinc-800/80 rounded-lg flex items-center gap-2 text-zinc-300">
                <Brain className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                <span className="font-semibold text-zinc-300">Thought</span>
              </div>

              {/* Step 2: PowerShell command */}
              <div className="p-2 bg-zinc-900/90 border border-zinc-800 rounded-lg flex items-center justify-between text-zinc-300">
                <div className="flex items-center gap-2">
                  <Terminal className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>Run terminal command <strong className="text-zinc-100 font-normal">powershell</strong></span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-4 h-4 rounded-full bg-rose-950 border border-rose-700 text-rose-400 text-[10px] font-bold flex items-center justify-center">!</span>
                  <ChevronDown className="w-3.5 h-3.5 text-zinc-500" />
                </div>
              </div>

              {/* Step 3: Cmd command */}
              <div className="p-2 bg-zinc-900/90 border border-zinc-800 rounded-lg flex items-center justify-between text-zinc-300">
                <div className="flex items-center gap-2">
                  <Terminal className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>Run terminal command <strong className="text-zinc-100 font-normal">cmd</strong></span>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-zinc-500" />
              </div>

              {/* Step 4: Thought */}
              <div className="p-2 bg-zinc-900/80 border border-zinc-800/80 rounded-lg flex items-center gap-2 text-zinc-300">
                <Brain className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                <span className="font-semibold text-zinc-300">Thought</span>
              </div>

              {/* Step 5: Read index.py */}
              <div className="p-2 bg-zinc-900/90 border border-zinc-800 rounded-lg flex items-center gap-2 text-zinc-300">
                <Search className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                <span>Read</span>
                <span className="px-1.5 py-0.5 bg-fuchsia-950 text-fuchsia-300 rounded border border-fuchsia-800/60 font-bold text-[10px] flex items-center gap-1">
                  <span className="w-2 h-2 rounded-sm bg-fuchsia-500" /> index.py
                </span>
              </div>

              {/* Step 6: Edited index.py */}
              <div className="p-2 bg-zinc-900/90 border border-zinc-800 rounded-lg flex items-center justify-between text-zinc-300">
                <div className="flex items-center gap-2">
                  <Edit3 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Edited</span>
                  <span className="px-1.5 py-0.5 bg-fuchsia-950 text-fuchsia-300 rounded border border-fuchsia-800/60 font-bold text-[10px] flex items-center gap-1">
                    <span className="w-2 h-2 rounded-sm bg-fuchsia-500" /> index.py
                  </span>
                </div>
                <div className="flex items-center gap-1 font-bold">
                  <span className="text-rose-400">-59</span>
                  <span className="text-emerald-400">+57</span>
                </div>
              </div>

              {/* Step 7: File not found */}
              <div className="p-2 bg-zinc-900/90 border border-zinc-800 rounded-lg flex items-center gap-2 text-zinc-400">
                <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>File not found <strong className="text-zinc-300 font-mono">Sesha_runtime.py</strong></span>
              </div>
            </div>

            {/* Review Summary & Action Controls */}
            <div className="pt-2 border-t border-zinc-800 space-y-2.5">
              <div className="flex items-center justify-between text-[11px]">
                <button className="flex items-center gap-1 text-zinc-300 hover:text-zinc-100 font-medium">
                  <span>Changes (1 artifact, 1 file)</span>
                  <ChevronDown className="w-3 h-3 text-zinc-400" />
                </button>
                <div className="flex items-center gap-1.5">
                  <button className="px-2.5 py-1 bg-zinc-850 hover:bg-zinc-800 border border-zinc-750 text-zinc-200 rounded font-semibold text-[11px] transition-colors">
                    Keep All
                  </button>
                  <button className="px-2.5 py-1 bg-zinc-850 hover:bg-zinc-800 border border-zinc-750 text-zinc-200 rounded font-semibold text-[11px] transition-colors">
                    Revert All
                  </button>
                  <button className="p-1 bg-purple-950/80 border border-purple-700/60 text-purple-300 rounded">
                    <Sparkles className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Interject to Steer Prompt Container */}
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-2.5 space-y-2">
                <input
                  type="text"
                  placeholder="Interject to steer the agent"
                  className="w-full bg-transparent text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none font-sans"
                />
                <div className="flex items-center justify-between pt-1 border-t border-zinc-850 text-[10px]">
                  <div className="flex items-center gap-2">
                    <button className="p-1 text-zinc-400 hover:text-zinc-200"><Paperclip className="w-3.5 h-3.5" /></button>
                    <span className="px-2 py-0.5 bg-amber-950/60 text-amber-300 border border-amber-800/60 rounded flex items-center gap-1 font-semibold">
                      <AlertTriangle className="w-3 h-3 text-amber-400" /> Unrestricted
                    </span>
                    <span className="text-zinc-400 font-mono">Gemini 3 Flash Preview</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="p-1.5 bg-rose-950 text-rose-300 border border-rose-800 rounded hover:bg-rose-900">
                      <Square className="w-3 h-3 fill-current" />
                    </button>
                    <span className="text-zinc-500 font-mono">562.4K / 1M</span>
                    <span className="px-1.5 py-0.5 bg-blue-900 text-blue-200 font-bold rounded text-[9px]">AI Pro</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TOP RIGHTBAR 4: DOCUMENTATION */}
        {activeTab === "docs" && (
          <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl space-y-3 text-zinc-300 leading-relaxed text-xs">
            <h3 className="text-sm font-bold text-cyan-300 border-b border-zinc-800 pb-2">Sesha Sovereign Architecture</h3>
            <p>Sesha AOI combines multi-agent directive execution, 3D Pet companion monitoring, and full-stack local file workspace management.</p>
            <ul className="list-disc pl-4 space-y-1 text-zinc-400">
              <li><strong className="text-cyan-400">L1 Panel:</strong> File Tree & Directives</li>
              <li><strong className="text-cyan-400">L2 Panel:</strong> Universal Code & File Inspector</li>
              <li><strong className="text-cyan-400">L3 Panel:</strong> MCP Tools, Webhook API, DB & Git</li>
              <li><strong className="text-cyan-400">L4 Panel:</strong> Terminal, Docker, Build, Problems</li>
            </ul>
          </div>
        )}
        {/* TAB 1: MCP TOOL DRAWER */}
        {activeTab === "tools" && (
          <div className="flex flex-col gap-3">
            <div className="flex items-center bg-zinc-900 border border-zinc-800 rounded px-2 py-1">
              <Search className="w-3.5 h-3.5 text-zinc-500 mr-1.5" />
              <input
                type="text"
                value={toolSearch}
                onChange={(e) => setToolSearch(e.target.value)}
                placeholder="Search MCP tools..."
                className="w-full bg-transparent text-zinc-200 focus:outline-none text-xs"
              />
            </div>

            {/* Tools Select */}
            <div className="flex flex-col gap-1.5">
              <span className="text-[10px] text-zinc-500 uppercase">Available Tools</span>
              {tools
                .filter((t) => t.name.includes(toolSearch))
                .map((t) => (
                  <div
                    key={t.id}
                    onClick={() => setSelectedTool(t)}
                    className={`p-2 rounded border cursor-pointer transition-all ${
                      selectedTool.id === t.id
                        ? "bg-cyan-950 border-cyan-500 text-cyan-200"
                        : "bg-zinc-900 border-zinc-800 text-zinc-300 hover:border-zinc-700"
                    }`}
                  >
                    <div className="flex items-center justify-between font-bold">
                      <span>{t.name}</span>
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-zinc-800 uppercase text-zinc-400">
                        {t.category}
                      </span>
                    </div>
                    <p className="text-[11px] text-zinc-400 font-sans mt-1">{t.description}</p>
                  </div>
                ))}
            </div>

            {/* Parameter Form */}
            {selectedTool && (
              <form onSubmit={handleToolRun} className="mt-2 p-3 bg-zinc-900/90 border border-zinc-800 rounded-lg flex flex-col gap-2">
                <span className="text-[11px] font-bold text-cyan-300">
                  Invoke {selectedTool.name}
                </span>

                {selectedTool.params.map((param) => (
                  <div key={param.name} className="flex flex-col gap-1">
                    <label className="text-[10px] text-zinc-400">
                      {param.name} <span className="text-zinc-500">({param.type})</span>
                    </label>
                    <input
                      type="text"
                      defaultValue={param.defaultVal || ""}
                      onChange={(e) =>
                        setToolParamValues({ ...toolParamValues, [param.name]: e.target.value })
                      }
                      className="bg-zinc-950 border border-zinc-750 rounded px-2 py-1 text-xs text-zinc-200 focus:border-cyan-400 focus:outline-none"
                    />
                  </div>
                ))}

                <button
                  type="submit"
                  className="mt-2 w-full py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded font-sans text-xs font-semibold flex items-center justify-center gap-1.5 shadow"
                >
                  <Play className="w-3.5 h-3.5" />
                  <span>Execute Tool</span>
                </button>
              </form>
            )}
          </div>
        )}

        {/* TAB 2: API PLAYGROUND */}
        {activeTab === "api" && (
          <div className="flex flex-col gap-3">
            <span className="text-[10px] text-zinc-500 uppercase">HTTP API Playground</span>

            <form onSubmit={handleApiSend} className="flex flex-col gap-2">
              <div className="flex gap-1">
                <select
                  value={apiMethod}
                  onChange={(e) => setApiMethod(e.target.value as any)}
                  className="bg-zinc-900 border border-zinc-750 text-cyan-400 font-bold px-2 py-1 rounded text-xs"
                >
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                </select>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  className="flex-1 bg-zinc-900 border border-zinc-750 rounded px-2 py-1 text-xs text-zinc-200 focus:outline-none"
                />
              </div>

              <div className="flex flex-col gap-1">
                <span className="text-[10px] text-zinc-400">Headers (JSON)</span>
                <textarea
                  value={apiHeaders}
                  onChange={(e) => setApiHeaders(e.target.value)}
                  className="h-16 bg-zinc-900 border border-zinc-800 rounded p-2 text-[11px] text-zinc-300 font-mono resize-none"
                />
              </div>

              {apiMethod !== "GET" && (
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] text-zinc-400">Request Body</span>
                  <textarea
                    value={apiBody}
                    onChange={(e) => setApiBody(e.target.value)}
                    className="h-24 bg-zinc-900 border border-zinc-800 rounded p-2 text-[11px] text-zinc-300 font-mono resize-none"
                  />
                </div>
              )}

              <button
                type="submit"
                className="py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded font-sans text-xs font-semibold flex items-center justify-center gap-1.5 shadow"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Send Request</span>
              </button>
            </form>

            {apiResponse && (
              <div className="mt-2 flex flex-col gap-1">
                <span className="text-[10px] text-emerald-400 font-bold">200 OK Response</span>
                <pre className="p-2.5 bg-zinc-900 border border-zinc-800 rounded text-[11px] text-emerald-300 max-h-48 overflow-auto">
                  {apiResponse}
                </pre>
              </div>
            )}
          </div>
        )}

        {/* TAB 3: DATABASE BROWSER */}
        {activeTab === "db" && (
          <div className="flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] text-zinc-500 uppercase">Database Manager (SQLite)</span>
              <span className="text-[10px] text-emerald-400 font-mono">Connected</span>
            </div>

            {/* Table Selector */}
            <div className="flex gap-1 overflow-x-auto pb-1">
              {dbTables.map((tbl) => (
                <button
                  key={tbl.name}
                  onClick={() => {
                    setSelectedTable(tbl);
                    setSqlQuery(`SELECT * FROM ${tbl.name} LIMIT 10;`);
                  }}
                  className={`px-2.5 py-1 rounded text-xs border transition-colors ${
                    selectedTable.name === tbl.name
                      ? "bg-cyan-950 border-cyan-500 text-cyan-300"
                      : "bg-zinc-900 border-zinc-800 text-zinc-400"
                  }`}
                >
                  {tbl.name}
                </button>
              ))}
            </div>

            {/* Query Runner Form */}
            <form onSubmit={handleRunQuery} className="flex flex-col gap-2">
              <textarea
                value={sqlQuery}
                onChange={(e) => setSqlQuery(e.target.value)}
                className="h-16 bg-zinc-900 border border-zinc-800 rounded p-2 text-xs text-zinc-200 font-mono focus:outline-none"
              />
              <button
                type="submit"
                className="py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-xs font-sans font-semibold flex items-center justify-center gap-1"
              >
                <Play className="w-3 h-3" />
                <span>Run Query</span>
              </button>
            </form>

            {/* Results Grid */}
            <div className="overflow-x-auto bg-zinc-900 border border-zinc-800 rounded">
              <table className="w-full text-left text-[11px] border-collapse">
                <thead>
                  <tr className="bg-zinc-925 border-b border-zinc-800 text-zinc-400">
                    {selectedTable.columns.map((col) => (
                      <th key={col} className="p-1.5 font-bold border-r border-zinc-800">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {selectedTable.data.map((row, idx) => (
                    <tr key={idx} className="border-b border-zinc-800/60 hover:bg-zinc-850">
                      {selectedTable.columns.map((col) => (
                        <td key={col} className="p-1.5 border-r border-zinc-800 text-zinc-300 truncate max-w-[120px]">
                          {String(row[col])}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 4: GIT GRAPH */}
        {activeTab === "git" && (
          <div className="flex flex-col gap-3">
            <span className="text-[10px] text-zinc-500 uppercase">Git Commit History</span>

            <div className="flex flex-col gap-2">
              {gitCommits.map((c) => (
                <div
                  key={c.hash}
                  className="p-2.5 bg-zinc-900 border border-zinc-800 rounded-lg flex flex-col gap-1 hover:border-purple-500/60 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-purple-400 text-xs">
                      #{c.hash} {c.isHead && "(HEAD)"}
                    </span>
                    <span className="text-[10px] text-zinc-500">{c.date}</span>
                  </div>
                  <p className="text-xs text-zinc-200 font-sans">{c.message}</p>
                  <span className="text-[10px] text-zinc-400 font-mono">{c.author}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 5: CI DASHBOARD */}
        {activeTab === "ci" && (
          <div className="flex flex-col gap-3">
            <span className="text-[10px] text-zinc-500 uppercase">CI/CD Pipeline Runs</span>

            <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Build & Test Pipeline #402</span>
                </div>
                <span className="text-[10px] text-zinc-500">2 mins ago</span>
              </div>
              <p className="text-xs text-zinc-300 font-sans">
                Triggered by commit #a9f2c14 (dual-interface spec)
              </p>
              <div className="flex items-center gap-2 mt-1 text-[10px] text-zinc-400">
                <span className="px-1.5 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-800 rounded">
                  Lint: Passed
                </span>
                <span className="px-1.5 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-800 rounded">
                  PyTest: 12/12 Passed
                </span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: SYSTEM DOCUMENTATION & WHITEPAPER */}
        {activeTab === "docs" && (
          <div className="flex flex-col gap-3 font-mono text-xs">
            <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider">Sanctum Architectural Whitepaper</span>
            
            <div className="p-3 bg-[#18110b] border border-amber-800/60 rounded-xl flex flex-col gap-2 text-stone-300 shadow-md">
              <h4 className="text-amber-300 font-bold flex items-center gap-1.5 text-xs">
                <FileText className="w-3.5 h-3.5 text-amber-400" />
                <span>Sesha-SANCTUM OS V4.2 SPEC</span>
              </h4>
              <p className="text-[11px] leading-relaxed text-stone-400">
                The Sanctum Kernel is modeled after Indian temple architecture (Mahaprakara, Garbhagriha, Gopuram), integrating 1.618 Phi golden ratio spatial snapping and generative cymatic soundwaves.
              </p>
              <div className="flex flex-col gap-1.5 mt-1 pt-2 border-t border-amber-900/50 text-[10px]">
                <div className="flex justify-between text-amber-400 font-semibold">
                  <span>Sovereign Mode</span>
                  <span>Interactive IDE Layer</span>
                </div>
                <div className="flex justify-between text-cyan-400 font-semibold">
                  <span>Sesha Core Mode</span>
                  <span>Autonomous Kernel Layer</span>
                </div>
                <div className="flex justify-between text-emerald-400 font-semibold">
                  <span>Generative Audio</span>
                  <span>Web Audio API Temple Engine</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
});

L3ToolsPanel.displayName = "L3ToolsPanel";

