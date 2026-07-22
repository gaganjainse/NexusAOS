import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

interface Ripple {
  id: number;
  x: number;
  y: number;
}

export const VisualHapticRipple: React.FC = () => {
  const [ripples, setRipples] = useState<Ripple[]>([]);

  useEffect(() => {
    const handleTriggerRipple = (e: CustomEvent<{ x?: number; y?: number }>) => {
      const x = e.detail?.x ?? window.innerWidth / 2;
      const y = e.detail?.y ?? window.innerHeight / 2;
      const id = Date.now() + Math.random();

      setRipples((prev) => [...prev, { id, x, y }]);

      // Automatically clean up ripple
      setTimeout(() => {
        setRipples((prev) => prev.filter((r) => r.id !== id));
      }, 1500);
    };

    const handleGlobalClick = (e: MouseEvent) => {
      triggerHapticRipple({ clientX: e.clientX, clientY: e.clientY } as any);
    };

    window.addEventListener("temple-haptic-ripple" as any, handleTriggerRipple);
    window.addEventListener("pointerdown", handleGlobalClick);
    return () => {
      window.removeEventListener("temple-haptic-ripple" as any, handleTriggerRipple);
      window.removeEventListener("pointerdown", handleGlobalClick);
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-[9999] overflow-hidden">
      <AnimatePresence>
        {ripples.map((ripple) => (
          <React.Fragment key={ripple.id}>
            {/* Concentric Temple Bell Sound Wave Ring 1 */}
            <motion.div
              initial={{ width: 0, height: 0, opacity: 0.9 }}
              animate={{ width: 320, height: 320, opacity: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 1.2, ease: "easeOut" }}
              style={{
                left: ripple.x,
                top: ripple.y,
                translateX: "-50%",
                translateY: "-50%",
              }}
              className="absolute rounded-full border-2 border-amber-400/90 shadow-[0_0_20px_#f59e0b]"
            />
            {/* Concentric Temple Bell Sound Wave Ring 2 (Delayed) */}
            <motion.div
              initial={{ width: 0, height: 0, opacity: 0.7 }}
              animate={{ width: 480, height: 480, opacity: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 1.5, ease: "easeOut", delay: 0.15 }}
              style={{
                left: ripple.x,
                top: ripple.y,
                translateX: "-50%",
                translateY: "-50%",
              }}
              className="absolute rounded-full border border-amber-300/60 shadow-[0_0_30px_#fbbf24]"
            />
          </React.Fragment>
        ))}
      </AnimatePresence>
    </div>
  );
};

// Global helper to trigger visual haptic ripple
export const triggerHapticRipple = (e?: React.MouseEvent) => {
  let x = window.innerWidth / 2;
  let y = window.innerHeight / 2;

  if (e) {
    x = e.clientX;
    y = e.clientY;
  }

  window.dispatchEvent(
    new CustomEvent("temple-haptic-ripple", {
      detail: { x, y },
    })
  );
};
