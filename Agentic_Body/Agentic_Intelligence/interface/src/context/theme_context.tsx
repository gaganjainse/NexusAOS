import React, { createContext, useContext, useState, useEffect } from "react";
import { ThemeId } from "../types/Sesha";

export interface ThemeDefinition {
  id: ThemeId;
  name: string;
  icon: string;
  description: string;
  vars: Record<string, string>;
}

export const THEMES: Record<ThemeId, ThemeDefinition> = {
  sandstone: {
    id: "sandstone",
    name: "Sandstone Mandir",
    icon: "🏛️",
    description: "Warm golden sandstone & terracotta amber glow",
    vars: {
      "--bg-primary": "#0a0604",
      "--panel-bg": "#120a06",
      "--header-bg": "#1f1712",
      "--border-color": "rgba(180, 83, 9, 0.6)",
      "--border-bright": "rgba(245, 158, 11, 0.85)",
      "--accent-color": "#f59e0b",
      "--accent-glow": "rgba(245, 158, 11, 0.35)",
      "--text-primary": "#f3f4f6",
      "--text-muted": "#d97706",
      "--pill-bg": "#221812",
      "--pill-border": "rgba(217, 119, 6, 0.6)",
      "--pill-hover": "#382215",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.92), inset 1px 1px 3px rgba(0, 0, 0, 0.98), inset -2px -2px 8px rgba(245, 158, 11, 0.25), inset 0 0 16px rgba(15, 9, 5, 0.85), 0 4px 18px rgba(0, 0, 0, 0.75), 0 0 2px rgba(217, 119, 6, 0.3)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.85), 0 2px 6px rgba(0, 0, 0, 0.9), inset 0 1.5px 3px rgba(251, 191, 36, 0.4), inset 0 -3px 8px rgba(0, 0, 0, 0.85), inset -1px 0 4px rgba(180, 83, 9, 0.2), 0 0 12px rgba(217, 119, 6, 0.15)",
    },
  },
  basalt: {
    id: "basalt",
    name: "Volcanic Basalt",
    icon: "🌋",
    description: "Deep charcoal basalt stone & molten crimson light",
    vars: {
      "--bg-primary": "#090607",
      "--panel-bg": "#12090b",
      "--header-bg": "#1d0e12",
      "--border-color": "rgba(190, 18, 60, 0.6)",
      "--border-bright": "rgba(244, 63, 94, 0.85)",
      "--accent-color": "#f43f5e",
      "--accent-glow": "rgba(244, 63, 94, 0.35)",
      "--text-primary": "#fecdd3",
      "--text-muted": "#e11d48",
      "--pill-bg": "#230f14",
      "--pill-border": "rgba(225, 29, 72, 0.6)",
      "--pill-hover": "#3b141d",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.95), inset 1px 1px 3px rgba(0, 0, 0, 0.98), inset -2px -2px 8px rgba(244, 63, 94, 0.25), inset 0 0 16px rgba(18, 9, 11, 0.85), 0 4px 18px rgba(0, 0, 0, 0.8), 0 0 2px rgba(225, 29, 72, 0.3)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.88), 0 2px 6px rgba(0, 0, 0, 0.92), inset 0 1.5px 3px rgba(251, 113, 133, 0.4), inset 0 -3px 8px rgba(0, 0, 0, 0.88), inset -1px 0 4px rgba(190, 18, 60, 0.2), 0 0 12px rgba(225, 29, 72, 0.15)",
    },
  },
  copper: {
    id: "copper",
    name: "Ancient Copper",
    icon: "🏺",
    description: "Burnished bronze, oxidized patina & warm fire",
    vars: {
      "--bg-primary": "#0c0804",
      "--panel-bg": "#160f08",
      "--header-bg": "#24180e",
      "--border-color": "rgba(217, 119, 6, 0.65)",
      "--border-bright": "rgba(251, 146, 60, 0.9)",
      "--accent-color": "#f97316",
      "--accent-glow": "rgba(249, 115, 22, 0.35)",
      "--text-primary": "#ffedd5",
      "--text-muted": "#ea580c",
      "--pill-bg": "#28170b",
      "--pill-border": "rgba(234, 88, 12, 0.6)",
      "--pill-hover": "#3d220f",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.92), inset 1px 1px 3px rgba(0, 0, 0, 0.98), inset -2px -2px 8px rgba(249, 115, 22, 0.25), inset 0 0 16px rgba(22, 15, 8, 0.85), 0 4px 18px rgba(0, 0, 0, 0.75), 0 0 2px rgba(234, 88, 12, 0.3)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.85), 0 2px 6px rgba(0, 0, 0, 0.9), inset 0 1.5px 3px rgba(253, 186, 116, 0.4), inset 0 -3px 8px rgba(0, 0, 0, 0.85), inset -1px 0 4px rgba(217, 119, 6, 0.2), 0 0 12px rgba(234, 88, 12, 0.15)",
    },
  },
  indigo: {
    id: "indigo",
    name: "Cosmic Indigo",
    icon: "🌌",
    description: "Sacred night sky, sapphire stone & starlight bioluminescence",
    vars: {
      "--bg-primary": "#04060c",
      "--panel-bg": "#090d18",
      "--header-bg": "#101627",
      "--border-color": "rgba(67, 56, 202, 0.65)",
      "--border-bright": "rgba(129, 140, 248, 0.9)",
      "--accent-color": "#6366f1",
      "--accent-glow": "rgba(99, 102, 241, 0.35)",
      "--text-primary": "#e0e7ff",
      "--text-muted": "#4f46e5",
      "--pill-bg": "#12182d",
      "--pill-border": "rgba(79, 70, 229, 0.6)",
      "--pill-hover": "#1e2747",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.95), inset 1px 1px 3px rgba(0, 0, 0, 0.98), inset -2px -2px 8px rgba(99, 102, 241, 0.25), inset 0 0 16px rgba(9, 13, 24, 0.85), 0 4px 18px rgba(0, 0, 0, 0.8), 0 0 2px rgba(79, 70, 229, 0.3)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.88), 0 2px 6px rgba(0, 0, 0, 0.92), inset 0 1.5px 3px rgba(165, 180, 252, 0.4), inset 0 -3px 8px rgba(0, 0, 0, 0.88), inset -1px 0 4px rgba(67, 56, 202, 0.2), 0 0 12px rgba(79, 70, 229, 0.15)",
    },
  },
  obsidian: {
    id: "obsidian",
    name: "Monochrome Obsidian",
    icon: "🖤",
    description: "Pure obsidian mirror & radiant gold trim",
    vars: {
      "--bg-primary": "#050505",
      "--panel-bg": "#0c0c0c",
      "--header-bg": "#171717",
      "--border-color": "rgba(161, 161, 170, 0.5)",
      "--border-bright": "rgba(228, 228, 231, 0.85)",
      "--accent-color": "#e4e4e7",
      "--accent-glow": "rgba(228, 228, 231, 0.25)",
      "--text-primary": "#f4f4f5",
      "--text-muted": "#a1a1aa",
      "--pill-bg": "#1c1c1f",
      "--pill-border": "rgba(113, 113, 122, 0.6)",
      "--pill-hover": "#2a2a2e",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.98), inset 1px 1px 3px rgba(0, 0, 0, 0.99), inset -2px -2px 8px rgba(255, 255, 255, 0.1), inset 0 0 16px rgba(12, 12, 12, 0.95), 0 4px 18px rgba(0, 0, 0, 0.85), 0 0 2px rgba(161, 161, 170, 0.2)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.9), 0 2px 6px rgba(0, 0, 0, 0.95), inset 0 1.5px 3px rgba(255, 255, 255, 0.3), inset 0 -3px 8px rgba(0, 0, 0, 0.9), inset -1px 0 4px rgba(161, 161, 170, 0.15), 0 0 12px rgba(228, 228, 231, 0.1)",
    },
  },
  emerald: {
    id: "emerald",
    name: "Forest Emerald",
    icon: "🌿",
    description: "Verdant jade temple, mossy stone & auric green",
    vars: {
      "--bg-primary": "#030805",
      "--panel-bg": "#07120a",
      "--header-bg": "#0e1f13",
      "--border-color": "rgba(16, 185, 129, 0.6)",
      "--border-bright": "rgba(52, 211, 153, 0.85)",
      "--accent-color": "#10b981",
      "--accent-glow": "rgba(16, 185, 129, 0.35)",
      "--text-primary": "#d1fae5",
      "--text-muted": "#059669",
      "--pill-bg": "#102316",
      "--pill-border": "rgba(5, 150, 105, 0.6)",
      "--pill-hover": "#173722",
      "--concave-shadow": "inset 4px 4px 12px rgba(0, 0, 0, 0.95), inset 1px 1px 3px rgba(0, 0, 0, 0.98), inset -2px -2px 8px rgba(16, 185, 129, 0.25), inset 0 0 16px rgba(7, 18, 10, 0.85), 0 4px 18px rgba(0, 0, 0, 0.8), 0 0 2px rgba(5, 150, 105, 0.3)",
      "--convex-shadow": "0 6px 20px rgba(0, 0, 0, 0.88), 0 2px 6px rgba(0, 0, 0, 0.92), inset 0 1.5px 3px rgba(110, 231, 183, 0.4), inset 0 -3px 8px rgba(0, 0, 0, 0.88), inset -1px 0 4px rgba(16, 185, 129, 0.2), 0 0 12px rgba(5, 150, 105, 0.15)",
    },
  },
};

interface ThemeContextType {
  theme: ThemeId;
  setTheme: (theme: ThemeId) => void;
  themeConfig: ThemeDefinition;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode; initialTheme?: ThemeId }> = ({
  children,
  initialTheme = "sandstone",
}) => {
  const [theme, setThemeState] = useState<ThemeId>(() => {
    const saved = localStorage.getItem("Sesha_theme");
    return (saved && saved in THEMES) ? (saved as ThemeId) : initialTheme;
  });

  const setTheme = (newTheme: ThemeId) => {
    setThemeState(newTheme);
    localStorage.setItem("Sesha_theme", newTheme);
  };

  const themeConfig = THEMES[theme] || THEMES.sandstone;

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute("data-theme", theme);
    Object.entries(themeConfig.vars).forEach(([key, val]: [string, string]) => {
      root.style.setProperty(key, val);
    });
  }, [theme, themeConfig]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themeConfig }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

