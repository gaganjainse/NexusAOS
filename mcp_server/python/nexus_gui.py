import json
import customtkinter as ctk
import sys
import logging
import time
import math
import subprocess
import yaml
from pathlib import Path

from tools.physiology_engine import PhysiologyEngine
from tools.nexus_lattice import LatticeEngine
from tools.nexus_liver import NexusLiver
from tools.nexus_senses import NexusSenses
from tools.physiological_gate import PhysiologicalGate
from tools.orchestrator_engine import OrchestratorEngine
from tools.service_heartbeat import ServiceHeartbeat
from tools.cellular_engine import CellularEngine
from tools.antibody_engine import AntibodyEngine
from tools.fission_fusion_engine import FissionFusionEngine
from tools.vision_engine import VisionEngine

# Configuration & Theming
THEME = {
    "bg": "#050508",
    "sidebar": "#0D0D14",
    "header": "#12121A",
    "card": "#161622",
    "accent": "#00F0FF",
    "alert": "#FF0055",
    "warning": "#FFA500",
    "success": "#39FF14",
    "text_main": "#E0E0E0",
    "text_dim": "#707075",
}

SERVICE_STALE = {
    "pulse": 360,
    "guardian": 30,
    "senses": 25,
    "orchestrator": 20,
    "supervisor": 30,
}


def get_base_dir():
    return Path(__file__).resolve().parent.parent.parent


def _ensure_plugins_path(base_dir: Path):
    root = str(base_dir)
    if root not in sys.path:
        sys.path.insert(0, root)


class NeuralOscillator(ctk.CTkCanvas):
    """Draws real-time animated waveforms for physiological metrics."""

    def __init__(self, master, color, **kwargs):
        super().__init__(master, bg=THEME["sidebar"], highlightthickness=0, **kwargs)
        self.color = color
        self.points = [0] * 50
        self.animate()

    def animate(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1:
            coords = []
            for i, p in enumerate(self.points):
                x = (i / len(self.points)) * w
                y = (h / 2) + (p * h / 2)
                coords.extend([x, y])
            if len(coords) >= 4:
                self.create_line(coords, fill=self.color, width=2, smooth=True)
        self.after(100, self.animate)

    def update_val(self, val):
        self.points.pop(0)
        self.points.append(val)


class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.base_dir = get_base_dir()
        _ensure_plugins_path(self.base_dir)

        self.phys = PhysiologyEngine(self.base_dir)
        self.lattice = LatticeEngine(self.base_dir)
        self.liver = NexusLiver(self.base_dir)
        self.senses = NexusSenses(self.base_dir)
        self.gate = PhysiologicalGate(self.base_dir)
        self.orchestrator = OrchestratorEngine(self.base_dir)
        self.cellular = CellularEngine(self.base_dir)
        self.antibody = AntibodyEngine(self.base_dir)
        self.fission_fusion = FissionFusionEngine(self.base_dir)
        self.vision = VisionEngine(self.base_dir)

        from plugins.plugin_registry import PluginRegistry
        self.plugin_registry = PluginRegistry(self.base_dir)

        self.logic_graph = self._load_logic_graph()
        self.roles_loaded = False

        self.title("AOS NEURAL TERMINAL V5.0")
        self.geometry("1500x980")
        self.configure(fg_color=THEME["bg"])

        self.grid_columnconfigure(0, weight=0, minsize=300)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1, minsize=350)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self._setup_physiological_sidebar()
        self._setup_cognitive_core()
        self._setup_intel_stack()
        self._setup_footer_matrix()

        self.sync_and_reload()
        self.auto_heartbeat()

    def _load_logic_graph(self):
        yaml_path = self.base_dir / "core" / "nlg" / "nexus_logic.yaml"
        if yaml_path.exists():
            try:
                with open(yaml_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or []
            except Exception:
                return []
        return []

    def _setup_physiological_sidebar(self):
        side = ctk.CTkFrame(self, fg_color=THEME["sidebar"], corner_radius=0)
        side.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            side, text="AOS", font=ctk.CTkFont(family="Orbitron", size=24, weight="bold"),
            text_color=THEME["accent"],
        ).pack(pady=(30, 5))
        ctk.CTkLabel(
            side, text="Agentic Operating System", font=ctk.CTkFont(size=9),
            text_color=THEME["text_dim"],
        ).pack()

        self.bpm_label = ctk.CTkLabel(
            side, text="❤ 60 BPM", font=ctk.CTkFont(size=12), text_color=THEME["alert"],
        )
        self.bpm_label.pack()

        self.ecg = NeuralOscillator(side, THEME["alert"], height=80)
        self.ecg.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            side, text="METABOLIC VIALS", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["text_dim"],
        ).pack(pady=(20, 10))
        self.energy_vial = ctk.CTkProgressBar(
            side, orientation="vertical", width=20, height=200, progress_color=THEME["success"],
        )
        self.energy_vial.pack(pady=5)
        self.energy_pct_label = ctk.CTkLabel(side, text="100%", font=ctk.CTkFont(size=11))
        self.energy_pct_label.pack()

        ctk.CTkLabel(
            side, text="HORMONE OSCILLATORS", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=THEME["text_dim"],
        ).pack(pady=(30, 5))
        self.dopamine_wave = NeuralOscillator(side, THEME["warning"], height=40)
        self.dopamine_wave.pack(fill="x", padx=30)
        self.serotonin_wave = NeuralOscillator(side, THEME["accent"], height=40)
        self.serotonin_wave.pack(fill="x", padx=30)
        self.cortisol_wave = NeuralOscillator(side, THEME["alert"], height=40)
        self.cortisol_wave.pack(fill="x", padx=30)

        self.search_entry = ctk.CTkEntry(
            side, placeholder_text="Search nodes...",
            fg_color="#0D0D14", border_color="#1A1A26",
        )
        self.search_entry.pack(fill="x", padx=20, pady=(20, 0))
        self.search_entry.bind("<KeyRelease>", lambda e: self.update_roles())

        self.role_list = ctk.CTkScrollableFrame(
            side, label_text="LATTICE NODES", fg_color="transparent",
        )
        self.role_list.pack(fill="both", expand=True, padx=10, pady=20)

    def _setup_cognitive_core(self):
        core = ctk.CTkFrame(self, fg_color="transparent")
        core.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        core.grid_rowconfigure(1, weight=1)
        core.grid_columnconfigure(0, weight=1)

        head = ctk.CTkFrame(core, fg_color=THEME["header"], corner_radius=15, height=120)
        head.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.node_title = ctk.CTkLabel(
            head, text="CORE INITIALIZED", font=ctk.CTkFont(size=28, weight="bold"),
            text_color=THEME["accent"],
        )
        self.node_title.place(x=30, y=25)
        self.vibe_tag = ctk.CTkLabel(
            head, text="STABLE", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=THEME["success"], text_color="black", corner_radius=5, width=120,
        )
        self.vibe_tag.place(relx=0.95, rely=0.35, anchor="ne")

        self.tabs = ctk.CTkTabview(core, segmented_button_selected_color=THEME["accent"])
        self.tabs.grid(row=1, column=0, sticky="nsew")
        self.tab_logic = self.tabs.add("Neural DNA")
        self.tab_lattice = self.tabs.add("Synaptic Flow")
        self.tab_autonomic = self.tabs.add("Autonomic Core")
        self.tab_immune = self.tabs.add("Immune System")
        self.tab_platform = self.tabs.add("Platform Layers")
        self.tab_lineage = self.tabs.add("Lineage")

        self.logic_view = ctk.CTkTextbox(
            self.tab_logic, font=ctk.CTkFont(family="Consolas", size=14),
            fg_color="#08080C", border_width=1, border_color="#1A1A26",
        )
        self.logic_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.lattice_scroll = ctk.CTkScrollableFrame(self.tab_lattice, fg_color="transparent")
        self.lattice_scroll.pack(fill="both", expand=True)

        self._setup_autonomic_tab()
        self._setup_immune_tab()
        self._setup_platform_tab()
        self._setup_lineage_tab()

        term_frame = ctk.CTkFrame(core, fg_color=THEME["header"], height=50, corner_radius=10)
        term_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        ctk.CTkLabel(
            term_frame, text="SOVEREIGN>", font=ctk.CTkFont(family="Consolas", weight="bold"),
            text_color=THEME["accent"],
        ).pack(side="left", padx=15)
        self.terminal = ctk.CTkEntry(
            term_frame, fg_color="transparent", border_width=0,
            font=ctk.CTkFont(family="Consolas"),
            placeholder_text="boot | status | directive <text> | patrol | cleanse",
        )
        self.terminal.pack(side="left", fill="x", expand=True, padx=5)
        self.terminal.bind("<Return>", self.execute_command)

    def _setup_autonomic_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_autonomic, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="ORCHESTRATOR CPU", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent"],
        ).pack(anchor="w", pady=(0, 5))
        self.orch_status_label = ctk.CTkLabel(
            frame, text="Status: IDLE", font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["text_main"], justify="left",
        )
        self.orch_status_label.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(
            frame, text="SERVICE HEARTBEATS", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent"],
        ).pack(anchor="w", pady=(0, 5))
        self.heartbeat_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.heartbeat_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            frame, text="CELLULAR HEALTH GRID", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent"],
        ).pack(anchor="w", pady=(0, 5))
        self.cellular_summary = ctk.CTkLabel(
            frame, text="Components: —", font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["text_dim"],
        )
        self.cellular_summary.pack(anchor="w", pady=(0, 5))
        self.cellular_grid = ctk.CTkFrame(frame, fg_color="transparent")
        self.cellular_grid.pack(fill="x")

    def _setup_immune_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_immune, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        header = ctk.CTkFrame(frame, fg_color=THEME["header"], corner_radius=10)
        header.pack(fill="x", pady=(0, 15))
        self.immune_temp_label = ctk.CTkLabel(
            header, text="TEMP: 98.6°F", font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color=THEME["success"],
        )
        self.immune_temp_label.pack(side="left", padx=20, pady=15)
        self.immune_threat_label = ctk.CTkLabel(
            header, text="THREAT: Negligible", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["success"],
        )
        self.immune_threat_label.pack(side="right", padx=20, pady=15)

        self.patrol_btn = ctk.CTkButton(
            frame, text="⚔ DEPLOY WBC PATROL", font=ctk.CTkFont(weight="bold"),
            fg_color=THEME["alert"], hover_color="#CC0044",
            command=self._run_patrol,
        )
        self.patrol_btn.pack(fill="x", pady=(0, 15))

        self.immune_cells_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.immune_cells_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            frame, text="PATROL LOG", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["text_dim"],
        ).pack(anchor="w")
        self.patrol_log = ctk.CTkTextbox(
            frame, height=120, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#08080C", border_width=1, border_color="#1A1A26",
        )
        self.patrol_log.pack(fill="x", pady=(5, 0))

    def _setup_platform_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_platform, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="AOS PLATFORM LAYERS", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["accent"],
        ).pack(anchor="w", pady=(0, 10))
        self.platform_summary = ctk.CTkLabel(
            frame, text="Cursor bridge: —", font=ctk.CTkFont(family="Consolas", size=10),
            text_color=THEME["text_dim"],
        )
        self.platform_summary.pack(anchor="w", pady=(0, 10))

        self.platform_layers_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.platform_layers_frame.pack(fill="x", pady=(0, 15))

        self.vision_section = ctk.CTkFrame(frame, fg_color=THEME["card"], corner_radius=10)
        self.vision_section.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(
            self.vision_section, text="VISION CACHE", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["warning"],
        ).pack(anchor="w", padx=15, pady=(10, 5))
        self.vision_scroll = ctk.CTkScrollableFrame(self.vision_section, fg_color="transparent", height=150)
        self.vision_scroll.pack(fill="x", padx=10, pady=(0, 10))

    def _setup_lineage_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_lineage, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="FISSION / FUSION LINEAGE", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["accent"],
        ).pack(anchor="w", pady=(0, 10))
        self.lineage_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.lineage_scroll.pack(fill="both", expand=True)

    def _setup_intel_stack(self):
        stack = ctk.CTkFrame(self, fg_color=THEME["sidebar"], corner_radius=0)
        stack.grid(row=0, column=2, sticky="nsew")

        ctk.CTkLabel(
            stack, text="INTELLIGENCE HUB", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent"],
        ).pack(pady=(30, 10))
        self.intel_scroll = ctk.CTkScrollableFrame(stack, fg_color="transparent", height=250)
        self.intel_scroll.pack(fill="x", padx=10)

        ctk.CTkLabel(
            stack, text="WISDOM REPOSITORY", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["warning"],
        ).pack(pady=(20, 10))
        self.wisdom_scroll = ctk.CTkScrollableFrame(stack, fg_color="transparent", height=150)
        self.wisdom_scroll.pack(fill="x", padx=10)

        ctk.CTkLabel(
            stack, text="SENSORY NERVES", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent"],
        ).pack(pady=(15, 10))
        self.sensory_scroll = ctk.CTkScrollableFrame(stack, fg_color="transparent", height=120)
        self.sensory_scroll.pack(fill="x", padx=10)
        self.sensory_status_label = ctk.CTkLabel(
            stack, text="STREAM: OFFLINE", font=ctk.CTkFont(size=9), text_color=THEME["text_dim"],
        )
        self.sensory_status_label.pack(pady=(0, 5))

        footer = ctk.CTkFrame(stack, fg_color=THEME["header"], corner_radius=10)
        footer.pack(fill="x", side="bottom", padx=10, pady=20)
        self.temp_label = ctk.CTkLabel(
            footer, text="TEMP: 98.6°F", font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=THEME["success"],
        )
        self.temp_label.pack(pady=5)

        self.threat_bar = ctk.CTkProgressBar(footer, height=6, progress_color=THEME["success"])
        self.threat_bar.pack(fill="x", padx=15, pady=2)
        self.threat_bar.set(0.1)

        ctk.CTkLabel(
            footer, text="TOXIC LOAD", font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["text_dim"],
        ).pack()
        self.toxicity_bar = ctk.CTkProgressBar(footer, height=6, progress_color=THEME["warning"])
        self.toxicity_bar.pack(fill="x", padx=15, pady=(2, 5))

        self.dampening_label = ctk.CTkLabel(
            footer, text="DAMPENING: CLEAR", font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["success"],
        )
        self.dampening_label.pack(pady=(0, 5))

        self.orchestrator_label = ctk.CTkLabel(
            footer, text="CPU: IDLE", font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["accent"],
        )
        self.orchestrator_label.pack(pady=(0, 10))

    def _setup_footer_matrix(self):
        bar = ctk.CTkFrame(self, fg_color=THEME["header"], corner_radius=0, height=36)
        bar.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.footer_dots = {}
        services = ["Pulse", "Guardian", "Senses", "Orchestrator", "Supervisor"]
        for i, name in enumerate(services):
            cell = ctk.CTkFrame(bar, fg_color="transparent")
            cell.pack(side="left", expand=True, fill="x", padx=8, pady=6)
            dot = ctk.CTkLabel(
                cell, text="●", font=ctk.CTkFont(size=14), text_color=THEME["alert"],
            )
            dot.pack(side="left", padx=(0, 6))
            lbl = ctk.CTkLabel(
                cell, text=name.upper(), font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=THEME["text_dim"],
            )
            lbl.pack(side="left")
            self.footer_dots[name.lower()] = dot

    def _service_alive(self, service_name: str) -> bool:
        hb = ServiceHeartbeat(self.base_dir, service_name)
        data = hb.read()
        if not data:
            return False
        max_age = SERVICE_STALE.get(service_name, 60)
        return (time.time() - data.get("timestamp", 0)) <= max_age

    def auto_heartbeat(self):
        try:
            self.sync_and_reload()
            self.ecg.update_val(math.sin(time.time() * 2) * 0.5 + (0.1 if time.time() % 2 < 0.2 else 0))
            self.bpm_label.configure(text=f"❤ {60 + int(time.time() % 5)} BPM")
        except Exception:
            pass
        self.after(5000, self.auto_heartbeat)

    def sync_and_reload(self):
        self.update_physiology()
        self.update_lattice()
        self.update_roles()
        self.update_intel()
        self.update_wisdom()
        self.update_toxicity()
        self.update_sensory()
        self.update_dampening()
        self.update_orchestrator()
        self.update_autonomic_core()
        self.update_immune_system()
        self.update_platform_layers()
        self.update_lineage()
        self.update_footer_matrix()

    def update_footer_matrix(self):
        try:
            for name, dot in self.footer_dots.items():
                alive = self._service_alive(name)
                dot.configure(text_color=THEME["success"] if alive else THEME["alert"])
        except Exception:
            pass

    def update_autonomic_core(self):
        try:
            status = self.orchestrator.get_status()
            cpu = status.get("status", "idle").upper()
            ticks = status.get("tick_count", 0)
            pending = status.get("pending_directives", 0)
            motor = status.get("motor_pending", 0)
            lattice = status.get("active_lattice_nodes", 0)
            last_tick = status.get("last_tick", 0)
            age = int(time.time() - last_tick) if last_tick else -1
            color = THEME["success"] if cpu == "RUNNING" else THEME["text_dim"]
            self.orch_status_label.configure(
                text=(
                    f"Status: {cpu}  |  Ticks: {ticks}  |  Pending: {pending}\n"
                    f"Motor queue: {motor}  |  Active synapses: {lattice}  |  Last tick: {age}s ago"
                ),
                text_color=color,
            )

            for w in self.heartbeat_frame.winfo_children():
                w.destroy()
            services = ServiceHeartbeat.all_services(self.base_dir)
            if not services:
                ctk.CTkLabel(
                    self.heartbeat_frame, text="No heartbeats — run 'boot' in Sovereign Terminal",
                    font=ctk.CTkFont(size=10), text_color=THEME["warning"],
                ).pack(anchor="w")
            else:
                for svc in services:
                    name = svc.get("service", "?")
                    stale_limit = SERVICE_STALE.get(name, 60)
                    age_s = int(time.time() - svc.get("timestamp", 0))
                    alive = age_s <= stale_limit
                    card = ctk.CTkFrame(
                        self.heartbeat_frame, fg_color=THEME["card"],
                        border_width=1, border_color=THEME["success"] if alive else THEME["alert"],
                    )
                    card.pack(fill="x", pady=2)
                    ctk.CTkLabel(
                        card,
                        text=f"{'●' if alive else '○'} {name.upper()} — {svc.get('status', '?')} ({age_s}s)",
                        font=ctk.CTkFont(family="Consolas", size=10),
                        text_color=THEME["success"] if alive else THEME["alert"],
                    ).pack(padx=10, pady=4, anchor="w")

            report = self.cellular.full_cell_report()
            self.cellular_summary.configure(
                text=(
                    f"Health: {report['health_pct']}% "
                    f"({report['healthy_components']}/{report['total_components']} components)"
                ),
                text_color=THEME["success"] if report["health_pct"] >= 80 else THEME["warning"],
            )
            for w in self.cellular_grid.winfo_children():
                w.destroy()
            row_frame = None
            for i, (name, cell) in enumerate(report["cells"].items()):
                if i % 3 == 0:
                    row_frame = ctk.CTkFrame(self.cellular_grid, fg_color="transparent")
                    row_frame.pack(fill="x", pady=2)
                healthy = cell.get("healthy", False)
                card = ctk.CTkFrame(
                    row_frame, fg_color=THEME["card"], border_width=1,
                    border_color=THEME["success"] if healthy else THEME["alert"],
                )
                card.pack(side="left", fill="x", expand=True, padx=3, pady=2)
                ctk.CTkLabel(
                    card, text=name.upper(), font=ctk.CTkFont(size=9, weight="bold"),
                    text_color=THEME["accent"],
                ).pack(padx=6, pady=(4, 0), anchor="w")
                ctk.CTkLabel(
                    card, text=str(cell.get("value", "?")), font=ctk.CTkFont(family="Consolas", size=10),
                    text_color=THEME["success"] if healthy else THEME["alert"],
                ).pack(padx=6, pady=(0, 4), anchor="w")
        except Exception:
            pass

    def update_immune_system(self):
        try:
            imm = self.antibody.get_immune_cells_status()
            temp = imm.get("body_temperature", 98.6)
            threat = imm.get("threat_level", "Unknown")
            self.immune_temp_label.configure(text=f"TEMP: {temp}°F")
            self.immune_temp_label.configure(
                text_color=THEME["alert"] if temp > 100 else THEME["success"],
            )
            self.immune_threat_label.configure(text=f"THREAT: {threat}")
            threat_colors = {
                "Negligible": THEME["success"], "Inflammation": THEME["warning"],
                "Fever": THEME["alert"], "Sepsis": THEME["alert"],
            }
            self.immune_threat_label.configure(text_color=threat_colors.get(threat, THEME["text_dim"]))

            for w in self.immune_cells_frame.winfo_children():
                w.destroy()
            cells = [
                ("WBC", imm.get("wbc_count", 0), THEME["accent"]),
                ("RBC", f"{imm.get('rbc_health_pct', 100):.0f}%", THEME["success"]),
                ("Platelet", imm.get("platelet_clotting", 0), THEME["warning"]),
                ("Antibody", imm.get("active_antibodies", 0), THEME["alert"]),
                ("Memory", len(imm.get("memory_cells", [])), THEME["text_dim"]),
            ]
            row = ctk.CTkFrame(self.immune_cells_frame, fg_color="transparent")
            row.pack(fill="x")
            for label, val, color in cells:
                card = ctk.CTkFrame(row, fg_color=THEME["card"], border_width=1, border_color=color)
                card.pack(side="left", fill="x", expand=True, padx=3)
                ctk.CTkLabel(
                    card, text=label, font=ctk.CTkFont(size=9, weight="bold"), text_color=color,
                ).pack(pady=(6, 0))
                ctk.CTkLabel(
                    card, text=str(val), font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
                    text_color=THEME["text_main"],
                ).pack(pady=(0, 6))
        except Exception:
            pass

    def update_platform_layers(self):
        try:
            status = self.plugin_registry.get_status()
            bridge = "ACTIVE" if status.get("cursor_bridge") else "OFFLINE"
            self.platform_summary.configure(
                text=f"Manifest: {status.get('manifest', '?')}  |  Cursor bridge: {bridge}",
            )
            for w in self.platform_layers_frame.winfo_children():
                w.destroy()
            layers = status.get("layers", {})
            layer_colors = {
                "plugins": THEME["accent"], "mcps": THEME["warning"], "skills": THEME["success"],
                "subagents": THEME["alert"], "rules": "#AA88FF", "commands": "#FFAA00", "hooks": "#88AAFF",
            }
            row = ctk.CTkFrame(self.platform_layers_frame, fg_color="transparent")
            row.pack(fill="x")
            for layer, count in layers.items():
                color = layer_colors.get(layer, THEME["text_dim"])
                card = ctk.CTkFrame(row, fg_color=THEME["card"], border_width=1, border_color=color)
                card.pack(side="left", fill="x", expand=True, padx=3, pady=2)
                ctk.CTkLabel(
                    card, text=layer.upper(), font=ctk.CTkFont(size=9, weight="bold"), text_color=color,
                ).pack(pady=(8, 0))
                ctk.CTkLabel(
                    card, text=str(count), font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
                    text_color=THEME["text_main"],
                ).pack(pady=(0, 8))

            for w in self.vision_scroll.winfo_children():
                w.destroy()
            cache_dir = self.base_dir / "core" / "monitoring" / "vision_cache"
            analyses = sorted(cache_dir.glob("*_analysis.json"), reverse=True) if cache_dir.exists() else []
            if not analyses:
                ctk.CTkLabel(
                    self.vision_scroll, text="No vision analyses cached",
                    font=ctk.CTkFont(size=10), text_color=THEME["text_dim"],
                ).pack(anchor="w", padx=5)
            else:
                for path in analyses[:8]:
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        card = ctk.CTkFrame(
                            self.vision_scroll, fg_color="#0D0D14", border_width=1, border_color="#2A2A36",
                        )
                        card.pack(fill="x", pady=2, padx=5)
                        understanding = data.get("understanding", data.get("path", path.stem))
                        ctk.CTkLabel(
                            card, text=understanding[:80], font=ctk.CTkFont(size=10),
                            wraplength=300, justify="left",
                        ).pack(padx=8, pady=4, anchor="w")
                    except Exception:
                        pass
        except Exception:
            pass

    def update_lineage(self):
        try:
            for w in self.lineage_scroll.winfo_children():
                w.destroy()
            events = self.fission_fusion.get_lineage_log()
            if not events:
                ctk.CTkLabel(
                    self.lineage_scroll, text="No fission/fusion events recorded",
                    font=ctk.CTkFont(size=11), text_color=THEME["text_dim"],
                ).pack(anchor="w", padx=5)
                return
            for evt in reversed(events[-20:]):
                evt_type = evt.get("type", "?").upper()
                color = THEME["accent"] if evt_type == "FISSION" else THEME["warning"]
                card = ctk.CTkFrame(
                    self.lineage_scroll, fg_color=THEME["card"], border_width=1, border_color=color,
                )
                card.pack(fill="x", pady=3, padx=5)
                ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(evt.get("timestamp", 0)))
                detail = evt.get("source") or evt.get("branch_a") or "?"
                target = evt.get("target") or evt.get("merged") or "?"
                ctk.CTkLabel(
                    card, text=f"{evt_type} | {ts}", font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=color,
                ).pack(padx=10, pady=(5, 0), anchor="w")
                ctk.CTkLabel(
                    card, text=f"{detail} → {target}", font=ctk.CTkFont(family="Consolas", size=10),
                    text_color=THEME["text_main"],
                ).pack(padx=10, pady=(0, 5), anchor="w")
        except Exception:
            pass

    def update_toxicity(self):
        try:
            load = self.liver.get_toxic_load()
            self.toxicity_bar.set(load["toxicity_pct"] / 100)
        except Exception:
            pass

    def update_sensory(self):
        try:
            status = self.senses.get_status()
            deprived = status.get("deprived", True)
            label = "STREAM: DEPRIVED" if deprived else "STREAM: LIVE"
            color = THEME["alert"] if deprived else THEME["success"]
            self.sensory_status_label.configure(text=label, text_color=color)

            feed = self.senses.get_feed(8)
            for w in self.sensory_scroll.winfo_children():
                w.destroy()
            for event in feed:
                salience = event.get("salience", "low")
                border = (
                    THEME["alert"] if salience == "critical"
                    else THEME["accent"] if salience == "high" else "#2A2A36"
                )
                card = ctk.CTkFrame(
                    self.sensory_scroll, fg_color=THEME["card"], border_width=1, border_color=border,
                )
                card.pack(fill="x", pady=3, padx=5)
                rel_path = event.get("path", "?")
                short = rel_path if len(rel_path) < 35 else "..." + rel_path[-32:]
                ctk.CTkLabel(
                    card, text=f"{event.get('event_type', '?')} | {short}",
                    font=ctk.CTkFont(size=10), wraplength=280, justify="left",
                ).pack(padx=8, pady=4, anchor="w")
        except Exception:
            pass

    def update_dampening(self):
        try:
            report = self.gate.get_dampening_report()
            blocked = [t for t, v in report["tools"].items() if not v["allowed"]]
            if blocked:
                self.dampening_label.configure(
                    text=f"DAMPENING: {len(blocked)} BLOCKED", text_color=THEME["alert"],
                )
            else:
                self.dampening_label.configure(text="DAMPENING: CLEAR", text_color=THEME["success"])
        except Exception:
            pass

    def update_orchestrator(self):
        try:
            status = self.orchestrator.get_status()
            cpu = status.get("status", "idle").upper()
            ticks = status.get("tick_count", 0)
            pending = status.get("pending_directives", 0)
            motor = status.get("motor_pending", 0)
            color = THEME["success"] if cpu == "RUNNING" else THEME["text_dim"]
            self.orchestrator_label.configure(
                text=f"CPU: {cpu} | T{ticks} | Q{pending} | M{motor}", text_color=color,
            )
        except Exception:
            pass

    def update_physiology(self):
        try:
            state = self.phys.get_state()
            met = state["metabolism"]
            pct = met["current_energy"] / met["max_energy"]
            self.energy_vial.set(pct)
            self.energy_pct_label.configure(text=f"{pct * 100:.1f}%")

            end = state["endocrine"]
            self.vibe_tag.configure(text=end["vibe"].upper())
            v_colors = {
                "Euphoric": THEME["warning"], "Stable": THEME["success"],
                "Stressed": "orange", "Depressed": THEME["alert"],
            }
            self.vibe_tag.configure(fg_color=v_colors.get(end["vibe"], THEME["header"]))

            h = end["hormones"]
            self.dopamine_wave.update_val((h["dopamine"] / 100) * math.sin(time.time()))
            self.serotonin_wave.update_val((h["serotonin"] / 100) * math.cos(time.time() * 0.5))
            self.cortisol_wave.update_val((h["cortisol"] / 100) * math.sin(time.time() * 1.5))

            imm = state["immune"]
            self.temp_label.configure(text=f"TEMP: {imm['temperature']}°F")
            self.temp_label.configure(
                text_color=THEME["alert"] if imm["temperature"] > 100 else THEME["success"],
            )
            self.threat_bar.set(min(1.0, (imm["temperature"] - 98) / 8))
        except Exception:
            pass

    def update_lattice(self):
        try:
            active = self.lattice.get_active_nodes()
            for w in self.lattice_scroll.winfo_children():
                w.destroy()
            for task in active:
                card = ctk.CTkFrame(
                    self.lattice_scroll, fg_color=THEME["card"], border_width=1, border_color=THEME["accent"],
                )
                card.pack(fill="x", pady=5, padx=5)
                elapsed = int(time.time() - task["started_at"])
                ctk.CTkLabel(
                    card, text=f"SYNAPSE: {task['from']} ➔ {task['to']}",
                    font=ctk.CTkFont(weight="bold"), text_color=THEME["accent"],
                ).pack(padx=10, pady=(5, 0), anchor="w")
                ctk.CTkLabel(
                    card, text=f"DIRECTIVE: {task['directive']}", font=ctk.CTkFont(size=11),
                    wraplength=400, justify="left",
                ).pack(padx=10, anchor="w")
                ctk.CTkLabel(
                    card, text=f"DURATION: {elapsed}s", font=ctk.CTkFont(family="Consolas", size=10),
                    text_color=THEME["text_dim"],
                ).pack(padx=10, pady=(0, 5), anchor="e")
        except Exception:
            pass

    def update_roles(self):
        if not hasattr(self, "search_entry"):
            return
        query = self.search_entry.get().lower()
        if self.roles_loaded and not query:
            return

        for w in self.role_list.winfo_children():
            w.destroy()
        roles = [n for n in self.logic_graph if n.get("type") == "Role"]
        if query:
            roles = [r for r in roles if query in r["title"].lower()]
        roles.sort(key=lambda x: x["title"])

        for r in roles:
            btn = ctk.CTkButton(
                self.role_list, text=r["title"], fg_color="transparent", anchor="w",
                hover_color=THEME["header"],
                command=lambda p=r["path"], t=r["title"]: self.show_role_logic(p, t),
            )
            btn.pack(fill="x", pady=1)
        self.roles_loaded = True

    def show_role_logic(self, rel_path, title):
        abs_path = self.base_dir / rel_path
        self.node_title.configure(text=title.upper())
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.logic_view.delete("1.0", "end")
            self.logic_view.insert("1.0", content)
        except Exception:
            self.logic_view.delete("1.0", "end")
            self.logic_view.insert("1.0", f"ERROR: Could not fetch DNA from {rel_path}")

    def update_intel(self):
        path = self.base_dir / "archives" / "core" / "monitoring" / "scraped_data.json"
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for w in self.intel_scroll.winfo_children():
                    w.destroy()
                for item in data[:15]:
                    card = ctk.CTkFrame(
                        self.intel_scroll, fg_color=THEME["card"], border_width=1, border_color="#2A2A36",
                    )
                    card.pack(fill="x", pady=4, padx=5)
                    tag = ctk.CTkLabel(
                        card, text=item.get("source", "SIGNAL").upper(),
                        font=ctk.CTkFont(size=9, weight="bold"), fg_color="#1A1A26", corner_radius=3,
                    )
                    tag.pack(padx=10, pady=(8, 2), anchor="w")
                    ctk.CTkLabel(
                        card, text=item.get("title", "Empty Signal"), font=ctk.CTkFont(size=12),
                        wraplength=280, justify="left",
                    ).pack(padx=10, pady=(2, 10), anchor="w")
            except Exception:
                pass

    def update_wisdom(self):
        learn_dir = self.base_dir / "archives" / "core" / "learning"
        if learn_dir.exists():
            try:
                reports = sorted(list(learn_dir.glob("*.md")), reverse=True)
                for w in self.wisdom_scroll.winfo_children():
                    w.destroy()
                for r in reports[:10]:
                    btn = ctk.CTkButton(
                        self.wisdom_scroll,
                        text=f"▶ {r.stem.replace('consolidation_', '')}",
                        font=ctk.CTkFont(size=11), text_color=THEME["warning"],
                        fg_color="transparent", anchor="w", hover_color=THEME["header"],
                        command=lambda p=f"archives/core/learning/{r.name}", t=r.stem: self.show_role_logic(p, t),
                    )
                    btn.pack(fill="x", padx=5, pady=1)
            except Exception:
                pass

    def _run_patrol(self):
        try:
            results = self.antibody.patrol()
            self.patrol_log.delete("1.0", "end")
            self.patrol_log.insert("1.0", "\n".join(results))
            self.update_immune_system()
            self.node_title.configure(text="WBC PATROL COMPLETE")
            self.after(3000, lambda: self.node_title.configure(text="CORE OPERATIONAL"))
        except Exception as e:
            self.patrol_log.delete("1.0", "end")
            self.patrol_log.insert("1.0", f"PATROL ERROR: {e}")

    def _show_terminal_output(self, title: str, output: str):
        self.node_title.configure(text=title)
        self.tabs.set("Neural DNA")
        self.logic_view.delete("1.0", "end")
        self.logic_view.insert("1.0", output)
        self.after(5000, lambda: self.node_title.configure(text="CORE OPERATIONAL"))

    def execute_command(self, event):
        cmd = self.terminal.get().strip()
        if not cmd:
            return
        logging.info(f"Sovereign Directive: {cmd}")
        self.terminal.delete(0, "end")

        lower = cmd.lower()
        try:
            if lower == "boot":
                supervisor_path = self.base_dir / "mcp_server" / "python" / "nexus_supervisor.py"
                if supervisor_path.exists():
                    from nexus_supervisor import boot_all
                    result = boot_all()
                else:
                    result = "Supervisor script not found."
                self._show_terminal_output("BOOT INITIATED", f"SOVEREIGN BOOT:\n{result}")

            elif lower == "status":
                orch = self.orchestrator.get_status()
                imm = self.antibody.get_immune_cells_status()
                cellular = self.cellular.full_cell_report()
                services = ServiceHeartbeat.all_services(self.base_dir)
                output = (
                    "=== AOS SYSTEM STATUS ===\n\n"
                    f"Orchestrator: {json.dumps(orch, indent=2)}\n\n"
                    f"Immune: {json.dumps(imm, indent=2)}\n\n"
                    f"Cellular health: {cellular['health_pct']}% "
                    f"({cellular['healthy_components']}/{cellular['total_components']})\n\n"
                    f"Services: {len(services)} heartbeat(s)\n"
                )
                self._show_terminal_output("SYSTEM STATUS", output)

            elif lower.startswith("directive"):
                text = cmd[9:].strip() if lower.startswith("directive ") else cmd
                if lower == "directive":
                    self._show_terminal_output("DIRECTIVE ERROR", "Usage: directive <your command text>")
                    return
                result = self.orchestrator.submit_directive(text, priority=8)
                self._show_terminal_output("DIRECTIVE QUEUED", f"ORCHESTRATOR:\n{result}")

            elif lower == "patrol":
                results = self.antibody.patrol()
                self.patrol_log.delete("1.0", "end")
                self.patrol_log.insert("1.0", "\n".join(results))
                self.tabs.set("Immune System")
                self._show_terminal_output("WBC PATROL", "\n".join(results))

            elif lower in ("cleanse", "filtrate", "liver"):
                result = self.liver.filter_toxins()
                self.update_toxicity()
                self._show_terminal_output("LIVER CLEANSE", f"FILTRATION RESULT:\n{result}")

            elif lower == "tick":
                result = self.orchestrator.tick()
                self._show_terminal_output("ORCHESTRATOR TICK", json.dumps(result, indent=2))

            else:
                result = self.orchestrator.submit_directive(cmd, priority=8)
                self._show_terminal_output("DIRECTIVE QUEUED", f"ORCHESTRATOR:\n{result}")

        except Exception as e:
            self._show_terminal_output("COMMAND ERROR", f"ERROR: {e}")


if __name__ == "__main__":
    app = NexusGUI()
    app.mainloop()
