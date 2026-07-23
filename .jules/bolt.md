## 2026-07-23 - Prevent continuous re-creation of requestAnimationFrame loops
**Learning:** Re-triggering `useEffect` with `requestAnimationFrame` on prop changes causes massive stuttering due to the destruction and recreation of loops and WebGL/Audio contexts.
**Action:** Use the "latest ref" pattern to cache frequently changing props (like `vitals` or `status`) in a `useRef`, and read from that ref inside the animation loop. Keep the `useEffect` dependencies for the animation loop empty (`[]`) so it only runs on mount/unmount.
