export type InterfaceMode = "sovereign" | "core";

export type ThemeId = "sandstone" | "basalt" | "copper" | "indigo" | "obsidian" | "emerald";

export type PetMood = "calm" | "focused" | "playful" | "concerned" | "happy";
export type PetState = "Idle" | "Thinking" | "Working" | "Focused" | "Concerned" | "Happy" | "Asleep" | "Anomaly";

export interface PetStatus {
  name: string;
  state: PetState;
  mood: PetMood;
  energy: number; // 0-100
  attention: boolean; // is Nexus looking at user
  avatarUrl?: string;
  speechText?: string;
}

export interface VitalsData {
  energy: number;
  ischemia: number; // Disk C %
  hypoxia: number;  // CPU stress %
  fever: number;    // Temperature °C
  vibe: number;     // Endocrine score e.g. +0.34
  status: "Homeostatic" | "Conservation" | "Hypoxic" | "Feverish" | "Alert";
  cpuUsage: number;
  memUsage: string;
  diskC: number;
  diskD: number;
  netDown: string;
  netUp: string;
  lastUpdate: string;
}

export interface SubTask {
  text: string;
  done: boolean;
}

export interface Directive {
  id: string;
  text: string;
  status: "Queued" | "Processing" | "Completed" | "Blocked" | "Failed";
  timestamp: string;
  priority: "High" | "Medium" | "Low";
  subtasks: SubTask[];
  agentBids: string[];
  outcome: string;
}

export interface AOSService {
  name: string;
  description: string;
  status: "online" | "warning" | "error";
  uptime: string;
  lastTick: string;
  logs: string[];
}

export interface FileNode {
  name: string;
  path: string;
  type: "file" | "folder";
  gitStatus?: "M" | "A" | "U" | "D" | "none";
  content?: string;
  language?: string;
  children?: FileNode[];
}

export interface MCPTool {
  id: string;
  name: string;
  category: "motor" | "lattice" | "immune" | "memory" | "evolve" | "endocrine" | "physiology" | "vision" | "mesh";
  description: string;
  params: { name: string; type: string; defaultVal?: string; description: string }[];
  lastResult?: string;
}

export interface DBTable {
  name: string;
  rowsCount: number;
  columns: string[];
  data: Record<string, any>[];
}

export interface APIPlaygroundItem {
  id: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  url: string;
  headers: string;
  body: string;
  responseStatus?: number;
  responseBody?: string;
  timestamp: string;
}

export interface GitCommit {
  hash: string;
  author: string;
  message: string;
  date: string;
  branch: string;
  isHead?: boolean;
}

export interface SystemProcess {
  name: string;
  pid: number;
  cpu: string;
  mem: string;
  path: string;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "nexus";
  text: string;
  timestamp: string;
  codeSnippet?: string;
  contextFile?: string;
}

export interface CoreWorkspaceState {
  focusFile: string;
  directiveBoard: {
    currentDirective: string;
    subtasks: SubTask[];
    blockers: string[];
  };
  openFiles: string[];
  activeSignals: { signal: string; level: string; source: string; since: string; status: string }[];
  agents: { name: string; type: string; status: string; load: string }[];
  instincts: { name: string; drive: string; weight: number }[];
  memoryStream: { title: string; file: string; date: string; category: string }[];
  pulseLog: { time: string; text: string; category: "info" | "warn" | "error" | "tool" }[];
}
