import React, { useEffect, useState } from "react";
import { motion } from "motion/react";
import { TrendingUp, Activity, Sparkles } from "lucide-react";

interface VibeHistorySparklineProps {
  currentVibe: number;
}

export const VibeHistorySparkline: React.FC<VibeHistorySparklineProps> = ({ currentVibe }) => {
  // Store up to 60 seconds (60 data points) of vibe history
  const [history, setHistory] = useState<number[]>([
    92, 93, 91, 94, 95, 93, 96, 97, 95, 98, 97, 99, 98, 96, 97, 98, currentVibe,
  ]);

  useEffect(() => {
    const timer = setInterval(() => {
      setHistory((prev) => {
        const next = [...prev, currentVibe];
        if (next.length > 60) next.shift(); // Keep last 60 seconds
        return next;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [currentVibe]);

  const maxVal = Math.max(...history, 100);
  const minVal = Math.min(...history, 80);
  const avgVal = Math.round(history.reduce((a, b) => a + b, 0) / history.length);

  const sparkWidth = 180;
  const sparkHeight = 28;

  const points = history
    .map((val, idx) => {
      const x = (idx / (history.length - 1 || 1)) * sparkWidth;
      const y = sparkHeight - ((val - minVal) / (maxVal - minVal || 1)) * (sparkHeight - 6) - 3;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  // Gradient stroke color based on homeostatic balance
  const isOptimal = currentVibe >= 95;

  return (
    <div className="flex items-center gap-2 px-2.5 py-1 bg-[#1a120b] border border-amber-800/60 rounded-lg shadow-sm font-mono text-[11px]">
      <div className="flex items-center gap-1 text-emerald-400 font-bold">
        <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
        <span>Vibe +{currentVibe}</span>
      </div>

      {/* SVG Sparkline Path */}
      <div className="relative flex items-center">
        <svg viewBox={`0 0 ${sparkWidth} ${sparkHeight}`} className="w-24 h-6 overflow-visible">
          <defs>
            <linearGradient id="sparkGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#d97706" />
              <stop offset="50%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor={isOptimal ? "#10b981" : "#fbbf24"} />
            </linearGradient>
            <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Fill under graph */}
          <polygon
            points={`0,${sparkHeight} ${points} ${sparkWidth},${sparkHeight}`}
            fill="url(#sparkFill)"
          />

          {/* Stroke Line */}
          <polyline
            fill="none"
            stroke="url(#sparkGrad)"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            points={points}
          />
        </svg>
      </div>

      <div className="hidden lg:flex items-center gap-1 text-[10px] text-amber-300/80 font-semibold">
        <Sparkles className="w-3 h-3 text-amber-400" />
        <span>60s Avg: {avgVal}</span>
      </div>
    </div>
  );
};
