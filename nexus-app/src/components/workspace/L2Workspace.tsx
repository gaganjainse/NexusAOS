import React, { useState } from "react";
import { FileNode, ChatMessage } from "../../types/nexus";
import {
  Code2,
  MessageSquare,
  GitCompare,
  FileText,
  X,
  Play,
  Sparkles,
  Command,
  Send,
  Check,
  RotateCcw,
  Bot,
  User,
  Copy,
  ChevronRight,
  ChevronLeft,
  Maximize2,
  Bug,
  Plus,
  Globe,
  Laptop,
  Tablet,
  Smartphone,
  ExternalLink,
  FileSpreadsheet,
  FileImage,
  Music,
  Film,
  FileCode,
  Terminal,
  Home,
  RefreshCw,
} from "lucide-react";

interface L2WorkspaceProps {
  activeFileNode: FileNode | null;
  openFiles: string[];
  onCloseFile: (path: string) => void;
  onSelectOpenFile: (path: string) => void;
  chatMessages: ChatMessage[];
  onSendChatMessage: (msg: string) => void;
  onUpdateFileContent?: (path: string, content: string) => void;
  onNewFile?: () => void;
  onRunFile?: (path: string) => void;
  onDebugFile?: (path: string) => void;
  inlinePromptOpen?: boolean;
  onSetInlinePromptOpen?: (open: boolean) => void;
  onSubmitDirective?: (text: string) => void;
  onRefactor?: () => void;
}

export const L2Workspace: React.FC<L2WorkspaceProps> = React.memo(({
  activeFileNode,
  openFiles,
  onCloseFile,
  onSelectOpenFile,
  chatMessages,
  onSendChatMessage,
  onUpdateFileContent,
  onNewFile,
  onRunFile,
  onDebugFile,
  inlinePromptOpen: externalInlinePromptOpen,
  onSetInlinePromptOpen,
  onSubmitDirective,
  onRefactor,
}) => {
  const [activeTab, setActiveTab] = useState<"code" | "browser" | "chat" | "diff" | "docs">("code");
  const [internalInlinePromptOpen, setInternalInlinePromptOpen] = useState(false);
  const inlinePromptOpen = externalInlinePromptOpen !== undefined ? externalInlinePromptOpen : internalInlinePromptOpen;
  const setInlinePromptOpen = (val: boolean) => {
    setInternalInlinePromptOpen(val);
    onSetInlinePromptOpen?.(val);
  };
  const [inlinePromptText, setInlinePromptText] = useState("");
  const [directiveText, setDirectiveText] = useState("");
  const [chatInput, setChatInput] = useState("");
  const [editorText, setEditorText] = useState(activeFileNode?.content || "");

  // Inbuilt Browser States
  const [browserUrl, setBrowserUrl] = useState("http://localhost:3000/app");
  const [browserDevice, setBrowserDevice] = useState<"desktop" | "tablet" | "mobile">("desktop");
  const [browserLogsOpen, setBrowserLogsOpen] = useState(false);
  const [browserCounter, setBrowserCounter] = useState(42);
  const [browserLogs, setBrowserLogs] = useState<string[]>([
    "[SYSTEM] Inbuilt Dev Browser connected to localhost:3000",
    "[HMR] Hot Module Replacement active",
    "[HTTP] GET /api/v1/vitals 200 OK (2.4ms)",
  ]);

  // Universal File Viewers State
  const [markdownPreviewMode, setMarkdownPreviewMode] = useState<"rendered" | "raw">("rendered");
  const [imageZoom, setImageZoom] = useState(100);

  // Update local editor text when active file changes
  React.useEffect(() => {
    if (activeFileNode?.content) {
      setEditorText(activeFileNode.content);
    }
  }, [activeFileNode?.path]);

  const handleEditorChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setEditorText(val);
    if (activeFileNode?.path) {
      onUpdateFileContent?.(activeFileNode.path, val);
    }
  };

  const handleInlinePromptSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inlinePromptText.trim()) return;
    const addition = `\n# AI Edit (${inlinePromptText}): Refactored for efficiency\n`;
    const newContent = editorText + addition;
    setEditorText(newContent);
    if (activeFileNode?.path) {
      onUpdateFileContent?.(activeFileNode.path, newContent);
    }
    setInlinePromptText("");
    setInlinePromptOpen(false);
  };

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    onSendChatMessage(chatInput.trim());
    setChatInput("");
  };

  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    // Check JSON payload from Explorer file tree
    const jsonStr = e.dataTransfer.getData("application/json");
    if (jsonStr) {
      try {
        const fileNode: FileNode = JSON.parse(jsonStr);
        if (fileNode.path) {
          onSelectOpenFile(fileNode.path);
          if (activeTab === "chat") {
            onSendChatMessage(`[Attached File Context]: ${fileNode.path}\n\`\`\`\n${fileNode.content || ""}\n\`\`\``);
          }
          return;
        }
      } catch (err) {
        // Fallback text
      }
    }

    const pathText = e.dataTransfer.getData("text/plain");
    if (pathText) {
      onSelectOpenFile(pathText);
      if (activeTab === "chat") {
        onSendChatMessage(`[Attached Context Path]: ${pathText}`);
      }
    }
  };

  const handleDirectiveSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!directiveText.trim()) return;
    onSubmitDirective?.(directiveText.trim());
    setDirectiveText("");
  };

  const lines = editorText.split("\n");
  const ext = activeFileNode?.name ? activeFileNode.name.split(".").pop()?.toLowerCase() || "" : "";

  return (
    <main
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`w-full h-full flex flex-col bg-[#140e0b] border-2 border-amber-800/60 rounded-xl overflow-hidden select-none relative shadow-xl transition-all shilpkari-concave oil-lamp-glow ${
        isDragOver ? "ring-2 ring-amber-400 bg-amber-950/40" : ""
      }`}
    >
      {/* Drop Target Indicator Overlay */}
      {isDragOver && (
        <div className="absolute inset-0 z-50 bg-amber-950/90 border-2 border-dashed border-amber-400 backdrop-blur-sm flex flex-col items-center justify-center gap-2 text-amber-200 font-mono">
          <Sparkles className="w-10 h-10 text-amber-400 animate-bounce" />
          <span className="text-sm font-bold">Drop file here to open in Temple Sanctum Editor</span>
        </div>
      )}

      {/* Persistent Workspace Top Directive Command Bar */}
      <div className="px-3 py-1.5 bg-[#18110b] flex flex-col md:flex-row items-stretch md:items-center gap-2 border-b border-amber-900/50 font-mono text-xs shrink-0">
        <form onSubmit={handleDirectiveSubmit} className="flex-1 flex items-center bg-[#1e1510] border border-amber-800/60 focus-within:border-amber-500 rounded-lg px-2.5 py-1 transition-all shadow-inner">
          <span className="text-amber-400 font-bold mr-2 text-xs">❯</span>
          <input
            type="text"
            value={directiveText}
            onChange={(e) => setDirectiveText(e.target.value)}
            placeholder="Issue Sacred Directive or command to Temple Sanctum Kernel..."
            className="w-full bg-transparent text-xs text-stone-100 placeholder-stone-500 focus:outline-none font-mono"
          />
          <button
            type="submit"
            className="ml-2 px-2.5 py-0.5 bg-[#1a120b] border border-amber-600/80 hover:border-amber-400 hover:shadow-[0_0_8px_rgba(245,158,11,0.4)] text-amber-300 hover:bg-amber-950/80 rounded-md text-[11px] font-bold flex items-center gap-1 transition-all cursor-pointer shrink-0"
          >
            <span>Submit</span>
            <Send className="w-3 h-3" />
          </button>
        </form>

        {/* Action Buttons: Run, Debug, Refactor (Outline Buttons) */}
        <div className="flex items-center gap-1.5 shrink-0">
          <button
            type="button"
            onClick={() => onRunFile?.(activeFileNode?.path || "main.py")}
            className="px-2.5 py-1 bg-[#1a120b] border border-emerald-600/80 hover:border-emerald-400 hover:shadow-[0_0_8px_rgba(16,185,129,0.4)] text-emerald-300 hover:bg-emerald-950/80 rounded-md text-[11px] font-bold flex items-center gap-1 transition-all cursor-pointer"
            title="Run Active File Execution"
          >
            <Play className="w-3 h-3 fill-emerald-300 text-emerald-300" />
            <span>Run</span>
          </button>

          <button
            type="button"
            onClick={() => onDebugFile?.(activeFileNode?.path || "main.py")}
            className="px-2.5 py-1 bg-[#1a120b] border border-amber-600/80 hover:border-amber-400 hover:shadow-[0_0_8px_rgba(245,158,11,0.4)] text-amber-300 hover:bg-amber-950/80 rounded-md text-[11px] font-bold flex items-center gap-1 transition-all cursor-pointer"
            title="Debug Diagnostics"
          >
            <Bug className="w-3 h-3 text-amber-400" />
            <span>Debug</span>
          </button>

          <button
            type="button"
            onClick={() => {
              if (onRefactor) onRefactor();
              else setInlinePromptOpen(true);
            }}
            className="px-2.5 py-1 bg-[#1a120b] border border-amber-500/80 hover:border-amber-400 hover:shadow-[0_0_8px_rgba(245,158,11,0.4)] text-amber-200 hover:bg-amber-950/80 rounded-md text-[11px] font-bold flex items-center gap-1 transition-all cursor-pointer"
            title="Inline AI Code Refactor (Cmd+K)"
          >
            <Sparkles className="w-3 h-3 text-amber-300 animate-pulse" />
            <span>Refactor</span>
          </button>
        </div>
      </div>


      {/* File Sub-Tabs Bar for Code Editor */}
      {activeTab === "code" && (
        <div className="flex items-center justify-between bg-[#1d1610] border-b border-amber-900/50 px-2.5 py-1 gap-2 overflow-x-auto shrink-0 font-mono text-xs">
          {/* File Tabs List */}
          <div className="flex items-center gap-1.5 overflow-x-auto py-0.5">
            {openFiles.map((path) => {
              const fileName = path.split("/").pop() || path;
              const isSelected = activeFileNode?.path === path;
              const pathExt = fileName.split(".").pop()?.toLowerCase() || "";

              let IconComponent = Code2;
              if (["svg", "png", "jpg", "jpeg", "gif"].includes(pathExt)) IconComponent = FileImage;
              else if (["mp3", "wav", "ogg"].includes(pathExt)) IconComponent = Music;
              else if (["mp4", "webm"].includes(pathExt)) IconComponent = Film;
              else if (["csv", "tsv"].includes(pathExt)) IconComponent = FileSpreadsheet;

              return (
                <div
                  key={path}
                  onClick={() => onSelectOpenFile(path)}
                  className={`flex items-center gap-2 px-2.5 py-1 rounded-lg border cursor-pointer transition-all group shrink-0 ${
                    isSelected
                      ? "bg-amber-950/90 text-amber-300 border-amber-500/80 shadow-md font-bold"
                      : "bg-[#251b14] text-stone-400 border-amber-900/40 hover:text-amber-200 hover:bg-[#2c2018]"
                  }`}
                >
                  <IconComponent className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                  <span className="truncate max-w-[120px]">{fileName}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onCloseFile(path);
                    }}
                    title="Close Tab"
                    className="p-0.5 hover:bg-stone-800 rounded text-stone-500 hover:text-rose-400 transition-colors"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              );
            })}

            {/* + Button to open/create new tab */}
            <button
              onClick={() => onNewFile?.()}
              title="New File Tab (+)"
              className="p-1.5 bg-[#251b14] hover:bg-amber-950 border border-amber-900/40 rounded-lg text-amber-400 hover:text-amber-200 transition-colors flex items-center justify-center shrink-0"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* TAB 1: CODE & UNIVERSAL FILE VIEWER */}
      {activeTab === "code" && (
        <div className="flex-1 relative flex flex-col bg-zinc-950 font-mono text-xs overflow-hidden">
          {/* Cmd+K Inline Edit Modal Popup */}
          {inlinePromptOpen && (
            <div className="absolute top-4 left-1/2 -translate-x-1/2 z-40 w-11/12 max-w-lg bg-zinc-900 border border-cyan-500/60 rounded-xl shadow-2xl p-3 backdrop-blur-md">
              <div className="flex items-center justify-between pb-2 border-b border-zinc-800">
                <div className="flex items-center gap-1.5 text-cyan-300 font-semibold text-xs">
                  <Sparkles className="w-4 h-4 text-cyan-400 animate-spin-slow" />
                  <span>Inline AI Code Refactoring (Cmd+K)</span>
                </div>
                <button
                  onClick={() => setInlinePromptOpen(false)}
                  className="text-zinc-500 hover:text-zinc-200"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <form onSubmit={handleInlinePromptSubmit} className="mt-2 flex gap-2">
                <input
                  type="text"
                  value={inlinePromptText}
                  onChange={(e) => setInlinePromptText(e.target.value)}
                  placeholder="e.g. Optimize memory consumption, add type checks, generate docstring..."
                  className="flex-1 bg-zinc-950 border border-zinc-700 rounded px-3 py-1.5 text-xs text-zinc-100 focus:outline-none focus:border-cyan-400"
                  autoFocus
                />
                <button
                  type="submit"
                  className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded font-sans text-xs font-medium"
                >
                  Apply
                </button>
              </form>
            </div>
          )}

          {/* DYNAMIC UNIVERSAL FILE VIEWER ENGINE */}
          {["svg", "png", "jpg", "jpeg", "gif", "webp", "ico"].includes(ext) ? (
            <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
              <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs">
                <div className="flex items-center gap-2 text-cyan-300 font-bold">
                  <FileImage className="w-4 h-4 text-cyan-400" />
                  <span>Image Inspection: {activeFileNode?.name}</span>
                </div>
                <div className="flex items-center gap-3 text-zinc-400 text-[11px]">
                  <span>Scale: {imageZoom}%</span>
                  <button onClick={() => setImageZoom((z) => Math.max(25, z - 25))} className="px-2 py-0.5 bg-zinc-800 rounded hover:text-white">-</button>
                  <button onClick={() => setImageZoom(100)} className="px-2 py-0.5 bg-zinc-800 rounded hover:text-white">Reset</button>
                  <button onClick={() => setImageZoom((z) => Math.min(400, z + 25))} className="px-2 py-0.5 bg-zinc-800 rounded hover:text-white">+</button>
                </div>
              </div>
              <div className="flex-1 p-8 flex items-center justify-center bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:16px_16px] overflow-auto">
                {ext === "svg" ? (
                  <div
                    style={{ transform: `scale(${imageZoom / 100})` }}
                    className="transition-transform duration-200 border border-zinc-800 rounded-xl bg-zinc-900 p-4 shadow-2xl"
                    dangerouslySetInnerHTML={{ __html: editorText }}
                  />
                ) : (
                  <img
                    src={editorText.startsWith("data:") ? editorText : "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80"}
                    alt={activeFileNode?.name}
                    style={{ transform: `scale(${imageZoom / 100})` }}
                    className="max-w-md max-h-96 rounded-xl border border-zinc-800 shadow-2xl transition-transform duration-200"
                  />
                )}
              </div>
            </div>
          ) : ["mp3", "wav", "ogg", "aac"].includes(ext) ? (
            <div className="flex-1 flex flex-col items-center justify-center p-8 bg-zinc-950 text-zinc-200">
              <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-2xl flex flex-col gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400">
                    <Music className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-zinc-100">{activeFileNode?.name}</h4>
                    <p className="text-xs text-zinc-500 font-mono">Audio Track • Audio Player</p>
                  </div>
                </div>
                <div className="flex items-end gap-1 h-16 py-2 bg-zinc-950 rounded-lg px-4 border border-zinc-800 justify-between">
                  {[40, 70, 30, 90, 60, 100, 45, 80, 20, 90, 65, 85, 40, 95, 30, 75, 50, 90, 35, 80].map((h, i) => (
                    <div key={i} style={{ height: `${h}%` }} className="w-1.5 bg-cyan-400/80 rounded-full animate-pulse" />
                  ))}
                </div>
                <audio controls src={editorText.startsWith("http") ? editorText : undefined} className="w-full mt-2" />
              </div>
            </div>
          ) : ["mp4", "webm"].includes(ext) ? (
            <div className="flex-1 flex flex-col items-center justify-center p-6 bg-zinc-950">
              <div className="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-2xl flex flex-col gap-3">
                <div className="flex items-center justify-between text-xs font-mono text-zinc-400 border-b border-zinc-800 pb-2">
                  <div className="flex items-center gap-2 text-cyan-300 font-bold">
                    <Film className="w-4 h-4 text-cyan-400" />
                    <span>Video Player: {activeFileNode?.name}</span>
                  </div>
                  <span className="px-2 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-800 rounded">1080p HD</span>
                </div>
                <video controls src={editorText.startsWith("http") ? editorText : "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"} className="w-full rounded-xl border border-zinc-800 max-h-[380px] bg-black" />
              </div>
            </div>
          ) : ["csv", "tsv"].includes(ext) ? (
            <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
              <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs">
                <div className="flex items-center gap-2 text-cyan-300 font-bold">
                  <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
                  <span>Structured CSV Grid: {activeFileNode?.name}</span>
                </div>
                <span className="text-zinc-500 font-mono">Rows: {editorText.split("\n").filter(Boolean).length - 1}</span>
              </div>
              <div className="flex-1 overflow-auto p-4">
                <table className="w-full border-collapse text-xs font-mono">
                  <thead>
                    <tr className="bg-zinc-900 text-cyan-300 border-b border-zinc-800 text-left">
                      {editorText.split("\n")[0]?.split(",").map((col, idx) => (
                        <th key={idx} className="p-2 border-r border-zinc-800 font-bold">{col.trim()}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {editorText.split("\n").slice(1).filter(Boolean).map((row, rIdx) => (
                      <tr key={rIdx} className="border-b border-zinc-850 hover:bg-zinc-900/60">
                        {row.split(",").map((val, cIdx) => (
                          <td key={cIdx} className="p-2 border-r border-zinc-850 text-zinc-300">{val.trim()}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : ext === "json" ? (
            <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
              <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs">
                <div className="flex items-center gap-2 text-cyan-300 font-bold">
                  <FileCode className="w-4 h-4 text-amber-400" />
                  <span>Formatted JSON: {activeFileNode?.name}</span>
                </div>
              </div>
              <div className="flex-1 overflow-auto p-4 font-mono text-xs text-amber-200/90 leading-6">
                <pre className="bg-zinc-900 p-4 rounded-xl border border-zinc-800 overflow-x-auto">
                  {(() => {
                    try { return JSON.stringify(JSON.parse(editorText), null, 2); } catch { return editorText; }
                  })()}
                </pre>
              </div>
            </div>
          ) : ["md", "txt"].includes(ext) ? (
            <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
              <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs">
                <div className="flex items-center gap-2 text-cyan-300 font-bold">
                  <FileText className="w-4 h-4 text-emerald-400" />
                  <span>Markdown Reader: {activeFileNode?.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => setMarkdownPreviewMode("rendered")} className={`px-2.5 py-1 rounded text-xs ${markdownPreviewMode === "rendered" ? "bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold" : "text-zinc-400"}`}>Formatted</button>
                  <button onClick={() => setMarkdownPreviewMode("raw")} className={`px-2.5 py-1 rounded text-xs ${markdownPreviewMode === "raw" ? "bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold" : "text-zinc-400"}`}>Raw</button>
                </div>
              </div>
              {markdownPreviewMode === "rendered" ? (
                <div className="flex-1 overflow-y-auto p-6 font-sans text-zinc-300 leading-relaxed max-w-4xl">
                  <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl shadow-xl space-y-4">
                    {editorText.split("\n").map((line, idx) => {
                      if (line.startsWith("# ")) return <h1 key={idx} className="text-2xl font-bold text-cyan-300 border-b border-zinc-800 pb-2">{line.slice(2)}</h1>;
                      if (line.startsWith("## ")) return <h2 key={idx} className="text-xl font-semibold text-zinc-100 mt-4">{line.slice(3)}</h2>;
                      if (line.startsWith("> ")) return <blockquote key={idx} className="border-l-4 border-cyan-500 pl-4 py-1 text-zinc-400 italic bg-zinc-950/60 rounded-r">{line.slice(2)}</blockquote>;
                      if (line.startsWith("- ")) return <li key={idx} className="ml-6 list-disc text-zinc-300">{line.slice(2)}</li>;
                      return <p key={idx} className="text-xs leading-relaxed">{line}</p>;
                    })}
                  </div>
                </div>
              ) : (
                <div className="flex-1 overflow-auto p-4 font-mono text-xs">
                  <textarea value={editorText} onChange={handleEditorChange} className="w-full h-full bg-transparent text-zinc-200 resize-none focus:outline-none" />
                </div>
              )}
            </div>
          ) : ext === "pdf" ? (
            <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
              <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs">
                <div className="flex items-center gap-2 text-rose-400 font-bold">
                  <FileText className="w-4 h-4" />
                  <span>PDF Document: {activeFileNode?.name}</span>
                </div>
                <span className="text-zinc-500 font-mono">Page 1 of 3</span>
              </div>
              <div className="flex-1 overflow-y-auto p-8 flex justify-center bg-zinc-900/60">
                <div className="w-full max-w-2xl bg-zinc-950 border border-zinc-800 rounded-xl p-8 shadow-2xl font-serif text-zinc-300 flex flex-col gap-4">
                  <div className="border-b border-zinc-800 pb-4 flex justify-between items-center font-sans">
                    <h2 className="text-xl font-bold text-cyan-300">Nexus Sovereign PDF Specification</h2>
                    <span className="text-xs text-zinc-500 font-mono">Kernel v13.0</span>
                  </div>
                  <p className="text-xs font-sans leading-relaxed text-zinc-300">
                    Sovereign document view for {activeFileNode?.name}.
                  </p>
                  <pre className="bg-zinc-900 p-4 rounded-lg font-mono text-[11px] text-zinc-400 overflow-x-auto">{editorText}</pre>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 relative flex bg-zinc-950 font-mono text-xs overflow-hidden no-scrollbar">
              <div className="w-12 bg-zinc-925/80 text-zinc-600 select-none py-3 pr-3 text-right font-mono border-r border-zinc-850 shrink-0">
                {lines.map((_, idx) => (
                  <div key={idx} className="leading-5">{idx + 1}</div>
                ))}
              </div>
              <div className="flex-1 relative overflow-auto p-3 no-scrollbar scrollbar-none">
                <textarea value={editorText} onChange={handleEditorChange} spellCheck={false} className="w-full h-full bg-transparent text-zinc-200 font-mono text-xs leading-5 resize-none focus:outline-none whitespace-pre no-scrollbar" />
              </div>
              <div className="hidden lg:block w-24 bg-zinc-925 border-l border-zinc-850 p-1 opacity-60 select-none overflow-hidden shrink-0 no-scrollbar scrollbar-none">
                {lines.slice(0, 40).map((line, i) => (
                  <div key={i} className="h-1 my-0.5 bg-zinc-700/50 rounded" style={{ width: `${Math.min(100, Math.max(10, line.length * 2))}%` }} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: INBUILT BROWSER & LIVE PREVIEW */}
      {activeTab === "browser" && (
        <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden font-mono">
          {/* Browser Navigation Bar */}
          <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-3 py-2 text-xs gap-2 shrink-0">
            <div className="flex items-center gap-1">
              <button onClick={() => setBrowserLogs((l) => [...l, "[BROWSER] Navigated Back"])} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-zinc-100" title="Back">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button onClick={() => setBrowserLogs((l) => [...l, "[BROWSER] Navigated Forward"])} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-zinc-100" title="Forward">
                <ChevronRight className="w-4 h-4" />
              </button>
              <button onClick={() => setBrowserLogs((l) => [...l, "[HMR] Refreshing page DOM..."])} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-zinc-100" title="Refresh">
                <RefreshCw className="w-4 h-4" />
              </button>
              <button onClick={() => setBrowserUrl("http://localhost:3000/app")} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-zinc-100" title="Home">
                <Home className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 max-w-xl flex items-center bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1 text-xs text-zinc-200 focus-within:border-cyan-400">
              <Globe className="w-3.5 h-3.5 text-emerald-400 shrink-0 mr-2" />
              <input type="text" value={browserUrl} onChange={(e) => setBrowserUrl(e.target.value)} className="w-full bg-transparent text-xs text-zinc-200 focus:outline-none" />
            </div>

            <div className="flex items-center gap-1 bg-zinc-950 border border-zinc-800 rounded-lg p-0.5 text-zinc-400">
              <button onClick={() => setBrowserDevice("desktop")} title="Desktop View" className={`p-1 rounded ${browserDevice === "desktop" ? "bg-cyan-950 text-cyan-300 font-bold" : "hover:bg-zinc-850"}`}>
                <Laptop className="w-3.5 h-3.5" />
              </button>
              <button onClick={() => setBrowserDevice("tablet")} title="Tablet View" className={`p-1 rounded ${browserDevice === "tablet" ? "bg-cyan-950 text-cyan-300 font-bold" : "hover:bg-zinc-850"}`}>
                <Tablet className="w-3.5 h-3.5" />
              </button>
              <button onClick={() => setBrowserDevice("mobile")} title="Mobile View" className={`p-1 rounded ${browserDevice === "mobile" ? "bg-cyan-950 text-cyan-300 font-bold" : "hover:bg-zinc-850"}`}>
                <Smartphone className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="flex items-center gap-1 text-zinc-400">
              <button onClick={() => setBrowserLogsOpen(!browserLogsOpen)} className={`px-2 py-1 rounded border text-[11px] flex items-center gap-1 transition-colors ${browserLogsOpen ? "bg-purple-950 border-purple-700 text-purple-300" : "bg-zinc-950 border-zinc-800 hover:text-zinc-200"}`}>
                <Terminal className="w-3 h-3" />
                <span>Console</span>
              </button>
              <a href={browserUrl} target="_blank" rel="noreferrer" className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-cyan-300" title="Open in new window">
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>

          <div className="flex-1 flex items-center justify-center bg-zinc-950 overflow-auto p-4">
            <div className={`bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden transition-all duration-300 h-full ${browserDevice === "mobile" ? "w-[375px] max-h-[667px]" : browserDevice === "tablet" ? "w-[768px] max-h-[800px]" : "w-full h-full"}`}>
              <div className="bg-zinc-925 border-b border-zinc-800 px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse" />
                  <span className="font-bold text-sm text-zinc-100 tracking-wide font-sans">NEXUS-AOS Live App Instance</span>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono">PORT 3000 • ONLINE</span>
              </div>
              <div className="flex-1 p-6 font-sans overflow-y-auto text-zinc-200 flex flex-col gap-6">
                <div className="bg-gradient-to-r from-cyan-950/80 to-purple-950/80 border border-cyan-500/40 rounded-2xl p-6 shadow-xl">
                  <h2 className="text-xl font-bold text-white mb-2">Welcome to Nexus Sovereign Operating Environment</h2>
                  <p className="text-xs text-zinc-300 leading-relaxed max-w-xl">This in-built browser renders real-time web previews, API test routes, and hot-module replaced interfaces directly inside your sovereign workspace.</p>
                  <div className="mt-4 flex items-center gap-3">
                    <button onClick={() => { setBrowserCounter((c) => c + 1); setBrowserLogs((l) => [...l, `[CLICK] Interactive state updated to ${browserCounter + 1}`]); }} className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-semibold shadow transition-colors">
                      Interactive Action Count: {browserCounter}
                    </button>
                    <button onClick={() => setBrowserLogs((l) => [...l, "[TEST] Simulated API GET /api/v1/ping -> 200 OK"])} className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-xl text-xs font-medium border border-zinc-700">
                      Trigger API Ping
                    </button>
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-zinc-925 border border-zinc-800 rounded-xl p-4">
                    <span className="text-xs text-zinc-500 font-mono">SERVER STATUS</span>
                    <h3 className="text-lg font-bold text-emerald-400 font-mono mt-1">200 OK</h3>
                    <p className="text-[11px] text-zinc-400 mt-1">Latency: 1.2ms</p>
                  </div>
                  <div className="bg-zinc-925 border border-zinc-800 rounded-xl p-4">
                    <span className="text-xs text-zinc-500 font-mono">WEBSOCKET SIGNAL</span>
                    <h3 className="text-lg font-bold text-cyan-400 font-mono mt-1">ACTIVE</h3>
                    <p className="text-[11px] text-zinc-400 mt-1">Packets: 12,480</p>
                  </div>
                  <div className="bg-zinc-925 border border-zinc-800 rounded-xl p-4">
                    <span className="text-xs text-zinc-500 font-mono">FRAME TIME</span>
                    <h3 className="text-lg font-bold text-purple-400 font-mono mt-1">60.0 FPS</h3>
                    <p className="text-[11px] text-zinc-400 mt-1">Zero drop rate</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {browserLogsOpen && (
            <div className="h-40 bg-zinc-950 border-t border-zinc-800 p-3 flex flex-col font-mono text-xs shrink-0">
              <div className="flex items-center justify-between pb-1 border-b border-zinc-800 text-zinc-400 text-[11px]">
                <span className="font-bold text-purple-400">INBUILT BROWSER CONSOLE</span>
                <button onClick={() => setBrowserLogs([])} className="hover:text-zinc-200">Clear Console</button>
              </div>
              <div className="flex-1 overflow-y-auto pt-2 space-y-1 text-zinc-300">
                {browserLogs.map((log, idx) => (
                  <div key={idx} className="leading-relaxed text-[11px] text-cyan-300/90">{log}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: NEXUS CHAT */}
      {activeTab === "chat" && (
        <div className="flex-1 flex flex-col bg-zinc-950 overflow-hidden">
          {/* Chat Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
            {chatMessages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 max-w-3xl ${
                  msg.sender === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
                }`}
              >
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border shadow-sm ${
                    msg.sender === "user"
                      ? "bg-cyan-950 border-cyan-700 text-cyan-300"
                      : "bg-purple-950 border-purple-700 text-purple-300"
                  }`}
                >
                  {msg.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                <div
                  className={`p-3.5 rounded-xl border text-xs leading-relaxed max-w-2xl font-sans ${
                    msg.sender === "user"
                      ? "bg-cyan-950/60 border-cyan-800/80 text-zinc-100"
                      : "bg-zinc-900 border-zinc-800 text-zinc-200"
                  }`}
                >
                  <div className="flex items-center justify-between border-b border-zinc-800/60 pb-1.5 mb-2 font-mono text-[10px] text-zinc-400">
                    <span className="font-bold uppercase tracking-wide">
                      {msg.sender === "user" ? "Sovereign Master" : "Nexus AI Companion"}
                    </span>
                    <span>{msg.timestamp}</span>
                  </div>

                  <p className="whitespace-pre-wrap">{msg.text}</p>

                  {msg.codeSnippet && (
                    <div className="mt-3 bg-zinc-950 border border-zinc-800 rounded-lg p-2.5 font-mono text-[11px] text-cyan-300 overflow-x-auto">
                      <pre>{msg.codeSnippet}</pre>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Chat Input Bar */}
          <form onSubmit={handleChatSubmit} className="p-3 bg-zinc-925 border-t border-zinc-800 flex gap-2">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder={`Ask Nexus about ${activeFileNode?.name || "workspace code"}, request edits, or run tests...`}
              className="flex-1 bg-zinc-900 border border-zinc-750 focus:border-purple-500 rounded-lg px-3 py-2 text-xs text-zinc-100 focus:outline-none font-mono"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors shadow"
            >
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      )}

      {/* TAB 3: DIFF / REVIEW */}
      {activeTab === "diff" && (
        <div className="flex-1 p-4 bg-zinc-950 overflow-y-auto flex flex-col gap-4 font-mono text-xs">
          <div className="flex items-center justify-between bg-zinc-900 p-3 rounded-lg border border-zinc-800">
            <div>
              <h3 className="font-bold text-zinc-100 text-sm">Git Workspace Review & Diff</h3>
              <p className="text-zinc-400 text-xs">Reviewing modified file: nexus_aos/src/main.py</p>
            </div>
            <div className="flex gap-2">
              <button className="px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded font-sans text-xs font-semibold flex items-center gap-1">
                <Check className="w-3.5 h-3.5" />
                <span>Accept Changes</span>
              </button>
              <button className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-sans text-xs">
                Revert
              </button>
            </div>
          </div>

          {/* Unified Diff View Simulation */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden">
            <div className="bg-zinc-925 px-3 py-2 border-b border-zinc-800 text-zinc-400 font-bold">
              --- a/nexus_aos/src/main.py +++ b/nexus_aos/src/main.py
            </div>
            <div className="p-3 leading-6">
              <div className="text-zinc-500">@@ -8,6 +8,10 @@ def evolve():</div>
              <div className="text-zinc-300"> orchestrator = OrchestratorEngine()</div>
              <div className="text-zinc-300"> vitals = HostVitalsMonitor()</div>
              <div className="bg-rose-950/60 text-rose-300 -mx-3 px-3 border-l-4 border-rose-500">
                - print("[NEXUS-AOS] Bootstrapping Loop...")
              </div>
              <div className="bg-emerald-950/60 text-emerald-300 -mx-3 px-3 border-l-4 border-emerald-500">
                + print("[NEXUS-AOS] Bootstrapping Homeostatic Control Loop with Ischemia patrol...")
              </div>
              <div className="text-zinc-300"> while True:</div>
              <div className="text-zinc-300"> state = vitals.scan_host()</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: DOCUMENTATION */}
      {activeTab === "docs" && (
        <div className="flex-1 p-6 bg-zinc-950 overflow-y-auto text-zinc-300 font-sans leading-relaxed">
          <div className="max-w-3xl mx-auto flex flex-col gap-4">
            <h1 className="text-2xl font-bold text-cyan-400 border-b border-zinc-800 pb-2">
              Nexus-AOS Architecture Documentation
            </h1>
            <p className="text-sm text-zinc-400">
              Nexus-AOS operates as a dual-interface intelligence platform combining Sovereign Terminal for master user control and Nexus Core for LLM orchestration.
            </p>

            <h2 className="text-lg font-semibold text-zinc-100 mt-2">Architecture Diagram</h2>
            <div className="bg-zinc-900 border border-zinc-800 p-4 rounded-xl font-mono text-xs text-cyan-300">
              <pre>{`┌─────────────────────────────────────────────────────────────┐
│                   SOVEREIGN TERMINAL                        │
│   ┌───────────────┬───────────────────┬──────────────────┐  │
│   │ L1: Explorer  │ L2: Workspace     │ L3: Tools Panel  │  │
│   │  (Pet Dock)   │ (Editor/Chat/Diff)│ (MCP/DB/Git)     │  │
│   └───────────────┴───────────────────┴──────────────────┘  │
│                   L4: Bottom Tool Window                     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Shared State Protocol
┌──────────────────────────────▼──────────────────────────────┐
│                      NEXUS CORE (LLM)                       │
│     Vitals • Directive Queue • Active Biosignals • Instincts  │
└─────────────────────────────────────────────────────────────┘`}</pre>
            </div>
          </div>
        </div>
      )}
    </main>
  );
});

L2Workspace.displayName = "L2Workspace";
