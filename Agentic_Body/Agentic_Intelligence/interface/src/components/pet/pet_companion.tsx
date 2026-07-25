import React, { useState, useEffect } from "react";
import { PetState, PetMood, PetStatus } from "../../types/Sesha";
import {
  Sparkles,
  Zap,
  Eye,
  Smile,
  AlertTriangle,
  Brain,
  Code2,
  Moon,
  Activity,
  Maximize2,
  RefreshCw,
} from "lucide-react";

interface PetCompanionProps {
  status: PetStatus;
  onUpdateStatus?: (newStatus: Partial<PetStatus>) => void;
  compact?: boolean;
  onOpenFull?: () => void;
}

export const PetCompanion: React.FC<PetCompanionProps> = ({
  status,
  onUpdateStatus,
  compact = false,
  onOpenFull,
}) => {
  const [glitch, setGlitch] = useState(false);
  const [typedText, setTypedText] = useState(status.speechText || "");

  // Auto glitch effect when state is Anomaly
  useEffect(() => {
    if (status.state === "Anomaly") {
      const interval = setInterval(() => {
        setGlitch((g) => !g);
      }, 200);
      return () => clearInterval(interval);
    } else {
      setGlitch(false);
    }
  }, [status.state]);

  // Handle speech updates
  useEffect(() => {
    if (status.speechText) {
      setTypedText(status.speechText);
    }
  }, [status.speechText]);

  const getStateColor = (state: PetState) => {
    switch (state) {
      case "Idle":
        return "from-emerald-500/20 to-teal-500/10 border-emerald-500/40 text-emerald-400";
      case "Thinking":
        return "from-cyan-500/20 to-blue-500/10 border-cyan-500/40 text-cyan-300";
      case "Working":
      case "Focused":
        return "from-violet-500/20 to-purple-500/10 border-violet-500/40 text-violet-300";
      case "Happy":
        return "from-amber-500/20 to-yellow-500/10 border-amber-500/40 text-amber-300";
      case "Concerned":
        return "from-orange-500/20 to-rose-500/10 border-orange-500/40 text-orange-400";
      case "Asleep":
        return "from-slate-700/30 to-zinc-800/20 border-slate-600/40 text-slate-400";
      case "Anomaly":
        return "from-red-600/40 to-rose-900/40 border-red-500 text-red-400 animate-pulse";
      default:
        return "from-cyan-500/20 to-blue-500/10 border-cyan-500/40 text-cyan-300";
    }
  };

  const getEyeExpression = (state: PetState) => {
    switch (state) {
      case "Asleep":
        return (
          <g stroke="#94a3b8" strokeWidth="2.5" strokeLinecap="round">
            <path d="M 32 38 Q 38 42 44 38" />
            <path d="M 56 38 Q 62 42 68 38" />
          </g>
        );
      case "Thinking":
        return (
          <g fill="#38bdf8">
            <circle cx="38" cy="32" r="5" className="animate-bounce" />
            <circle cx="62" cy="32" r="5" className="animate-bounce" />
            <circle cx="40" cy="31" r="2" fill="#ffffff" />
            <circle cx="64" cy="31" r="2" fill="#ffffff" />
          </g>
        );
      case "Concerned":
        return (
          <g fill="#fb923c">
            <path d="M 30 28 L 44 32" stroke="#fb923c" strokeWidth="2.5" />
            <path d="M 70 28 L 56 32" stroke="#fb923c" strokeWidth="2.5" />
            <circle cx="37" cy="36" r="4" />
            <circle cx="63" cy="36" r="4" />
          </g>
        );
      case "Happy":
        return (
          <g stroke="#facc15" strokeWidth="3" strokeLinecap="round" fill="none">
            <path d="M 30 38 Q 38 28 46 38" />
            <path d="M 54 38 Q 62 28 70 38" />
          </g>
        );
      case "Focused":
      case "Working":
        return (
          <g fill="#a855f7">
            <rect x="32" y="32" width="12" height="6" rx="2" className="animate-pulse" />
            <rect x="56" y="32" width="12" height="6" rx="2" className="animate-pulse" />
            <circle cx="38" cy="35" r="1.5" fill="#ffffff" />
            <circle cx="62" cy="35" r="1.5" fill="#ffffff" />
          </g>
        );
      case "Anomaly":
        return (
          <g fill="#ef4444">
            <line x1="30" y1="30" x2="44" y2="44" stroke="#ef4444" strokeWidth="3" />
            <line x1="44" y1="30" x2="30" y2="44" stroke="#ef4444" strokeWidth="3" />
            <line x1="56" y1="30" x2="70" y2="44" stroke="#ef4444" strokeWidth="3" />
            <line x1="70" y1="30" x2="56" y2="44" stroke="#ef4444" strokeWidth="3" />
          </g>
        );
      default: // Idle
        return (
          <g fill="#34d399">
            <circle cx="38" cy="36" r="5" />
            <circle cx="62" cy="36" r="5" />
            <circle cx="40" cy="34" r="2" fill="#ffffff" />
            <circle cx="64" cy="34" r="2" fill="#ffffff" />
          </g>
        );
    }
  };

  const getMouthExpression = (state: PetState) => {
    switch (state) {
      case "Happy":
        return <path d="M 38 52 Q 50 64 62 52" stroke="#facc15" strokeWidth="3" fill="none" strokeLinecap="round" />;
      case "Concerned":
        return <path d="M 38 58 Q 50 48 62 58" stroke="#fb923c" strokeWidth="3" fill="none" strokeLinecap="round" />;
      case "Working":
      case "Focused":
        return <line x1="42" y1="54" x2="58" y2="54" stroke="#a855f7" strokeWidth="2.5" strokeLinecap="round" />;
      case "Asleep":
        return <ellipse cx="50" cy="54" rx="4" ry="2" fill="#64748b" />;
      case "Anomaly":
        return <path d="M 36 56 Q 42 50 48 58 Q 54 50 64 56" stroke="#ef4444" strokeWidth="3" fill="none" />;
      default:
        return <path d="M 42 54 Q 50 58 58 54" stroke="#34d399" strokeWidth="2.5" fill="none" strokeLinecap="round" />;
    }
  };

  if (compact) {
    return (
      <div className="p-3 bg-zinc-950/80 border-t border-zinc-800 rounded-b-lg flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`relative w-9 h-9 rounded-full bg-gradient-to-br ${getStateColor(status.state)} flex items-center justify-center border shadow-inner overflow-hidden`}>
              <svg viewBox="0 0 100 100" className={`w-8 h-8 ${glitch ? "scale-105 skew-x-2" : ""}`}>
                {/* Silhouette Aura */}
                <circle cx="50" cy="50" r="42" fill="none" stroke="currentColor" strokeWidth="2" strokeDasharray="4 2" className="animate-spin-slow opacity-40" />
                {/* Face Mask */}
                <rect x="20" y="20" width="60" height="50" rx="14" fill="#090d16" stroke="currentColor" strokeWidth="2" />
                {getEyeExpression(status.state)}
                {getMouthExpression(status.state)}
              </svg>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs font-semibold text-zinc-100">{status.name}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono uppercase tracking-wider border ${getStateColor(status.state)}`}>
                  {status.state}
                </span>
              </div>
              <div className="text-[11px] text-zinc-400 flex items-center gap-2 mt-0.5">
                <span className="flex items-center gap-1">
                  <Zap className="w-3 h-3 text-amber-400" />
                  {status.energy}%
                </span>
                <span className="text-zinc-600">•</span>
                <span className="capitalize">{status.mood}</span>
              </div>
            </div>
          </div>

          <button
            onClick={onOpenFull}
            title="Expand Companion Panel"
            className="p-1.5 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 rounded transition-colors"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Energy bar */}
        <div className="w-full bg-zinc-900 rounded-full h-1.5 overflow-hidden border border-zinc-800">
          <div
            className={`h-full transition-all duration-500 ${
              status.energy > 60
                ? "bg-emerald-500"
                : status.energy > 30
                ? "bg-amber-500"
                : "bg-rose-500"
            }`}
            style={{ width: `${status.energy}%` }}
          />
        </div>

        {/* Attention indicator */}
        <div className="flex items-center justify-between text-[10px] text-zinc-500 font-mono">
          <span className="flex items-center gap-1">
            <Eye className={`w-3 h-3 ${status.attention ? "text-cyan-400" : "text-zinc-600"}`} />
            {status.attention ? "Observing Sovereign" : "Internal Processing"}
          </span>
          <span className="text-zinc-400">{status.state === "Asleep" ? "💤 Resting" : "🟢 Online"}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="relative flex flex-col items-center p-4 bg-zinc-950/90 border border-zinc-800 rounded-xl shadow-2xl backdrop-blur-md max-w-sm w-full">
      {/* Header Controls */}
      <div className="w-full flex items-center justify-between border-b border-zinc-800/80 pb-2 mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <span className="text-sm font-bold text-zinc-100 tracking-wide">{status.name}</span>
          <span className="text-[10px] bg-cyan-950 text-cyan-400 border border-cyan-800/60 px-2 py-0.5 rounded font-mono">
            COMPANION-α
          </span>
        </div>
        <div className="flex items-center gap-1 text-xs">
          <span className={`px-2 py-0.5 rounded-full font-mono text-[10px] uppercase border ${getStateColor(status.state)}`}>
            {status.state}
          </span>
        </div>
      </div>

      {/* Speech Bubble */}
      {typedText && (
        <div className="relative mb-4 w-full bg-zinc-900/90 border border-cyan-500/30 text-zinc-200 text-xs p-2.5 rounded-lg shadow-lg font-mono leading-relaxed">
          <div className="absolute bottom-[-6px] left-8 w-3 h-3 bg-zinc-900 border-r border-b border-cyan-500/30 rotate-45" />
          <p className="text-cyan-200 font-sans">"{typedText}"</p>
        </div>
      )}

      {/* Semi-Realistic Animated Digital Avatar Canvas */}
      <div className={`relative w-36 h-36 rounded-2xl bg-gradient-to-br ${getStateColor(status.state)} p-1 border shadow-2xl transition-all duration-300 flex items-center justify-center`}>
        {/* Holographic background grid lines */}
        <div className="absolute inset-0 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:8px_8px] opacity-20 rounded-2xl pointer-events-none" />

        <svg viewBox="0 0 100 100" className={`w-full h-full ${glitch ? "scale-105 skew-x-3 filter contrast-150" : ""}`}>
          <defs>
            <linearGradient id="cyberGlow" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#0284c7" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0f172a" stopOpacity="0.9" />
            </linearGradient>
            <radialGradient id="eyeLight" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="100%" stopColor="#38bdf8" />
            </radialGradient>
          </defs>

          {/* Hologram halo ring */}
          <circle cx="50" cy="50" r="46" fill="none" stroke="currentColor" strokeWidth="1.5" strokeDasharray="6 3" className="animate-spin-slow opacity-60" />

          {/* Head Structure */}
          <path
            d="M 22 28 Q 50 14 78 28 Q 84 55 74 76 Q 50 90 26 76 Q 16 55 22 28 Z"
            fill="url(#cyberGlow)"
            stroke="currentColor"
            strokeWidth="2"
          />

          {/* Visor / Face Display Screen */}
          <path
            d="M 26 32 Q 50 22 74 32 Q 78 50 72 64 Q 50 74 28 64 Q 22 50 26 32 Z"
            fill="#030712"
            stroke="currentColor"
            strokeWidth="1.5"
          />

          {/* Eyebrows / Expression lines */}
          {status.state === "Concerned" && (
            <g stroke="#fb923c" strokeWidth="2.5" strokeLinecap="round">
              <line x1="30" y1="28" x2="42" y2="32" />
              <line x1="70" y1="28" x2="58" y2="32" />
            </g>
          )}

          {/* Eyes Expression Rendering */}
          {getEyeExpression(status.state)}

          {/* Mouth Rendering */}
          {getMouthExpression(status.state)}

          {/* Dynamic Working / Typing Screen Reflection Overlay */}
          {(status.state === "Working" || status.state === "Focused") && (
            <g fill="none" stroke="#a855f7" strokeWidth="1" opacity="0.4" className="animate-pulse">
              <line x1="28" y1="42" x2="72" y2="42" />
              <line x1="32" y1="48" x2="68" y2="48" />
            </g>
          )}

          {/* Asleep ZZZ */}
          {status.state === "Asleep" && (
            <text x="68" y="24" fill="#94a3b8" fontSize="10" className="animate-bounce font-mono">
              zZZ
            </text>
          )}
        </svg>

        {/* Live Status Badge on Avatar */}
        <div className="absolute bottom-2 right-2 bg-zinc-950/90 border border-zinc-700 text-zinc-300 text-[9px] font-mono px-1.5 py-0.5 rounded shadow">
          {status.state === "Working" ? "⚡ TYPING" : status.mood.toUpperCase()}
        </div>
      </div>

      {/* Mood & Energy Info */}
      <div className="w-full mt-4 flex flex-col gap-2">
        <div className="flex items-center justify-between text-xs font-mono text-zinc-400">
          <span className="flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            Energy: <strong className="text-zinc-200">{status.energy}%</strong>
          </span>
          <span className="flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
            Vibe: <strong className="text-emerald-400">+0.34</strong>
          </span>
        </div>

        <div className="w-full bg-zinc-900 rounded-full h-2 overflow-hidden border border-zinc-800">
          <div
            className={`h-full transition-all duration-500 ${
              status.energy > 60
                ? "bg-gradient-to-r from-emerald-500 to-teal-400"
                : status.energy > 30
                ? "bg-gradient-to-r from-amber-500 to-yellow-400"
                : "bg-gradient-to-r from-rose-600 to-red-500"
            }`}
            style={{ width: `${status.energy}%` }}
          />
        </div>

        {/* Quick State Simulation Triggers */}
        <div className="mt-2 pt-2 border-t border-zinc-800/80 w-full flex flex-col gap-1.5">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider">
            Simulate Companion State
          </span>
          <div className="grid grid-cols-4 gap-1">
            {(
              [
                { label: "Idle", state: "Idle", icon: Smile },
                { label: "Think", state: "Thinking", icon: Brain },
                { label: "Work", state: "Working", icon: Code2 },
                { label: "Focus", state: "Focused", icon: Zap },
                { label: "Happy", state: "Happy", icon: Sparkles },
                { label: "Warn", state: "Concerned", icon: AlertTriangle },
                { label: "Sleep", state: "Asleep", icon: Moon },
                { label: "Glitch", state: "Anomaly", icon: RefreshCw },
              ] as const
            ).map((item) => {
              const IconComp = item.icon;
              return (
                <button
                  key={item.state}
                  onClick={() =>
                    onUpdateStatus?.({
                      state: item.state as PetState,
                      speechText: `Switched mode to ${item.state}. System standing by.`,
                    })
                  }
                  className={`flex flex-col items-center justify-center p-1.5 rounded text-[10px] font-mono border transition-all ${
                    status.state === item.state
                      ? "bg-cyan-950 border-cyan-500 text-cyan-300 shadow"
                      : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850"
                  }`}
                >
                  <IconComp className="w-3 h-3 mb-0.5" />
                  {item.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

