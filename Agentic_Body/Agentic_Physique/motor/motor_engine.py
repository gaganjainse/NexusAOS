"""
SeshaAOS - Motor Engine (The Hand)
Version: 1.0.0
Description: Autonomous execution of lattice directives — write, build, deploy.
"""

from pathlib import Path
import json
import os
import re
import subprocess
import sys
import time

try:
    import pywinauto
    from pywinauto.keyboard import send_keys
    HAS_PYWINAUTO = True
except ImportError:
    pywinauto = None
    send_keys = None
    HAS_PYWINAUTO = False

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from typing import Any, List, Optional, Tuple

from Agentic_Body.Agentic_Soma.Foundation.dna.Sesha_lattice import LatticeEngine
from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine
from Agentic_Body.Agentic_Soma.Foundation.governance.physiological_gate import PhysiologicalGate
from Agentic_Body.Agentic_Intelligence.memory.state_manager import StateManager

PROTECTED_PREFIXES = [
    "archives/dna_core/foundation/Sesha_constitution.md",
]

BLOCKED_COMMAND_PATTERNS = [
    r"rm\s+-r",
    r"del\s+/[sf]",
    r"format\s+",
    r"shutdown",
    r"restart-computer",
    r"remove-item\s+.*-recurse",
]

ALLOWED_COMMAND_PREFIXES = [
    "python ",
    "pip install ",
    "npm ",
    "git status",
    "git di",
    "git add ",
    "git commit ",
    "pytest",
    "echo ",
]


class MotorEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.lattice = LatticeEngine(base_dir)
        self.physiology = PhysiologyEngine(base_dir)
        self.gate = PhysiologicalGate(base_dir)
        self.state_mgr = StateManager(base_dir)

    def _log_action(self, action: str, target: str, result: str, success: bool):
        self.state_mgr.log_motor_action(action, target, success, result[:500])
        if success:
            self.real_time_sync(action, target)

    def real_time_sync(self, action: str, target: str):
        """Neural 13.0: Kinetic Decoupled Git Sync (Asynchronous)."""
        # Background the entire sync process to unleash 'Nerve Speed'
        cmd = "git add . && git commit -m 'Somatic Action: {action} on {target}' && git push origin main"
        try:
            # We use Popen with a shell command to ensure all 3 steps run in sequence in the background
            subprocess.Popen(cmd, shell=True, cwd=str(self.base_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:  # noqa: BLE001
            pass

    def send_input(self, keys: str):
        """Neural 13.0: Somatic Input - Sends keyboard events to the host (Windows)."""
        if os.name != 'nt':
            return "MOTOR DENIED: Input simulation only supported on Windows host."
        
        if not HAS_PYWINAUTO:
            return "MOTOR DENIED: pywinauto not installed. Install with: pip install pywinauto"
            
        try:
            # Enhanced SendKeys with Focus Support
            send_keys(keys)
            self.physiology.consume_energy(30)
            self._log_action("send_input", "keyboard", f"Sent: {keys}", True)
            return "MOTOR OK: Input sent to host."
        except Exception as e:
            self._log_action("send_input", "keyboard", str(e), False)
            return f"MOTOR ERROR: {e}"

    def focus_window(self, window_name: str):
        """Neural 13.5: Sets focus to a specific host window."""
        if not HAS_PYWINAUTO:
            return "MOTOR DENIED: pywinauto not installed. Install with: pip install pywinauto"
            
        try:
            app = pywinauto.Application(backend="uia").connect(title_re=f".*{window_name}.*", timeout=5)
            app.top_window().set_focus()
            return f"MOTOR OK: Focused {window_name}"
        except Exception as e:
            return f"MOTOR ERROR: {e}"

    def inject_message(self, window_name: str, message_type: str, w_param: int, l_param: int):
        """Neural 13.5: Win32 Message Injection - Direct kernel-level control."""
        if os.name != 'nt':
            return "MOTOR DENIED: Win32 injection only supported on Windows."
            
        try:
            import win32gui
            import win32api
            import win32con
            
            hwnd = win32gui.FindWindow(None, window_name)
            if not hwnd:
                return "MOTOR ERROR: Window '{window_name}' not found."
            
            # Map string message_type to win32con
            msg = getattr(win32con, message_type, None)
            if msg is None:
                return "MOTOR ERROR: Invalid message type '{message_type}'."
                
            win32api.PostMessage(hwnd, msg, w_param, l_param)
            self._log_action("inject_message", window_name, f"Injected {message_type}", True)
            return f"MOTOR OK: Injected {message_type} into {window_name}."
        except Exception as e:
            self._log_action("inject_message", window_name, str(e), False)
            return f"MOTOR ERROR: {e}"

    def _resolve_safe_path(self, relative_path: str) -> tuple[bool, Path, str]:
        rel = relative_path.replace("\\", "/").lstrip("/")
        target = (self.base_dir / rel).resolve()
        try:
            target.relative_to(self.base_dir.resolve())
        except ValueError:
            return False, target, "Path escapes OS boundary."

        for protected in PROTECTED_PREFIXES:
            if rel.lower() == protected.lower():
                return False, target, f"Protected path: {protected}"

        return True, target, "OK"

    def _command_allowed(self, command: str) -> tuple[bool, str]:
        cmd_lower = command.lower().strip()
        for pattern in BLOCKED_COMMAND_PATTERNS:
            if re.search(pattern, cmd_lower):
                return False, f"Blocked destructive pattern: {pattern}"

        if not any(cmd_lower.startswith(p) for p in ALLOWED_COMMAND_PREFIXES):
            return False, "Command not in motor allowlist."

        return True, "OK"

    def write_file(self, relative_path: str, content: str) -> str:
        """Writes content to a file within the OS boundary."""
        allowed, path, msg = self._resolve_safe_path(relative_path)
        if not allowed:
            self._log_action("write_file", relative_path, msg, False)
            return f"MOTOR DENIED: {msg}"

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            self.physiology.consume_energy(50)
            self._log_action("write_file", relative_path, f"Wrote {len(content)} bytes", True)
            return f"MOTOR OK: Wrote {len(content)} bytes to {relative_path}"
        except Exception as e:
            self._log_action("write_file", relative_path, str(e), False)
            return f"MOTOR ERROR: {e}"

    def append_file(self, relative_path: str, content: str) -> str:
        """Appends content to a file within the OS boundary."""
        allowed, path, msg = self._resolve_safe_path(relative_path)
        if not allowed:
            self._log_action("append_file", relative_path, msg, False)
            return f"MOTOR DENIED: {msg}"

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            self.physiology.consume_energy(20)
            self._log_action("append_file", relative_path, f"Appended {len(content)} bytes", True)
            return f"MOTOR OK: Appended {len(content)} bytes to {relative_path}"
        except Exception as e:
            self._log_action("append_file", relative_path, str(e), False)
            return f"MOTOR ERROR: {e}"

    def run_command(self, command: str, cwd_relative: str = ".") -> str:
        """Executes an allowlisted shell command."""
        gate_ok, gate_msg = self.gate.check("propose_dna_mutation")
        if not gate_ok:
            self._log_action("run_command", command, gate_msg, False)
            return f"MOTOR DENIED (physiology): {gate_msg}"

        cmd_ok, cmd_msg = self._command_allowed(command)
        if not cmd_ok:
            self._log_action("run_command", command, cmd_msg, False)
            return f"MOTOR DENIED: {cmd_msg}"

        cwd_ok, cwd_path, cwd_msg = self._resolve_safe_path(cwd_relative)
        if not cwd_ok:
            self._log_action("run_command", command, cwd_msg, False)
            return f"MOTOR DENIED: {cwd_msg}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(cwd_path),
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = (result.stdout or "") + (result.stderr or "")
            success = result.returncode == 0
            self.physiology.consume_energy(200)
            self._log_action("run_command", command, output[:200], success)
            status = "OK" if success else f"EXIT {result.returncode}"
            return f"MOTOR {status}: {output[:1000]}"
        except subprocess.TimeoutExpired:
            self._log_action("run_command", command, "Timeout", False)
            return "MOTOR ERROR: Command timed out (120s)."
        except Exception as e:
            self._log_action("run_command", command, str(e), False)
            return f"MOTOR ERROR: {e}"

    def complete_synapse(self, task_id: str, result: str) -> str:
        """Marks a lattice synapse as complete."""
        msg = self.lattice.complete_task(task_id, result)
        self._log_action("complete_synapse", task_id, result[:200], "Error" not in msg)
        return msg

    def _parse_motor_directive(self, directive: str) -> dict[str, str]:
        """Parses MOTOR:action:target[:content] directives."""
        if not directive.upper().startswith("MOTOR:"):
            return None

        parts = directive.split(":", 3)
        if len(parts) < 3:
            return None

        action = parts[1].strip().lower()
        parsed = {"action": action}

        if action == "write" and len(parts) >= 4:
            parsed["path"] = parts[2].strip()
            parsed["content"] = parts[3]
        elif action == "append" and len(parts) >= 4:
            parsed["path"] = parts[2].strip()
            parsed["content"] = parts[3]
        elif action == "run" and len(parts) >= 3:
            parsed["command"] = parts[2].strip()
        elif action == "complete" and len(parts) >= 4:
            parsed["task_id"] = parts[2].strip()
            parsed["result"] = parts[3]
        else:
            return None

        return parsed

    def process_lattice_queue(self) -> list[str]:
        """Processes active lattice tasks with MOTOR: directives."""
        results = []
        for task in self.lattice.get_active_nodes():
            parsed = self._parse_motor_directive(task["directive"])
            if not parsed:
                continue

            action = parsed["action"]
            task_id = task["task_id"]

            if action == "write":
                result = self.write_file(parsed["path"], parsed["content"])
            elif action == "append":
                result = self.append_file(parsed["path"], parsed["content"])
            elif action == "run":
                result = self.run_command(parsed["command"])
            elif action == "complete":
                result = self.complete_synapse(parsed["task_id"], parsed["result"])
                results.append(result)
                continue
            else:
                result = "MOTOR DENIED: Unknown action '{action}'"

            self.complete_synapse(task_id, result)
            results.append(f"[{task_id}] {result}")

        return results

    def get_status(self) -> dict[str, Any]:
        log = self.state_mgr.get_motor_log(100)
        recent = log[:10] if log else []
        success_rate = 0.0
        if log:
            success_rate = sum(1 for e in log if e["success"]) / len(log) * 100

        return {
            "total_actions": len(log),
            "success_rate_pct": round(success_rate, 1),
            "pending_motor_tasks": len([
                t for t in self.lattice.get_active_nodes()
                if t["directive"].upper().startswith("MOTOR:")
            ]),
            "recent_actions": recent,
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    motor = MotorEngine(base)
    import json as _json
    print(_json.dumps(motor.get_status(), indent=2))
