import React, { useEffect, useRef, useState } from "react";
import { Volume2, VolumeX, Bell, Music, Sparkles } from "lucide-react";
import { motion } from "motion/react";
import { VitalsData } from "../types/Sesha";

interface SoundscapeEngineProps {
  vitals: VitalsData;
  soundEnabled: boolean;
  onToggleSound: () => void;
  activeSoundscape?: "monsoon" | "chanting" | "bells" | "solfeggio";
}

export const SoundscapeEngine: React.FC<SoundscapeEngineProps> = ({
  vitals,
  soundEnabled,
  onToggleSound,
  activeSoundscape = "bells",
}) => {
  const audioCtxRef = useRef<AudioContext | null>(null);
  const masterGainRef = useRef<GainNode | null>(null);
  const bellOsc1Ref = useRef<OscillatorNode | null>(null);
  const bellOsc2Ref = useRef<OscillatorNode | null>(null);
  const bowlOscRef = useRef<OscillatorNode | null>(null);
  const filterRef = useRef<BiquadFilterNode | null>(null);

  const canvasTLRef = useRef<HTMLCanvasElement | null>(null);
  const canvasTRRef = useRef<HTMLCanvasElement | null>(null);
  const canvasBLRef = useRef<HTMLCanvasElement | null>(null);
  const canvasBRRef = useRef<HTMLCanvasElement | null>(null);

  const [currentFreq, setCurrentFreq] = useState<number>(432);

  // Initialize Web Audio Context & Synthesizer Nodes
  useEffect(() => {
    if (!soundEnabled) {
      if (audioCtxRef.current && audioCtxRef.current.state === "running") {
        audioCtxRef.current.suspend();
      }
      return;
    }

    try {
      if (!audioCtxRef.current) {
        const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
        const ctx = new AudioCtx();
        audioCtxRef.current = ctx;

        // Master Gain
        const masterGain = ctx.createGain();
        masterGain.gain.setValueAtTime(0.08, ctx.currentTime);
        masterGainRef.current = masterGain;

        // Lowpass Filter for warm temple resonance
        const filter = ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(800, ctx.currentTime);
        filterRef.current = filter;

        // 1. Temple Bell Fundamental (432Hz - Golden Frequency)
        const osc1 = ctx.createOscillator();
        osc1.type = "sine";
        osc1.frequency.setValueAtTime(432, ctx.currentTime);
        bellOsc1Ref.current = osc1;

        // 2. Harmonic Overtone (528Hz Solfeggio / Temple Chime)
        const osc2 = ctx.createOscillator();
        osc2.type = "sine";
        osc2.frequency.setValueAtTime(528, ctx.currentTime);
        bellOsc2Ref.current = osc2;

        // 3. Deep Tibetan Singing Bowl Sub-resonance (108Hz Sacred Frequency)
        const bowlOsc = ctx.createOscillator();
        bowlOsc.type = "triangle";
        bowlOsc.frequency.setValueAtTime(108, ctx.currentTime);
        bowlOscRef.current = bowlOsc;

        // Connect graph
        osc1.connect(filter);
        osc2.connect(filter);
        bowlOsc.connect(filter);
        filter.connect(masterGain);
        masterGain.connect(ctx.destination);

        osc1.start();
        osc2.start();
        bowlOsc.start();
      } else if (audioCtxRef.current.state === "suspended") {
        audioCtxRef.current.resume();
      }
    } catch (err) {
      console.warn("AudioContext init error:", err);
    }

    return () => {
      // Clean up on unmount
    };
  }, [soundEnabled]);

  // Modulate Audio Frequencies based on Vitals & Active Soundscape
  useEffect(() => {
    if (!soundEnabled || !audioCtxRef.current) return;

    const ctx = audioCtxRef.current;

    let target432 = 432 + (vitals.vibe - 95) * 2;
    let target528 = 528 + (vitals.fever - 36) * 5;
    let target108 = 108 + (vitals.energy - 80) * 0.5;

    if (activeSoundscape === "monsoon") {
      target432 = 216; // Soft rain drone base
      target528 = 432;
      target108 = 72;
    } else if (activeSoundscape === "chanting") {
      target432 = 136.1; // Om Frequency (136.1Hz)
      target528 = 272.2;
      target108 = 54;
    } else if (activeSoundscape === "solfeggio") {
      target432 = 528; // Transformation & DNA Repair Solfeggio
      target528 = 639;
      target108 = 432;
    }

    setCurrentFreq(Math.round(target432));

    if (bellOsc1Ref.current) {
      bellOsc1Ref.current.frequency.setTargetAtTime(target432, ctx.currentTime, 0.5);
    }
    if (bellOsc2Ref.current) {
      bellOsc2Ref.current.frequency.setTargetAtTime(target528, ctx.currentTime, 0.5);
    }
    if (bowlOscRef.current) {
      bowlOscRef.current.frequency.setTargetAtTime(target108, ctx.currentTime, 0.5);
    }
    if (filterRef.current) {
      const cutoff = activeSoundscape === "monsoon" ? 400 : 600 + vitals.diskC * 10;
      filterRef.current.frequency.setTargetAtTime(cutoff, ctx.currentTime, 0.5);
    }

    // Granular Synthesis: Trigger a subtle randomized temple chime ping when CPU load fluctuates
    const playGranularPing = () => {
      try {
        const pingOsc = ctx.createOscillator();
        const pingGain = ctx.createGain();

        // Sacred Pentatonic / Solfeggio Granular Frequencies (864Hz, 1056Hz, 1296Hz, 1728Hz)
        const scale = [864, 1056, 1296, 1728, 2160];
        const freq = scale[Math.floor(Math.random() * scale.length)];

        pingOsc.type = "sine";
        pingOsc.frequency.setValueAtTime(freq, ctx.currentTime);

        const now = ctx.currentTime;
        pingGain.gain.setValueAtTime(0.001, now);
        pingGain.gain.exponentialRampToValueAtTime(0.025, now + 0.05); // Soft attack
        pingGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2); // Bell ring decay

        pingOsc.connect(pingGain);
        if (masterGainRef.current) {
          pingGain.connect(masterGainRef.current);
        } else {
          pingGain.connect(ctx.destination);
        }

        pingOsc.start(now);
        pingOsc.stop(now + 1.3);
      } catch (err) {
        // Silently handle audio node cleanup
      }
    };

    // Trigger granular ping based on energy/CPU variation
    if (Math.random() > 0.4) {
      playGranularPing();
    }
  }, [vitals, soundEnabled]);

  // Sound Wave Visualizer Canvas Animation Loop (Temple Cymatic Waves in 4 Corners)
  useEffect(() => {
    let animId: number;
    let phase = 0;

    const drawCornerWave = (
      canvas: HTMLCanvasElement | null,
      flipX: boolean,
      flipY: boolean
    ) => {
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      const width = canvas.width;
      const height = canvas.height;

      ctx.clearRect(0, 0, width, height);

      // Save context state for flips
      ctx.save();
      if (flipX) {
        ctx.translate(width, 0);
        ctx.scale(-1, 1);
      }
      if (flipY) {
        ctx.translate(0, height);
        ctx.scale(1, -1);
      }

      // Temple Golden Ratio Cymatic Sound Waves
      const wavesCount = 4;
      const energyFactor = vitals.energy / 100;

      for (let i = 0; i < wavesCount; i++) {
        ctx.beginPath();
        const amplitude = (12 + i * 8) * energyFactor;
        const frequency = 0.05 + i * 0.02;
        const speed = 0.03 * (i + 1);

        ctx.strokeStyle = `rgba(245, 158, 11, ${0.4 - i * 0.08})`;
        ctx.lineWidth = 1.5 - i * 0.2;

        for (let x = 0; x < width; x += 2) {
          const y =
            height / 2 +
            Math.sin(x * frequency + phase * speed + i) * amplitude * Math.sin(x / 30);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // Temple Corner Mandala Ring
      ctx.beginPath();
      ctx.arc(0, 0, 35 + Math.sin(phase * 0.05) * 5, 0, Math.PI / 2);
      ctx.strokeStyle = `rgba(217, 119, 6, ${0.6 * energyFactor})`;
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.restore();
    };

    const render = () => {
      phase += 1;
      drawCornerWave(canvasTLRef.current, false, false);
      drawCornerWave(canvasTRRef.current, true, false);
      drawCornerWave(canvasBLRef.current, false, true);
      drawCornerWave(canvasBRRef.current, true, true);
      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animId);
    };
  }, [vitals]);

  return (
    <>
      {/* 4 CORNER SOUND WAVE CYMATIC VISUALIZERS */}
      {/* Top Left Corner */}
      <div className="absolute top-0 left-0 w-24 h-24 pointer-events-none z-30 opacity-80 overflow-hidden">
        <canvas ref={canvasTLRef} width={96} height={96} />
      </div>

      {/* Top Right Corner */}
      <div className="absolute top-0 right-0 w-24 h-24 pointer-events-none z-30 opacity-80 overflow-hidden">
        <canvas ref={canvasTRRef} width={96} height={96} />
      </div>

      {/* Bottom Left Corner */}
      <div className="absolute bottom-0 left-0 w-24 h-24 pointer-events-none z-30 opacity-80 overflow-hidden">
        <canvas ref={canvasBLRef} width={96} height={96} />
      </div>

      {/* Bottom Right Corner */}
      <div className="absolute bottom-0 right-0 w-24 h-24 pointer-events-none z-30 opacity-80 overflow-hidden">
        <canvas ref={canvasBRRef} width={96} height={96} />
      </div>

      {/* SOUNDSCAPE CONTROL BUTTON - Elegant Pill in Header/StatusBar */}
      <motion.button
        onClick={onToggleSound}
        whileHover={{ scale: 1.05, y: -1 }}
        whileTap={{ scale: 0.95 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
        title={
          soundEnabled
            ? `Soundscape Active (${currentFreq}Hz Temple Resonance) - Click to Mute`
            : "Click to Enable Subtle Temple Soundscape (432Hz Acoustic Resonance)"
        }
        className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono border transition-all duration-300 shadow-md cursor-pointer ${
          soundEnabled
            ? "bg-amber-950/90 text-amber-300 border-amber-500/80 shadow-amber-950/50 ring-1 ring-amber-500/30"
            : "bg-[#1f1711] text-stone-400 border-stone-800 hover:text-amber-200 hover:border-amber-700/60"
        }`}
      >
        <Bell className={`w-3.5 h-3.5 ${soundEnabled ? "text-amber-400 animate-pulse" : "text-stone-500"}`} />
        <span className="font-bold">{soundEnabled ? `${currentFreq}Hz Resonance` : "Soundscape Off"}</span>
        {soundEnabled ? (
          <Volume2 className="w-3 h-3 text-amber-400" />
        ) : (
          <VolumeX className="w-3 h-3 text-stone-500" />
        )}
      </motion.button>
    </>
  );
};

/**
 * Triggers a multi-harmonic Temple Bell Echo ping with spatial stereo panning and exponential decay.
 */
export function playTempleBellEcho(corner: "left" | "right" | "both" = "both") {
  try {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();

    const now = ctx.currentTime;

    // Frequencies representing traditional brass temple bell chime (Fundamental 528Hz + 1.618 golden ratio harmonics)
    const baseFreqs = [528, 854.3, 1382.3, 2236.6];

    baseFreqs.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, now);

      // Stereo panner for localized corner speaker ping
      if (ctx.createStereoPanner) {
        const panner = ctx.createStereoPanner();
        const panValue = corner === "left" ? -0.8 : corner === "right" ? 0.8 : idx % 2 === 0 ? -0.5 : 0.5;
        panner.pan.setValueAtTime(panValue, now);
        osc.connect(gain);
        gain.connect(panner);
        panner.connect(ctx.destination);
      } else {
        osc.connect(gain);
        gain.connect(ctx.destination);
      }

      const volume = 0.25 / (idx + 1);
      gain.gain.setValueAtTime(volume, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.5 + idx * 0.4);

      osc.start(now);
      osc.stop(now + 3.0);
    });
  } catch (err) {
    console.warn("Temple Bell Audio Echo context failed:", err);
  }
}


