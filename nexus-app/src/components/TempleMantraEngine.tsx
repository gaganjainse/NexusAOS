import React, { useEffect, useRef } from "react";

interface TempleMantraEngineProps {
  mantraBlend: number; // 0 (100% Bell) to 1 (100% Mantra)
  soundEnabled: boolean;
}

let mantraAudioCtx: AudioContext | null = null;
let mantraMasterGain: GainNode | null = null;
let mantraOsc1: OscillatorNode | null = null;
let mantraOsc2: OscillatorNode | null = null;
let mantraSubOsc: OscillatorNode | null = null;
let mantraFilter: BiquadFilterNode | null = null;
let mantraLfo: OscillatorNode | null = null;

export const TempleMantraEngine: React.FC<TempleMantraEngineProps> = ({
  mantraBlend,
  soundEnabled,
}) => {
  const isPlayingRef = useRef<boolean>(false);

  useEffect(() => {
    if (!soundEnabled || mantraBlend <= 0) {
      if (mantraMasterGain && mantraAudioCtx) {
        mantraMasterGain.gain.setTargetAtTime(0, mantraAudioCtx.currentTime, 0.2);
      }
      return;
    }

    try {
      if (!mantraAudioCtx) {
        const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
        mantraAudioCtx = new AudioCtx();
      }

      const ctx = mantraAudioCtx;
      if (ctx.state === "suspended") {
        ctx.resume();
      }

      if (!mantraMasterGain) {
        mantraMasterGain = ctx.createGain();
        mantraMasterGain.gain.setValueAtTime(0, ctx.currentTime);

        // Warm Lowpass Filter simulating vocal tract resonance
        mantraFilter = ctx.createBiquadFilter();
        mantraFilter.type = "lowpass";
        mantraFilter.frequency.setValueAtTime(280, ctx.currentTime);
        mantraFilter.Q.setValueAtTime(3.5, ctx.currentTime);

        // Low frequency chant oscillators: 108Hz (Sacred sub-drone) + 136.1Hz (Cosmic Om)
        mantraOsc1 = ctx.createOscillator();
        mantraOsc1.type = "sawtooth";
        mantraOsc1.frequency.setValueAtTime(108, ctx.currentTime);

        mantraOsc2 = ctx.createOscillator();
        mantraOsc2.type = "triangle";
        mantraOsc2.frequency.setValueAtTime(136.1, ctx.currentTime);

        mantraSubOsc = ctx.createOscillator();
        mantraSubOsc.type = "sine";
        mantraSubOsc.frequency.setValueAtTime(54, ctx.currentTime); // Deep octave sub

        // LFO for natural breath/vibrato chanting rhythm
        mantraLfo = ctx.createOscillator();
        mantraLfo.type = "sine";
        mantraLfo.frequency.setValueAtTime(0.2, ctx.currentTime); // 0.2 Hz slow breath cycle

        const lfoGain = ctx.createGain();
        lfoGain.gain.setValueAtTime(45, ctx.currentTime); // modulate filter cutoff

        mantraLfo.connect(lfoGain);
        lfoGain.connect(mantraFilter.frequency);

        mantraOsc1.connect(mantraFilter);
        mantraOsc2.connect(mantraFilter);
        mantraSubOsc.connect(mantraFilter);
        mantraFilter.connect(mantraMasterGain);
        mantraMasterGain.connect(ctx.destination);

        mantraOsc1.start();
        mantraOsc2.start();
        mantraSubOsc.start();
        mantraLfo.start();
        isPlayingRef.current = true;
      }

      // Update volume based on blend (0 to 1) -> Target gain around 0.12 * mantraBlend
      const targetVol = 0.12 * mantraBlend;
      mantraMasterGain.gain.setTargetAtTime(targetVol, ctx.currentTime, 0.3);
    } catch (err) {
      console.warn("TempleMantraEngine error:", err);
    }
  }, [mantraBlend, soundEnabled]);

  return null;
};

/**
 * Triggers a generative low-frequency Mantra chant burst with custom blend ratio.
 */
export function playGenerativeMantraPulse(blendRatio: number = 0.5) {
  if (blendRatio <= 0.05) return;
  try {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    const osc = ctx.createOscillator();
    const subOsc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(108, now); // 108Hz

    subOsc.type = "sine";
    subOsc.frequency.setValueAtTime(54, now); // Sub octave

    filter.type = "lowpass";
    filter.frequency.setValueAtTime(240, now);
    filter.Q.setValueAtTime(4, now);

    const vol = 0.15 * blendRatio;
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.exponentialRampToValueAtTime(vol, now + 0.3);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.5);

    osc.connect(filter);
    subOsc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    subOsc.start(now);
    osc.stop(now + 2.6);
    subOsc.stop(now + 2.6);
  } catch (err) {
    console.warn("Generative Mantra Pulse error:", err);
  }
}
