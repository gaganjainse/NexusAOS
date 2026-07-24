import React, { useState } from "react";
import {
  FileNode,
  Directive,
  AOSService,
  PetStatus,
} from "../../types/Sesha";
import { PetCompanion } from "../pet/PetCompanion";
import {
  Folder,
  FolderOpen,
  FileCode,
  FileText,
  ChevronRight,
  ChevronDown,
  Plus,
  Play,
  RotateCcw,
  Search,
  CheckCircle2,
  Clock,
  AlertOctagon,
  Activity,
  Server,
  Layers,
  Sparkles,
  GitCommit,
  Filter,
  X,
} from "lucide-react";

interface L1ExplorerPanelProps {
  files: FileNode[];
  directives: Directive[];
  services: AOSService[];
  petStatus: PetStatus;
  activeFile: string;
  onSelectFile: (fileNode: FileNode) => void;
  onUpdatePetStatus: (newStatus: Partial<PetStatus>) => void;
  onOpenFullPet: () => void;
  onResubmitDirective: (text: string) => void;
  onClosePanel?: () => void;
  activeTab?: "project" | "directives" | "system";
}

export const L1ExplorerPanel: React.FC<L1ExplorerPanelProps> = React.memo(({
  files,
  directives,
  services,
  petStatus,
  activeFile,
  onSelectFile,
  onUpdatePetStatus,
  onOpenFullPet,
  onResubmitDirective,
  onClosePanel,
  activeTab = "project",
}) => {
  const [expandedFolders, setExpandedFolders] = useState<Record<string, boolean>>({
    Sesha_aos: true,
    "Sesha_aos/src": true,
  });
  const [directiveFilter, setDirectiveFilter] = useState("");
  const [expandedDirectiveId, setExpandedDirectiveId] = useState<string | null>("DIR-101");
  const [selectedService, setSelectedService] = useState<AOSService | null>(null);

  const toggleFolder = (path: string) => {
    setExpandedFolders((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  const renderFileTree = (nodes: FileNode[], level = 0) => {
    return nodes.map((node) => {
      const isExpanded = expandedFolders[node.path];
      const isSelected = activeFile === node.path;

      if (node.type === "folder") {
        return (
          <div key={node.path} className="select-none">
            <div
              onClick={() => toggleFolder(node.path)}
              className="flex items-center gap-1.5 px-2 py-1 hover:bg-zinc-850 rounded cursor-pointer text-xs text-zinc-300 font-mono"
              style={{ paddingLeft: `${level * 12 + 8}px` }}
            >
              {isExpanded ? (
                <ChevronDown className="w-3.5 h-3.5 text-zinc-500 shrink-0" />
              ) : (
                <ChevronRight className="w-3.5 h-3.5 text-zinc-500 shrink-0" />
              )}
              {isExpanded ? (
                <FolderOpen className="w-4 h-4 text-cyan-400 shrink-0" />
              ) : (
                <Folder className="w-4 h-4 text-cyan-500 shrink-0" />
              )}
              <span className="font-semibold text-zinc-200">{node.name}</span>
            </div>
            {isExpanded && node.children && (
              <div>{renderFileTree(node.children, level + 1)}</div>
            )}
          </div>
        );
      }

      const getGitBadge = (status?: string) => {
        if (status === "M") return <span className="text-[10px] font-mono text-amber-400 font-bold ml-auto">M</span>;
        if (status === "A") return <span className="text-[10px] font-mono text-emerald-400 font-bold ml-auto">A</span>;
        if (status === "D") return <span className="text-[10px] font-mono text-rose-400 font-bold ml-auto">D</span>;
        return null;
      };

      return (
        <div
          key={node.path}
          draggable
          onDragStart={(e) => {
            e.dataTransfer.setData("application/json", JSON.stringify(node));
            e.dataTransfer.setData("text/plain", node.path);
          }}
          onClick={() => onSelectFile(node)}
          className={`flex items-center gap-1.5 px-2 py-1 hover:bg-zinc-800 rounded cursor-grab active:cursor-grabbing text-xs font-mono transition-colors ${
            isSelected
              ? "bg-cyan-950/80 text-cyan-300 border-l-2 border-cyan-400 font-medium"
              : "text-zinc-400 hover:text-zinc-200"
          }`}
          style={{ paddingLeft: `${level * 12 + 20}px` }}
        >
          <FileCode className="w-3.5 h-3.5 text-cyan-400/80 shrink-0" />
          <span className="truncate">{node.name}</span>
          {getGitBadge(node.gitStatus)}
        </div>
      );
    });
  };

  const filteredDirectives = directives.filter((d) =>
    d.text.toLowerCase().includes(directiveFilter.toLowerCase())
  );

  return (
    <aside className="w-full h-full bg-[#120a06]/95 rounded-2xl border-2 border-amber-800/60 flex flex-col select-none overflow-hidden shadow-2xl relative oil-lamp-glow ring-1 ring-amber-500/20 backdrop-blur-md">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-amber-800/60 bg-[#1f1712] px-3 py-2 text-xs font-mono shrink-0">
        <div className="flex items-center gap-2 font-bold text-amber-300 tracking-wider">
          {activeTab === "project" && (
            <>
              <Folder className="w-3.5 h-3.5 text-cyan-400" />
              <span>PROJECT EXPLORER</span>
            </>
          )}
          {activeTab === "directives" && (
            <>
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span>DIRECTIVES QUEUE</span>
            </>
          )}
          {activeTab === "system" && (
            <>
              <Server className="w-3.5 h-3.5 text-emerald-400" />
              <span>AOS SERVICES</span>
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

      {/* Main Tab Content Area */}
      <div className="flex-1 overflow-y-auto p-2">
        {/* TAB 1: Project Explorer */}
        {activeTab === "project" && (
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono px-2 py-1 uppercase tracking-wider">
              <span>Project Files</span>
              <div className="flex items-center gap-1 text-zinc-500">
                <button title="New File" className="hover:text-zinc-200 p-0.5">
                  <Plus className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
            {renderFileTree(files)}
          </div>
        )}

        {/* TAB 2: Directive History */}
        {activeTab === "directives" && (
          <div className="flex flex-col gap-2">
            {/* Search filter */}
            <div className="flex items-center bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-xs">
              <Search className="w-3.5 h-3.5 text-zinc-500 mr-1.5" />
              <input
                type="text"
                value={directiveFilter}
                onChange={(e) => setDirectiveFilter(e.target.value)}
                placeholder="Filter history..."
                className="w-full bg-transparent text-zinc-200 focus:outline-none text-xs font-mono"
              />
            </div>

            {/* Directives List */}
            <div className="flex flex-col gap-2 mt-1">
              {filteredDirectives.map((d) => {
                const isExpanded = expandedDirectiveId === d.id;
                return (
                  <div
                    key={d.id}
                    className="p-2.5 bg-zinc-900/80 border border-zinc-800 rounded-lg flex flex-col gap-2 transition-all hover:border-zinc-700"
                  >
                    <div
                      onClick={() => setExpandedDirectiveId(isExpanded ? null : d.id)}
                      className="flex items-start justify-between cursor-pointer"
                    >
                      <div className="flex items-center gap-1.5">
                        <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 border border-cyan-800/60 px-1.5 py-0.5 rounded">
                          {d.id}
                        </span>
                        <span className="text-xs font-semibold text-zinc-200 line-clamp-1">
                          {d.text}
                        </span>
                      </div>
                      <span
                        className={`text-[9px] font-mono px-1.5 py-0.5 rounded-full uppercase border ${
                          d.status === "Completed"
                            ? "bg-emerald-950 text-emerald-400 border-emerald-800"
                            : "bg-amber-950 text-amber-400 border-amber-800"
                        }`}
                      >
                        {d.status}
                      </span>
                    </div>

                    {isExpanded && (
                      <div className="pt-2 border-t border-zinc-800/80 flex flex-col gap-2 text-xs font-mono">
                        <p className="text-zinc-300 font-sans text-xs bg-zinc-950 p-2 rounded border border-zinc-850">
                          "{d.text}"
                        </p>

                        <div>
                          <span className="text-[10px] text-zinc-500 uppercase tracking-wider block mb-1">
                            Dispatched Sub-tasks
                          </span>
                          <div className="flex flex-col gap-1">
                            {d.subtasks.map((st, idx) => (
                              <div key={idx} className="flex items-center gap-1.5 text-[11px] text-zinc-400">
                                <CheckCircle2 className="w-3 h-3 text-emerald-400 shrink-0" />
                                <span>{st.text}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {d.outcome && (
                          <div className="bg-cyan-950/40 border border-cyan-800/40 p-2 rounded text-[11px] text-cyan-300">
                            <strong>Outcome:</strong> {d.outcome}
                          </div>
                        )}

                        <div className="flex items-center justify-between pt-1">
                          <span className="text-[10px] text-zinc-500">{d.timestamp}</span>
                          <button
                            onClick={() => onResubmitDirective(d.text)}
                            className="flex items-center gap-1 px-2 py-0.5 bg-zinc-800 hover:bg-cyan-900 hover:text-cyan-200 text-zinc-300 text-[10px] rounded transition-colors"
                          >
                            <RotateCcw className="w-3 h-3" />
                            <span>Re-submit</span>
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 3: System Overview (AOS Services) */}
        {activeTab === "system" && (
          <div className="flex flex-col gap-2">
            <span className="text-[11px] text-zinc-500 font-mono px-2 py-1 uppercase tracking-wider">
              AOS Runtime Services
            </span>

            <div className="flex flex-col gap-2">
              {services.map((svc) => (
                <div
                  key={svc.name}
                  onClick={() => setSelectedService(selectedService?.name === svc.name ? null : svc)}
                  className={`p-2.5 bg-zinc-900 border rounded-lg cursor-pointer transition-all ${
                    selectedService?.name === svc.name
                      ? "border-cyan-500 bg-cyan-950/30"
                      : "border-zinc-800 hover:border-zinc-700"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span className="text-xs font-bold text-zinc-100 font-mono">{svc.name}</span>
                    </div>
                    <span className="text-[10px] font-mono text-zinc-400">{svc.uptime}</span>
                  </div>

                  <p className="text-[11px] text-zinc-400 mt-1">{svc.description}</p>

                  <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500 mt-2 pt-1 border-t border-zinc-800/60">
                    <span>Last tick: {svc.lastTick}</span>
                    <span className="text-emerald-400 uppercase">{svc.status}</span>
                  </div>

                  {selectedService?.name === svc.name && (
                    <div className="mt-2 pt-2 border-t border-zinc-800 bg-zinc-950 p-2 rounded text-[10px] font-mono text-cyan-300 flex flex-col gap-1 max-h-32 overflow-y-auto">
                      <span className="text-zinc-500 uppercase">Recent Service Logs:</span>
                      {svc.logs.map((log, idx) => (
                        <div key={idx} className="text-zinc-400 truncate">
                          {log}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Pet Status Dock at Bottom of L1 */}
      <PetCompanion
        status={petStatus}
        compact={true}
        onOpenFull={onOpenFullPet}
        onUpdateStatus={onUpdatePetStatus}
      />
    </aside>
  );
});

L1ExplorerPanel.displayName = "L1ExplorerPanel";

