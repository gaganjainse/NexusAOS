import React from "react";

interface GoldenRatioOverlayProps {
  showGrid: boolean;
  showSpiral: boolean;
  showMandapa: boolean;
  isDragging?: boolean;
  isSnapped?: boolean;
  snappedTargetName?: string;
}

export const GoldenRatioOverlay: React.FC<GoldenRatioOverlayProps> = ({
  showGrid,
  showSpiral,
  showMandapa,
  isDragging = false,
  isSnapped = false,
  snappedTargetName = "φ = 1.618",
}) => {
  if (!showGrid && !showSpiral && !showMandapa && !isDragging) return null;

  const activeGrid = showGrid || isDragging;

  return (
    <div className="absolute inset-0 pointer-events-none z-40 overflow-hidden font-mono text-[10px] text-amber-500/70">
      {/* Golden Ratio Grid (Phi = 1.618 division lines) */}
      {activeGrid && (
        <svg
          className={`w-full h-full absolute inset-0 transition-all duration-200 ${
            isSnapped
              ? "stroke-amber-300 opacity-100 drop-shadow-[0_0_12px_rgba(245,158,11,0.8)]"
              : isDragging
              ? "stroke-amber-400 opacity-90"
              : "stroke-amber-500/30 opacity-70"
          }`}
          strokeWidth={isSnapped ? "2" : isDragging ? "1.5" : "0.8"}
        >
          {/* Vertical Phi divisions (23.6%, 38.2%, 61.8%, 76.4%) */}
          <line x1="38.2%" y1="0" x2="38.2%" y2="100%" strokeDasharray={isDragging ? "6 3" : "4 4"} />
          <line x1="61.8%" y1="0" x2="61.8%" y2="100%" strokeDasharray={isDragging ? "6 3" : "4 4"} />
          {isDragging && (
            <>
              <line x1="23.6%" y1="0" x2="23.6%" y2="100%" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" opacity="0.75" />
              <line x1="76.4%" y1="0" x2="76.4%" y2="100%" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" opacity="0.75" />
            </>
          )}

          {/* Horizontal Phi divisions (23.6%, 38.2%, 61.8%, 76.4%) */}
          <line x1="0" y1="38.2%" x2="100%" y2="38.2%" strokeDasharray={isDragging ? "6 3" : "4 4"} />
          <line x1="0" y1="61.8%" x2="100%" y2="61.8%" strokeDasharray={isDragging ? "6 3" : "4 4"} />
          {isDragging && (
            <>
              <line x1="0" y1="23.6%" x2="100%" y2="23.6%" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" opacity="0.75" />
              <line x1="0" y1="76.4%" x2="100%" y2="76.4%" stroke="#38bdf8" strokeWidth="1" strokeDasharray="3 3" opacity="0.75" />
            </>
          )}

          {/* Label Phi Intersections */}
          <text x="38.5%" y="37.5%" fill={isDragging ? "#fbbf24" : "#f59e0b"} fontSize="10" fontWeight="bold">φ1 (0.618)</text>
          <text x="62.1%" y="37.5%" fill={isDragging ? "#fbbf24" : "#f59e0b"} fontSize="10" fontWeight="bold">φ2 (1.618)</text>
          <text x="38.5%" y="61.2%" fill={isDragging ? "#fbbf24" : "#f59e0b"} fontSize="10" fontWeight="bold">φ3 (2.618)</text>
          <text x="62.1%" y="61.2%" fill={isDragging ? "#fbbf24" : "#f59e0b"} fontSize="10" fontWeight="bold">φ4 (4.236)</text>

          {isDragging && (
            <g className="animate-pulse">
              <circle cx="38.2%" cy="38.2%" r={isSnapped ? "14" : "10"} fill="none" stroke={isSnapped ? "#fef08a" : "#fbbf24"} strokeWidth="2" />
              <circle cx="61.8%" cy="38.2%" r={isSnapped ? "14" : "10"} fill="none" stroke={isSnapped ? "#fef08a" : "#fbbf24"} strokeWidth="2" />
              <circle cx="38.2%" cy="61.8%" r={isSnapped ? "14" : "10"} fill="none" stroke={isSnapped ? "#fef08a" : "#fbbf24"} strokeWidth="2" />
              <circle cx="61.8%" cy="61.8%" r={isSnapped ? "14" : "10"} fill="none" stroke={isSnapped ? "#fef08a" : "#fbbf24"} strokeWidth="2" />
            </g>
          )}
        </svg>
      )}

      {/* HUD Banner for Golden Ratio Snapping Gravity Force */}
      {isDragging && (
        <div className="absolute top-12 left-1/2 -translate-x-1/2 pointer-events-none z-50 flex items-center gap-2 px-3 py-1.5 bg-[#140a05]/90 border border-amber-500/80 rounded-full shadow-2xl backdrop-blur-md text-amber-300 font-bold tracking-wider text-[11px] animate-in fade-in zoom-in-95 duration-150">
          <span className={`inline-block w-2 h-2 rounded-full ${isSnapped ? "bg-amber-300 animate-ping" : "bg-sky-400"}`} />
          {isSnapped ? (
            <span className="text-amber-200">
              🧲 GOLDEN GRAVITY ATTRACTION: Locked to {snappedTargetName} (Drag forcefully to pull out)
            </span>
          ) : (
            <span className="text-amber-400/90">
              📐 GOLDEN GRID ALIGNMENT ACTIVE (φ = 1.618033)
            </span>
          )}
        </div>
      )}

      {/* Fibonacci Golden Spiral */}
      {showSpiral && (
        <svg viewBox="0 0 1000 618" preserveAspectRatio="none" className="w-full h-full absolute inset-0 opacity-40">
          <path
            d="M 0 618 A 618 618 0 0 1 618 0 A 382 382 0 0 1 1000 382 A 236 236 0 0 1 764 618 A 146 146 0 0 1 618 472 A 90 90 0 0 1 708 382"
            fill="none"
            stroke="#fbbf24"
            strokeWidth="1.5"
            strokeDasharray="6 3"
          />
        </svg>
      )}

      {/* Concentric Temple Mandapa Alignment Enclosures */}
      {showMandapa && (
        <div className="absolute inset-2 border border-amber-500/25 rounded-2xl flex items-center justify-center pointer-events-none">
          <div className="w-[85%] h-[85%] border border-amber-500/35 rounded-xl flex items-center justify-center">
            <div className="w-[68%] h-[68%] border border-amber-400/40 rounded-lg flex items-center justify-center">
              <div className="w-[45%] h-[45%] border-2 border-dashed border-amber-300/50 rounded-md flex items-center justify-center bg-amber-950/5">
                <span className="text-[10px] text-amber-300 font-bold tracking-widest uppercase">
                  GARBHAGRIHA SANCTUM CORE
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
