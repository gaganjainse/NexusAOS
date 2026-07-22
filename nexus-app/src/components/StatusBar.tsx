import React, { useEffect, useState } from "react";
import { VitalsData } from "../types/nexus";
import {
  GitBranch,
  Zap,
  Activity,
  ShieldCheck,
  TrendingUp,
  History,
  X,
} from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { VibeHistorySparkline } from "./VibeHistorySparkline";

export interface StripItem {
  id: string;
  label: string;
  icon: any;
}

interface StatusBarProps {
  vitals: VitalsData;
  activeFile?: string;
  cursorPos?: { line: number; col: number };
  onOpenInlineRefactor?: () => void;
  activeSoundscape?: "monsoon" | "chanting" | "bells" | "solfeggio";
  onChangeSoundscape?: (scape: "monsoon" | "chanting" | "bells" | "solfeggio") => void;
}

export const StatusBar: React.FC<StatusBarProps> = ({
  vitals,
  activeFile = "main.py",
  cursorPos = { line: 12, col: 18 },
}) => {
  const [showHistory, setShowHistory] = useState(false);
  const [vibeHistory, setVibeHistory] = useState<number[]>([
    92, 94, 93, 95, 96, 94, 97, 98, 96, 99, 97, 98, vitals.vibe,
  ]);

  // Record vitals.vibe history over time
  useEffect(() => {
    setVibeHistory((prev) => {
      const next = [...prev, vitals.vibe];
      if (next.length > 25) next.shift();
      return next;
    });
  }, [vitals.vibe]);

  const maxVibe = Math.max(...vibeHistory, 100);
  const minVibe = Math.min(...vibeHistory, 80);
  const avgVibe = Math.round(vibeHistory.reduce((a, b) => a + b, 0) / vibeHistory.length);

  // SVG Sparkline path calculation
  const sparkWidth = 220;
  const sparkHeight = 40;
  const points = vibeHistory
    .map((val, idx) => {
      const x = (idx / (vibeHistory.length - 1 || 1)) * sparkWidth;
      const y = sparkHeight - ((val - minVibe) / (maxVibe - minVibe || 1)) * (sparkHeight - 8) - 4;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  return (
    <footer className="relative flex items-center justify-between px-3.5 py-1.5 bg-[#18110b]/95 border border-amber-800/40 rounded-xl text-[11px] font-mono text-stone-300 select-none z-30 shrink-0 gap-2.5 shadow-xl transition-all duration-300 overflow-visible">
      {/* Left Sanctum AOS Tag & Three System Vitals Tags */}
      <div className="flex items-center gap-2 shrink-0 whitespace-nowrap">
        {/* SANCTUM AOS Tag (Bottom Left) */}
        <motion.div
          whileHover={{ scale: 1.03 }}
          transition={{ type: "spring", stiffness: 400, damping: 25 }}
          className="flex items-center gap-1.5 text-amber-300 font-bold px-2.5 py-1 bg-amber-950/90 rounded-lg border border-amber-500/80 shadow-md shadow-amber-950/60 ring-1 ring-amber-500/30 whitespace-nowrap cursor-pointer shrink-0"
        >
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400 animate-pulse shrink-0" />
          <span>SANCTUM AOS: {vitals.status.toUpperCase()}</span>
        </motion.div>

        {/* Three System Vitals Container (Energy, Disk, Vibe) */}
        <div className="flex items-center gap-1.5 p-0.5 bg-[#221812] border border-amber-800/50 rounded-lg shadow-inner">
          <div className="flex items-center gap-1 text-amber-400 font-semibold px-2 py-0.5 rounded bg-[#1c130d]">
            <Zap className="w-3 h-3 text-amber-400" />
            <span>Energy: <strong className="text-amber-200">{vitals.energy}%</strong></span>
          </div>

          <div className="flex items-center gap-1 text-cyan-300 font-semibold px-2 py-0.5 rounded bg-[#1c130d]">
            <Zap className="w-3 h-3 text-cyan-400" />
            <span>Disk: <strong className="text-cyan-200">{vitals.diskC}%</strong></span>
          </div>

          <div className="flex items-center gap-1 text-emerald-400 font-semibold px-2 py-0.5 rounded bg-[#1c130d]">
            <Activity className="w-3 h-3 text-emerald-400" />
            <span>Vibe: <strong className="text-emerald-200">+{vitals.vibe}</strong></span>
          </div>
        </div>

        {/* Real-time VibeHistorySparkline inline */}
        <VibeHistorySparkline currentVibe={vitals.vibe} />

        {/* Interactive Vibe History Button */}
        <motion.button
          onClick={() => setShowHistory(!showHistory)}
          whileHover={{ scale: 1.05, y: -1 }}
          whileTap={{ scale: 0.95 }}
          transition={{ type: "spring", stiffness: 400, damping: 25 }}
          className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-bold transition-all shadow-md cursor-pointer ${
            showHistory
              ? "bg-amber-950 text-amber-300 border-amber-500 shadow-amber-950/60 ring-1 ring-amber-500/40"
              : "bg-emerald-950/80 text-emerald-300 border-emerald-700/60 hover:bg-emerald-900"
          }`}
          title="Toggle System Vibe Sparkline Waveform History"
        >
          <History className="w-3.5 h-3.5 text-amber-400" />
          <span>Details</span>
        </motion.button>
      </div>

      {/* Center Git Branch & File Coordinates */}
      <div className="hidden lg:flex items-center gap-3 shrink-0 text-stone-300 whitespace-nowrap">
        <div className="flex items-center gap-1 text-emerald-400 font-semibold">
          <GitBranch className="w-3.5 h-3.5" />
          <span>main</span>
        </div>

        <div className="text-stone-600">•</div>

        <div className="text-stone-300">
          File: <span className="text-amber-300 font-bold">{activeFile}</span>
        </div>

        <div className="text-stone-400">
          Ln {cursorPos.line}, Col {cursorPos.col}
        </div>
      </div>

      {/* Right UTF-8 Status */}
      <div className="flex items-center gap-2 shrink-0 whitespace-nowrap">
        <div className="flex items-center gap-1 text-stone-500 font-mono text-[10px]">
          <span>UTF-8</span>
        </div>
      </div>

      {/* VIBE HISTORY WAVEFORM POPOVER CARD - ALWAYS ON TOP (z-[100] fixed/absolute) */}
      <AnimatePresence>
        {showHistory && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400, damping: 28 }}
            className="absolute left-4 bottom-12 w-80 bg-[#1c140e] border-2 border-amber-500/90 rounded-xl p-3 shadow-2xl z-[100] font-mono text-stone-200 backdrop-blur-xl oil-lamp-glow"
          >
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-amber-900/60">
              <div className="flex items-center gap-1.5 text-xs font-bold text-amber-300">
                <TrendingUp className="w-3.5 h-3.5 text-amber-400" />
                <span>Sacred Vibe Resonance History</span>
              </div>
              <button
                onClick={() => setShowHistory(false)}
                className="p-1 hover:bg-stone-800 text-stone-400 hover:text-amber-300 rounded cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Sparkline Waveform SVG */}
            <div className="bg-[#120a06] border border-amber-900/40 rounded-lg p-2 flex flex-col gap-1">
              <div className="flex items-center justify-between text-[10px] text-stone-400">
                <span>Peak: <strong className="text-emerald-400">{maxVibe}</strong></span>
                <span>Avg: <strong className="text-amber-300">{avgVibe}</strong></span>
                <span>Current: <strong className="text-amber-400">+{vitals.vibe}</strong></span>
              </div>

              <svg viewBox={`0 0 ${sparkWidth} ${sparkHeight}`} className="w-full h-12 overflow-visible">
                <defs>
                  <linearGradient id="vibeGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                <polygon
                  points={`0,${sparkHeight} ${points} ${sparkWidth},${sparkHeight}`}
                  fill="url(#vibeGrad)"
                />
                <polyline
                  fill="none"
                  stroke="#f59e0b"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points={points}
                />
              </svg>
            </div>

            <div className="mt-2 flex items-center justify-between text-[10px] text-stone-400">
              <span>Acoustic Tuning: <strong className="text-amber-400">432Hz Golden Ratio</strong></span>
              <span className="text-emerald-400 font-bold">HARMONIOUS</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </footer>
  );
};

