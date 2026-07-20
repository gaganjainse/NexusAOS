# Implementation Plan: Nexus Web Data Collection & Human Viewing Layer

This plan outlines the creation of the **Oracle Data Scraper** for automated market/competitor intelligence and the **Nexus Human Viewing Layer**, a modern web-based dashboard to replace and enhance the current markdown-based artifact system.

## User Review Required

> [!IMPORTANT]
> **Architectural Transition:** We are moving from a static `.md` file system to a dynamic **JSON-backed Web Dashboard**. The markdown files will remain as "Cold Storage" (Golden Master), while the Web Dashboard will serve as the "Hot" Human Interface.
> **Technological Choice:** I propose using **React (Vite)** for the frontend and **Python (FastAPI/MCP)** for the data collection backend.

## Open Questions

- **Specific Data Sources:** Besides general web scraping, are there specific competitor sites or market databases you want the Oracle to target first?
- **Auth Requirements:** Should the Human Viewing Layer have a login system, or remains local-only (within the OS environment)?

---

## Proposed Changes

### [Component] Oracle Data Scraper (Backend)
Creation of the automated intelligence gathering module.

#### [NEW] [oracle_scraper.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/oracle_scraper.py)
A Python service using `BeautifulSoup` or `Playwright` to fetch market data, formatted for the `Market Intel Analyst` and `Oracle Interface Agent`.

#### [MODIFY] [oracle_interface_agent.md](file:///C:/Users/gagan/Downloads/nexus_corporate_os/archives/roles/hq/ncc/oracle_interface_agent.md)
Update role description to include management of the automated scraping pipelines.

---

### [Component] Nexus Human Viewing Layer (Frontend)
The "Human viewing layer" replacing `.md` with a reactive, better-suited UI.

#### [NEW] [nexus_dashboard/](file:///C:/Users/gagan/Downloads/nexus_corporate_os/core/ui/nexus_dashboard/)
A React-based dashboard project containing:
- **Navigation Bar:** Visual site map.
- **Role Viewer:** Dynamic card-based view of all 225+ roles (replacing `.md` lists).
- **Ledger Monitor:** Live feed of the Operational Ledger.
- **Intelligence Hub:** Visualization of the scraped data from the Oracle.

#### [MODIFY] [corporate_os_handbook.md](file:///C:/Users/gagan/Downloads/nexus_corporate_os/archives/core/foundation/corporate_os_handbook.md)
Update the handbook to point to the new Live Dashboard URL as the primary "Human Viewing Layer".

---

### [Component] Logic Synchronization
Ensuring the YAML/JSON core remains the source of truth.

#### [MODIFY] [nlg_renderer.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/nlg_renderer.py)
Update the renderer to also output the JSON schema required by the React Dashboard, ensuring zero-latency updates when logic changes.

---

## Verification Plan

### Automated Tests
- `pytest mcp_server/python/test_oracle_scraper.py`: Verify scraper fetches and parses correctly.
- `npm test` (within dashboard): Verify UI components render role data accurately.

### Manual Verification
- Launch the **Nexus Dashboard** and verify it displays the `Chief Executive Officer` role with more clarity and better visual hierarchy than the previous `.md` file.
- Trigger a "Scrape" directive and confirm the `Market Intel Analyst` registry is updated.
