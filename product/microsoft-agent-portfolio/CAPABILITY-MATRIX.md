# Capability Matrix — 15 Agents × Microsoft Services

Maps each agent to the Microsoft services it exercises, so a reviewer sees the **breadth of stack skills** the portfolio demonstrates.

**Legend:** `X` = service named in the agent's catalog stack line. For the agent-platform columns, an `X` means the agent's catalog entry names that platform as a viable runtime — several agents list *"Copilot Studio **or** Agent Framework"*, so both are marked. **Agent Framework** is marked for all 15 because it is the universal runtime every agent can be built on; the **Copilot Studio** and **Foundry Agent Service** columns show where a low-code or managed-template path also applies.

| # | Agent | Agent Framework | Copilot Studio | Foundry Agent Svc | AI Search (RAG) | Document Intelligence | Dynamics 365 | Azure ML | Synapse | Logic Apps | Cosmos DB |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Payables | X | X | - | X | X | X (Finance) | - | - | X | X |
| 2 | FP&A Planning | X | - | - | X | - | X (Finance) | - | X | X | X |
| 3 | A/R Collections | X | X | - | X | - | X (Finance+Sales) | X | - | X | X |
| 4 | Financial Close | X | - | - | X | - | X (Finance) | - | X | - | X |
| 5 | Procurement RFQ | X | X | - | X | X | X (SCM) | - | - | X | X |
| 6 | Inventory Optimization | X | - | - | X | - | X (SCM) | X | X | X | X |
| 7 | Supplier Risk & Compliance | X | X | - | X | - | X (SCM) | - | - | X | X |
| 8 | Sales RFP Response | X | - | - | X | X | X (Sales) | - | - | X | X |
| 9 | Quote-to-Cash | X | X | - | - | - | X (Sales+Finance+SCM) | - | - | X | X |
| 10 | Insurance Claims | X | X | X | X | X | X (Finance) | X | - | X | X |
| 11 | Prior Authorization | X | X | X | X | X | X (Health) | - | - | - | X |
| 12 | Contract Lifecycle | X | X | - | X | X | X | - | - | X | X |
| 13 | Talent Acquisition | X | X | - | X | X | X (Talent) | - | - | X | X |
| 14 | IT Incident Response | X | X | - | X | - | - | - | X | X | X |
| 15 | Predictive Maintenance | X | - | - | X | - | X (Field Service) | X | X | X | X |

## Coverage summary (counts derived directly from the cells above)
- **Agent Framework** — 15/15 (universal orchestration backbone)
- **Copilot Studio** — 10/15 (low-code alternate path: collections, RFQ, supplier risk, contracts, recruiting, claims, prior auth, incident, payables, Q2C)
- **Foundry Agent Service** — 2/15 (managed-template path: insurance claims, prior authorization)
- **Azure AI Search (RAG)** — 14/15 (templates, policies, competitive intel, precedents)
- **Document Intelligence** — 7/15 (invoices, RFQ/RFP responses, claims, contracts, resumes)
- **Dynamics 365** — 14/15 (universal enterprise ERP/CRM; all but IT Incident)
- **Azure ML** — 4/15 (propensity scoring, demand forecasting, fraud + failure prediction: agents 3, 6, 10, 15)
- **Azure Synapse** — 5/15 (analytics, time-series, data integration — incl. IT Incident anomaly detection)
- **Logic Apps** — 13/15 (triggers, notifications, orchestration)
- **Cosmos DB** — 15/15 (state + audit logs)

Ten core Azure services exercised across the portfolio → comprehensive, demonstrable Microsoft-stack mastery.

> **Note:** common plumbing services (Cosmos DB for state/audit, Logic Apps for triggers) are marked wherever the catalog names them; an unmarked cell means that agent's catalog entry did not call the service out, not that it is technically impossible.

## Orchestration pattern coverage
- **Single-agent + tool-use w/ escalation:** Payables, A/R Collections, Procurement RFQ, Supplier Risk, Contract Lifecycle, Talent Acquisition, Inventory.
- **Multi-agent handoff / graph workflow:** FP&A (per-department sub-agents + synthesis), Financial Close (parallel reconciliation + consolidation), Insurance Claims, Prior Authorization (parallel clinical + eligibility), Sales RFP, Quote-to-Cash, IT Incident, Predictive Maintenance.
- **RAG (Azure AI Search):** 14/15 — agentic retrieval over policies, templates, precedents.

## Governance & security talking points (apply to every agent)
1. **Entra Agent ID** — dedicated agent identity for secure API access.
2. **Azure RBAC** — role-based access control on agent operations.
3. **Agent Governance Toolkit** — OWASP Agentic Top 10 mitigations. ([repo](https://github.com/microsoft/agent-governance-toolkit))
4. **Content Safety** — prompt-injection and unsafe-output guardrails.
5. **Audit logging** — Cosmos DB trail of every decision + escalation.
6. **MCP** — Model Context Protocol tools for external system access.

> **Hiring signal:** baking governance in from day one is a differentiator — enterprises are risk-averse with agents, and toolkit fluency sets you apart.
