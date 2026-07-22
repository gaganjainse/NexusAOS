"""
NexusAOS - NEURAL Compiler (The Transplanter)
Version: 2.0.0
Description: Compiles Sigil 2.0 pulses into performance-ready Genomes for the SHM Synaptic Bus.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List

class NeuralCompiler:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.output_dir = base_dir / "mcp_server" / "kernels"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.compiled_file = self.output_dir / "compiled_genomes.json"

    def compile_pulse(self, pulse_text: str) -> Dict[str, Any]:
        """
        Parses Sigil 2.0 pulse and returns a compiled genome.
        """
        lines = pulse_text.split("\n")
        parsed = {"receptors": [], "emitters": [], "id": "unknown"}
        
        # Identity
        if "[[ID]]" in pulse_text:
             parsed["id"] = pulse_text.split("[[ID]]")[1].split("\n")[0].strip()

        # Sigil Parsing (::P, ::X, ::Z, ::!, ::◊, ::~)
        parts = pulse_text.split("::")
        for p in parts:
            if not p: continue
            sigil = p[0]
            content = p[1:].strip()
            
            if sigil == "P": parsed["purpose"] = content
            elif sigil == "X": parsed["execution"] = content
            elif sigil == "Z": parsed["vibe_label"] = content
            elif sigil == "!": parsed["evidentiality"] = "Known"
            elif sigil == "◊": parsed["evidentiality"] = "Predicted"
            elif sigil == "~": parsed["evidentiality"] = "Reported"
            elif sigil == "R": parsed["receptors"].append(content)
            elif sigil == "D": parsed["deliverables"] = content
            
        # Default evidentiality if missing
        if "evidentiality" not in parsed:
            parsed["evidentiality"] = "Predicted"

        # Generate Latent Vibe Vector (Simulated)
        vibe_hash = hashlib.sha256(parsed.get("vibe_label", "STABLE").encode()).hexdigest()
        parsed["vibe_vector"] = [int(vibe_hash[i:i+2], 16) / 255.0 for i in range(0, 16, 2)] # 8D vector

        return parsed

    def compile_all(self):
        """Scans active_core/pulses and compiles all .nxp files."""
        pulses_dir = self.base_dir / "active_core" / "pulses"
        all_genomes = {}
        
        for nxp in pulses_dir.glob("*.nxp"):
            content = nxp.read_text(encoding="utf-8")
            # Pulses are separated by ---Pulse-Break---
            sections = content.split("---Pulse-Break---")
            for section in sections:
                if "[[ID]]" in section:
                    genome = self.compile_pulse(section)
                    all_genomes[genome["id"]] = genome
        
        self.compiled_file.write_text(json.dumps(all_genomes, indent=4), encoding="utf-8")
        return len(all_genomes)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    compiler = NeuralCompiler(base)
    print(compiler.compile_pulse("::P Optimize Latency ::X Use io_uring", "zig"))
