# NexusAOS Agent Instructions

## Scope
Work only on the recovery-safe application layer unless the task explicitly asks for governance or documentation changes.

## Priority order
1. Keep the repository buildable.
2. Keep governance files minimal and explicit.
3. Prefer small, reviewable changes.
4. Preserve audit history and generated artifacts as separate from source.

## Working rules
- Do not edit `.artifacts/` or other generated outputs unless the task is specifically about recovery or archival cleanup.
- Do not reintroduce mythology, identity claims, or self-referential prose into source files.
- Keep `README.md` human-readable and technical.
- Keep runtime code separated from policy code.
- When a change touches the UI, make sure the app still starts from `src/main.tsx`.

## Commands
- Install deps: `npm install`
- Dev server: `npm run dev`
- Build: `npm run build`
- Type check: `npm run lint`

## Preferred implementation shape
- `src/core/` for domain logic
- `src/App.tsx` for composition only
- `src/index.css` for global styling
- `README.md` for human-facing overview

## Do not
- Rewrite rules files from runtime code
- Mix prompt text with source logic
- Delete generated archives without explicit instruction
- Introduce new architecture names without updating the canonical docs
