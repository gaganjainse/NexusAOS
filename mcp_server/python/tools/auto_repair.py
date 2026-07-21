"""
NexusAOS - Autonomous Repair Engine (ARE)
Version: 3.0.0
Description: Proactive prevention + barriers + validation + rate limiting + self-healing.
"""
from pathlib import Path
from typing import Dict, List, Optional, Callable
import time
import re
import hashlib


class CallGuard:
    """Rate limiter and barrier for dangerous operations."""
    
    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.call_history: Dict[str, List[float]] = {}
    
    def check(self, caller_id: str) -> Dict:
        """Check if call is allowed under rate limit."""
        now = time.time()
        if caller_id not in self.call_history:
            self.call_history[caller_id] = []
        
        # Remove old entries
        self.call_history[caller_id] = [
            ts for ts in self.call_history[caller_id] 
            if now - ts < self.window_seconds
        ]
        
        current_count = len(self.call_history[caller_id])
        
        if current_count >= self.max_calls:
            return {
                "allowed": False,
                "reason": "rate_limit",
                "current": current_count,
                "max": self.max_calls,
                "window_seconds": self.window_seconds,
                "retry_after": self.window_seconds - (now - self.call_history[caller_id][0])
            }
        
        return {"allowed": True}
    
    def record(self, caller_id: str):
        """Record a successful call."""
        now = time.time()
        if caller_id not in self.call_history:
            self.call_history[caller_id] = []
        self.call_history[caller_id].append(now)
    
    def get_status(self) -> Dict:
        return {
            "tracked_callers": len(self.call_history),
            "total_calls_in_window": sum(len(v) for v in self.call_history.values())
        }


class InputValidator:
    """Validates inputs before execution to prevent errors."""
    
    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"sudo\s+",
        r"chmod\s+777",
        r">\s*/dev/",
        r"eval\s*\(",
        r"__import__\s*\(",
    ]
    
    def validate_command(self, command: str) -> Dict:
        """Validate a shell command for dangerous patterns."""
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "safe": False,
                    "reason": f"Dangerous pattern detected: {pattern}",
                    "command": command
                }
        return {"safe": True, "command": command}
    
    def validate_path(self, path: str, allowed_dirs: List[str] = None) -> Dict:
        """Validate a file path is within allowed directories."""
        path_obj = Path(path).resolve()
        
        if allowed_dirs:
            allowed = any(
                str(path_obj).startswith(str(Path(d).resolve()))
                for d in allowed_dirs
            )
            if not allowed:
                return {
                    "safe": False,
                    "reason": "Path outside allowed directories",
                    "path": str(path_obj),
                    "allowed_dirs": allowed_dirs
                }
        
        return {"safe": True, "resolved_path": str(path_obj)}
    
    def validate_json(self, json_str: str) -> Dict:
        """Validate JSON string."""
        import json
        try:
            parsed = json.loads(json_str)
            return {"valid": True, "parsed": parsed}
        except json.JSONDecodeError as e:
            return {"valid": False, "error": str(e)}


class AutoRepairEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.target_files = {
            "nexus_gui.py": self._repair_gui,
            "nlg_compiler.py": self._repair_config_paths,
            "nxp_forge.py": self._repair_config_paths,
            "index.py": self._repair_index
        }
        self.call_guard = CallGuard(max_calls=20, window_seconds=60)
        self.validator = InputValidator()
        self.repair_log: List[Dict] = []
        self._load_repair_log()
    
    def _load_repair_log(self):
        log_path = self.base_dir / "core" / "monitoring" / "repair_log.json"
        if log_path.exists():
            import json
            with open(log_path, "r") as f:
                self.repair_log = json.load(f)
    
    def _save_repair_log(self):
        log_path = self.base_dir / "core" / "monitoring" / "repair_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(log_path, "w") as f:
            json.dump(self.repair_log[-100:], f, indent=2)  # Keep last 100
    
    def _log_repair(self, action: str, file_path: str, success: bool, details: str = ""):
        self.repair_log.append({
            "timestamp": time.time(),
            "action": action,
            "file": file_path,
            "success": success,
            "details": details
        })
        self._save_repair_log()
    
    # --- Barriers ---
    
    def check_call_barrier(self, caller_id: str) -> Dict:
        """Check rate limit barrier before allowing repair."""
        result = self.call_guard.check(caller_id)
        if result.get("allowed"):
            self.call_guard.record(caller_id)
        return result
    
    # --- Validation ---
    
    def validate_repair_target(self, path: Path) -> Dict:
        """Validate a file is safe to repair."""
        if not path.exists():
            return {"safe": False, "reason": "File does not exist"}
        
        if not path.is_file():
            return {"safe": False, "reason": "Path is not a file"}
        
        # Check file is within base_dir
        try:
            path.relative_to(self.base_dir)
        except ValueError:
            return {"safe": False, "reason": "File outside base directory"}
        
        return {"safe": True, "path": str(path)}
    
    # --- Repair Logic ---
    
    def scan_and_fix(self, caller_id: str = "system") -> Dict:
        """Scan and fix with barriers and validation."""
        # Check rate limit
        barrier = self.check_call_barrier(caller_id)
        if not barrier.get("allowed"):
            return {"status": "blocked", "reason": barrier, "report": []}
        
        report = []
        
        for filename, repair_func in self.target_files.items():
            possible_paths = [
                self.base_dir / "mcp_server" / "python" / filename,
                self.base_dir / "mcp_server" / "python" / "tools" / filename
            ]
            
            file_path = next((p for p in possible_paths if p.exists()), None)
            
            if not file_path:
                report.append({"file": filename, "status": "missing", "action": "none"})
                continue
            
            validation = self.validate_repair_target(file_path)
            if not validation.get("safe"):
                report.append({"file": filename, "status": "blocked", "reason": validation["reason"]})
                continue
            
            try:
                fix_applied = repair_func(file_path)
                self._log_repair("scan_fix", filename, fix_applied)
                report.append({
                    "file": filename,
                    "status": "fixed" if fix_applied else "healthy",
                    "action": "repair"
                })
            except Exception as e:
                self._log_repair("scan_fix", filename, False, str(e))
                report.append({"file": filename, "status": "error", "error": str(e)})
        
        # Check pulse density
        pulse_dir = self.base_dir / "core" / "pulses"
        if pulse_dir.exists():
            nxp_files = list(pulse_dir.glob("*.nxp"))
            if len(nxp_files) < 5:
                report.append({
                    "file": "pulses",
                    "status": "warning",
                    "message": "Low pulse density detected"
                })
        
        return {
            "status": "complete",
            "report": report,
            "call_barrier": barrier
        }
    
    def repair_file(self, file_path: str, caller_id: str = "manual") -> Dict:
        """Repair a specific file with validation."""
        path = Path(file_path)
        
        # Validate
        validation = self.validate_repair_target(path)
        if not validation.get("safe"):
            return {"success": False, "error": validation["reason"]}
        
        # Check barrier
        barrier = self.check_call_barrier(caller_id)
        if not barrier.get("allowed"):
            return {"success": False, "error": f"Rate limited: {barrier}", "blocked": True}
        
        # Find repair function
        filename = path.name
        repair_func = self.target_files.get(filename)
        
        if repair_func:
            try:
                result = repair_func(path)
                self._log_repair("manual_repair", filename, result)
                return {"success": True, "fixed": result, "file": filename}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "No repair strategy for this file"}
    
    def validate_json_file(self, file_path: str) -> Dict:
        """Validate a JSON file for corruption."""
        path = Path(file_path)
        if not path.exists():
            return {"valid": False, "error": "File not found"}
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return {"valid": False, "error": "Empty file"}
                json.loads(content)
            return {"valid": True, "file": str(path)}
        except Exception as e:
            return {"valid": False, "error": str(e), "file": str(path)}
    
    def repair_json_file(self, file_path: str) -> Dict:
        """Attempt to repair a corrupted JSON file."""
        validation = self.validate_json_file(file_path)
        if validation.get("valid"):
            return {"success": True, "message": "File already valid"}
        
        path = Path(file_path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Try common fixes
            fixed = content
            
            # Fix trailing commas
            fixed = re.sub(r",\s*([}\]])", r"\1", fixed)
            
            # Fix missing quotes around keys
            fixed = re.sub(r"(\w+)\s*:", r'"\1":', fixed)
            
            # Try parse
            import json
            json.loads(fixed)
            
            # Write back
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            
            self._log_repair("json_repair", file_path, True)
            return {"success": True, "message": "JSON repaired", "file": file_path}
        except Exception as e:
            self._log_repair("json_repair", file_path, False, str(e))
            return {"success": False, "error": str(e)}
    
    # --- Original repair functions ---
    
    def _repair_config_paths(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        changed = False
        if 'BASE_DIR = Path(r"C:/Users/' in content:
            content = re.sub(
                r'BASE_DIR = Path\(r"C:/Users/.*?"\)',
                'BASE_DIR = Path(__file__).resolve().parent.parent.parent',
                content
            )
            changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return changed
    
    def _repair_gui(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        changed = False
        if "Path(__file__).resolve()" not in content:
            content = content.replace("Path(__file__)", "Path(__file__).resolve()")
            changed = True
        if 'geometry("1100x700")' in content:
            content = content.replace('geometry("1100x700")', 'geometry("1200x800")')
            changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return changed
    
    def _repair_index(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        changed = False
        # Ensure new tools are imported
        required_imports = [
            "from tools.github_receptor import GitHubReceptor",
            "from tools.slack_receptor import SlackReceptor",
            "from tools.sentry_receptor import SentryReceptor",
            "from tools.geo_receptor import GeoReceptor",
            "from tools.database_receptor import DatabaseReceptor",
            "from tools.developmental_boot import DevelopmentalBoot",
        ]
        for imp in required_imports:
            if imp not in content:
                # Add after last tools import
                content = content.replace(
                    "from tools.dream_engine import DreamEngine\n",
                    "from tools.dream_engine import DreamEngine\n" + imp + "\n"
                )
                changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return changed
    
    def _repair_scraper(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        changed = False
        if "Global Intelligence" not in content:
            changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return changed
    
    def get_status(self) -> Dict:
        return {
            "monitored_files": len(self.target_files),
            "repair_log_entries": len(self.repair_log),
            "call_guard": self.call_guard.get_status(),
            "validator_ready": True
        }


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    are = AutoRepairEngine(base)
    result = are.scan_and_fix("manual")
    print(result)