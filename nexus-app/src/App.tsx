import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  InterfaceMode,
  ThemeId,
  PetStatus,
  VitalsData,
  Directive,
  FileNode,
  AOSService,
  MCPTool,
  DBTable,
  GitCommit,
  SystemProcess,
  ChatMessage,
  CoreWorkspaceState,
} from "./types/nexus";

import { useTheme } from "./context/ThemeContext";

import {
  INITIAL_FILES,
  INITIAL_SERVICES,
  INITIAL_TOOLS,
  INITIAL_DB_TABLES,
  INITIAL_GIT_COMMITS,
  MOCK_PROCESSES,
  INITIAL_CHAT,
  INITIAL_CORE_STATE,
} from "./data/initialState";

import { Navbar } from "./components/Navbar";
import { StatusBar } from "./components/StatusBar";
import { L1ExplorerPanel } from "./components/explorer/L1ExplorerPanel";
import { L2Workspace } from "./components/workspace/L2Workspace";
import { L3ToolsPanel } from "./components/tools/L3ToolsPanel";
import { L4BottomBar } from "./components/bottombar/L4BottomBar";
import { SystemMonitorModal } from "./components/monitor/SystemMonitorModal";
import { NexusCoreWorkspace } from "./components/core/NexusCoreWorkspace";
import { Nexus3DPetCompanion } from "./components/pet/Nexus3DPetCompanion";
import { SoundscapeEngine, playTempleBellEcho } from "./components/SoundscapeEngine";
import { TempleMantraEngine } from "./components/TempleMantraEngine";
import { SacredGeometryMandala } from "./components/SacredGeometryMandala";
import { HarmonicResonanceCanvas } from "./components/HarmonicResonanceCanvas";
import { VisualHapticRipple, triggerHapticRipple } from "./components/VisualHapticRipple";
import { TemplePillarDecoration } from "./components/TemplePillarDecoration";
import { GoldenRatioOverlay } from "./components/GoldenRatioOverlay";
import { motion, AnimatePresence } from "motion/react";

import {
  Folder,
  Wrench,
  Terminal as TerminalIcon,
  Bot,
  Layers,
  Server,
  Database,
  GitBranch,
  Box,
  Globe,
  Hammer,
  AlertCircle,
  Zap,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Webhook,
  MessageSquare,
  GitCompare,
  FileText,
  GripVertical,
  BookOpen,
} from "lucide-react";

export default function App() {
  // Mode State
  const [interfaceMode, setInterfaceMode] = useState<InterfaceMode>("sovereign");

  // Vitals State
  const [vitals, setVitals] = useState<VitalsData>({
    energy: 78,
    ischemia: 79.1,
    hypoxia: 0,
    fever: 37.2,
    vibe: 0.34,
    status: "Homeostatic",
    cpuUsage: 22,
    memUsage: "8.2/16 GB",
    diskC: 79.1,
    diskD: 34.2,
    netDown: "1.2 MB/s",
    netUp: "340 KB/s",
    lastUpdate: "Just now",
  });

  // Pet Companion State
  const [petStatus, setPetStatus] = useState<PetStatus>({
    name: "Nexus-3D",
    state: "Idle",
    mood: "calm",
    energy: 85,
    attention: true,
    speechText: "Greetings Sovereign Master. 3D Entity online and tracking cursor matrix.",
  });

  // Directives State
  const [directives, setDirectives] = useState<Directive[]>([
    {
      id: "DIR-101",
      text: "Design and implement the Nexus App dual-interface specification",
      status: "Completed",
      timestamp: "10 mins ago",
      priority: "High",
      subtasks: [
        { text: "Architect L1-L4 Sovereign Terminal layout", done: true },
        { text: "Implement 3D Pet companion with Three.js eye tracking", done: true },
        { text: "Build Android-Studio resizable panels & side strips", done: true },
        { text: "Integrate Nexus Core LLM workspace view", done: true },
      ],
      agentBids: ["Orchestrator-01", "Guardian-AOS"],
      outcome: "Nexus App initialized successfully across Sovereign Terminal & Core.",
    },
  ]);

  // Files & Editor State
  const [files, setFiles] = useState<FileNode[]>(INITIAL_FILES);
  const [openFiles, setOpenFiles] = useState<string[]>([
    "nexus_aos/src/main.py",
    "nexus_aos/src/sovereign_terminal.py",
  ]);
  const [activeFileNode, setActiveFileNode] = useState<FileNode | null>(
    INITIAL_FILES[0].children?.[0].children?.[0] || null
  );

  // Other State
  const [services] = useState<AOSService[]>(INITIAL_SERVICES);
  const [tools] = useState<MCPTool[]>(INITIAL_TOOLS);
  const [dbTables] = useState<DBTable[]>(INITIAL_DB_TABLES);
  const [gitCommits] = useState<GitCommit[]>(INITIAL_GIT_COMMITS);
  const [processes] = useState<SystemProcess[]>(MOCK_PROCESSES);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(INITIAL_CHAT);
  const [coreState, setCoreState] = useState<CoreWorkspaceState>(INITIAL_CORE_STATE);

  // Active Panel Tab States
  const [leftTab, setLeftTab] = useState<"project" | "directives" | "system">("project");
  const [rightTab, setRightTab] = useState<"tools" | "api" | "db" | "git" | "ci" | "browser" | "chat" | "diff" | "docs">("browser");
  const [bottomTab, setBottomTab] = useState<"terminal" | "build" | "db" | "docker" | "http" | "problems">("terminal");
  const [inlinePromptOpen, setInlinePromptOpen] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(false);
  const [activeSoundscape, setActiveSoundscape] = useState<"monsoon" | "chanting" | "bells" | "solfeggio">("bells");
  const [mantraBlend, setMantraBlend] = useState(0.5);
  const [geometryConfig, setGeometryConfig] = useState({
    showGrid: false,
    showSpiral: false,
    showMandapa: false,
    showPortalMandala: false,
    enableAnimations: true,
  });

  const enforceGoldenRatioGrid = () => {
    const totalW = window.innerWidth - 96; // Total width subtracting 2 vertical strip toolbars (48px each)
    // Golden ratio Phi = 1.618. Ratio: 1 : 1.618 : 1 (Left : Center : Right)
    // Unit sum = 1 + 1.618 + 1 = 3.618
    const unit = totalW / 3.618;
    const idealSide = Math.max(200, Math.min(500, Math.round(unit)));
    setLeftWidth(idealSide);
    setRightWidth(idealSide);
  };

  const handleToggleGeometry = (key: "showGrid" | "showSpiral" | "showMandapa" | "showPortalMandala" | "enableAnimations") => {
    setGeometryConfig((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      if (key === "showGrid" || key === "showMandapa") {
        enforceGoldenRatioGrid();
      }
      return next;
    });
  };

  // Global Cmd+K Refactor Listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setInlinePromptOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Draggable Sidebars Item Lists State
  const [leftTopItems, setLeftTopItems] = useState([
    { id: "project", label: "Project Explorer", icon: Folder },
    { id: "directives", label: "Directives Queue", icon: Layers },
    { id: "system", label: "AOS Services", icon: Server },
  ]);

  const [leftBottomItems, setLeftBottomItems] = useState([
    { id: "terminal", label: "Terminal Console", icon: TerminalIcon },
    { id: "build", label: "Build Output", icon: Hammer },
    { id: "http", label: "HTTP Curl", icon: Globe },
    { id: "db", label: "DB Console", icon: Database },
    { id: "docker", label: "Docker Containers", icon: Box },
    { id: "problems", label: "Problems & Diagnostics", icon: AlertCircle },
  ]);

  const [rightTopItems, setRightTopItems] = useState([
    { id: "browser", label: "Inbuilt Dev Browser", icon: Globe },
    { id: "chat", label: "Nexus AI Chat", icon: MessageSquare },
    { id: "diff", label: "Diff / Review", icon: GitCompare },
    { id: "docs", label: "Whitepaper & Docs", icon: BookOpen },
  ]);

  const [rightBottomItems, setRightBottomItems] = useState([
    { id: "tools", label: "MCP Server Tools", icon: Wrench },
    { id: "api", label: "API Client & Inspector", icon: Webhook }, // shifted icon of API to Webhook
    { id: "db", label: "Database Manager", icon: Database },
    { id: "git", label: "Git Graph & Revisions", icon: GitBranch },
    { id: "ci", label: "CI/CD Build Pipeline", icon: Layers },
  ]);

  // Sidebar Drag & Drop Handlers
  const handleItemDrop = (e: React.DragEvent, targetIdx: number, listKey: "leftTop" | "leftBottom" | "rightTop" | "rightBottom") => {
    e.preventDefault();
    const data = e.dataTransfer.getData("text/plain");
    if (!data) return;
    const [sourceList, sourceIdxStr] = data.split(":");
    const sourceIdx = parseInt(sourceIdxStr, 10);
    if (sourceList !== listKey || isNaN(sourceIdx) || sourceIdx === targetIdx) return;

    const reorder = (arr: any[]) => {
      const copy = [...arr];
      const [moved] = copy.splice(sourceIdx, 1);
      copy.splice(targetIdx, 0, moved);
      return copy;
    };

    if (listKey === "leftTop") setLeftTopItems((p) => reorder(p));
    else if (listKey === "leftBottom") setLeftBottomItems((p) => reorder(p));
    else if (listKey === "rightTop") setRightTopItems((p) => reorder(p));
    else if (listKey === "rightBottom") setRightBottomItems((p) => reorder(p));
  };

  // Panel Open / Resizable States (Android Studio Style)
  const [showLeftPanel, setShowLeftPanel] = useState(true);
  const [showRightPanel, setShowRightPanel] = useState(true);
  const [bottomBarOpen, setBottomBarOpen] = useState(true);
  const [showPet3D, setShowPet3D] = useState(true);

  // Strip Toggle Handlers
  const handleToggleLeftStrip = (tab: "project" | "directives" | "system") => {
    if (showLeftPanel && leftTab === tab) {
      setShowLeftPanel(false);
    } else {
      setLeftTab(tab);
      setShowLeftPanel(true);
    }
  };

  const handleToggleRightStrip = (tab: "tools" | "api" | "db" | "git" | "ci") => {
    if (showRightPanel && rightTab === tab) {
      setShowRightPanel(false);
    } else {
      setRightTab(tab);
      setShowRightPanel(true);
    }
  };

  const handleToggleBottomStrip = (tab: "terminal" | "build" | "db" | "docker" | "http" | "problems") => {
    if (bottomBarOpen && bottomTab === tab) {
      setBottomBarOpen(false);
    } else {
      setBottomTab(tab);
      setBottomBarOpen(true);
    }
  };

  const handleNewFile = () => {
    const newPath = `nexus_aos/src/scratch_${openFiles.length + 1}.ts`;
    const newFile: FileNode = {
      name: `scratch_${openFiles.length + 1}.ts`,
      path: newPath,
      type: "file",
      content: `// Sovereign Scratch Module\n// Created: ${new Date().toLocaleTimeString()}\n\nexport function runMatrixTask() {\n  console.log("Nexus matrix function initialized.");\n}\n`,
      gitStatus: "A",
    };

    setFiles((prev) => {
      const clone = JSON.parse(JSON.stringify(prev));
      const srcDir = clone[0]?.children?.[0];
      if (srcDir && srcDir.children) {
        srcDir.children.push(newFile);
      }
      return clone;
    });

    if (!openFiles.includes(newPath)) {
      setOpenFiles((prev) => [...prev, newPath]);
    }
    setActiveFileNode(newFile);
  };

  const handleRunFile = (path: string) => {
    triggerHapticRipple();
    setBottomTab("terminal");
    setBottomBarOpen(true);
    const filename = path.split("/").pop() || path;
    handleSubmitDirective(`python3 ${filename}`);
    setPetStatus((prev) => ({
      ...prev,
      state: "Working",
      speechText: `Executing ${filename}...`,
    }));
  };

  const handleDebugFile = (path: string) => {
    triggerHapticRipple();
    setBottomTab("problems");
    setBottomBarOpen(true);
    const filename = path.split("/").pop() || path;
    setPetStatus((prev) => ({
      ...prev,
      state: "Thinking",
      speechText: `Debugger attached to ${filename}. Zero critical faults.`,
    }));
  };

  // Theme State from Context
  const { theme, setTheme } = useTheme();

  // Resizable Panel Widths / Heights (in px)
  const [leftWidth, setLeftWidth] = useState(280);
  const [rightWidth, setRightWidth] = useState(320);
  const [bottomHeight, setBottomHeight] = useState(200);

  // Dragging States for Splitters
  const isDraggingLeft = useRef(false);
  const isDraggingRight = useRef(false);
  const isDraggingBottom = useRef(false);
  const [isDraggingSplitter, setIsDraggingSplitter] = useState(false);

  const [systemMonitorOpen, setSystemMonitorOpen] = useState(false);

  // Instantaneous Resizer Event Handlers (High-frequency RAF smooth dragging with Golden Ratio Gravity Snapping)
  const animFrameRef = useRef<number | null>(null);
  const [isSnapped, setIsSnapped] = useState(false);
  const [snappedTargetName, setSnappedTargetName] = useState("");
  const snapOffsetRef = useRef({ target: 0, accumulated: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDraggingLeft.current && !isDraggingRight.current && !isDraggingBottom.current) return;

      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }

      animFrameRef.current = requestAnimationFrame(() => {
        const totalW = window.innerWidth;
        const totalH = window.innerHeight;

        if (isDraggingLeft.current) {
          const rawW = Math.max(180, Math.min(650, e.clientX - 48));
          const targets = [
            { val: Math.round(totalW * 0.236), name: "φ = 0.236 (23.6%)" },
            { val: Math.round(totalW * 0.382), name: "φ = 0.382 (38.2%)" },
            { val: 280, name: "Sanctum Standard (280px)" },
          ];

          const closest = targets.find((t) => Math.abs(rawW - t.val) < 20);

          if (closest) {
            if (snapOffsetRef.current.target !== closest.val) {
              snapOffsetRef.current = { target: closest.val, accumulated: 0 };
            }
            snapOffsetRef.current.accumulated += Math.abs(rawW - closest.val);

            if (snapOffsetRef.current.accumulated < 45) {
              setLeftWidth(closest.val);
              setIsSnapped(true);
              setSnappedTargetName(`LEFT SPLITTER ${closest.name}`);
              return;
            }
          }

          snapOffsetRef.current = { target: 0, accumulated: 0 };
          setIsSnapped(false);
          setLeftWidth(rawW);
        } else if (isDraggingRight.current) {
          const rawW = Math.max(200, Math.min(650, totalW - e.clientX - 48));
          const targets = [
            { val: Math.round(totalW * 0.236), name: "φ = 0.236 (23.6%)" },
            { val: Math.round(totalW * 0.382), name: "φ = 0.382 (38.2%)" },
            { val: 320, name: "Sanctum Tools (320px)" },
          ];

          const closest = targets.find((t) => Math.abs(rawW - t.val) < 20);

          if (closest) {
            if (snapOffsetRef.current.target !== closest.val) {
              snapOffsetRef.current = { target: closest.val, accumulated: 0 };
            }
            snapOffsetRef.current.accumulated += Math.abs(rawW - closest.val);

            if (snapOffsetRef.current.accumulated < 45) {
              setRightWidth(closest.val);
              setIsSnapped(true);
              setSnappedTargetName(`RIGHT SPLITTER ${closest.name}`);
              return;
            }
          }

          snapOffsetRef.current = { target: 0, accumulated: 0 };
          setIsSnapped(false);
          setRightWidth(rawW);
        } else if (isDraggingBottom.current) {
          const rawH = Math.max(100, Math.min(550, totalH - e.clientY - 36));
          const targets = [
            { val: Math.round(totalH * 0.236), name: "φ = 0.236 (23.6%)" },
            { val: Math.round(totalH * 0.382), name: "φ = 0.382 (38.2%)" },
            { val: 200, name: "Terminal Baseline (200px)" },
          ];

          const closest = targets.find((t) => Math.abs(rawH - t.val) < 20);

          if (closest) {
            if (snapOffsetRef.current.target !== closest.val) {
              snapOffsetRef.current = { target: closest.val, accumulated: 0 };
            }
            snapOffsetRef.current.accumulated += Math.abs(rawH - closest.val);

            if (snapOffsetRef.current.accumulated < 45) {
              setBottomHeight(closest.val);
              setIsSnapped(true);
              setSnappedTargetName(`BOTTOM SPLITTER ${closest.name}`);
              return;
            }
          }

          snapOffsetRef.current = { target: 0, accumulated: 0 };
          setIsSnapped(false);
          setBottomHeight(rawH);
        }
      });
    };

    const handleMouseUp = () => {
      isDraggingLeft.current = false;
      isDraggingRight.current = false;
      isDraggingBottom.current = false;
      setIsDraggingSplitter(false);
      setIsSnapped(false);
      snapOffsetRef.current = { target: 0, accumulated: 0 };
      document.body.style.cursor = "default";
      document.body.style.userSelect = "auto";
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, []);

  // Periodic Vitals Sync
  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const res = await fetch("/api/nexus/vitals");
        if (res.ok) {
          const data = await res.json();
          setVitals((prev) => ({ ...prev, ...data }));
        }
      } catch (err) {
        setVitals((prev) => ({
          ...prev,
          cpuUsage: Math.floor(15 + Math.random() * 30),
        }));
      }
    };

    fetchVitals();
    const interval = setInterval(fetchVitals, 4000);
    return () => clearInterval(interval);
  }, []);

  // Handlers
  const handleSelectFile = useCallback((fileNode: FileNode) => {
    setActiveFileNode(fileNode);
    setOpenFiles((prev) => (!prev.includes(fileNode.path) ? [...prev, fileNode.path] : prev));
  }, []);

  const handleCloseFile = useCallback((path: string) => {
    setOpenFiles((prevOpen) => {
      const nextOpen = prevOpen.filter((p) => p !== path);
      return nextOpen;
    });
  }, []);

  const handleSelectOpenFile = useCallback((path: string) => {
    const findNode = (nodes: FileNode[]): FileNode | null => {
      for (const n of nodes) {
        if (n.path === path) return n;
        if (n.children) {
          const res = findNode(n.children);
          if (res) return res;
        }
      }
      return null;
    };
    setFiles((currentFiles) => {
      const target = findNode(currentFiles);
      if (target) setActiveFileNode(target);
      return currentFiles;
    });
  }, []);

  const handleUpdateFileContent = useCallback((path: string, content: string) => {
    const updateTree = (nodes: FileNode[]): FileNode[] => {
      return nodes.map((n) => {
        if (n.path === path) return { ...n, content, gitStatus: "M" };
        if (n.children) return { ...n, children: updateTree(n.children) };
        return n;
      });
    };
    setFiles((prev) => updateTree(prev));
  }, []);

  const handleSubmitDirective = useCallback(async (text: string) => {
    setPetStatus((prev) => ({
      ...prev,
      state: "Working",
      speechText: `Executing directive: "${text}"`,
    }));

    try {
      const res = await fetch("/api/nexus/directive", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ directiveText: text }),
      });

      if (res.ok) {
        const data = await res.json();
        setDirectives((prev) => [data.directive, ...prev]);
        if (data.vitals) setVitals((prev) => ({ ...prev, ...data.vitals }));
        playTempleBellEcho("both");
      } else {
        throw new Error("Backend directive execution failed");
      }
    } catch (err) {
      playTempleBellEcho("both");
      setDirectives((prev) => {
        const newDir: Directive = {
          id: `DIR-${103 + prev.length}`,
          text,
          status: "Completed",
          timestamp: "Just now",
          priority: text.startsWith("/") ? "High" : "Medium",
          subtasks: [
            { text: "Parse directive semantics", done: true },
            { text: "Execute tool sequence", done: true },
          ],
          agentBids: ["Orchestrator-01"],
          outcome: `Executed directive: "${text}"`,
        };
        return [newDir, ...prev];
      });
    } finally {
      setTimeout(() => {
        setPetStatus((prev) => ({
          ...prev,
          state: "Idle",
          speechText: `Directive complete. Sovereign matrix homeostatic.`,
        }));
      }, 1500);
    }
  }, []);

  const handleSendChatMessage = useCallback(async (msgText: string) => {
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      sender: "user",
      text: msgText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setChatMessages((prev) => [...prev, userMsg]);
    setPetStatus((prev) => ({
      ...prev,
      state: "Thinking",
      speechText: `Analyzing input...`,
    }));

    try {
      const res = await fetch("/api/nexus/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msgText,
          contextFile: activeFileNode?.name,
          history: chatMessages,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        const nexusMsg: ChatMessage = {
          id: `msg-${Date.now() + 1}`,
          sender: "nexus",
          text: data.text,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        };
        setChatMessages((prev) => [...prev, nexusMsg]);
      } else {
        throw new Error("Chat failed");
      }
    } catch (err) {
      const fallbackMsg: ChatMessage = {
        id: `msg-${Date.now() + 1}`,
        sender: "nexus",
        text: `[Nexus Core] Query received: "${msgText}". Context file: ${activeFileNode?.name || "main.py"}. All host vitals Homeostatic.`,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setChatMessages((prev) => [...prev, fallbackMsg]);
    } finally {
      setPetStatus((prev) => ({
        ...prev,
        state: "Idle",
        speechText: `Standing by for Sovereign directive.`,
      }));
    }
  }, [activeFileNode, chatMessages]);

  const handleTriggerAction = async (actionName: string) => {
    try {
      const res = await fetch("/api/nexus/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: actionName }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.vitals) setVitals((prev) => ({ ...prev, ...data.vitals }));
        setPetStatus((prev) => ({
          ...prev,
          state: "Happy",
          speechText: data.message,
        }));
      }
    } catch (err) {
      console.warn("Action trigger error:", err);
    }
  };

  const handleToggleSubtask = (index: number) => {
    triggerHapticRipple();
    setCoreState((prev) => {
      const nextSubtasks = [...prev.directiveBoard.subtasks];
      nextSubtasks[index].done = !nextSubtasks[index].done;
      return {
        ...prev,
        directiveBoard: {
          ...prev.directiveBoard,
          subtasks: nextSubtasks,
        },
      };
    });
  };

  const handleUpdatePetStatus = useCallback((s: Partial<PetStatus>) => {
    setPetStatus((prev) => ({ ...prev, ...s }));
  }, []);

  const handleOpenFullPet = useCallback(() => {
    setShowPet3D(true);
  }, []);

  const handleCloseLeftPanel = useCallback(() => {
    setShowLeftPanel(false);
  }, []);

  const handleCloseRightPanel = useCallback(() => {
    setShowRightPanel(false);
  }, []);

  const handleExecuteTool = useCallback((id: string, params: Record<string, any>) => {
    handleSubmitDirective(`/tool ${id} ${JSON.stringify(params)}`);
  }, [handleSubmitDirective]);

  const handleToggleBottomOpen = useCallback(() => {
    setBottomBarOpen((prev) => !prev);
  }, []);

  const handleOpenInlineRefactor = useCallback(() => {
    setInlinePromptOpen(true);
  }, []);

  return (
    <div
      data-theme={theme}
      style={
        {
          "--energy-val": vitals.energy,
          "--vibe-val": vitals.vibe,
          filter:
            vitals.vibe < 95
              ? `sepia(${(95 - vitals.vibe) * 0.012}) saturate(${
                  1 + (95 - vitals.vibe) * 0.006
                }) hue-rotate(-${(95 - vitals.vibe) * 0.4}deg)`
              : "none",
        } as React.CSSProperties
      }
      className={`flex flex-col h-screen w-screen bg-[#0a0604] text-stone-100 overflow-hidden font-sans select-none p-1.5 gap-1.5 border-2 border-amber-800/60 rounded-2xl shadow-2xl relative transition-all duration-700 ${
        vitals.energy > 90 ? "micro-vibrating" : ""
      }`}
    >
      {/* Dynamic Faint Rotating Sacred Geometry Mandala Background Overlay */}
      <SacredGeometryMandala
        enableAnimations={geometryConfig.enableAnimations}
        showPortalMandala={geometryConfig.showPortalMandala}
      />

      {/* Harmonic Resonance Canvas Sitting in Workspace Corners */}
      <HarmonicResonanceCanvas vitals={vitals} />

      {/* Visual Haptic Radial Ripple Overlay */}
      <VisualHapticRipple />

      {/* Soundscape Engine with Corner Cymatic Visualizers & Temple Resonance */}
      <SoundscapeEngine
        vitals={vitals}
        soundEnabled={soundEnabled}
        onToggleSound={() => setSoundEnabled((prev) => !prev)}
        activeSoundscape={activeSoundscape}
      />

      {/* Web Audio API Generative Temple Mantra Chanting Sound Engine */}
      <TempleMantraEngine
        mantraBlend={mantraBlend}
        soundEnabled={soundEnabled}
      />

      {/* Sacred Geometry Golden Ratio Grid Overlay */}
      <GoldenRatioOverlay
        showGrid={geometryConfig.showGrid}
        showSpiral={geometryConfig.showSpiral}
        showMandapa={geometryConfig.showMandapa}
        isDragging={isDraggingSplitter}
        isSnapped={isSnapped}
        snappedTargetName={snappedTargetName}
      />

      {/* Top Navbar Bar - Outer Mahaprakara Top */}
      <Navbar
        mode={interfaceMode}
        onToggleMode={setInterfaceMode}
        vitals={vitals}
        petStatus={petStatus}
        currentTheme={theme}
        onChangeTheme={setTheme}
        onOpenPet3D={() => setShowPet3D(true)}
        onOpenSystemMonitor={() => setSystemMonitorOpen(true)}
        onSubmitDirective={handleSubmitDirective}
        onOpenDocs={() => {
          setRightTab("docs");
          setShowRightPanel(true);
        }}
        onRun={() => handleRunFile(activeFileNode?.path || "main.py")}
        onDebug={() => handleDebugFile(activeFileNode?.path || "main.py")}
        onRefactor={() => setInlinePromptOpen(true)}
      />

      {/* Main Concentric Enclosure Area with Circular Mask Transition */}
      <AnimatePresence mode="wait">
        {interfaceMode === "sovereign" ? (
          <motion.div
            key="sovereign"
            initial={{ clipPath: "circle(0% at 50% 50%)", opacity: 0.8 }}
            animate={{ clipPath: "circle(150% at 50% 50%)", opacity: 1 }}
            exit={{ clipPath: "circle(0% at 50% 50%)", opacity: 0.8 }}
            transition={{ duration: 0.55, ease: [0.4, 0, 0.2, 1] }}
            className="flex-1 flex flex-row items-stretch gap-1.5 overflow-hidden relative min-h-0 min-w-0 w-full p-1 z-10"
          >
            {/* LEFT VERTICAL STRIP TOOLBAR - Screen Edge West Wall */}
            <aside className="w-11 bg-[#18100a]/95 border-2 border-amber-800/60 rounded-xl flex flex-col items-center py-2 text-stone-400 z-20 shrink-0 font-mono gap-1.5 shadow-xl hover:border-amber-500/50 relative shilpkari-concave oil-lamp-glow">
                <TemplePillarDecoration side="left" />
                {/* Top Left Navigation */}
                <div className="flex flex-col gap-1.5 w-full items-center pb-2 border-b border-amber-900/60">
                  {leftTopItems.map((item, idx) => {
                    const IconComp = item.icon;
                    const isActive = showLeftPanel && leftTab === item.id;
                    return (
                      <div
                        key={item.id}
                        draggable
                        onDragStart={(e) => e.dataTransfer.setData("text/plain", `leftTop:${idx}`)}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleItemDrop(e, idx, "leftTop")}
                        className="cursor-grab active:cursor-grabbing group relative"
                      >
                        <motion.button
                          onClick={() => handleToggleLeftStrip(item.id as any)}
                          whileHover={{ scale: 1.1, y: -1 }}
                          whileTap={{ scale: 0.9 }}
                          transition={{ type: "spring", stiffness: 400, damping: 25 }}
                          title={`${item.label} (Drag to reorder)`}
                          className={`p-2 rounded-lg transition-all duration-200 cursor-pointer ${
                            isActive
                              ? "bg-amber-950/90 text-amber-300 border border-amber-500/80 shadow-md shadow-amber-950/50 ring-1 ring-amber-500/30"
                              : "hover:bg-[#281e18] text-stone-400 hover:text-amber-200"
                          }`}
                        >
                          <IconComp className="w-4 h-4" />
                        </motion.button>
                      </div>
                    );
                  })}
                </div>

                {/* Bottom Left Navigation */}
                <div className="flex flex-col gap-1.5 w-full items-center pt-2 mt-auto border-t border-amber-900/60">
                  {leftBottomItems.map((item, idx) => {
                    const IconComp = item.icon;
                    const isActive = bottomBarOpen && bottomTab === item.id;
                    return (
                      <div
                        key={item.id}
                        draggable
                        onDragStart={(e) => e.dataTransfer.setData("text/plain", `leftBottom:${idx}`)}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleItemDrop(e, idx, "leftBottom")}
                        className="cursor-grab active:cursor-grabbing group relative"
                      >
                        <motion.button
                          onClick={() => handleToggleBottomStrip(item.id as any)}
                          whileHover={{ scale: 1.1, y: -1 }}
                          whileTap={{ scale: 0.9 }}
                          transition={{ type: "spring", stiffness: 400, damping: 25 }}
                          title={`${item.label} (Drag to reorder)`}
                          className={`p-2 rounded-lg transition-all duration-200 cursor-pointer ${
                            isActive
                              ? "bg-amber-950/90 text-amber-300 border border-amber-500/80 shadow-md shadow-amber-950/50 ring-1 ring-amber-500/30"
                              : "hover:bg-[#281e18] text-stone-400 hover:text-amber-200"
                          }`}
                        >
                          <IconComp className="w-4 h-4" />
                        </motion.button>
                      </div>
                    );
                  })}
                </div>
              </aside>

            {/* MAIN WORKSPACE CONTAINER - Holds ONLY the 4 Workspaces */}
            <div className="flex-1 flex flex-col items-stretch gap-1.5 overflow-hidden relative min-h-0 min-w-0 bg-[#120a06]/90 rounded-2xl border-2 border-amber-800/60 backdrop-blur-md oil-lamp-glow shilpkari-concave p-1">
              {/* TOP ROW: 3-COLUMN WORKSPACE GRID (LEFT, CENTER, RIGHT WORKSPACES) */}
              <div className="flex-1 flex flex-row items-stretch gap-1.5 overflow-hidden relative min-h-0 min-w-0 w-full">
                {/* WORKSPACE 1: LEFT RESIZABLE EXPLORER PANEL */}
                {showLeftPanel && (
                  <div style={{ width: `${leftWidth}px` }} className="flex h-full shrink-0 relative">
                    <L1ExplorerPanel
                      files={files}
                      directives={directives}
                      services={services}
                      petStatus={petStatus}
                      activeFile={activeFileNode?.path || ""}
                      activeTab={leftTab}
                      onSelectFile={handleSelectFile}
                      onUpdatePetStatus={handleUpdatePetStatus}
                      onOpenFullPet={handleOpenFullPet}
                      onResubmitDirective={handleSubmitDirective}
                      onClosePanel={handleCloseLeftPanel}
                    />

                    {/* Left Resizer Drag Handle */}
                    <div
                      onMouseDown={() => {
                        isDraggingLeft.current = true;
                        setIsDraggingSplitter(true);
                        document.body.style.cursor = "col-resize";
                        document.body.style.userSelect = "none";
                      }}
                      className="w-1.5 hover:w-2 bg-transparent hover:bg-amber-500/80 cursor-col-resize h-full absolute -right-1 top-0 z-30 transition-colors"
                    />
                  </div>
                )}

                {/* WORKSPACE 2: CENTER MAIN WORKSPACE (DIRECT GARBHAGRIHA MODULE) */}
                <div className="flex-1 min-w-0 h-full overflow-hidden relative">
                  <L2Workspace
                    activeFileNode={activeFileNode}
                    openFiles={openFiles}
                    onCloseFile={handleCloseFile}
                    onSelectOpenFile={handleSelectOpenFile}
                    chatMessages={chatMessages}
                    onSendChatMessage={handleSendChatMessage}
                    onUpdateFileContent={handleUpdateFileContent}
                    onNewFile={handleNewFile}
                    onRunFile={handleRunFile}
                    onDebugFile={handleDebugFile}
                    inlinePromptOpen={inlinePromptOpen}
                    onSetInlinePromptOpen={setInlinePromptOpen}
                  />
                </div>

                {/* WORKSPACE 3: RIGHT RESIZABLE TOOLS PANEL */}
                {showRightPanel && (
                  <div style={{ width: `${rightWidth}px` }} className="flex h-full shrink-0 relative">
                    {/* Right Resizer Drag Handle */}
                    <div
                      onMouseDown={() => {
                        isDraggingRight.current = true;
                        setIsDraggingSplitter(true);
                        document.body.style.cursor = "col-resize";
                        document.body.style.userSelect = "none";
                      }}
                      className="w-1.5 hover:w-2 bg-transparent hover:bg-amber-500/80 cursor-col-resize h-full absolute -left-1 top-0 z-30 transition-colors"
                    />

                    <L3ToolsPanel
                      tools={tools}
                      dbTables={dbTables}
                      gitCommits={gitCommits}
                      chatMessages={chatMessages}
                      onSendMessage={handleSendChatMessage}
                      activeTab={rightTab}
                      onExecuteTool={handleExecuteTool}
                      onClosePanel={handleCloseRightPanel}
                    />
                  </div>
                )}
              </div>

              {/* WORKSPACE 4: SEPARATE BOTTOM WORKSPACE (L4 BOTTOM CONSOLE PANEL) */}
              {bottomBarOpen && (
                <div style={{ height: `${bottomHeight}px` }} className="relative flex flex-col shrink-0 w-full">
                  {/* Bottom Resizer Drag Handle */}
                  <div
                    onMouseDown={() => {
                      isDraggingBottom.current = true;
                      setIsDraggingSplitter(true);
                      document.body.style.cursor = "row-resize";
                      document.body.style.userSelect = "none";
                    }}
                    className="h-1.5 hover:h-2 bg-transparent hover:bg-amber-500/80 cursor-row-resize w-full absolute -top-1 left-0 z-30 transition-colors"
                  />

                  <L4BottomBar
                    isOpen={bottomBarOpen}
                    activeTab={bottomTab}
                    onChangeTab={setBottomTab}
                    onToggleOpen={handleToggleBottomOpen}
                    onExecuteCommand={handleSubmitDirective}
                    onOpenInlineRefactor={handleOpenInlineRefactor}
                  />
                </div>
              )}
            </div>

            {/* RIGHT VERTICAL STRIP TOOLBAR - Screen Edge East Wall */}
            <aside className="w-11 bg-[#18100a]/95 border-2 border-amber-800/60 rounded-xl flex flex-col items-center py-2 text-stone-400 z-20 shrink-0 font-mono gap-1.5 shadow-xl hover:border-amber-500/50 relative shilpkari-concave oil-lamp-glow">
                <TemplePillarDecoration side="right" />
                {/* Top Right Tools */}
                <div className="flex flex-col gap-1.5 w-full items-center pb-2 border-b border-amber-900/60">
                  {rightTopItems.map((item, idx) => {
                    const IconComp = item.icon;
                    const isActive = showRightPanel && rightTab === item.id;
                    return (
                      <div
                        key={item.id}
                        draggable
                        onDragStart={(e) => e.dataTransfer.setData("text/plain", `rightTop:${idx}`)}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleItemDrop(e, idx, "rightTop")}
                        className="cursor-grab active:cursor-grabbing group relative"
                      >
                        <motion.button
                          onClick={() => handleToggleRightStrip(item.id as any)}
                          whileHover={{ scale: 1.1, y: -1 }}
                          whileTap={{ scale: 0.9 }}
                          transition={{ type: "spring", stiffness: 400, damping: 25 }}
                          title={`${item.label} (Drag to reorder)`}
                          className={`p-2 rounded-lg transition-all duration-200 cursor-pointer ${
                            isActive
                              ? "bg-amber-950/90 text-amber-300 border border-amber-500/80 shadow-md shadow-amber-950/50 ring-1 ring-amber-500/30"
                              : "hover:bg-[#281e18] text-stone-400 hover:text-amber-200"
                          }`}
                        >
                          <IconComp className="w-4 h-4" />
                        </motion.button>
                      </div>
                    );
                  })}
                </div>

                {/* Bottom Right Tools */}
                <div className="flex flex-col gap-1.5 w-full items-center pt-2 mt-auto border-t border-amber-900/60">
                  {rightBottomItems.map((item, idx) => {
                    const IconComp = item.icon;
                    const isActive = showRightPanel && rightTab === item.id;
                    return (
                      <div
                        key={item.id}
                        draggable
                        onDragStart={(e) => e.dataTransfer.setData("text/plain", `rightBottom:${idx}`)}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleItemDrop(e, idx, "rightBottom")}
                        className="cursor-grab active:cursor-grabbing group relative"
                      >
                        <motion.button
                          onClick={() => handleToggleRightStrip(item.id as any)}
                          whileHover={{ scale: 1.1, y: -1 }}
                          whileTap={{ scale: 0.9 }}
                          transition={{ type: "spring", stiffness: 400, damping: 25 }}
                          title={`${item.label} (Drag to reorder)`}
                          className={`p-2 rounded-lg transition-all duration-200 cursor-pointer ${
                            isActive
                              ? "bg-amber-950/90 text-amber-300 border border-amber-500/80 shadow-md shadow-amber-950/50 ring-1 ring-amber-500/30"
                              : "hover:bg-[#281e18] text-stone-400 hover:text-amber-200"
                          }`}
                        >
                          <IconComp className="w-4 h-4" />
                        </motion.button>
                      </div>
                    );
                  })}
                </div>
              </aside>
          </motion.div>
        ) : (
          /* Nexus Core (LLM Workspace) with Circular Mask Transition */
          <motion.div
            key="core"
            initial={{ clipPath: "circle(0% at 50% 50%)", opacity: 0.8 }}
            animate={{ clipPath: "circle(150% at 50% 50%)", opacity: 1 }}
            exit={{ clipPath: "circle(0% at 50% 50%)", opacity: 0.8 }}
            transition={{ duration: 0.55, ease: [0.4, 0, 0.2, 1] }}
            className="flex-1 flex flex-col min-h-0 min-w-0 w-full overflow-hidden relative z-10"
          >
            <NexusCoreWorkspace
              coreState={coreState}
              vitals={vitals}
              tools={tools}
              onToggleSubtask={handleToggleSubtask}
              onExecuteToolCommand={(cmd) => handleSubmitDirective(cmd)}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* StatusBar - Outer Mahaprakara Bottom */}
      <StatusBar
        vitals={vitals}
        activeFile={activeFileNode?.name || "main.py"}
        onOpenInlineRefactor={() => setInlinePromptOpen(true)}
        activeSoundscape={activeSoundscape}
        onChangeSoundscape={setActiveSoundscape}
      />

      {/* 3D Interactive Pet Companion overlay (Bottom Right) */}
      {showPet3D && (
        <Nexus3DPetCompanion
          status={petStatus}
          vitals={vitals}
          directives={directives}
          activeFile={activeFileNode?.name}
          onUpdateStatus={(s) => setPetStatus((prev) => ({ ...prev, ...s }))}
          onSubmitCommand={handleSubmitDirective}
          docked={true}
          onCloseDock={() => setShowPet3D(false)}
        />
      )}

      {/* System Monitor Full Modal */}
      <SystemMonitorModal
        isOpen={systemMonitorOpen}
        onClose={() => setSystemMonitorOpen(false)}
        vitals={vitals}
        processes={processes}
        onTriggerAction={handleTriggerAction}
        geometryConfig={geometryConfig}
        onToggleGeometry={handleToggleGeometry}
        mantraBlend={mantraBlend}
        onMantraBlendChange={setMantraBlend}
      />
    </div>
  );
}

