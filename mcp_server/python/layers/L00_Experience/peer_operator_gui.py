"""
NexusAOS - Peer-Operator Experience (L00)
Version: 13.0.0
Description: Multimodal UI for real-time AOS monitoring and strategic control.
"""

import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from PIL import Image

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L02_Agent.physiology_engine import PhysiologyEngine
from layers.L05_Memory.state_manager import StateManager
from layers.L11_Data.signal_router import SignalRouter

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PeerOperatorGUI(ctk.CTk):
    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir
        self.physiology = PhysiologyEngine(base_dir)
        self.state_mgr = StateManager(base_dir)
        self.signals = SignalRouter(base_dir)

        self.title("NexusAOS - Peer-Operator Dashboard")
        self.geometry("1100x700")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Vitals)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self._init_sidebar()

        # Main Content
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self._init_main_content()

        # Update Thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

    def _init_sidebar(self):
        self.vitals_label = ctk.CTkLabel(self.sidebar, text="SYSTEM VITALS", font=ctk.CTkFont(size=20, weight="bold"))
        self.vitals_label.pack(pady=20)

        # Energy Meter
        self.energy_label = ctk.CTkLabel(self.sidebar, text="Metabolism (ATP): 0%")
        self.energy_label.pack(pady=5)
        self.energy_bar = ctk.CTkProgressBar(self.sidebar)
        self.energy_bar.pack(pady=10, padx=20)

        # Hormones
        self.vibe_label = ctk.CTkLabel(self.sidebar, text="Vibe: Stable", font=ctk.CTkFont(size=16))
        self.vibe_label.pack(pady=20)

        self.hormone_frame = ctk.CTkFrame(self.sidebar)
        self.hormone_frame.pack(pady=10, fill="x", padx=10)
        self.cortisol_label = ctk.CTkLabel(self.hormone_frame, text="Cortisol: 0.0")
        self.cortisol_label.pack()
        self.dopamine_label = ctk.CTkLabel(self.hormone_frame, text="Dopamine: 0.0")
        self.dopamine_label.pack()

        # Immune status
        self.immune_status = ctk.CTkLabel(self.sidebar, text="Immune: Negligible", text_color="green")
        self.immune_status.pack(pady=20)

    def _init_main_content(self):
        # Tabs
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_terminal = self.tabview.add("Neural Terminal")
        self.tab_signals = self.tabview.add("Synaptic Feed")
        self.tab_tasks = self.tabview.add("Lattice Tasks")

        # Terminal Tab
        self.terminal_output = ctk.CTkTextbox(self.tab_terminal, height=400)
        self.terminal_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.input_frame = ctk.CTkFrame(self.tab_terminal)
        self.input_frame.pack(fill="x", side="bottom", pady=5)
        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Strategic Directive...")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.input_entry.bind("<Return>", self._submit_directive)
        self.submit_btn = ctk.CTkButton(self.input_frame, text="FIRE", width=100, command=self._submit_directive)
        self.submit_btn.pack(side="right", padx=5)

        # Signals Tab
        self.signal_list = ctk.CTkTextbox(self.tab_signals)
        self.signal_list.pack(fill="both", expand=True)

        # Tasks Tab
        self.task_list = ctk.CTkTextbox(self.tab_tasks)
        self.task_list.pack(fill="both", expand=True)

    def _submit_directive(self, event=None):
        text = self.input_entry.get()
        if text:
            self.input_entry.delete(0, "end")
            self._log_terminal(f">>> Sovereign: {text}")
            from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
            orch = OrchestratorEngine(self.base_dir)
            res = orch.submit_directive(text)
            self._log_terminal(f"AOS: Directive Queued [{res}]")

    def _log_terminal(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.insert("end", f"[{timestamp}] {msg}\n")
        self.terminal_output.see("end")

    def _update_loop(self):
        while self.running:
            try:
                # Update Physiology
                state = self.physiology.get_state()
                met = state["metabolism"]
                energy_pct = met["current_energy"] / met["max_energy"]
                self.energy_bar.set(energy_pct)
                self.energy_label.configure(text=f"Metabolism (ATP): {int(energy_pct*100)}%")
                
                self.vibe_label.configure(text=f"Vibe: {state['endocrine']['vibe']}")
                h = state["endocrine"]["hormones"]
                self.cortisol_label.configure(text=f"Cortisol: {h.get('cortisol', 0.0):.1f}")
                self.dopamine_label.configure(text=f"Dopamine: {h.get('dopamine', 0.0):.1f}")
                
                imm_status = state["immune"]["threat_level"]
                self.immune_status.configure(text=f"Immune: {imm_status}", 
                                           text_color="red" if imm_status != "Negligible" else "green")

                # Update Signals
                active_signals = self.signals.get_active_signals()
                self.signal_list.delete("1.0", "end")
                for sig, data in active_signals.items():
                    self.signal_list.insert("end", f"[{sig}] {data.get('evidentiality', '')} {json.dumps(data.get('payload', {}))}\n")

                # Update Tasks
                tasks = self.state_mgr.get_active_tasks()
                self.task_list.delete("1.0", "end")
                for t in tasks:
                    self.task_list.insert("end", f"[{t['task_id']}] {t['from_role']} -> {t['to_role']}: {t['status']}\n")
                
            except Exception as e:
                print(f"GUI Update Error: {e}")
            
            time.sleep(1)

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    app = PeerOperatorGUI(base)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
