import React from "react";
import { motion } from "motion/react";

interface SacredGeometryMandalaProps {
  enableAnimations?: boolean;
  showPortalMandala?: boolean;
}

export const SacredGeometryMandala: React.FC<SacredGeometryMandalaProps> = ({
  enableAnimations = true,
  showPortalMandala = false,
}) => {
  return (
    <div
      className={`fixed inset-0 pointer-events-none z-0 overflow-hidden flex items-center justify-center select-none transition-opacity duration-700 ${
        showPortalMandala ? "opacity-25 scale-110" : "opacity-10"
      }`}
    >
      {/* Outer Rotating Sacred Sri Yantra / Lotus Mandala */}
      <motion.svg
        viewBox="0 0 800 800"
        className="w-[900px] h-[900px] text-amber-500"
        animate={enableAnimations ? { rotate: 360 } : { rotate: 0 }}
        transition={{ duration: showPortalMandala ? 60 : 180, repeat: Infinity, ease: "linear" }}
      >
        <defs>
          <linearGradient id="amberGlow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
            <stop offset="50%" stopColor="#d97706" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#78350f" stopOpacity="0.2" />
          </linearGradient>
        </defs>

        {/* Concentric Golden Ratio Circles */}
        <circle cx="400" cy="400" r="380" fill="none" stroke="url(#amberGlow)" strokeWidth="1" strokeDasharray="4 8" />
        <circle cx="400" cy="400" r="350" fill="none" stroke="url(#amberGlow)" strokeWidth="1.5" />
        <circle cx="400" cy="400" r="280" fill="none" stroke="url(#amberGlow)" strokeWidth="1" />
        <circle cx="400" cy="400" r="216" fill="none" stroke="url(#amberGlow)" strokeWidth="1.5" strokeDasharray="8 6" />
        <circle cx="400" cy="400" r="133" fill="none" stroke="url(#amberGlow)" strokeWidth="1" />
        <circle cx="400" cy="400" r="82" fill="none" stroke="url(#amberGlow)" strokeWidth="1.5" />

        {/* Extra Portal Transition Rings when Portal Vibe Enabled */}
        {showPortalMandala && (
          <>
            <circle cx="400" cy="400" r="310" fill="none" stroke="#fbbf24" strokeWidth="2" strokeDasharray="12 12" />
            <circle cx="400" cy="400" r="170" fill="none" stroke="#f59e0b" strokeWidth="2" strokeDasharray="6 6" />
          </>
        )}

        {/* 12 Outer Lotus Petals */}
        {Array.from({ length: 12 }).map((_, i) => {
          const angle = (i * 30 * Math.PI) / 180;
          const x1 = 400 + Math.cos(angle) * 216;
          const y1 = 400 + Math.sin(angle) * 216;
          const x2 = 400 + Math.cos(angle) * 350;
          const y2 = 400 + Math.sin(angle) * 350;
          return (
            <g key={i}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="url(#amberGlow)" strokeWidth="1" opacity="0.6" />
              <circle cx={x2} cy={y2} r="4" fill="#f59e0b" opacity="0.4" />
            </g>
          );
        })}

        {/* Interlocking Triangles (Sacred Geometry Sri Yantra) */}
        <polygon points="400,120 640,540 160,540" fill="none" stroke="url(#amberGlow)" strokeWidth="1.2" opacity="0.7" />
        <polygon points="400,680 640,260 160,260" fill="none" stroke="url(#amberGlow)" strokeWidth="1.2" opacity="0.7" />
        <polygon points="400,200 580,510 220,510" fill="none" stroke="url(#amberGlow)" strokeWidth="1" opacity="0.5" />
        <polygon points="400,600 580,290 220,290" fill="none" stroke="url(#amberGlow)" strokeWidth="1" opacity="0.5" />

        {/* Central Bindu Point */}
        <circle cx="400" cy="400" r="6" fill="#fbbf24" />
      </motion.svg>

      {/* Counter-Rotating Inner Sacred Ring */}
      <motion.svg
        viewBox="0 0 500 500"
        className="w-[500px] h-[500px] absolute text-amber-400"
        animate={enableAnimations ? { rotate: -360 } : { rotate: 0 }}
        transition={{ duration: showPortalMandala ? 40 : 120, repeat: Infinity, ease: "linear" }}
      >
        <circle cx="250" cy="250" r="230" fill="none" stroke="#d97706" strokeWidth="0.8" strokeDasharray="3 9" />
        <circle cx="250" cy="250" r="140" fill="none" stroke="#f59e0b" strokeWidth="1" />
        {Array.from({ length: 8 }).map((_, i) => {
          const angle = (i * 45 * Math.PI) / 180;
          const cx = 250 + Math.cos(angle) * 140;
          const cy = 250 + Math.sin(angle) * 140;
          return <circle key={i} cx={cx} cy={cy} r="20" fill="none" stroke="#f59e0b" strokeWidth="0.8" opacity="0.5" />;
        })}
      </motion.svg>
    </div>
  );
};

