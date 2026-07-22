import React, { useState, useMemo } from "react";
import {
  Terminal as TerminalIcon,
  Hammer,
  Database,
  Box,
  Globe,
  AlertCircle,
  X,
  ChevronDown,
  Play,
  Trash2,
  Send,
  CheckCircle2,
  Sparkles,
  Plus,
  Copy,
  Check,
  Search,
  Filter,
  Pause,
  ArrowDown,
  WrapText,
  SlidersHorizontal,
  Volume2,
  Activity,
  Layers,
} from "lucide-react";
import { motion } from "motion/react";

interface TerminalSession {
  id: string;
  title: string;
  logs: { id: string; time: string; level: "VERBOSE" | "DEBUG" | "INFO" | "WARN" | "ERROR"; tag: string; message: string }[];
}

interface L4BottomBarProps {
  onExecuteCommand?: (cmd: string) => void;
  isOpen: boolean;
  onToggleOpen: () => void;
  activeTab?: "terminal" | "build" | "db" | "docker" | "http" | "problems";
  onChangeTab?: (tab: "terminal" | "build" | "db" | "docker" | "http" | "problems") => void;
  onOpenInlineRefactor?: () => void;
}

export const L4BottomBar: React.FC<L4BottomBarProps> = React.memo(({
  onExecuteCommand,
  isOpen,
  onToggleOpen,
  activeTab: externalTab,
  onChangeTab,
  onOpenInlineRefactor,
}) => {
  const [internalTab, setInternalTab] = useState<"terminal" | "build" | "db" | "docker" | "http" | "problems">("terminal");
  const activeTab = externalTab || internalTab;
  const setActiveTab = (tab: "terminal" | "build" | "db" | "docker" | "http" | "problems") => {
    setInternalTab(tab);
    onChangeTab?.(tab);
  };

  // 2025 Multi-Session Terminal State
  const [terminalSessions, setTerminalSessions] = useState<TerminalSession[]>([
    {
      id: "term-1",
      title: "Terminal 1 (AOS Shell)",
      logs: [
        { id: "1", time: "10:42:01", level: "INFO", tag: "NEXUS-SANCTUM", message: "Temple Sanctum Kernel v13.0 Initialized." },
        { id: "2", time: "10:42:02", level: "DEBUG", tag: "ACOUSTICS", message: "Nada Brahma Golden Ratio soundwave frequencies tuned to φ 1.618." },
        { id: "3", time: "10:42:05", level: "VERBOSE", tag: "GARBHAGRIHA", message: "Scanning host processes... 0 anomalies detected." },
        { id: "4", time: "10:42:10", level: "INFO", tag: "PYTEST", message: "python -m pytest tests/ :: 100% PASSED in 0.12s" },
      ],
    },
    {
      id: "term-2",
      title: "Android Studio Logcat",
      logs: [
        { id: "101", time: "10:43:00", level: "INFO", tag: "com.nexus.sanctum", message: "Activity.onCreate() -> SurfaceView bound to Vulkan Engine" },
        { id: "102", time: "10:43:01", level: "DEBUG", tag: "RenderThread", message: "Frame 60.0 FPS synchronized with Golden Ratio baseline" },
        { id: "103", time: "10:43:03", level: "WARN", tag: "AudioTrack", message: "Buffer underrun mitigated via Soundwave Cymatic smoother" },
        { id: "104", time: "10:43:08", level: "ERROR", tag: "NetworkStack", message: "Handshake delayed on fallback socket — retried successfully" },
      ],
    },
  ]);
  const [activeSessionId, setActiveSessionId] = useState("term-1");
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState("");

  // Android Studio Logcat Filtering & Engine Controls
  const [logLevelFilter, setLogLevelFilter] = useState<"ALL" | "VERBOSE" | "DEBUG" | "INFO" | "WARN" | "ERROR">("ALL");
  const [selectedProcess, setSelectedProcess] = useState("com.nexus.sanctum (PID 1024)");
  const [searchQuery, setSearchQuery] = useState("");
  const [isPaused, setIsPaused] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const [softWrap, setSoftWrap] = useState(true);
  const [copied, setCopied] = useState(false);
  const [terminalInput, setTerminalInput] = useState("");

  const activeSession = terminalSessions.find((s) => s.id === activeSessionId) || terminalSessions[0];

  // Add new Terminal Session Tab (+)
  const handleAddSession = () => {
    const newId = `term-${Date.now()}`;
    const newSession: TerminalSession = {
      id: newId,
      title: `Terminal ${terminalSessions.length + 1}`,
      logs: [
        { id: `${Date.now()}-1`, time: new Date().toLocaleTimeString(), level: "INFO", tag: "SANCTUM", message: "New Terminal session attached to Temple Shell." },
      ],
    };
    setTerminalSessions((prev) => [...prev, newSession]);
    setActiveSessionId(newId);
  };

  // Close Terminal Session Tab (X)
  const handleCloseSession = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (terminalSessions.length <= 1) return; // Keep at least 1 session
    const filtered = terminalSessions.filter((s) => s.id !== id);
    setTerminalSessions(filtered);
    if (activeSessionId === id) {
      setActiveSessionId(filtered[0].id);
    }
  };

  // Start Inline Edit Title
  const handleStartEditTitle = (session: TerminalSession) => {
    setEditingSessionId(session.id);
    setEditingTitle(session.title);
  };

  // Save Edit Title
  const handleSaveEditTitle = (id: string) => {
    if (editingTitle.trim()) {
      setTerminalSessions((prev) =>
        prev.map((s) => (s.id === id ? { ...s, title: editingTitle.trim() } : s))
      );
    }
    setEditingSessionId(null);
  };

  // Filter logs according to Log Level and Search query
  const filteredLogs = useMemo(() => {
    if (!activeSession) return [];
    return activeSession.logs.filter((log) => {
      // Level check
      if (logLevelFilter !== "ALL") {
        const levels = ["VERBOSE", "DEBUG", "INFO", "WARN", "ERROR"];
        if (levels.indexOf(log.level) < levels.indexOf(logLevelFilter)) return false;
      }
      // Search query check
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        return (
          log.message.toLowerCase().includes(q) ||
          log.tag.toLowerCase().includes(q) ||
          log.level.toLowerCase().includes(q)
        )
      }
      return true;
    });
  }, [activeSession, logLevelFilter, searchQuery]);

  const handleTerminalSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!terminalInput.trim()) return;
    const cmd = terminalInput.trim();

    const newLog = {
      id: `${Date.now()}`,
      time: new Date().toLocaleTimeString(),
      level: "INFO" as const,
      tag: "USER-CMD",
      message: `$ ${cmd}`,
    };

    setTerminalSessions((prev) =>
      prev.map((s) =>
        s.id === activeSessionId
          ? {
              ...s,
              logs: [
                ...s.logs,
                newLog,
                {
                  id: `${Date.now() + 1}`,
                  time: new Date().toLocaleTimeString(),
                  level: "VERBOSE" as const,
                  tag: "EXEC-OUT",
                  message: `✔ Executed command [${cmd}] on ${selectedProcess}`,
                },
              ],
            }
          : s
      )
    );

    onExecuteCommand?.(cmd);
    setTerminalInput("");
  };

  const handleCopyLogs = () => {
    const logText = filteredLogs.map((l) => `[${l.time}] [${l.level}] [${l.tag}]: ${l.message}`).join("\n");
    navigator.clipboard.writeText(logText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClearLogs = () => {
    setTerminalSessions((prev) =>
      prev.map((s) => (s.id === activeSessionId ? { ...s, logs: [] } : s))
    );
  };

  if (!isOpen) return null;

  return (
    <div className="h-full w-full bg-[#16100c]/95 border-2 border-amber-800/60 rounded-xl flex flex-col select-none z-20 font-mono text-xs overflow-hidden shadow-2xl backdrop-blur-md transition-all duration-300 ease-in-out shilpkari-concave oil-lamp-glow">
      {/* Integrated Single Header Bar with Panel Tabs, Sessions, Nada Brahma Visualizer & Down Arrow */}
      <div className="flex flex-wrap items-center justify-between bg-[#1f1712] border-b border-amber-800/60 px-3 py-1.5 gap-2 shrink-0">
        {/* Main Panel Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto py-0.5 scrollbar-none">
          {[
            { id: "terminal", label: "Terminal Engine", icon: TerminalIcon },
            { id: "build", label: "Build Output", icon: Hammer },
            { id: "db", label: "DB Console", icon: Database },
            { id: "docker", label: "Docker Services", icon: Box },
            { id: "http", label: "HTTP Curl", icon: Globe },
            { id: "problems", label: "Diagnostics (0)", icon: AlertCircle },
          ].map((tab) => {
            const Icon = tab.icon;
            const isTabActive = activeTab === tab.id;
            return (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                whileHover={{ scale: 1.05, y: -1 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 400, damping: 25 }}
                className={`flex items-center gap-1.5 px-3 py-0.5 rounded-md border transition-all duration-300 ease-in-out shrink-0 cursor-pointer ${
                  isTabActive
                    ? "border-amber-500/80 text-amber-300 bg-amber-950/90 font-bold shadow-md shadow-amber-950/40 ring-1 ring-amber-500/30"
                    : "border-stone-800/80 text-stone-400 hover:text-amber-200 hover:bg-[#281e18]"
                }`}
              >
                <Icon className="w-3.5 h-3.5 text-amber-400" />
                <span>{tab.label}</span>
              </motion.button>
            );
          })}
        </div>

        {/* Right Section: Nada Brahma Soundwave + Minimize Down Arrow Button */}
        <div className="flex items-center gap-2 shrink-0">
          {/* Acoustic Cymatic Soundwave Harmonic Resonance Visualizer */}
          <div className="flex items-center gap-2 px-2 py-0.5 rounded-md bg-amber-950/40 border border-amber-800/60 text-[10px] text-amber-300">
            <Volume2 className="w-3 h-3 text-amber-400 animate-pulse" />
            <span className="font-bold hidden sm:inline">Nada Brahma Soundwave:</span>
            <div className="flex items-end gap-0.5 h-3.5">
              {[40, 90, 60, 100, 30, 80, 50, 95, 70, 40].map((h, idx) => (
                <div
                  key={idx}
                  style={{ height: `${h}%` }}
                  className="w-1 bg-amber-400/90 rounded-full animate-pulse"
                />
              ))}
            </div>
          </div>

          {/* Minimize Down Arrow Button shifted right next to Nada Brahma Soundwave button */}
          <motion.button
            onClick={onToggleOpen}
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.92 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            className="p-1 hover:bg-[#281e18] text-amber-400 hover:text-amber-200 rounded-md border border-amber-800/60 transition-colors cursor-pointer bg-amber-950/60 shadow-sm"
            title="Minimize Bottom Panel"
          >
            <ChevronDown className="w-4 h-4" />
          </motion.button>
        </div>
      </div>

      {/* TERMINAL MULTI-SESSION SUB-NAVBAR & ANDROID STUDIO LOGCAT CONTROLS */}
      {activeTab === "terminal" && (
        <div className="flex flex-col border-b border-amber-800/40 bg-[#1a130e] shrink-0">
          {/* Sub-Tabs Row (+ & X Support) */}
          <div className="flex items-center justify-between px-3 py-1 border-b border-stone-800/80 text-[11px]">
            <div className="flex items-center gap-1 overflow-x-auto py-0.5 max-w-full scrollbar-none">
              {terminalSessions.map((session) => {
                const isSelected = session.id === activeSessionId;
                return (
                  <div
                    key={session.id}
                    onClick={() => setActiveSessionId(session.id)}
                    onDoubleClick={() => handleStartEditTitle(session)}
                    className={`flex items-center gap-2 px-2.5 py-0.5 rounded-md border cursor-pointer transition-all duration-200 group shrink-0 ${
                      isSelected
                        ? "bg-amber-950/90 text-amber-200 border-amber-500/80 font-bold shadow-sm"
                        : "bg-[#221913] text-stone-400 border-stone-800/90 hover:text-stone-200 hover:bg-[#2a1f18]"
                    }`}
                  >
                    <TerminalIcon className="w-3 h-3 text-amber-400 shrink-0" />
                    {editingSessionId === session.id ? (
                      <input
                        type="text"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        onBlur={() => handleSaveEditTitle(session.id)}
                        onKeyDown={(e) => e.key === "Enter" && handleSaveEditTitle(session.id)}
                        autoFocus
                        className="bg-black/60 text-amber-200 px-1 rounded border border-amber-500/80 focus:outline-none w-28"
                      />
                    ) : (
                      <span className="truncate max-w-[140px]">{session.title}</span>
                    )}

                    {terminalSessions.length > 1 && (
                      <button
                        onClick={(e) => handleCloseSession(session.id, e)}
                        className="p-0.5 rounded hover:bg-rose-950/80 hover:text-rose-300 text-stone-500 transition-colors"
                        title="Close Session (X)"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                );
              })}

              {/* Add New Session Button (+) */}
              <button
                onClick={handleAddSession}
                className="p-1 bg-[#221913] hover:bg-amber-950 border border-stone-800 hover:border-amber-600/80 rounded-md text-amber-400 hover:text-amber-200 transition-colors flex items-center justify-center shrink-0"
                title="Add New Terminal Session (+)"
              >
                <Plus className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Android Studio Logcat Filtering Control Bar */}
          <div className="flex flex-wrap items-center justify-between px-3 py-1.5 gap-2 text-[11px] bg-[#18110c]">
            {/* Process & Log Level Selector */}
            <div className="flex items-center gap-2 flex-wrap">
              {/* Process Selector */}
              <div className="flex items-center gap-1.5 bg-[#221913] border border-stone-800 px-2 py-1 rounded-md text-stone-300">
                <Layers className="w-3 h-3 text-amber-400" />
                <select
                  value={selectedProcess}
                  onChange={(e) => setSelectedProcess(e.target.value)}
                  className="bg-transparent text-amber-200 focus:outline-none cursor-pointer"
                >
                  <option value="com.nexus.sanctum (PID 1024)">com.nexus.sanctum (PID 1024)</option>
                  <option value="node server.ts (PID 3000)">node server.ts (PID 3000)</option>
                  <option value="python main.py (PID 8420)">python main.py (PID 8420)</option>
                  <option value="kernel.sys (PID 1)">kernel.sys (PID 1)</option>
                </select>
              </div>

              {/* Log Level Filter Pills */}
              <div className="flex items-center bg-[#221913] border border-stone-800 rounded-md p-0.5 gap-0.5">
                {(["ALL", "VERBOSE", "DEBUG", "INFO", "WARN", "ERROR"] as const).map((level) => (
                  <button
                    key={level}
                    onClick={() => setLogLevelFilter(level)}
                    className={`px-2 py-0.5 rounded text-[10px] font-bold transition-all ${
                      logLevelFilter === level
                        ? level === "ERROR"
                          ? "bg-rose-950 text-rose-300 border border-rose-700/80"
                          : level === "WARN"
                          ? "bg-orange-950 text-orange-300 border border-orange-700/80"
                          : "bg-amber-950 text-amber-300 border border-amber-600/80"
                        : "text-stone-400 hover:text-stone-200"
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Input & Action Controls */}
            <div className="flex items-center gap-2">
              {/* Live Search Filter Input */}
              <div className="flex items-center bg-[#221913] border border-stone-800 focus-within:border-amber-500 rounded-md px-2 py-0.5 text-stone-200">
                <Search className="w-3 h-3 text-amber-400 mr-1.5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter logs / regex..."
                  className="bg-transparent text-[11px] text-amber-100 placeholder-stone-500 focus:outline-none w-28 md:w-40"
                />
              </div>

              {/* Pause / Resume */}
              <button
                onClick={() => setIsPaused(!isPaused)}
                className={`p-1 rounded border transition-colors ${
                  isPaused
                    ? "bg-amber-950 text-amber-300 border-amber-600"
                    : "bg-[#221913] border-stone-800 text-stone-400 hover:text-stone-200"
                }`}
                title={isPaused ? "Resume Live Log Stream" : "Pause Live Stream"}
              >
                <Pause className="w-3.5 h-3.5" />
              </button>

              {/* Auto Scroll */}
              <button
                onClick={() => setAutoScroll(!autoScroll)}
                className={`p-1 rounded border transition-colors ${
                  autoScroll
                    ? "bg-amber-950 text-amber-300 border-amber-600"
                    : "bg-[#221913] border-stone-800 text-stone-400 hover:text-stone-200"
                }`}
                title="Toggle Auto-Scroll"
              >
                <ArrowDown className="w-3.5 h-3.5" />
              </button>

              {/* Soft Wrap */}
              <button
                onClick={() => setSoftWrap(!softWrap)}
                className={`p-1 rounded border transition-colors ${
                  softWrap
                    ? "bg-amber-950 text-amber-300 border-amber-600"
                    : "bg-[#221913] border-stone-800 text-stone-400 hover:text-stone-200"
                }`}
                title="Toggle Soft Wrap"
              >
                <WrapText className="w-3.5 h-3.5" />
              </button>

              {/* Copy All Logs */}
              <button
                onClick={handleCopyLogs}
                className="p-1 bg-[#221913] hover:bg-amber-950 border border-stone-800 rounded text-stone-400 hover:text-amber-200 transition-colors"
                title="Copy Filtered Logs"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>

              {/* Clear Console */}
              <button
                onClick={handleClearLogs}
                className="p-1 bg-[#221913] hover:bg-rose-950 border border-stone-800 rounded text-stone-400 hover:text-rose-300 transition-colors"
                title="Clear Session Logs"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Tab Content Output Area */}
      <div className="flex-1 overflow-y-auto p-3 text-stone-300 bg-[#140e0a]">
        {/* TERMINAL */}
        {activeTab === "terminal" && (
          <div className="flex flex-col h-full justify-between gap-2">
            <div className={`flex-1 overflow-y-auto flex flex-col gap-1 pr-1 font-mono text-xs ${softWrap ? "whitespace-pre-wrap" : "whitespace-nowrap"}`}>
              {filteredLogs.length === 0 ? (
                <div className="text-stone-500 italic p-2">
                  No logs matching filter criteria in {activeSession?.title}.
                </div>
              ) : (
                filteredLogs.map((log) => (
                  <div key={log.id} className="flex items-start gap-2 leading-relaxed hover:bg-amber-950/20 px-1.5 py-0.5 rounded">
                    <span className="text-stone-500 shrink-0 font-mono text-[10px]">{log.time}</span>
                    <span
                      className={`px-1 rounded text-[9px] font-bold shrink-0 ${
                        log.level === "ERROR"
                          ? "bg-rose-950 text-rose-300 border border-rose-800"
                          : log.level === "WARN"
                          ? "bg-orange-950 text-orange-300 border border-orange-800"
                          : log.level === "DEBUG"
                          ? "bg-cyan-950 text-cyan-300 border border-cyan-800"
                          : "bg-amber-950 text-amber-300 border border-amber-800"
                      }`}
                    >
                      {log.level}
                    </span>
                    <span className="text-amber-400/90 font-bold shrink-0">[{log.tag}]</span>
                    <span
                      className={
                        log.message.startsWith("$")
                          ? "text-amber-300 font-bold"
                          : log.level === "ERROR"
                          ? "text-rose-300"
                          : log.level === "WARN"
                          ? "text-orange-200"
                          : "text-stone-200"
                      }
                    >
                      {log.message}
                    </span>
                  </div>
                ))
              )}
            </div>

            {/* Interactive Shell Command Form */}
            <form onSubmit={handleTerminalSubmit} className="flex items-center gap-2 pt-2 border-t border-amber-800/40 shrink-0">
              <span className="text-amber-400 font-bold">$</span>
              <input
                type="text"
                value={terminalInput}
                onChange={(e) => setTerminalInput(e.target.value)}
                placeholder={`Type shell command on ${selectedProcess} (e.g. pytest, python main.py, git status)...`}
                className="flex-1 bg-transparent text-xs text-amber-100 placeholder-stone-500 focus:outline-none font-mono"
              />
              <button
                type="submit"
                className="px-3 py-1 bg-amber-600 hover:bg-amber-500 text-black font-bold rounded-lg text-xs flex items-center gap-1 transition-colors shadow-md"
              >
                <span>Run</span>
                <Send className="w-3 h-3" />
              </button>
            </form>
          </div>
        )}

        {/* BUILD */}
        {activeTab === "build" && (
          <div className="flex flex-col gap-2 font-mono text-xs">
            <div className="text-emerald-400 font-bold flex items-center gap-2 bg-emerald-950/40 p-2 rounded border border-emerald-800/60">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>✔ Temple Sanctum Build Succeeded in 0.38s</span>
            </div>
            <div className="p-3 bg-[#1e1610] rounded-lg border border-stone-800 space-y-1 text-stone-300">
              <div className="text-amber-400">[esbuild] server.ts compiled to dist/server.cjs</div>
              <div className="text-amber-300">[vite] v6.2.3 bundle ready on http://localhost:3000</div>
              <div className="text-stone-400">[golden-ratio] All structural dimensions aligned to φ 1.618</div>
            </div>
          </div>
        )}

        {/* DOCKER */}
        {activeTab === "docker" && (
          <div className="flex flex-col gap-2">
            <span className="text-[10px] text-amber-400 uppercase font-bold tracking-wider">
              Temple Compose Microservices
            </span>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              {[
                { name: "sanctum_aos_app", status: "running", ports: "3000:3000", uptime: "16 hours" },
                { name: "sanctum_postgres", status: "running", ports: "5432:5432", uptime: "16 hours" },
                { name: "sanctum_redis", status: "running", ports: "6379:6379", uptime: "16 hours" },
              ].map((c) => (
                <div key={c.name} className="p-3 bg-[#1e1610] border border-amber-800/60 rounded-xl flex flex-col gap-1 shadow-md">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-amber-200">{c.name}</span>
                    <span className="text-[9px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                      {c.status}
                    </span>
                  </div>
                  <span className="text-[10px] text-stone-400">Ports: {c.ports} • Uptime: {c.uptime}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* DIAGNOSTICS / PROBLEMS */}
        {activeTab === "problems" && (
          <div className="flex items-center gap-2 text-emerald-400 bg-emerald-950/40 p-3 rounded-xl border border-emerald-800/60">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span className="font-semibold">0 syntax errors or architectural anomalies detected in Temple Sanctum workspace.</span>
          </div>
        )}

        {/* HTTP / DB FALLBACK */}
        {(activeTab === "db" || activeTab === "http") && (
          <div className="p-3 bg-[#1e1610] border border-stone-800 rounded-xl text-stone-300">
            Interactive Temple DB / HTTP console ready. Issue SQL queries or HTTP endpoints in Terminal or L3 Tools Panel.
          </div>
        )}
      </div>
    </div>
  );
});

L4BottomBar.displayName = "L4BottomBar";

