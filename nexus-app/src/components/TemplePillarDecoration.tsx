import React, { useState } from "react";

interface TemplePillarDecorationProps {
  side: "left" | "right";
  isGlowing?: boolean;
}

export const TemplePillarDecoration: React.FC<TemplePillarDecorationProps> = ({ side, isGlowing }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`absolute top-0 bottom-0 ${
        side === "left" ? "-left-2" : "-right-2"
      } w-3.5 pointer-events-auto z-30 flex flex-col justify-between items-center transition-all duration-300 ${
        hovered || isGlowing ? "opacity-100 scale-105" : "opacity-80"
      }`}
    >
      {/* Pillar Capital (Top Carved Crown / Kalasha) */}
      <svg
        viewBox="0 0 14 28"
        className={`w-3.5 h-7 text-amber-500/90 shrink-0 drop-shadow transition-all duration-300 ${
          hovered || isGlowing ? "text-amber-300 drop-shadow-[0_0_8px_rgba(245,158,11,0.9)]" : ""
        }`}
      >
        <path
          d="M2 0 H12 L14 7 L10 14 L12 19 L7 28 L2 19 L4 14 L0 7 Z"
          fill="currentColor"
          stroke="#f59e0b"
          strokeWidth="0.6"
        />
        <circle cx="7" cy="7" r="2" fill="#fbbf24" />
      </svg>

      {/* Fluted Pillar Shaft (Vertical Gradient Bar with Carved Grooves & Shilpkari Relief) */}
      <div
        className={`flex-1 w-2.5 my-0.5 bg-gradient-to-b from-amber-800/90 via-amber-950/80 to-amber-800/90 border-x border-amber-500/60 rounded-sm relative overflow-hidden shadow-inner transition-all duration-300 ${
          hovered || isGlowing ? "border-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.6)]" : ""
        }`}
      >
        {/* Fine vertical shaft grooves */}
        <div className="absolute inset-y-0 left-0.5 w-0.5 bg-amber-400/40" />
        <div className="absolute inset-y-0 right-0.5 w-0.5 bg-amber-400/40" />
        {/* Transverse ring bands along shaft */}
        <div className="absolute top-1/5 left-0 right-0 h-0.5 bg-amber-300/80 shadow-sm" />
        <div className="absolute top-2/5 left-0 right-0 h-0.5 bg-amber-300/80 shadow-sm" />
        <div className="absolute top-3/5 left-0 right-0 h-0.5 bg-amber-300/80 shadow-sm" />
        <div className="absolute top-4/5 left-0 right-0 h-0.5 bg-amber-300/80 shadow-sm" />
      </div>

      {/* Pillar Base Pedestal (Bottom Carved Lotus Base) */}
      <svg
        viewBox="0 0 14 28"
        className={`w-3.5 h-7 text-amber-500/90 shrink-0 rotate-180 drop-shadow transition-all duration-300 ${
          hovered || isGlowing ? "text-amber-300 drop-shadow-[0_0_8px_rgba(245,158,11,0.9)]" : ""
        }`}
      >
        <path
          d="M2 0 H12 L14 7 L10 14 L12 19 L7 28 L2 19 L4 14 L0 7 Z"
          fill="currentColor"
          stroke="#f59e0b"
          strokeWidth="0.6"
        />
        <circle cx="7" cy="7" r="2" fill="#fbbf24" />
      </svg>
    </div>
  );
};

/* Universal Shilpkari Panel Frame for Deep Indian Temple Carved Boundaries */
export const ShilpkariPanelFrame: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className = "",
}) => {
  return (
    <div
      className={`relative bg-[#120a06]/95 border-2 border-amber-800/70 rounded-2xl shadow-2xl oil-lamp-glow overflow-hidden ${className}`}
    >
      {/* Corner Shilpkari Lotus Rosette Ornaments */}
      <div className="absolute top-1 left-1 w-2.5 h-2.5 border-t-2 border-l-2 border-amber-400/90 rounded-tl pointer-events-none z-20" />
      <div className="absolute top-1 right-1 w-2.5 h-2.5 border-t-2 border-r-2 border-amber-400/90 rounded-tr pointer-events-none z-20" />
      <div className="absolute bottom-1 left-1 w-2.5 h-2.5 border-b-2 border-l-2 border-amber-400/90 rounded-bl pointer-events-none z-20" />
      <div className="absolute bottom-1 right-1 w-2.5 h-2.5 border-b-2 border-r-2 border-amber-400/90 rounded-br pointer-events-none z-20" />

      {/* Side Pillar Column Accents */}
      <TemplePillarDecoration side="left" />
      <TemplePillarDecoration side="right" />

      {children}
    </div>
  );
};

