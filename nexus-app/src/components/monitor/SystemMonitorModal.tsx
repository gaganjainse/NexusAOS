import React, { useState, useEffect } from "react";
import { VitalsData, SystemProcess } from "../../types/nexus";
import {
  X,
  RefreshCw,
  HardDrive,
  Cpu,
  Wifi,
  Activity,
  Zap,
  Shield,
  Flame,
  Wind,
  CheckCircle2,
  AlertTriangle,
  Play,
  Grid,
  Compass,
} from "lucide-react";

interface SystemMonitorModalProps {
  isOpen: boolean;
  onClose: () => void;
  vitals: VitalsData;
  processes: SystemProcess[];
  onTriggerAction: (actionName: string) => void;
  geometryConfig?: {
    showGrid: boolean;
    showSpiral: boolean;
    showMandapa: boolean;
    showPortalMandala: boolean;
    enableAnimations: boolean;
  };
  onToggleGeometry?: (key: "showGrid" | "showSpiral" | "showMandapa" | "showPortalMandala" | "enableAnimations") => void;
  mantraBlend?: number;
  onMantraBlendChange?: (blend: number) => void;
}

export const SystemMonitorModal: React.FC<SystemMonitorModalProps> = ({
  isOpen,
  onClose,
  vitals,
  processes,
  onTriggerAction,
  geometryConfig = {
    showGrid: false,
    showSpiral: false,
    showMandapa: false,
    showPortalMandala: false,
    enableAnimations: true,
  },
  onToggleGeometry,
  mantraBlend = 0.5,
  onMantraBlendChange,
}) => {
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date().toLocaleTimeString());
  const [activeTab, setActiveTab] = useState<"telemetry" | "sanctum_history">("telemetry");

  // Sanctum History Vibe Fluctuations with Ink-Wash Brushstroke Data
  const [historyRecords] = useState([
    { time: "07:48:09", vibe: 98, energy: 95, state: "Sublime Resonance", strokeWidth: 16, inkColor: "from-amber-500/90 via-amber-700/60 to-transparent" },
    { time: "07:32:15", vibe: 94, energy: 88, state: "Harmonic Equilibrium", strokeWidth: 12, inkColor: "from-amber-600/80 via-orange-900/50 to-transparent" },
    { time: "07:18:40", vibe: 86, energy: 72, state: "Sanctum Ischemia Surge", strokeWidth: 20, inkColor: "from-rose-600/90 via-red-950/70 to-transparent" },
    { time: "07:04:10", vibe: 96, energy: 91, state: "Garbhagriha Recalibration", strokeWidth: 14, inkColor: "from-emerald-500/80 via-teal-950/50 to-transparent" },
    { time: "06:48:00", vibe: 91, energy: 82, state: "Sovereign AOS Genesis", strokeWidth: 10, inkColor: "from-cyan-500/80 via-blue-950/50 to-transparent" },
  ]);

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      setLastUpdated(new Date().toLocaleTimeString());
    }, 2000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto font-mono select-none">
      <div className="bg-zinc-950 border border-zinc-800 rounded-lg w-full max-w-5xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-3.5 bg-zinc-925 border-b border-zinc-800 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-cyan-400" />
              <h2 className="text-base font-bold text-zinc-100 tracking-wide">
                NEXUS SYSTEM MONITOR
              </h2>
            </div>

            {/* Modal Navigation Tabs */}
            <div className="flex items-center bg-zinc-900 border border-zinc-800 rounded-lg p-0.5 text-xs">
              <button
                onClick={() => setActiveTab("telemetry")}
                className={`px-3 py-1 rounded font-bold transition-all cursor-pointer ${
                  activeTab === "telemetry"
                    ? "bg-amber-950 text-amber-300 border border-amber-600/80 shadow"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                Host Telemetry
              </button>
              <button
                onClick={() => setActiveTab("sanctum_history")}
                className={`px-3 py-1 rounded font-bold transition-all cursor-pointer ${
                  activeTab === "sanctum_history"
                    ? "bg-amber-950 text-amber-300 border border-amber-600/80 shadow"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                Sanctum History
              </button>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs">
            <span className="text-zinc-500">Last update: {lastUpdated}</span>
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`px-2.5 py-1 rounded border transition-colors cursor-pointer ${
                autoRefresh
                  ? "bg-cyan-950 border-cyan-700 text-cyan-300"
                  : "bg-zinc-900 border-zinc-800 text-zinc-500"
              }`}
            >
              {autoRefresh ? "Auto Refresh: ON" : "Auto Refresh: OFF"}
            </button>
            <button
              onClick={onClose}
              className="p-1 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        {activeTab === "telemetry" ? (
          <div className="p-6 overflow-y-auto flex flex-col gap-6 text-xs text-zinc-300">
          {/* Top 4 Hardware Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* DISK */}
            <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-2 shadow">
              <div className="flex items-center justify-between text-zinc-400 font-bold">
                <span className="flex items-center gap-1.5 text-cyan-400">
                  <HardDrive className="w-4 h-4" /> DISK C: / D:
                </span>
                <span className="text-amber-400">{vitals.diskC}%</span>
              </div>
              <div className="w-full bg-zinc-950 rounded-full h-2 overflow-hidden border border-zinc-800">
                <div
                  className="h-full bg-amber-500 transition-all duration-500"
                  style={{ width: `${vitals.diskC}%` }}
                />
              </div>
              <div className="flex justify-between text-[11px] text-zinc-500 pt-1">
                <span>C: {vitals.diskC}%</span>
                <span>D: 34.2%</span>
              </div>
            </div>

            {/* CPU */}
            <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-2 shadow">
              <div className="flex items-center justify-between text-zinc-400 font-bold">
                <span className="flex items-center gap-1.5 text-purple-400">
                  <Cpu className="w-4 h-4" /> CPU
                </span>
                <span className="text-purple-300">{vitals.cpuUsage}%</span>
              </div>
              <div className="w-full bg-zinc-950 rounded-full h-2 overflow-hidden border border-zinc-800">
                <div
                  className="h-full bg-purple-500 transition-all duration-500"
                  style={{ width: `${vitals.cpuUsage}%` }}
                />
              </div>
              <div className="flex justify-between text-[11px] text-zinc-500 pt-1">
                <span>Usage: {vitals.cpuUsage}%</span>
                <span>Temp: {vitals.fever}°C</span>
              </div>
            </div>

            {/* MEMORY */}
            <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-2 shadow">
              <div className="flex items-center justify-between text-zinc-400 font-bold">
                <span className="flex items-center gap-1.5 text-emerald-400">
                  <Activity className="w-4 h-4" /> MEMORY
                </span>
                <span className="text-emerald-300">{vitals.memUsage}</span>
              </div>
              <div className="w-full bg-zinc-950 rounded-full h-2 overflow-hidden border border-zinc-800">
                <div className="h-full bg-emerald-500 w-[51%]" />
              </div>
              <div className="flex justify-between text-[11px] text-zinc-500 pt-1">
                <span>Used: 8.2 GB</span>
                <span>Swap: 1.4 GB</span>
              </div>
            </div>

            {/* NETWORK */}
            <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-2 shadow">
              <div className="flex items-center justify-between text-zinc-400 font-bold">
                <span className="flex items-center gap-1.5 text-blue-400">
                  <Wifi className="w-4 h-4" /> NETWORK
                </span>
                <span className="text-blue-300">↓ {vitals.netDown}</span>
              </div>
              <div className="flex justify-between text-[11px] text-zinc-500 pt-2">
                <span>Down: {vitals.netDown}</span>
                <span>Up: {vitals.netUp}</span>
              </div>
            </div>
          </div>

          {/* PROCESSES TABLE */}
          <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-3">
            <h3 className="font-bold text-zinc-200 text-sm">ACTIVE HOST PROCESSES</h3>
            <div className="overflow-x-auto border border-zinc-800 rounded">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-zinc-925 text-zinc-400 border-b border-zinc-800">
                    <th className="p-2 border-r border-zinc-800">Name</th>
                    <th className="p-2 border-r border-zinc-800">PID</th>
                    <th className="p-2 border-r border-zinc-800">CPU</th>
                    <th className="p-2 border-r border-zinc-800">Mem</th>
                    <th className="p-2">Path</th>
                  </tr>
                </thead>
                <tbody>
                  {processes.map((proc) => (
                    <tr key={proc.pid} className="border-b border-zinc-800/60 hover:bg-zinc-850">
                      <td className="p-2 font-bold text-cyan-300 border-r border-zinc-800">
                        {proc.name}
                      </td>
                      <td className="p-2 text-zinc-400 border-r border-zinc-800">{proc.pid}</td>
                      <td className="p-2 text-purple-300 border-r border-zinc-800">{proc.cpu}</td>
                      <td className="p-2 text-emerald-300 border-r border-zinc-800">{proc.mem}</td>
                      <td className="p-2 text-zinc-500 truncate max-w-xs">{proc.path}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* NEXUS VITALS (Mapped to Host) */}
          <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-zinc-200 text-sm">NEXUS VITALS (Mapped to Host)</h3>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => onTriggerAction("conservation")}
                  className="px-3 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded text-xs font-semibold flex items-center gap-1 transition-colors shadow"
                >
                  <Zap className="w-3.5 h-3.5" />
                  <span>Trigger Conservation</span>
                </button>
                <button
                  onClick={() => onTriggerAction("immune")}
                  className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold flex items-center gap-1 transition-colors shadow"
                >
                  <Shield className="w-3.5 h-3.5" />
                  <span>Run Immune Patrol</span>
                </button>
                <button
                  onClick={() => onTriggerAction("evolve")}
                  className="px-3 py-1 bg-purple-600 hover:bg-purple-500 text-white rounded text-xs font-semibold flex items-center gap-1 transition-colors shadow"
                >
                  <Activity className="w-3.5 h-3.5" />
                  <span>Evolve Skill</span>
                </button>
              </div>
            </div>

            <div className="overflow-x-auto border border-zinc-800 rounded">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-zinc-925 text-zinc-400 border-b border-zinc-800">
                    <th className="p-2 border-r border-zinc-800">Signal</th>
                    <th className="p-2 border-r border-zinc-800">Level</th>
                    <th className="p-2 border-r border-zinc-800">Source</th>
                    <th className="p-2 border-r border-zinc-800">Since</th>
                    <th className="p-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-zinc-800/60 hover:bg-zinc-850">
                    <td className="p-2 font-bold text-amber-400 border-r border-zinc-800">⚡ Energy</td>
                    <td className="p-2 text-zinc-200 border-r border-zinc-800">{vitals.energy}%</td>
                    <td className="p-2 text-zinc-400 border-r border-zinc-800">Metabolism</td>
                    <td className="p-2 text-zinc-500 border-r border-zinc-800">Always</td>
                    <td className="p-2 text-emerald-400 font-bold">Homeostatic</td>
                  </tr>
                  <tr className="border-b border-zinc-800/60 hover:bg-zinc-850">
                    <td className="p-2 font-bold text-rose-400 border-r border-zinc-800">🩸 Ischemia</td>
                    <td className="p-2 text-zinc-200 border-r border-zinc-800">{vitals.diskC}%</td>
                    <td className="p-2 text-zinc-400 border-r border-zinc-800">Disk C</td>
                    <td className="p-2 text-zinc-500 border-r border-zinc-800">14 min</td>
                    <td className="p-2 text-amber-400 font-bold">{vitals.status}</td>
                  </tr>
                  <tr className="border-b border-zinc-800/60 hover:bg-zinc-850">
                    <td className="p-2 font-bold text-cyan-400 border-r border-zinc-800">💨 Hypoxia</td>
                    <td className="p-2 text-zinc-200 border-r border-zinc-800">{vitals.hypoxia}%</td>
                    <td className="p-2 text-zinc-400 border-r border-zinc-800">CPU</td>
                    <td className="p-2 text-zinc-500 border-r border-zinc-800">—</td>
                    <td className="p-2 text-emerald-400 font-bold">Normal</td>
                  </tr>
                  <tr className="border-b border-zinc-800/60 hover:bg-zinc-850">
                    <td className="p-2 font-bold text-orange-400 border-r border-zinc-800">🔥 Fever</td>
                    <td className="p-2 text-zinc-200 border-r border-zinc-800">{vitals.fever}°C</td>
                    <td className="p-2 text-zinc-400 border-r border-zinc-800">Immune</td>
                    <td className="p-2 text-zinc-500 border-r border-zinc-800">—</td>
                    <td className="p-2 text-emerald-400 font-bold">Normal</td>
                  </tr>
                  <tr className="hover:bg-zinc-850">
                    <td className="p-2 font-bold text-emerald-400 border-r border-zinc-800">💚 Vibe</td>
                    <td className="p-2 text-zinc-200 border-r border-zinc-800">+{vitals.vibe}</td>
                    <td className="p-2 text-zinc-400 border-r border-zinc-800">Endocrine</td>
                    <td className="p-2 text-zinc-500 border-r border-zinc-800">—</td>
                    <td className="p-2 text-emerald-400 font-bold">Positive</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* SACRED GEOMETRY CONFIG PANEL & MANTRA SOUNDSCAPE SLIDER */}
          <div className="p-4 bg-amber-950/20 border border-amber-800/60 rounded-lg flex flex-col gap-4">
            <div className="flex items-center justify-between border-b border-amber-900/60 pb-2">
              <div className="flex items-center gap-2 text-amber-300 font-bold text-sm">
                <Compass className="w-4 h-4 text-amber-400" />
                <span>SACRED GEOMETRY & ACOUSTIC MANTRA SYNTHESIS</span>
              </div>
              <span className="text-[11px] text-amber-400/80 font-mono">Phi Ratio φ = 1.6180339</span>
            </div>

            {/* Mantra Blend Slider */}
            <div className="p-3 bg-zinc-900/90 border border-amber-900/60 rounded-lg flex flex-col gap-2">
              <div className="flex items-center justify-between text-xs font-bold text-amber-200">
                <span className="flex items-center gap-1.5">
                  <Zap className="w-3.5 h-3.5 text-amber-400" />
                  TEMPLE ACOUSTIC RESONANCE BLEND
                </span>
                <span className="text-amber-400 font-mono text-[11px]">
                  {Math.round((1 - mantraBlend) * 100)}% Bell Echo / {Math.round(mantraBlend * 100)}% Low-Freq Mantra
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-[10px] text-zinc-400 font-mono">Temple Bell</span>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={mantraBlend}
                  onChange={(e) => onMantraBlendChange?.(parseFloat(e.target.value))}
                  className="flex-1 h-2 bg-zinc-950 rounded-lg appearance-none cursor-pointer accent-amber-500 border border-amber-900/60"
                />
                <span className="text-[10px] text-zinc-400 font-mono">Generative Mantra</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-2.5">
              {/* Toggle Golden Ratio Grid */}
              <button
                onClick={() => onToggleGeometry?.("showGrid")}
                className={`p-2.5 rounded-lg border text-left flex items-center justify-between transition-all cursor-pointer ${
                  geometryConfig.showGrid
                    ? "bg-amber-950/80 border-amber-500 text-amber-200 shadow"
                    : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Grid className="w-4 h-4 text-amber-400" />
                  <div>
                    <div className="font-bold text-xs">Golden Grid</div>
                    <div className="text-[10px] text-zinc-500">φ 1.618 lines</div>
                  </div>
                </div>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${geometryConfig.showGrid ? "bg-amber-500 text-black" : "bg-zinc-800 text-zinc-400"}`}>
                  {geometryConfig.showGrid ? "ON" : "OFF"}
                </span>
              </button>

              {/* Toggle Fibonacci Spiral */}
              <button
                onClick={() => onToggleGeometry?.("showSpiral")}
                className={`p-2.5 rounded-lg border text-left flex items-center justify-between transition-all cursor-pointer ${
                  geometryConfig.showSpiral
                    ? "bg-amber-950/80 border-amber-500 text-amber-200 shadow"
                    : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-amber-400" />
                  <div>
                    <div className="font-bold text-xs">Fibonacci Spiral</div>
                    <div className="text-[10px] text-zinc-500">Growth curve</div>
                  </div>
                </div>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${geometryConfig.showSpiral ? "bg-amber-500 text-black" : "bg-zinc-800 text-zinc-400"}`}>
                  {geometryConfig.showSpiral ? "ON" : "OFF"}
                </span>
              </button>

              {/* Toggle Mandapa Alignment */}
              <button
                onClick={() => onToggleGeometry?.("showMandapa")}
                className={`p-2.5 rounded-lg border text-left flex items-center justify-between transition-all cursor-pointer ${
                  geometryConfig.showMandapa
                    ? "bg-amber-950/80 border-amber-500 text-amber-200 shadow"
                    : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-amber-400" />
                  <div>
                    <div className="font-bold text-xs">Mandapa Bounds</div>
                    <div className="text-[10px] text-zinc-500">Sanctum alignment</div>
                  </div>
                </div>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${geometryConfig.showMandapa ? "bg-amber-500 text-black" : "bg-zinc-800 text-zinc-400"}`}>
                  {geometryConfig.showMandapa ? "ON" : "OFF"}
                </span>
              </button>

              {/* Toggle Portal Mandala Pattern */}
              <button
                onClick={() => onToggleGeometry?.("showPortalMandala")}
                className={`p-2.5 rounded-lg border text-left flex items-center justify-between transition-all cursor-pointer ${
                  geometryConfig.showPortalMandala
                    ? "bg-amber-950/80 border-amber-500 text-amber-200 shadow"
                    : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Compass className="w-4 h-4 text-amber-400 animate-spin" />
                  <div>
                    <div className="font-bold text-xs">Portal Mandala</div>
                    <div className="text-[10px] text-zinc-500">Transition pattern</div>
                  </div>
                </div>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${geometryConfig.showPortalMandala ? "bg-amber-500 text-black" : "bg-zinc-800 text-zinc-400"}`}>
                  {geometryConfig.showPortalMandala ? "ON" : "OFF"}
                </span>
              </button>

              {/* Toggle Geometry Animations (CPU Optimization) */}
              <button
                onClick={() => onToggleGeometry?.("enableAnimations")}
                className={`p-2.5 rounded-lg border text-left flex items-center justify-between transition-all cursor-pointer ${
                  geometryConfig.enableAnimations
                    ? "bg-emerald-950/80 border-emerald-500 text-emerald-200 shadow"
                    : "bg-rose-950/60 border-rose-800 text-rose-300"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-emerald-400" />
                  <div>
                    <div className="font-bold text-xs">Animations</div>
                    <div className="text-[10px] text-zinc-500">Ripple & Mandala</div>
                  </div>
                </div>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${geometryConfig.enableAnimations ? "bg-emerald-500 text-black" : "bg-rose-900 text-rose-200"}`}>
                  {geometryConfig.enableAnimations ? "ENABLED" : "LOW CPU"}
                </span>
              </button>
            </div>
          </div>

          {/* RESOURCE TIMELINE (Last 60 min) */}
          <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-lg flex flex-col gap-2">
            <h3 className="font-bold text-zinc-200 text-sm">RESOURCE TIMELINE (Last 60 min)</h3>
            <div className="bg-zinc-950 p-3 rounded border border-zinc-800 text-xs leading-6 text-zinc-400 font-mono">
              <div>CPU ████████░░░░████████░░░░████░░░░░░████████░░░░████░░</div>
              <div>Mem ██████████░░██████████░░████████░░░░██████████░░████</div>
              <div>DSK ████████████████████████████████████████████████████</div>
            </div>
          </div>
        </div>
      ) : (
        /* SANCTUM HISTORY TAB: INK-WASH BRUSHSTROKE VIBE TIMELINE */
        <div className="p-6 overflow-y-auto flex flex-col gap-6 text-xs text-zinc-300">
          <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-lg flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
              <h3 className="font-bold text-amber-300 text-sm flex items-center gap-2">
                <Activity className="w-4 h-4 text-amber-400" />
                SANCTUM ARCHITECTURAL VIBE FLUCTUATIONS TIMELINE
              </h3>
              <span className="text-[11px] text-zinc-500">Ink-wash brushstroke representations</span>
            </div>

            <p className="text-zinc-400 leading-relaxed text-[11px]">
              Historical timeline recording key architectural resonance events and energetic shifts within Sanctum AOS.
              Each state is symbolized by organic ink-wash brushstrokes scaled to vibe amplitude.
            </p>

            <div className="flex flex-col gap-4 pt-2">
              {historyRecords.map((rec, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-zinc-950/80 border border-zinc-800/80 rounded-lg flex flex-col gap-2 relative overflow-hidden"
                >
                  <div className="flex items-center justify-between font-bold">
                    <span className="text-amber-400 font-mono">{rec.time}</span>
                    <span className="text-zinc-200">{rec.state}</span>
                    <span className="text-emerald-400 font-mono">Vibe: +{rec.vibe}</span>
                    <span className="text-cyan-400 font-mono">Energy: {rec.energy}%</span>
                  </div>

                  {/* Aesthetic Ink-Wash Brushstroke SVG Graphic */}
                  <div className="w-full h-10 relative flex items-center justify-center overflow-hidden rounded bg-black/40 border border-zinc-900">
                    <div
                      className={`absolute inset-0 bg-gradient-to-r ${rec.inkColor} opacity-90 blur-[1px]`}
                      style={{
                        height: `${rec.strokeWidth}px`,
                        top: "50%",
                        transform: "translateY(-50%)",
                        borderRadius: "9999px",
                        clipPath: "polygon(0% 20%, 25% 80%, 50% 10%, 75% 90%, 100% 30%, 100% 70%, 75% 100%, 50% 40%, 25% 100%, 0% 80%)",
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};
