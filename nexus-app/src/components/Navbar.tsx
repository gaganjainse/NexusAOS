import React, { useState } from "react";
import { InterfaceMode, VitalsData, PetStatus } from "../types/nexus";
import {
  Terminal,
  Cpu,
  Zap,
  Activity,
  HardDrive,
  Sparkles,
  HelpCircle,
  Edit3,
  Eye,
  Compass,
  Code2,
  Hammer,
  Wrench,
  Bot,
  Volume2,
  FileText,
  Palette,
} from "lucide-react";
import { motion } from "motion/react";
import { ThemeId } from "../types/nexus";
import { ThemeSwitcher } from "./ThemeSwitcher";

interface NavbarProps {
  mode: InterfaceMode;
  onToggleMode: (newMode: InterfaceMode) => void;
  vitals: VitalsData;
  petStatus: PetStatus;
  onOpenPet3D: () => void;
  onOpenSystemMonitor: () => void;
  onSubmitDirective?: (text: string) => void;
  onOpenDocs?: () => void;
  onRun?: () => void;
  onDebug?: () => void;
  onRefactor?: () => void;
  activeSoundscape?: "monsoon" | "chanting" | "bells" | "solfeggio";
  onChangeSoundscape?: (scape: "monsoon" | "chanting" | "bells" | "solfeggio") => void;
  currentTheme?: ThemeId;
  onChangeTheme?: (theme: ThemeId) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  mode,
  onToggleMode,
  vitals,
  petStatus,
  onOpenPet3D,
  onOpenSystemMonitor,
  activeSoundscape = "bells",
  onChangeSoundscape,
  currentTheme = "sandstone",
  onChangeTheme,
}) => {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);

  const menuConfig = [
    { name: "File", icon: FileText },
    { name: "Edit", icon: Edit3 },
    { name: "View", icon: Eye },
    { name: "Navigate", icon: Compass },
    { name: "Code", icon: Code2 },
    { name: "Build", icon: Hammer },
    { name: "Tools", icon: Wrench },
    { name: "Help", icon: HelpCircle },
  ];

  return (
    <header className="flex flex-col bg-[#160f0a]/95 border-b-2 border-amber-800/60 text-stone-200 select-none z-30 shrink-0 overflow-hidden rounded-xl shadow-2xl transition-all duration-300 oil-lamp-glow">
      {/* Top Mahaprakara Gopuram Header */}
      <div className="flex items-center justify-between px-3.5 py-1.5 text-xs gap-2">
        {/* Left: Architectural Dropdown Menu Bar */}
        <div className="flex items-center gap-3">
          <nav className="hidden lg:flex items-center gap-1 p-1 bg-[#1a120b] border border-amber-800/70 rounded-lg shadow-inner font-sans">
            {menuConfig.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.name}
                  className="relative"
                  onMouseEnter={() => setActiveMenu(item.name)}
                  onMouseLeave={() => setActiveMenu(null)}
                >
                  <motion.button
                    whileHover={{ scale: 1.04 }}
                    whileTap={{ scale: 0.96 }}
                    className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium transition-all duration-200 cursor-pointer ${
                      activeMenu === item.name
                        ? "bg-amber-950 text-amber-200 font-semibold border border-amber-600/80 shadow-md"
                        : "text-stone-300 hover:text-amber-200 hover:bg-[#281e18]"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5 text-amber-400" />
                    <span>{item.name}</span>
                  </motion.button>

                  {activeMenu === item.name && (
                    <motion.div
                      initial={{ opacity: 0, y: 4, scale: 0.97 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 4, scale: 0.97 }}
                      transition={{ duration: 0.15 }}
                      className="absolute left-0 mt-0.5 w-52 bg-[#1c1510] border-2 border-amber-700/80 rounded-lg shadow-2xl py-1 z-50 text-xs font-mono backdrop-blur-md oil-lamp-glow"
                    >
                      <button
                        onClick={() => {
                          if (item.name === "View") onOpenSystemMonitor();
                          setActiveMenu(null);
                        }}
                        className="w-full text-left px-3 py-1.5 hover:bg-amber-950 hover:text-amber-300 flex items-center justify-between cursor-pointer"
                      >
                        <span>{item.name === "View" ? "Open System Monitor" : `${item.name} Actions`}</span>
                        <kbd className="text-[10px] text-stone-500">Alt+{item.name[0]}</kbd>
                      </button>
                      <button
                        onClick={() => {
                          onToggleMode(mode === "sovereign" ? "core" : "sovereign");
                          setActiveMenu(null);
                        }}
                        className="w-full text-left px-3 py-1.5 hover:bg-amber-950 hover:text-amber-300 cursor-pointer"
                      >
                        Switch Interface Mode
                      </button>
                    </motion.div>
                  )}
                </div>
              );
            })}
          </nav>
        </div>

        {/* Center: Dual Interface Switcher with Smooth Slide Animation */}
        <div className="relative flex items-center bg-[#140e0a] border border-amber-800/60 rounded-lg p-1 shadow-inner overflow-hidden font-mono">
          <button
            onClick={() => onToggleMode("sovereign")}
            className="relative z-10 flex items-center gap-1.5 px-3.5 py-1 text-xs font-bold transition-colors cursor-pointer text-stone-200"
          >
            <Terminal className="w-3.5 h-3.5 text-amber-400" />
            <span>Sovereign Terminal</span>
            {mode === "sovereign" && (
              <motion.div
                layoutId="activeModePill"
                className="absolute inset-0 bg-amber-950 border border-amber-500/80 rounded-md shadow-md ring-1 ring-amber-500/30 -z-10"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
          </button>

          <button
            onClick={() => onToggleMode("core")}
            className="relative z-10 flex items-center gap-1.5 px-3.5 py-1 text-xs font-bold transition-colors cursor-pointer text-stone-200"
          >
            <Cpu className="w-3.5 h-3.5 text-amber-400" />
            <span>Nexus Core (Garbhagriha)</span>
            {mode === "core" && (
              <motion.div
                layoutId="activeModePill"
                className="absolute inset-0 bg-amber-900 border border-amber-500/80 rounded-md shadow-md ring-1 ring-amber-500/30 -z-10"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
          </button>
        </div>

        {/* Right: Soundscape Icon + Theme Switcher + 3D Pet Companion + System Health Tags + System Monitor */}
        <div className="flex items-center gap-2 font-mono">
          {/* Temple Theme Switcher */}
          <ThemeSwitcher />

          {/* Soundscape Selector Icon Button */}
          <div className="relative group">
            <button
              className="p-1.5 bg-[#221812] border border-amber-600/70 hover:border-amber-400 hover:bg-amber-950 rounded-lg text-amber-300 transition-all flex items-center gap-1 cursor-pointer"
              title="Temple Soundscape Settings"
            >
              <Volume2 className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
              <select
                value={activeSoundscape}
                onChange={(e) => onChangeSoundscape?.(e.target.value as any)}
                className="bg-transparent text-amber-300 text-[10px] font-bold cursor-pointer focus:outline-none"
              >
                <option value="bells" className="bg-zinc-900 text-amber-300">🔔 Bells</option>
                <option value="monsoon" className="bg-zinc-900 text-amber-300">🌧️ Rain</option>
                <option value="chanting" className="bg-zinc-900 text-amber-300">🧘 Chant</option>
                <option value="solfeggio" className="bg-zinc-900 text-amber-300">✨ 528Hz</option>
              </select>
            </button>
          </div>

          {/* 3D Pet Companion Launcher (Shifted to Right) */}
          <motion.button
            onClick={onOpenPet3D}
            whileHover={{ scale: 1.04, y: -1 }}
            whileTap={{ scale: 0.96 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            title="Open 3D Sacred Guardian Matrix"
            className="group flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#221812] border border-amber-600/70 hover:border-amber-400 hover:bg-amber-950/80 transition-all duration-300 shadow-md active:scale-95 cursor-pointer shrink-0"
          >
            <div className="relative w-4 h-4 rounded bg-amber-950 border border-amber-500/80 flex items-center justify-center text-amber-300">
              <Bot className="w-3 h-3 text-amber-400 animate-pulse" />
              <span className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 rounded-full bg-emerald-400 border border-stone-950 animate-ping" />
            </div>
            <span className="font-bold text-amber-300 text-[11px] group-hover:text-amber-200">
              {petStatus.name}
            </span>
          </motion.button>

          {/* System Health Tags */}
          <div className="hidden xl:flex items-center gap-1.5 font-mono text-[11px] p-0.5 bg-[#1a120b] border border-amber-800/70 rounded-lg shadow-inner">
            <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#221812] border border-amber-800/50 text-amber-300 shadow-sm">
              <Zap className="w-3 h-3 text-amber-400" />
              <span>{vitals.energy}%</span>
            </div>

            <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#221812] border border-amber-800/50 text-cyan-300 shadow-sm">
              <HardDrive className="w-3 h-3 text-cyan-400" />
              <span>{vitals.diskC}%</span>
            </div>

            <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#221812] border border-amber-800/50 text-emerald-400 shadow-sm">
              <Activity className="w-3 h-3" />
              <span>+{vitals.vibe}</span>
            </div>
          </div>

          {/* System Monitor Modal Button (Smaller Curve: rounded-lg) */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            onClick={onOpenSystemMonitor}
            className="flex items-center gap-1.5 px-2.5 py-1 bg-amber-950/90 hover:bg-amber-900 border border-amber-600/70 text-amber-300 rounded-lg text-xs transition-colors shadow-sm font-semibold cursor-pointer shrink-0"
          >
            <Activity className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
            <span className="hidden lg:inline">System Monitor</span>
          </motion.button>
        </div>
      </div>
    </header>
  );
};


