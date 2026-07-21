"""
NexusAOS - Neural Terminal GUI (V5.0)
"""
import sys
import json
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext

try:
    import customtkinter as ctk
except ImportError:
    print("customtkinter not installed! Installing via pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

BASE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE / "mcp_server" / "python"))

from tools.physiology_engine import PhysiologyEngine
from tools.orchestrator_engine import OrchestratorEngine
from tools.nexus_lattice import LatticeEngine
from tools.nexus_liver import NexusLiver
from tools.antibody_engine import AntibodyEngine
from tools.service_heartbeat import ServiceHeartbeat


class NexusAOSGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NexusAOI Terminal - Powered by AOS")
        self.geometry("1400x800")
        self.configure(fg_color="#050508")

        # Set appearance mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create tabs
        self.tabview = ctk.CTkTabview(self, fg_color="#0a0a10", segmented_button_fg_color="#1a1a2e", segmented_button_selected_color="#00F0FF")
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs
        self.tabview.add("Autonomic Core")
        self.tabview.add("Immune System")
        self.tabview.add("Platform Layers")
        self.tabview.add("Terminal")

        self._setup_autonomic_core_tab()
        self._setup_immune_system_tab()
        self._setup_platform_layers_tab()
        self._setup_terminal_tab()

        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

    def _setup_autonomic_core_tab(self):
        tab = self.tabview.tab("Autonomic Core")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Create frame for core metrics
        core_frame = ctk.CTkFrame(tab, fg_color="#0a0a10")
        core_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Physiology status
        self.physiology_label = ctk.CTkLabel(core_frame, text="Physiology Status", font=("Orbitron", 16), text_color="#00F0FF")
        self.physiology_label.pack(pady=10)

        self.physiology_text = scrolledtext.ScrolledText(core_frame, height=10, bg="#0a0a10", fg="#00F0FF", insertbackground="#00F0FF", font=("Consolas", 10))
        self.physiology_text.pack(fill="both", expand=True, padx=10)

        # Toxicity Meter
        self.toxicity_label = ctk.CTkLabel(core_frame, text="Toxicity Meter", font=("Orbitron", 16), text_color="#FFAA00")
        self.toxicity_label.pack(pady=10)

        self.toxicity_progress = ctk.CTkProgressBar(core_frame, orientation="horizontal", width=600, height=20)
        self.toxicity_progress.pack(pady=5)

        self.toxicity_value_label = ctk.CTkLabel(core_frame, text="0%", font=("Orbitron", 14), text_color="#FFAA00")
        self.toxicity_value_label.pack(pady=5)

        # Cleanse button
        cleanse_button = ctk.CTkButton(core_frame, text="Trigger Cleanse", fg_color="#FFAA00", hover_color="#cc8800", command=self._trigger_cleanse)
        cleanse_button.pack(pady=10)

        # Service status
        self.service_label = ctk.CTkLabel(core_frame, text="Service Heartbeats", font=("Orbitron", 16), text_color="#39FF14")
        self.service_label.pack(pady=10)

        self.service_text = scrolledtext.ScrolledText(core_frame, height=8, bg="#0a0a10", fg="#39FF14", insertbackground="#39FF14", font=("Consolas", 10))
        self.service_text.pack(fill="both", expand=True, padx=10)

    def _setup_immune_system_tab(self):
        tab = self.tabview.tab("Immune System")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        immune_frame = ctk.CTkFrame(tab, fg_color="#0a0a10")
        immune_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Immune status
        self.immune_label = ctk.CTkLabel(immune_frame, text="Immune Status", font=("Orbitron", 16), text_color="#FF0055")
        self.immune_label.pack(pady=10)

        self.immune_text = scrolledtext.ScrolledText(immune_frame, height=20, bg="#0a0a10", fg="#FF0055", insertbackground="#FF0055", font=("Consolas", 10))
        self.immune_text.pack(fill="both", expand=True, padx=10)

        # Patrol button
        patrol_button = ctk.CTkButton(immune_frame, text="Run Immune Patrol", fg_color="#FF0055", hover_color="#cc0044", command=self._run_immune_patrol)
        patrol_button.pack(pady=10)

    def _setup_platform_layers_tab(self):
        tab = self.tabview.tab("Platform Layers")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        layers_frame = ctk.CTkFrame(tab, fg_color="#0a0a10")
        layers_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.layers_label = ctk.CTkLabel(layers_frame, text="Platform Layers", font=("Orbitron", 16), text_color="#00F0FF")
        self.layers_label.pack(pady=10)

        self.layers_text = scrolledtext.ScrolledText(layers_frame, height=25, bg="#0a0a10", fg="#00F0FF", insertbackground="#00F0FF", font=("Consolas", 10))
        self.layers_text.pack(fill="both", expand=True, padx=10)

    def _setup_terminal_tab(self):
        tab = self.tabview.tab("Terminal")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        terminal_frame = ctk.CTkFrame(tab, fg_color="#0a0a10")
        terminal_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.terminal_output = scrolledtext.ScrolledText(terminal_frame, height=20, bg="#0a0a10", fg="#00F0FF", insertbackground="#00F0FF", font=("Consolas", 10))
        self.terminal_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.terminal_input = ctk.CTkEntry(terminal_frame, placeholder_text="Enter command...")
        self.terminal_input.pack(fill="x", padx=10)
        self.terminal_input.bind("<Return>", self._handle_terminal_command)

    def _update_loop(self):
        while self.running:
            try:
                # Update physiology
                phys_engine = PhysiologyEngine(BASE)
                phys_state = phys_engine.get_state()
                phys_display = json.dumps(phys_state, indent=2)
                self.after(0, lambda: self._update_text_widget(self.physiology_text, phys_display))

                # Update toxicity meter
                liver = NexusLiver(BASE)
                toxic_load = liver.get_toxic_load()
                toxicity_pct = toxic_load.get("toxicity_pct", 0)
                self.after(0, lambda: self.toxicity_progress.set(toxicity_pct / 100.0))
                self.after(0, lambda: self.toxicity_value_label.configure(text=f"{toxicity_pct:.1f}%"))

                # Update services
                services = ServiceHeartbeat.all_services(BASE)
                services_display = json.dumps(services, indent=2)
                self.after(0, lambda: self._update_text_widget(self.service_text, services_display))

                # Update immune
                ab_engine = AntibodyEngine(BASE)
                immune_status = ab_engine.get_immune_cells_status()
                immune_display = json.dumps(immune_status, indent=2)
                self.after(0, lambda: self._update_text_widget(self.immune_text, immune_display))

                # Update layers
                layers_info = {
                    "Plugins": "Active",
                    "MCP": "Active",
                    "Skills": "Active",
                    "Subagents": "Active",
                    "Rules": "Active",
                    "Commands": "Active",
                    "Hooks": "Active"
                }
                layers_display = json.dumps(layers_info, indent=2)
                self.after(0, lambda: self._update_text_widget(self.layers_text, layers_display))

            except Exception as e:
                print(f"Update loop error: {e}")

            time.sleep(1)

    def _trigger_cleanse(self):
        try:
            liver = NexusLiver(BASE)
            report = liver.filter_toxins()
            self._update_text_widget(self.terminal_output, report)
        except Exception as e:
            self._update_text_widget(self.terminal_output, f"Cleanse error: {e}")

    def _update_text_widget(self, widget, text):
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)

    def _run_immune_patrol(self):
        try:
            ab_engine = AntibodyEngine(BASE)
            results = ab_engine.patrol()
            self._update_text_widget(self.terminal_output, "\n".join(results))
        except Exception as e:
            self._update_text_widget(self.terminal_output, f"Patrol error: {e}")

    def _handle_terminal_command(self, event):
        command = self.terminal_input.get().strip()
        self.terminal_input.delete(0, tk.END)

        if command:
            try:
                if command.lower() in ["quit", "exit"]:
                    self.running = False
                    self.destroy()
                elif command.lower() == "patrol":
                    self._run_immune_patrol()
                elif command.lower().startswith("submit "):
                    directive = command[7:]
                    orch = OrchestratorEngine(BASE)
                    result = orch.submit_directive(directive, priority=5)
                    self._update_text_widget(self.terminal_output, result)
                else:
                    self._update_text_widget(self.terminal_output, f"Unknown command: {command}")
            except Exception as e:
                self._update_text_widget(self.terminal_output, f"Command error: {e}")

    def on_closing(self):
        self.running = False
        self.destroy()


if __name__ == "__main__":
    app = NexusAOSGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
