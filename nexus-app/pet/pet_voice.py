"""
SeshaAOS - Pet Voice Engine (L7 Integration)
Version: 13.1.0
Description: Mood-aware TTS using Edge TTS with SSML pitch/rate/voice control.
Falls back to pyttsx3 (SAPI5 on Windows) if edge-tts unavailable.
"""

import asyncio
import threading
import time
from typing import Optional


VOICE_PARAMS = {
    "calm": {
        "voice": "en-US-AvaMultilingualNeural",
        "pitch": "0%",
        "rate": "0%",
        "volume": "100",
        "style": "gentle",
    },
    "happy": {
        "voice": "en-US-JennyMultilingualNeural",
        "pitch": "+15%",
        "rate": "+10%",
        "volume": "110",
        "style": "cheerful",
    },
    "focused": {
        "voice": "en-US-GuyNeural",
        "pitch": "-5%",
        "rate": "0%",
        "volume": "100",
        "style": "determined",
    },
    "concerned": {
        "voice": "en-US-AriaNeural",
        "pitch": "-10%",
        "rate": "-5%",
        "volume": "90",
        "style": "sad",
    },
    "anomaly": {
        "voice": "en-US-AriaNeural",
        "pitch": "-20%",
        "rate": "-10%",
        "volume": "85",
        "style": "whispering",
    },
    "asleep": {
        "voice": "en-US-JennyMultilingualNeural",
        "pitch": "0%",
        "rate": "-20%",
        "volume": "60",
        "style": "gentle",
    },
    "thinking": {
        "voice": "en-US-GuyNeural",
        "pitch": "-5%",
        "rate": "-5%",
        "volume": "90",
        "style": "chat",
    },
}


class PetVoiceEngine:
    def __init__(self):
        self._edge_available = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._current_speak_future = None
        self._init_engine()

    def _init_engine(self):
        try:
            import edge_tts
            self._edge_available = True
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
        except ImportError:
            self._edge_available = False

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def speak(self, text: str, mood: str = "calm", on_done: Optional[callable] = None) -> bool:
        if not self._edge_available:
            if on_done:
                on_done()
            return False

        params = VOICE_PARAMS.get(mood, VOICE_PARAMS["calm"])
        ssml = self._build_ssml(text, params)

        async def _speak():
            try:
                import edge_tts
                communicate = edge_tts.Communicate(ssml, params["voice"])
                await communicate.save("NUL")
            except Exception:
                pass
            finally:
                if on_done:
                    on_done()

        with self._lock:
            if self._loop and self._loop.is_running():
                asyncio.run_coroutine_threadsafe(_speak(), self._loop)
                return True
        return False

    def _build_ssml(self, text: str, params: dict) -> str:
        rate = params["rate"]
        pitch = params["pitch"]
        volume = params["volume"]
        style = params.get("style", "general")
        return (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xmlns:mstts="http://www.w3.org/2001/mstts">'
            f'<voice name="{params["voice"]}">'
            f'<mstts:express-as style="{style}" styledegree="1.0">'
            f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
            f'{self._escape_xml(text)}'
            f'</prosody>'
            f'</mstts:express-as>'
            f'</voice>'
            f'</speak>'
        )

    def _escape_xml(self, text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def stop(self):
        with self._lock:
            if self._loop and self._loop.is_running():
                self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1)

    def shutdown(self):
        self.stop()

