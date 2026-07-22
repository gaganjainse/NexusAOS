import React, { useEffect, useRef } from "react";
import { VitalsData } from "../types/nexus";

interface HarmonicResonanceCanvasProps {
  vitals: VitalsData;
  frequency?: number;
  bellIntensity?: number;
}

export const HarmonicResonanceCanvas: React.FC<HarmonicResonanceCanvasProps> = ({
  vitals,
  frequency = 432,
  bellIntensity = 1.0,
}) => {
  const canvasTLRef = useRef<HTMLCanvasElement | null>(null);
  const canvasTRRef = useRef<HTMLCanvasElement | null>(null);
  const canvasBLRef = useRef<HTMLCanvasElement | null>(null);
  const canvasBRRef = useRef<HTMLCanvasElement | null>(null);

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
      const wavesCount = 5;
      const energyFactor = (vitals.energy / 100) * bellIntensity;
      const freqFactor = frequency / 432;

      for (let i = 0; i < wavesCount; i++) {
        ctx.beginPath();
        const amplitude = (14 + i * 9) * energyFactor;
        const waveFreq = (0.04 + i * 0.02) * freqFactor;
        const speed = 0.035 * (i + 1);

        ctx.strokeStyle = `rgba(245, 158, 11, ${0.45 - i * 0.08})`;
        ctx.lineWidth = 1.6 - i * 0.25;

        for (let x = 0; x < width; x += 2) {
          const y =
            height / 2 +
            Math.sin(x * waveFreq + phase * speed + i) * amplitude * Math.sin(x / 28);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // Temple Concentric Bell Ring Ripples
      ctx.beginPath();
      const rippleRadius = (phase * 0.8) % 60;
      ctx.arc(0, 0, rippleRadius, 0, Math.PI / 2);
      ctx.strokeStyle = `rgba(251, 191, 36, ${Math.max(0, 0.5 - rippleRadius / 60)})`;
      ctx.lineWidth = 1.2;
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
  }, [vitals, frequency, bellIntensity]);

  return (
    <div className="absolute inset-0 pointer-events-none z-20 overflow-hidden">
      {/* Top Left Corner Canvas */}
      <div className="absolute top-0 left-0 w-28 h-28 opacity-85">
        <canvas ref={canvasTLRef} width={112} height={112} />
      </div>

      {/* Top Right Corner Canvas */}
      <div className="absolute top-0 right-0 w-28 h-28 opacity-85">
        <canvas ref={canvasTRRef} width={112} height={112} />
      </div>

      {/* Bottom Left Corner Canvas */}
      <div className="absolute bottom-0 left-0 w-28 h-28 opacity-85">
        <canvas ref={canvasBLRef} width={112} height={112} />
      </div>

      {/* Bottom Right Corner Canvas */}
      <div className="absolute bottom-0 right-0 w-28 h-28 opacity-85">
        <canvas ref={canvasBRRef} width={112} height={112} />
      </div>
    </div>
  );
};
