"""
NexusAOS - Peer-Operator GUI (L00)
Version: 13.0.0
Description: Multimodal interface for human-agent co-habitation.
Framework: customtkinter
"""

import tkinter
import customtkinter
import json
import time
import threading
import sys
from pathlib import Path

# Ensure root is in path
_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
from layers.L02_Agent.physiology_engine import PhysiologyEngine

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class PeerOperatorGUI(customtkinter.CTk):
    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir
        self.orch = OrchestratorEngine(base_dir)
        self.phys = PhysiologyEngine(base_dir)
        
        self.title("Nexus AOS - Peer-Operator Terminal (L00)")
        self.geometry("1200x800")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Vitals)
        self.sidebar = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.vitals_label = customtkinter.CTkLabel(self.sidebar, text="SYSTEM VITALS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.vitals_label.pack(pady=20)
        
        self.energy_bar = customtkinter.CTkProgressBar(self.sidebar)
        self.energy_bar.pack(pady=10, padx=20)
        self.energy_text = customtkinter.CTkLabel(self.sidebar, text="Energy: --%")
        self.energy_text.pack()
        
        self.vibe_label = customtkinter.CTkLabel(self.sidebar, text="Vibe: Stable", text_color="green")
        self.vibe_label.pack(pady=20)

        # Main Terminal
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.console = customtkinter.CTkTextbox(self.main_frame, font=customtkinter.CTkFont(family="Consolas", size=12))
        self.console.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.input_field = customtkinter.CTkEntry(self.main_frame, placeholder_text="Enter Sovereign Directive...")
        self.input_field.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_field.bind("<Return>", self.submit_directive)

        # Start background polling
        self.update_vitals()

    def submit_directive(self, event=None):
        text = self.input_field.get()
        if text:
            self.input_field.delete(0, tkinter.END)
            self.log(f">>> {text}")
            res = self.orch.submit_directive(text)
            self.log(f"SYS: {res}")

    def log(self, message: str):
        self.console.insert(tkinter.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.console.see(tkinter.END)

    def update_vitals(self):
        state = self.phys.get_state()
        met = state.get("metabolism", {})
        energy = met.get("current_energy", 0)
        max_e = met.get("max_energy", 1000)
        
        pct = energy / max_e
        self.energy_bar.set(pct)
        self.energy_text.configure(text=f"Energy: {energy}/{max_e} ({pct*100:.1f}%)")
        
        vibe = state.get("endocrine", {}).get("vibe", "Stable")
        self.vibe_label.configure(text=f"Vibe: {vibe}")
        
        self.after(2000, self.update_vitals)

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    app = PeerOperatorGUI(base)
    app.mainloop()
