# NexusAOS v2

NexusAOS v2 is being rebuilt as a lean desktop shell:

- Rust for the core runtime, governance, registry, and persistence
- Tauri for the desktop wrapper
- Vanilla TypeScript for the UI layer

## Current shape

- structured genome model
- explicit runtime loop
- fail-closed governance
- offline mutation path for evolution
- plain TypeScript dashboard

## Run locally

```bash
npm install
npm run tauri:dev
```

## Build

```bash
npm run build
npm run tauri:build
```

## Development rules

- Keep generated artifacts separate from source
- Keep governance minimal and explicit
- Keep the genome structured, not free-form
- Keep runtime logic out of documentation
- Keep the desktop shell small unless the core architecture is changing
