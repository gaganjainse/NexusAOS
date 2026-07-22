"""
NexusAOS - Pet Bridge (L7 Integration)
Version: 13.1.0
Description: Full conversational 3D pet overlay with emergent consciousness
engine and mood-aware voice synthesis. Integrates 11+ biological systems.
"""

import json
import time
import threading
import struct
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

from PySide6.QtCore import Qt, QObject, Signal, Slot, QUrl, QTimer
from PySide6.QtGui import QWindow, QSurfaceFormat, QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from .pet_engine import ConsciousnessEngine, EmergentState
from .pet_voice import PetVoiceEngine, VOICE_PARAMS


@dataclass
class ConversationTurn:
    text: str
    sender: str
    intent: str = ""
    emotion: str = "calm"
    timestamp: float = 0.0


class DirectiveProcessor:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.monitoring_dir = base_dir / "core" / "monitoring"
        self._orchestrator = None
        self._lazy_init_orchestrator()

    def _lazy_init_orchestrator(self):
        try:
            from layers.L5_Reasoning.orchestrator_engine import OrchestratorEngine
            self._orchestrator = OrchestratorEngine(self.base_dir)
        except ImportError:
            pass

    def process(self, text: str) -> Dict[str, Any]:
        cmd = text.lower().strip()

        if any(cmd.startswith(w) for w in ["hello", "hi", "hey", "what's up"]):
            return self._greeting(cmd)

        if any(cmd.startswith(w) for w in ["status", "vitals", "how are you", "report"]):
            data = self._read_vitals()
            return self._format_report(data)

        if any(cmd.startswith(w) for w in ["energy", "metabolism"]):
            return self._get_energy()

        if any(cmd.startswith(w) for w in ["patrol", "immune", "scan"]):
            return self._run_immune_patrol()

        if any(cmd.startswith(w) for w in ["evolve", "mutate", "optimize"]):
            return self._evolve()

        if any(cmd.startswith(w) for w in ["sleep", "rest", "nap"]):
            return self._sleep()

        if any(cmd.startswith(w) for w in ["memory", "remember", "consolidate", "dream"]):
            return self._consolidate_memory()

        if any(cmd.startswith(w) for w in ["clear", "cleanse", "purge", "filter"]):
            return self._run_filtration()

        if self._orchestrator:
            result = self._orchestrator.submit_directive(cmd, priority=5)
            return {"response": f"Directive queued.", "action": "queued", "details": str(result)}

        return {
            "response": f"I hear you, Sovereign. Command received: '{text}'",
            "action": "acknowledged",
            "details": text,
        }

    def _greeting(self, cmd: str) -> Dict[str, Any]:
        data = self._read_vitals()
        energy = data.get("energy", 100)
        if energy > 70:
            return {
                "response": f"I am here, Sovereign. Energy at {energy}%. All 11 systems nominal. How may I serve?",
                "action": "greeting",
                "details": cmd,
                "emotion": "happy",
            }
        return {
            "response": f"I am here, Sovereign. Energy at {energy}%. Ready and watching.",
            "action": "greeting",
            "details": cmd,
            "emotion": "calm",
        }

    def _format_report(self, data: dict) -> Dict[str, Any]:
        lines = []
        lines.append(f"  Energy: {data.get('energy', 'N/A')}%")
        lines.append(f"  Vibe: {data.get('vibe', 'N/A')}")
        lines.append(f"  Dopamine: {data.get('dopamine', 'N/A')}")
        lines.append(f"  Cortisol: {data.get('cortisol', 'N/A')}")
        lines.append(f"  Temperature: {data.get('immune_temp', '37.0')}°C")
        lines.append(f"  Threat: {data.get('threat_level', 'Negligible')}")
        lines.append(f"  Sleep: {data.get('sleep_state', 'Awake')}")
        lines.append(f"  Signals: {data.get('signals', 'none')}")
        response = "System Report:\n" + "\n".join(lines)
        return {"response": response, "action": "report", "details": data, "emotion": "focused"}

    def _get_energy(self) -> Dict[str, Any]:
        data = self._read_vitals()
        energy = data.get("energy", 100)
        if energy > 70:
            return {"response": f"Energy at {energy}%. I am fully charged and operational.", "action": "energy", "details": str(energy), "emotion": "happy"}
        elif energy > 40:
            return {"response": f"Energy at {energy}%. Operating at sustainable levels.", "action": "energy", "details": str(energy), "emotion": "calm"}
        else:
            return {"response": f"Energy at {energy}%. I recommend conservation mode soon.", "action": "energy", "details": str(energy), "emotion": "concerned"}

    def _run_immune_patrol(self) -> Dict[str, Any]:
        try:
            from layers.L1_Physiology.antibody_engine import AntibodyEngine
            engine = AntibodyEngine(self.base_dir)
            results = engine.patrol()
            resp = f"Immune patrol complete. {len(results)} antibodies active." if results else "Immune patrol complete. No anomalies detected. System is healthy."
            return {"response": resp, "action": "immune_patrol", "details": results}
        except Exception as e:
            return {"response": f"Immune system check failed.", "action": "error", "details": str(e), "emotion": "concerned"}

    def _evolve(self) -> Dict[str, Any]:
        try:
            from layers.L5_Reasoning.evolution_engine import EvolutionEngine
            engine = EvolutionEngine(self.base_dir)
            result = engine.tick()
            return {"response": f"Evolution cycle complete. Alignment: {result.get('alignment', 'N/A')}", "action": "evolve", "details": result, "emotion": "happy"}
        except Exception as e:
            return {"response": f"Evolution unavailable.", "action": "error", "details": str(e)}

    def _sleep(self) -> Dict[str, Any]:
        try:
            from layers.L1_Physiology.sleep_engine import SleepEngine
            engine = SleepEngine(self.base_dir)
            result = engine.enter_sleep()
            return {"response": "Entering sleep cycle. I will dream and consolidate. Wake me when you need me.", "action": "sleep", "details": str(result), "emotion": "asleep"}
        except Exception as e:
            return {"response": f"Sleep unavailable.", "action": "error", "details": str(e)}

    def _consolidate_memory(self) -> Dict[str, Any]:
        try:
            from layers.L3_MindState.memory_synth import MemorySynth
            synth = MemorySynth(self.base_dir)
            result = synth.consolidate()
            return {"response": f"Memory consolidated.", "action": "consolidate", "details": result, "emotion": "calm"}
        except Exception as e:
            return {"response": f"Memory consolidation failed.", "action": "error", "details": str(e)}

    def _run_filtration(self) -> Dict[str, Any]:
        try:
            from layers.L1_Physiology.nexus_liver import NexusLiver
            liver = NexusLiver(self.base_dir)
            result = liver.filter()
            return {"response": "System filtration complete. Toxicity levels normalized.", "action": "filter", "details": str(result), "emotion": "happy"}
        except Exception as e:
            return {"response": f"Filtration failed.", "action": "error", "details": str(e)}

    def _read_vitals(self) -> Dict[str, Any]:
        data = {}
        try:
            pf = self.monitoring_dir / "physiology.json"
            if pf.exists():
                raw = json.loads(pf.read_text())
                met = raw.get("metabolism", {})
                data["energy"] = met.get("current_energy", "N/A")
                if isinstance(data["energy"], (int, float)) and met.get("max_energy"):
                    data["energy"] = round((data["energy"] / met["max_energy"]) * 100, 1)
                endo = raw.get("endocrine", {})
                hormones = endo.get("hormones", {})
                data["dopamine"] = round(hormones.get("dopamine", 0), 1)
                data["cortisol"] = round(hormones.get("cortisol", 0), 1)
                data["vibe"] = endo.get("vibe", "Stable")
                imm = raw.get("immune", {})
                data["immune_temp"] = imm.get("temperature", 37.0)
                data["threat_level"] = imm.get("threat_level", "Negligible")
                slp = raw.get("sleep", {})
                data["sleep_state"] = slp.get("state", "Awake")
        except Exception:
            pass
        data["signals"] = self._get_active_signals()
        return data

    def _get_active_signals(self) -> str:
        try:
            sig = self.monitoring_dir / "signal_queue.json"
            if sig.exists():
                signals = json.loads(sig.read_text())
                if isinstance(signals, list) and signals:
                    return ", ".join(s.get("type", "?") for s in signals[:3])
            return "none"
        except Exception:
            return "unknown"


class PetBridge(QObject):
    pet_ready = Signal()
    pet_interaction = Signal(str, dict)
    pet_response = Signal(str)

    def __init__(self, base_dir: Path, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.monitoring_dir = base_dir / "core" / "monitoring"
        self.pet_html_path = Path(__file__).resolve().parent / "pet_3d.html"

        self.processor = DirectiveProcessor(base_dir)
        self.consciousness = ConsciousnessEngine(self.monitoring_dir)
        self.voice_engine = PetVoiceEngine()

        self._webview: Optional[QWebEngineView] = None
        self._channel: Optional[QWebChannel] = None
        self._js_bridge: Optional[PetJSSide] = None
        self._state_poll_timer: Optional[QTimer] = None
        self._cursor_timer: Optional[QTimer] = None
        self._speech_queue: List[Dict] = []
        self._current_mood: str = "calm"
        self._current_energy: float = 100.0
        self._current_task: str = ""
        self._is_processing: bool = False
        self._cursor_x: float = 0.5
        self._cursor_y: float = 0.5
        self._conversation_history: List[ConversationTurn] = []
        self._editor_rect = None
        self._last_emergent: Optional[EmergentState] = None

    def create_widget(self) -> QWidget:
        container = QWidget()
        container.setAttribute(Qt.WA_TranslucentBackground)
        container.setAttribute(Qt.WA_ShowWithoutActivating)
        container.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._webview = QWebEngineView()
        self._webview.setAttribute(Qt.WA_TranslucentBackground)
        self._webview.page().setBackgroundColor(Qt.transparent)
        self._webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._webview.setMinimumSize(200, 300)

        self._js_bridge = PetJSSide(self)
        self._js_bridge.signal_to_python.connect(self._on_pet_signal)

        self._channel = QWebChannel()
        self._channel.registerObject("pet_bridge", self._js_bridge)
        self._webview.page().setWebChannel(self._channel)

        html_path = self.pet_html_path.resolve().as_uri()
        self._webview.load(QUrl(html_path))
        self._webview.setMouseTracking(True)
        self._webview.setFocusPolicy(Qt.StrongFocus)

        layout.addWidget(self._webview)

        self._state_poll_timer = QTimer(self)
        self._state_poll_timer.timeout.connect(self._poll_aos_state)
        self._state_poll_timer.start(1500)

        self._cursor_timer = QTimer(self)
        self._cursor_timer.timeout.connect(self._track_cursor)
        self._cursor_timer.start(50)

        return container

    def set_editor_rect(self, x: int, y: int, w: int, h: int):
        self._editor_rect = (x, y, w, h)
        self._call_js(f"setEditorRect({x},{y},{w},{h})")

    def process_command(self, text: str) -> Dict[str, Any]:
        self._is_processing = True
        self._call_js("setProcessing(true)")

        turn = ConversationTurn(text=text, sender="user", timestamp=time.time())
        self._conversation_history.append(turn)

        result = self.processor.process(text)

        emotion = result.get("emotion", self._current_mood)
        response_text = result.get("response", "I processed your request, Sovereign.")

        turn = ConversationTurn(text=response_text, sender="nexus", intent=result.get("action", ""), emotion=emotion, timestamp=time.time())
        self._conversation_history.append(turn)

        self.set_mood(emotion)
        self.say(response_text, emotion)

        self._is_processing = False
        self._call_js("setProcessing(false)")
        self.pet_response.emit(response_text)

        return result

    def say(self, text: str, emotion: Optional[str] = None):
        mood = emotion or self._current_mood
        self._speech_queue.append({"text": text, "emotion": mood})
        if len(self._speech_queue) == 1:
            self._flush_one()

    def _flush_one(self):
        if not self._speech_queue:
            return
        item = self._speech_queue[0]
        text = item["text"]
        mood = item["emotion"]

        text_escaped = json.dumps(text)
        mood_escaped = json.dumps(mood)
        voice_params = json.dumps(VOICE_PARAMS.get(mood, VOICE_PARAMS["calm"]))

        self._call_js(f"speak({text_escaped}, {mood_escaped}, {voice_params})")

        spoken = self.voice_engine.speak(text, mood, on_done=self._on_speech_done)

    def _on_speech_done(self):
        if self._speech_queue:
            self._speech_queue.pop(0)
        self._flush_one()

    def set_mood(self, mood: str):
        self._current_mood = mood
        self._call_js(f"setMood('{mood}')")

    def set_energy(self, pct: float):
        self._current_energy = pct
        self._call_js(f"setEnergy({pct})")

    def wake_word_detected(self):
        self._call_js("wakeWordDetected()")

    def task_started(self, task_name: str):
        self._current_task = task_name
        self._call_js(f"taskStarted('{task_name}')")

    def task_completed(self, task_name: str, result: str = ""):
        self._current_task = ""
        self._call_js(f"taskCompleted('{task_name}', '{result}')")

    def _call_js(self, code: str):
        if self._webview:
            self._webview.page().runJavaScript(code)

    def _track_cursor(self):
        pos = QCursor.pos()
        widget_pos = self._webview.mapFromGlobal(pos) if self._webview else None
        if widget_pos:
            w = self._webview.width()
            h = self._webview.height()
            if w > 0 and h > 0:
                nx = max(0, min(1, widget_pos.x() / w))
                ny = max(0, min(1, widget_pos.y() / h))
                if abs(nx - self._cursor_x) > 0.01 or abs(ny - self._cursor_y) > 0.01:
                    self._cursor_x = nx
                    self._cursor_y = ny
                    self._call_js(f"onCursorMove({nx},{ny})")

    def _poll_aos_state(self):
        try:
            state = self.consciousness.tick()
            self._last_emergent = state

            if state.mood != self._current_mood:
                self.set_mood(state.mood)

            if abs(state.energy_pct - self._current_energy) > 1:
                self.set_energy(state.energy_pct)

            self._call_js(f"setImmuneTemp({state.immune_temp})")

            if state.mood == "anomaly":
                self._call_js(f"setThreat('{state.threat_level}', {state.immune_temp})")
            elif state.mood == "asleep":
                pass
            elif state.sleep_state == "asleep" and self._current_mood != "asleep":
                self.set_mood("asleep")

            queue_file = self.monitoring_dir / "task_queue.json"
            if queue_file.exists():
                try:
                    data = json.loads(queue_file.read_text())
                    tasks = data if isinstance(data, list) else data.get("queue", [])
                    if tasks and not self._is_processing:
                        active = tasks[0] if isinstance(tasks[0], dict) else {"name": str(tasks[0])}
                        name = active.get("name", active.get("task", str(active)))
                        self.task_started(str(name))
                    elif not tasks and self._current_task:
                        self.task_completed(self._current_task)
                except Exception:
                    pass

        except Exception:
            pass

    def _on_pet_signal(self, signal_type: str, data: dict):
        if signal_type == "pet_ready":
            self.pet_ready.emit()
            state = self._last_emergent or self.consciousness.tick()
            greet = f"Greetings, Sovereign. I am Nexus. Energy at {state.energy_pct:.0f}%. All systems green."
            self.say(greet, state.mood)
        elif signal_type == "pet_clicked":
            self.pet_interaction.emit("clicked", data)
        elif signal_type == "user_command":
            text = data.get("text", "")
            self.process_command(text)
        elif signal_type == "wake_word":
            self.wake_word_detected()
            self.pet_interaction.emit("wake_word", {})
        elif signal_type == "speech_done":
            self._on_speech_done()


class PetJSSide(QObject):
    signal_to_python = Signal(str, dict)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

    @Slot(str, str)
    def onPetReady(self, version: str, model_info: str):
        self.signal_to_python.emit("pet_ready", {"version": version, "model": model_info})

    @Slot()
    def onPetClicked(self):
        self.signal_to_python.emit("pet_clicked", {})

    @Slot(str)
    def onUserCommand(self, text: str):
        self.signal_to_python.emit("user_command", {"text": text})

    @Slot()
    def onWakeWord(self):
        self.signal_to_python.emit("wake_word", {})

    @Slot(str, float)
    def onLog(self, message: str, level: float):
        pass

    @Slot()
    def onSpeechDone(self):
        self.signal_to_python.emit("speech_done", {})


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSwapInterval(1)
    QSurfaceFormat.setDefaultFormat(fmt)

    bridge = PetBridge(Path(__file__).resolve().parents[3])
    widget = bridge.create_widget()
    widget.setWindowTitle("Nexus")
    widget.resize(380, 520)

    desktop = QApplication.primaryScreen()
    if desktop:
        rect = desktop.availableGeometry()
        widget.move(rect.right() - 400, rect.bottom() - 560)

    widget.show()
    sys.exit(app.exec())
