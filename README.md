# NexusAOS v2

A recovery-oriented rewrite of the Nexus project into a simple, explicit, genome-driven cognitive shell.

## What this repo is now

- A structured genome model that defines the agent configuration
- A visible runtime loop with observe / plan / act style stages
- A hard governance layer that fails closed
- A mutation path for offline evolution only
- A lightweight React dashboard for inspecting the system

## Run locally

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Development rules

- Keep generated artifacts separate from source
- Keep governance minimal and explicit
- Keep the genome structured, not free-form
- Keep runtime logic out of documentation
