import React, { useState, useRef, useEffect } from "react";
import { Palette, Check, Sparkles } from "lucide-react";
import { useTheme, THEMES } from "../context/ThemeContext";
import { ThemeId } from "../types/Sesha";

export const ThemeSwitcher: React.FC = () => {
  const { theme, setTheme, themeConfig } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative font-mono" ref={dropdownRef}>
      {/* Theme Trigger Button */}
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex items-center gap-1.5 px-2.5 py-1 bg-[#221812] hover:bg-[#322319] border border-amber-600/70 hover:border-amber-400 rounded-lg text-amber-300 hover:text-amber-200 text-[11px] font-bold shadow-md transition-all duration-200 active:scale-95 cursor-pointer ring-1 ring-amber-500/20"
        title="Change Temple Aesthetic Theme"
      >
        <span className="text-xs">{themeConfig.icon}</span>
        <span className="hidden sm:inline tracking-wider">{themeConfig.name}</span>
        <Palette className="w-3.5 h-3.5 text-amber-400 animate-pulse ml-0.5" />
      </button>

      {/* Theme Options Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-[#140b07]/98 border-2 border-amber-800/80 rounded-xl shadow-2xl p-2 z-50 backdrop-blur-xl ring-1 ring-amber-500/30 shilpkari-concave space-y-1 text-xs animate-in fade-in zoom-in-95 duration-150">
          <div className="flex items-center justify-between border-b border-amber-800/50 pb-1.5 px-2 mb-1">
            <span className="text-[10px] font-bold text-amber-400 tracking-widest uppercase flex items-center gap-1">
              <Sparkles className="w-3 h-3" /> Temple Aesthetic Themes
            </span>
            <span className="text-[9px] text-stone-400">6 Presets</span>
          </div>

          {(Object.keys(THEMES) as ThemeId[]).map((tId) => {
            const t = THEMES[tId];
            const isSelected = theme === tId;
            return (
              <button
                key={tId}
                onClick={() => {
                  setTheme(tId);
                  setIsOpen(false);
                }}
                className={`w-full flex items-start gap-2.5 p-2 rounded-lg text-left transition-all duration-150 cursor-pointer ${
                  isSelected
                    ? "bg-amber-950/80 border border-amber-500/80 text-amber-200 shadow-sm"
                    : "hover:bg-amber-950/40 border border-transparent text-stone-300 hover:text-amber-200"
                }`}
              >
                <span className="text-base leading-none mt-0.5">{t.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-[11px] tracking-wide truncate">{t.name}</span>
                    {isSelected && <Check className="w-3.5 h-3.5 text-amber-400 shrink-0" />}
                  </div>
                  <p className="text-[9.5px] text-stone-400 truncate mt-0.5 font-sans leading-tight">
                    {t.description}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

