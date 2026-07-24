import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { PetStatus, PetState, VitalsData, Directive } from "../../types/Sesha";
import {
  Volume2,
  VolumeX,
  Send,
  Maximize2,
  Minimize2,
  Sparkles,
  Zap,
  Activity,
  Mic,
  Cpu,
  RotateCcw,
  Bot,
  MessageSquare,
  Shield,
  X,
} from "lucide-react";

interface Sesha3DPetCompanionProps {
  status: PetStatus;
  vitals: VitalsData;
  directives?: Directive[];
  activeFile?: string;
  onUpdateStatus?: (newStatus: Partial<PetStatus>) => void;
  onSubmitCommand?: (cmd: string) => void;
  docked?: boolean;
  onCloseDock?: () => void;
}

export const Sesha3DPetCompanion: React.FC<Sesha3DPetCompanionProps> = ({
  status,
  vitals,
  directives = [],
  activeFile,
  onUpdateStatus,
  onSubmitCommand,
  docked = true,
  onCloseDock,
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [speechMuted, setSpeechMuted] = useState(false);
  const [inputText, setInputText] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechBubble, setSpeechBubble] = useState<string>(
    status.speechText || "Greetings Sovereign. 3D Companion Sesha initialized."
  );
  const [minimized, setMinimized] = useState(false);

  // Targets for 3D Gaze Tracking
  // gazeTarget: NORMALISED coordinates (-1 to 1)
  const mousePosRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const gazeTargetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const isWorkingRef = useRef<boolean>(false);
  const isFocusedOnUserRef = useRef<boolean>(false);

  // Update speech bubble when status changes
  useEffect(() => {
    if (status.speechText) {
      setSpeechBubble(status.speechText);
      speakText(status.speechText);
    }
  }, [status.speechText]);

  // Voice Speech Synthesis
  const speakText = (text: string) => {
    if (speechMuted || !("speechSynthesis" in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.05;
      utterance.pitch = 1.1;
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("Speech synthesis error", e);
    }
  };

  // Listen to mouse movement for 3D eye tracking across window
  useEffect(() => {
    const handlePointerMove = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = -(e.clientY / window.innerHeight) * 2 + 1;
      mousePosRef.current = { x, y };
    };

    window.addEventListener("pointermove", handlePointerMove);
    return () => window.removeEventListener("pointermove", handlePointerMove);
  }, []);

  // Update mode triggers for gaze target
  useEffect(() => {
    isWorkingRef.current = status.state === "Working" || status.state === "Thinking";
    isFocusedOnUserRef.current = status.attention || status.state === "Happy";
  }, [status.state, status.attention]);

  // Three.js 3D Model Construction & Animation Loop
  useEffect(() => {
    if (!mountRef.current) return;
    const container = mountRef.current;
    const width = container.clientWidth || 220;
    const height = container.clientHeight || 220;

    // 1. SCENE, CAMERA, RENDERER
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 2. LIGHTS
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const coreLight = new THREE.PointLight(0x00f2fe, 2, 10);
    coreLight.position.set(0, 0, 2);
    scene.add(coreLight);

    const backLight = new THREE.PointLight(0xa855f7, 1.5, 10);
    backLight.position.set(-2, 2, -2);
    scene.add(backLight);

    // 3. MODEL CREATION
    const petGroup = new THREE.Group();
    scene.add(petGroup);

    // Head Base - Sleek Cybernetic Orb
    const headGeo = new THREE.SphereGeometry(1, 32, 32);
    const headMat = new THREE.MeshStandardMaterial({
      color: 0x0f172a,
      roughness: 0.2,
      metalness: 0.8,
    });
    const headMesh = new THREE.Mesh(headGeo, headMat);
    petGroup.add(headMesh);

    // Visor Face Plate
    const visorGeo = new THREE.SphereGeometry(0.85, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.55);
    const visorMat = new THREE.MeshStandardMaterial({
      color: 0x020617,
      roughness: 0.1,
      metalness: 0.9,
    });
    const visorMesh = new THREE.Mesh(visorGeo, visorMat);
    visorMesh.rotation.x = Math.PI * 0.5;
    visorMesh.position.z = 0.2;
    petGroup.add(visorMesh);

    // Eyes Group
    const eyesGroup = new THREE.Group();
    petGroup.add(eyesGroup);

    // Left Eye Outer Ring & Pupil
    const eyeGeo = new THREE.SphereGeometry(0.18, 16, 16);
    const eyeMat = new THREE.MeshStandardMaterial({
      color: 0x00f2fe,
      emissive: 0x00f2fe,
      emissiveIntensity: 0.8,
    });

    const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
    leftEye.position.set(-0.35, 0.1, 0.82);
    eyesGroup.add(leftEye);

    const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
    rightEye.position.set(0.35, 0.1, 0.82);
    eyesGroup.add(rightEye);

    // Eye Pupils
    const pupilGeo = new THREE.SphereGeometry(0.08, 16, 16);
    const pupilMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      emissive: 0xffffff,
      emissiveIntensity: 1,
    });
    const leftPupil = new THREE.Mesh(pupilGeo, pupilMat);
    leftPupil.position.set(0, 0, 0.12);
    leftEye.add(leftPupil);

    const rightPupil = new THREE.Mesh(pupilGeo, pupilMat);
    rightPupil.position.set(0, 0, 0.12);
    rightEye.add(rightPupil);

    // Floating Orbital Halo Rings
    const ring1Geo = new THREE.TorusGeometry(1.3, 0.03, 16, 64);
    const ring1Mat = new THREE.MeshStandardMaterial({
      color: 0x38bdf8,
      emissive: 0x0284c7,
      emissiveIntensity: 0.5,
      wireframe: true,
    });
    const ring1 = new THREE.Mesh(ring1Geo, ring1Mat);
    petGroup.add(ring1);

    const ring2Geo = new THREE.TorusGeometry(1.5, 0.02, 16, 64);
    const ring2Mat = new THREE.MeshStandardMaterial({
      color: 0xa855f7,
      emissive: 0x7e22ce,
      emissiveIntensity: 0.5,
    });
    const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
    ring2.rotation.x = Math.PI / 3;
    petGroup.add(ring2);

    // Ears / Antennas
    const earGeo = new THREE.CylinderGeometry(0.02, 0.08, 0.6, 12);
    const earMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.9 });
    
    const leftEar = new THREE.Mesh(earGeo, earMat);
    leftEar.position.set(-1.05, 0.6, 0);
    leftEar.rotation.z = Math.PI / 4;
    petGroup.add(leftEar);

    const rightEar = new THREE.Mesh(earGeo, earMat);
    rightEar.position.set(1.05, 0.6, 0);
    rightEar.rotation.z = -Math.PI / 4;
    petGroup.add(rightEar);

    // 4. ANIMATION LOOP
    const startTime = performance.now();
    let animId: number;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const elapsed = (performance.now() - startTime) / 1000;

      // Determine Target Gaze Coordinates
      let targetX = mousePosRef.current.x;
      let targetY = mousePosRef.current.y;

      // MODE SWITCHING:
      // When command running -> Look at editor area (Left center screen: x = -0.6, y = 0.2)
      if (isWorkingRef.current) {
        targetX = -0.6;
        targetY = 0.2;
      } else if (isFocusedOnUserRef.current) {
        // Look straight forward at camera
        targetX = 0;
        targetY = 0;
      }

      // Smooth Lerp Gaze Target
      gazeTargetRef.current.x += (targetX - gazeTargetRef.current.x) * 0.08;
      gazeTargetRef.current.y += (targetY - gazeTargetRef.current.y) * 0.08;

      // Head Rotation towards gaze target
      const maxRotY = 0.6;
      const maxRotX = 0.4;
      petGroup.rotation.y = gazeTargetRef.current.x * maxRotY;
      petGroup.rotation.x = -gazeTargetRef.current.y * maxRotX;

      // Pupil Translation inside Eye
      const pupilShiftX = gazeTargetRef.current.x * 0.06;
      const pupilShiftY = gazeTargetRef.current.y * 0.06;
      leftPupil.position.x = pupilShiftX;
      leftPupil.position.y = pupilShiftY;
      rightPupil.position.x = pupilShiftX;
      rightPupil.position.y = pupilShiftY;

      // Natural Breathing Float (Sine Wave)
      petGroup.position.y = Math.sin(elapsed * 2) * 0.08;

      // Orbital Rings Rotation
      ring1.rotation.z = elapsed * 0.5;
      ring2.rotation.y = elapsed * 0.8;

      // State-Based Visual Reactions
      if (status.state === "Working" || status.state === "Thinking") {
        ring1.rotation.z = elapsed * 2.5;
        eyeMat.color.setHex(0xa855f7);
        eyeMat.emissive.setHex(0xa855f7);
        coreLight.color.setHex(0xa855f7);
      } else if (vitals.fever > 38 || status.state === "Concerned") {
        eyeMat.color.setHex(0xf97316);
        eyeMat.emissive.setHex(0xf97316);
        coreLight.color.setHex(0xf97316);
      } else if (status.state === "Happy") {
        eyeMat.color.setHex(0x10b981);
        eyeMat.emissive.setHex(0x10b981);
        coreLight.color.setHex(0x10b981);
        petGroup.rotation.z = Math.sin(elapsed * 4) * 0.15;
      } else {
        eyeMat.color.setHex(0x00f2fe);
        eyeMat.emissive.setHex(0x00f2fe);
        coreLight.color.setHex(0x00f2fe);
      }

      renderer.render(scene, camera);
    };

    animate();

    // Resize Observer
    const handleResize = () => {
      if (!mountRef.current) return;
      const w = mountRef.current.clientWidth || 220;
      const h = mountRef.current.clientHeight || 220;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [status.state, vitals.fever]);

  // Handle Command Submissions & Sesha Calls
  const handleCommandSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim()) return;

    const cmd = inputText.trim();
    setInputText("");

    // Look straight at user when user submits command
    onUpdateStatus?.({ attention: true, state: "Thinking" });

    // Handle Quick Intelligence Commands
    if (cmd.toLowerCase().includes("report") || cmd.toLowerCase().includes("status")) {
      const activeDirCount = directives.filter((d) => d.status === "Processing").length;
      const reportText = `Sovereign Report: CPU at ${vitals.cpuUsage}%, Disk C at ${vitals.diskC}%, Energy at ${vitals.energy}%. ${activeDirCount} active directives in queue. Systems Homeostatic.`;
      setSpeechBubble(reportText);
      speakText(reportText);
      setTimeout(() => {
        onUpdateStatus?.({ state: "Happy" });
      }, 1000);
    } else if (cmd.toLowerCase().includes("Sesha")) {
      const focusText = `Sesha online! Focusing directly on you, Sovereign Master. How shall I optimize your workspace?`;
      setSpeechBubble(focusText);
      speakText(focusText);
      onUpdateStatus?.({ state: "Happy", attention: true });
    } else {
      onSubmitCommand?.(cmd);
      setSpeechBubble(`Dispatching command to Sovereign execution matrix: "${cmd}"`);
      speakText(`Executing command: ${cmd}`);
    }
  };

  const handleCallSesha = () => {
    onUpdateStatus?.({ attention: true, state: "Happy" });
    const text = "Yes Sovereign? Sesha is locked on your coordinates. Direct me!";
    setSpeechBubble(text);
    speakText(text);
  };

  return (
    <div
      className={`select-none transition-all duration-300 font-mono text-xs ${
        docked
          ? "fixed bottom-8 right-4 z-40 w-72 bg-zinc-950/95 border border-cyan-500/40 rounded-2xl shadow-2xl backdrop-blur-xl p-3 flex flex-col gap-2"
          : "w-full h-full bg-zinc-950/90 border border-zinc-800 rounded-xl p-4 flex flex-col gap-3"
      }`}
    >
      {/* Header Bar */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#00f2fe]" />
          <span className="font-bold text-zinc-100 tracking-wider text-xs flex items-center gap-1">
            Sesha <span className="text-cyan-400">3D-ENTITY</span>
          </span>
          <span className="text-[9px] px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
            {status.state}
          </span>
        </div>

        <div className="flex items-center gap-1 text-zinc-400">
          <button
            onClick={() => setSpeechMuted(!speechMuted)}
            title={speechMuted ? "Unmute Voice" : "Mute Voice"}
            className="p-1 hover:text-cyan-300 rounded hover:bg-zinc-850"
          >
            {speechMuted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-cyan-400" />}
          </button>
          {docked && (
            <button
              onClick={() => setMinimized(!minimized)}
              title={minimized ? "Expand" : "Minimize"}
              className="p-1 hover:text-zinc-100 rounded hover:bg-zinc-850"
            >
              {minimized ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}
            </button>
          )}
          {onCloseDock && (
            <button
              onClick={onCloseDock}
              className="p-1 hover:text-rose-400 rounded hover:bg-zinc-850"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {!minimized && (
        <>
          {/* Speech Bubble */}
          <div className="relative bg-zinc-900/90 border border-cyan-500/30 p-2.5 rounded-xl shadow-lg text-zinc-200 text-xs">
            <div className="flex items-start gap-2">
              <Bot className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
              <p className="font-sans text-[11px] leading-relaxed text-cyan-100">
                "{speechBubble}"
              </p>
            </div>
            {isSpeaking && (
              <div className="flex items-center gap-1 mt-2 pt-1 border-t border-cyan-500/20 text-[9px] text-cyan-400">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
                <span>Vocalizing Voice Synthesis...</span>
              </div>
            )}
          </div>

          {/* 3D WebGL Canvas Container */}
          <div
            onClick={handleCallSesha}
            title="Click to call Sesha & focus camera"
            className="relative w-full h-44 bg-gradient-to-b from-zinc-925 to-zinc-950 border border-zinc-800 rounded-xl overflow-hidden cursor-pointer group flex items-center justify-center shadow-inner"
          >
            <div ref={mountRef} className="w-full h-full" />

            {/* Overlay Status Badge */}
            <div className="absolute top-2 left-2 bg-zinc-950/80 border border-zinc-800 text-[9px] px-1.5 py-0.5 rounded text-zinc-400">
              GAZE: {isWorkingRef.current ? "EDITOR" : status.attention ? "SOVEREIGN" : "CURSOR"}
            </div>

            <div className="absolute bottom-2 right-2 bg-cyan-950/90 text-cyan-300 border border-cyan-700/60 text-[9px] px-2 py-0.5 rounded shadow group-hover:bg-cyan-600 group-hover:text-white transition-colors">
              Call "Sesha" ❯
            </div>
          </div>

          {/* Direct Interactive Command & Voice Bar */}
          <form onSubmit={handleCommandSubmit} className="flex items-center gap-1.5 bg-zinc-900 border border-zinc-750 focus-within:border-cyan-400 rounded-lg p-1.5">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask Sesha or give command ('report', 'vitals', 'Sesha')..."
              className="flex-1 bg-transparent text-[11px] text-zinc-100 placeholder-zinc-500 focus:outline-none px-1"
            />
            <button
              type="submit"
              className="p-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded transition-colors shadow"
            >
              <Send className="w-3 h-3" />
            </button>
          </form>

          {/* Quick Action Chips */}
          <div className="flex items-center gap-1 overflow-x-auto text-[9px] text-zinc-400 pt-0.5">
            <button
              onClick={() => {
                setInputText("give me a system report");
                handleCommandSubmit();
              }}
              className="px-2 py-0.5 bg-zinc-900 border border-zinc-800 hover:border-cyan-500 rounded whitespace-nowrap"
            >
              📊 System Report
            </button>
            <button
              onClick={() => {
                setInputText("Sesha");
                handleCommandSubmit();
              }}
              className="px-2 py-0.5 bg-zinc-900 border border-zinc-800 hover:border-cyan-500 rounded whitespace-nowrap text-cyan-300"
            >
              🎯 Focus Sesha
            </button>
            <button
              onClick={() => {
                onSubmitCommand?.("/patrol");
                setSpeechBubble("Running immune system patrol...");
              }}
              className="px-2 py-0.5 bg-zinc-900 border border-zinc-800 hover:border-cyan-500 rounded whitespace-nowrap"
            >
              🛡️ Immune Patrol
            </button>
          </div>
        </>
      )}
    </div>
  );
};

