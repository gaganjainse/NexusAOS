import React, { useState } from "react";
import { CoreWorkspaceState, VitalsData, MCPTool } from "../../types/nexus";
import {
  Cpu,
  Zap,
  Activity,
  HardDrive,
  Flame,
  Brain,
  Sparkles,
  Layers,
  FileCode,
  Wrench,
  CheckSquare,
  Square,
  Clock,
  ShieldAlert,
  Server,
  ArrowUpRight,
  Terminal,
} from "lucide-react";

interface NexusCoreWorkspaceProps {
  coreState: CoreWorkspaceState;
  vitals: VitalsData;
  tools: MCPTool[];
  onToggleSubtask: (index: number) => void;
  onExecuteToolCommand: (cmd: string) => void;
}

export const NexusCoreWorkspace: React.FC<NexusCoreWorkspaceProps> = ({
  coreState,
  vitals,
  tools,
  onToggleSubtask,
  onExecuteToolCommand,
}) => {
  const [leftWidth, setLeftWidth] = useState(300);
  const [rightWidth, setRightWidth] = useState(280);
  const isDraggingLeft = React.useRef(false);
  const isDraggingRight = React.useRef(false);

  const paletteCmds = [
    "/motor",
    "/lattice",
    "/immune",
    "/memory",
    "/evolve",
    "/endocrine",
    "/physiology",
    "/vision",
    "/mesh",
  ];

  // Mouse move handlers for resizable panels
  const handleMouseDownLeft = (e: React.MouseEvent) => {
    e.preventDefault();
    isDraggingLeft.current = true;
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
  };

  const handleMouseDownRight = (e: React.MouseEvent) => {
    e.preventDefault();
    isDraggingRight.current = true;
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (isDraggingLeft.current) {
      setLeftWidth(Math.max(220, Math.min(450, e.clientX - 16)));
    } else if (isDraggingRight.current) {
      const newWidth = window.innerWidth - e.clientX - 16;
      setRightWidth(Math.max(220, Math.min(450, newWidth)));
    }
  };

  const handleMouseUp = () => {
    isDraggingLeft.current = false;
    isDraggingRight.current = false;
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);
  };

  return (
    <div className="flex-1 bg-[#120c08] font-mono text-xs flex flex-col h-full overflow-hidden text-stone-300 select-none transition-all duration-300 p-2 gap-2">
      {/* Top Banner Header - Temple Sanctum Garbhagriha */}
      <div className="px-4 py-2 bg-[#1f1610] border-2 border-amber-800/60 rounded-xl flex items-center justify-between shrink-0 shilpkari-concave oil-lamp-glow">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-lg bg-amber-950 border border-amber-500 flex items-center justify-center text-amber-300 font-bold shadow-md">
            <Cpu className="w-4 h-4 text-amber-400 animate-pulse" />
          </div>
          <div>
            <span className="font-bold text-amber-300 text-sm tracking-wide">
              NEXUS CORE: GARBHAGRIHA SANCTUM v13.0
            </span>
            <span className="text-[10px] text-amber-500/80 ml-2 font-semibold">
              [Golden Ratio φ 1.618 Sacred Intelligence Environment]
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="text-stone-400">
            Vital Energy: <strong className="text-amber-400">{vitals.energy}%</strong>
          </span>
          <span className="text-stone-400">
            Harmonic Balance: <strong className="text-emerald-400">{vitals.status}</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-amber-950/80 text-amber-200 border border-amber-600/80 text-[10px] font-bold shadow-sm">
            SYNCHRONIZED WITH SOVEREIGN MANDAPA
          </span>
        </div>
      </div>

      {/* Resizable 3-Column Layout */}
      <div className="flex-1 flex overflow-hidden gap-2">
        {/* COLUMN 1: STATE PANEL (Left Resizable Workspace) */}
        <aside
          style={{ width: `${leftWidth}px` }}
          className="bg-[#17110c] border-2 border-amber-800/60 rounded-2xl p-3 overflow-y-auto flex flex-col gap-4 shrink-0 shilpkari-concave oil-lamp-glow no-scrollbar"
        >
          {/* Vitals Summary */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider flex items-center justify-between">
              <span>Temple System Vitals</span>
              <Activity className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
            </span>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-[#140e0a] p-2 rounded-lg border border-amber-900/40">
                <span className="text-[10px] text-stone-500 block">Vital Energy</span>
                <span className="text-amber-400 font-bold">{vitals.energy}%</span>
              </div>
              <div className="bg-[#140e0a] p-2 rounded-lg border border-amber-900/40">
                <span className="text-[10px] text-stone-500 block">Ischemia</span>
                <span className="text-rose-400 font-bold">{vitals.diskC}%</span>
              </div>
              <div className="bg-[#140e0a] p-2 rounded-lg border border-amber-900/40">
                <span className="text-[10px] text-stone-500 block">Temperature</span>
                <span className="text-orange-400 font-bold">{vitals.fever}°C</span>
              </div>
              <div className="bg-[#140e0a] p-2 rounded-lg border border-amber-900/40">
                <span className="text-[10px] text-stone-500 block">Vibe Resonance</span>
                <span className="text-emerald-400 font-bold">+{vitals.vibe}</span>
              </div>
            </div>
          </div>

          {/* Active Biosignals */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider">
              Harmonic Biosignals
            </span>
            <div className="flex flex-col gap-1.5">
              {coreState.activeSignals.map((sig, idx) => (
                <div
                  key={idx}
                  className="p-1.5 bg-[#140e0a] border border-amber-900/30 rounded-lg flex items-center justify-between text-[11px]"
                >
                  <span className="font-bold text-amber-200">{sig.signal}</span>
                  <span className="text-amber-300">{sig.level}</span>
                  <span className="text-[9px] text-stone-500">{sig.status}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Active Agents */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider">
              Coordinated Guardians
            </span>
            <div className="flex flex-col gap-1.5">
              {coreState.agents.map((ag) => (
                <div
                  key={ag.name}
                  className="p-1.5 bg-[#140e0a] border border-amber-900/30 rounded-lg flex items-center justify-between text-[11px]"
                >
                  <div>
                    <span className="font-bold text-stone-200 block">{ag.name}</span>
                    <span className="text-[9px] text-stone-500">{ag.type}</span>
                  </div>
                  <span className="text-emerald-400 text-[10px] font-semibold">{ag.status} ({ag.load})</span>
                </div>
              ))}
            </div>
          </div>

          {/* Active Instinct Drives */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider">
              Sacred Instinct Drives
            </span>
            <div className="flex flex-col gap-1.5">
              {coreState.instincts.map((ins) => (
                <div key={ins.name} className="flex flex-col gap-1">
                  <div className="flex justify-between text-[10px]">
                    <span className="text-stone-300">{ins.name}</span>
                    <span className="text-amber-400 font-bold">{(ins.weight * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-[#140e0a] rounded-full h-1.5 overflow-hidden border border-amber-900/30">
                    <div
                      className="h-full bg-gradient-to-r from-amber-600 to-amber-400 rounded-full"
                      style={{ width: `${ins.weight * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* Drag Handle 1 */}
        <div
          onMouseDown={handleMouseDownLeft}
          className="w-1.5 hover:w-2 bg-amber-900/40 hover:bg-amber-500/80 cursor-col-resize transition-all rounded-full shrink-0"
        />

        {/* COLUMN 2: CENTER WORKSPACE */}
        <main className="flex-1 p-4 bg-[#140e0b] border-2 border-amber-800/60 rounded-2xl overflow-y-auto flex flex-col gap-4 shilpkari-concave oil-lamp-glow no-scrollbar">
          {/* Focus Bar */}
          <div className="p-2.5 bg-[#1e1610] border border-amber-800/50 rounded-xl flex items-center justify-between shadow-md">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold text-amber-300 uppercase bg-amber-950 px-2.5 py-0.5 rounded-md border border-amber-600/80">
                Sanctum Focus
              </span>
              <span className="text-xs text-stone-100 font-bold">{coreState.focusFile}</span>
            </div>
            <span className="text-[10px] text-stone-500 font-mono">Golden Ratio Schema v13.0</span>
          </div>

          {/* Current Directive Board */}
          <div className="p-4 bg-[#1b130e] border border-amber-800/60 rounded-2xl flex flex-col gap-3 shadow-xl">
            <div className="flex items-center justify-between border-b border-amber-900/40 pb-2">
              <span className="text-xs font-bold text-amber-300 uppercase tracking-wide flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" /> Sacred Master Directive
              </span>
              <span className="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded-md font-semibold">
                Harmonizing
              </span>
            </div>

            <p className="text-sm font-sans text-stone-100 bg-[#140e0a] p-3.5 rounded-xl border border-amber-900/40 leading-relaxed shadow-inner">
              "{coreState.directiveBoard.currentDirective}"
            </p>

            <div className="flex flex-col gap-2 mt-1">
              <span className="text-[10px] text-stone-400 uppercase tracking-wider font-semibold">Sub-Tasks Dispatched</span>
              <div className="flex flex-col gap-1.5">
                {coreState.directiveBoard.subtasks.map((st, idx) => (
                  <div
                    key={idx}
                    onClick={() => onToggleSubtask(idx)}
                    className="flex items-center gap-2 p-2.5 bg-[#140e0a] border border-stone-800 hover:border-amber-600/80 rounded-xl hover:bg-amber-950/40 cursor-pointer text-xs transition-colors"
                  >
                    {st.done ? (
                      <CheckSquare className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <Square className="w-4 h-4 text-stone-600 shrink-0" />
                    )}
                    <span className={st.done ? "line-through text-stone-500" : "text-stone-200"}>
                      {st.text}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Tool Palette Bar */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 uppercase font-bold tracking-wider">
              AOS Service Tools Palette
            </span>
            <div className="flex items-center gap-1.5 flex-wrap">
              {paletteCmds.map((cmd) => (
                <button
                  key={cmd}
                  onClick={() => onExecuteToolCommand(cmd)}
                  className="px-3 py-1 bg-[#140e0a] hover:bg-amber-950 hover:text-amber-200 border border-stone-800 hover:border-amber-600/80 text-stone-300 rounded-lg text-xs font-semibold transition-colors"
                >
                  <strong className="text-amber-400">{cmd}</strong>
                </button>
              ))}
            </div>
          </div>

          {/* Memory Stream Artifacts */}
          <div className="p-3 bg-[#1e1610] border border-amber-800/50 rounded-xl flex flex-col gap-2 shadow-md">
            <span className="text-[10px] text-amber-400 uppercase font-bold tracking-wider">
              Memory Stream & Wisdom Artifacts
            </span>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {coreState.memoryStream.map((mem, idx) => (
                <div key={idx} className="p-2.5 bg-[#140e0a] border border-amber-900/30 rounded-xl flex flex-col gap-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-stone-200">{mem.title}</span>
                    <span className="text-[9px] px-2 py-0.5 rounded-md bg-amber-950 text-amber-300 border border-amber-800 font-semibold">
                      {mem.category}
                    </span>
                  </div>
                  <span className="text-[10px] text-stone-500">{mem.file} • {mem.date}</span>
                </div>
              ))}
            </div>
          </div>
        </main>

        {/* Drag Handle 2 */}
        <div
          onMouseDown={handleMouseDownRight}
          className="w-1.5 hover:w-2 bg-amber-900/40 hover:bg-amber-500/80 cursor-col-resize transition-all rounded-full shrink-0"
        />

        {/* COLUMN 3: REAL-TIME PULSE LOG (Right Resizable Workspace) */}
        <aside
          style={{ width: `${rightWidth}px` }}
          className="bg-[#17110c] border-2 border-amber-800/60 rounded-2xl p-3 overflow-y-auto flex flex-col gap-3 shrink-0 shilpkari-concave oil-lamp-glow no-scrollbar"
        >
          <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider flex items-center justify-between">
            <span>Real-time Pulse Log</span>
            <Terminal className="w-3.5 h-3.5 text-amber-400" />
          </span>

          <div className="flex flex-col gap-1.5">
            {coreState.pulseLog.map((log, idx) => (
              <div
                key={idx}
                className="p-2 bg-[#1e1610] border border-stone-800/80 rounded-lg text-[11px] leading-relaxed shadow-sm"
              >
                <div className="flex items-center justify-between text-[9px] text-stone-500 mb-0.5">
                  <span>{log.time}</span>
                  <span className="uppercase text-amber-400 font-bold">{log.category}</span>
                </div>
                <p className="text-stone-300">{log.text}</p>
              </div>
            ))}
          </div>
        </aside>
      </div>
    </div>
  );
};
