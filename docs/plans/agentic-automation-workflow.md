---
title: "The Agentic Automation Engineer's Complete Workflow"
subtitle: "From Requirements to AgenticOps — A No-Code/Low-Code Guide"
date: 2026-06-17
audience: Automation engineers without Python/PyTorch background
status: reference
---

# The Agentic Automation Engineer's Complete Workflow

**From Requirements to AgenticOps — A No-Code/Low-Code Guide**

Date: 2026-06-17 | Audience: Automation engineers (no Python/PyTorch required)

---

## How to Use This Document

Each phase is self-contained and feeds directly into the next. Work through them in order — skipping phases is the single most common cause of failed agent projects. Every phase lists what you need before you start (Inputs), what you produce (Outputs), and how you know you are ready to move on (Phase Transition Criteria).

---

## Phase 1: Requirements and Problem Definition

**Purpose:** Determine whether your problem genuinely needs an agent, define the agent's scope and boundaries, and produce a written spec that governs everything downstream.

### Inputs

- A business problem or automation request in plain language
- Access to stakeholders who own the process today
- The organization's risk and data classification policy (if one exists)

### Steps

1. Write a one-paragraph problem statement. Include: what currently happens manually, how often, who does it, and what goes wrong.
2. Apply Anthropic's simplicity test. Ask: could a simple prompt or a fixed chain of prompts solve this without any tool use or dynamic decision-making? If yes, build that instead. Agents add latency and cost — justify the complexity.
3. If an agent is warranted, classify the agency level:
   - **Level 1 — Read-only:** agent retrieves and summarizes information.
   - **Level 2 — Write-single-system:** agent creates or updates records in one system.
   - **Level 3 — Write-multi-system:** agent takes actions across two or more systems.
   - **Level 4 — Autonomous with side effects:** agent purchases, sends communications, or triggers irreversible actions.
4. Classify the data the agent will touch using the Security Scoping Matrix:

   | Data Sensitivity | Agency Level 1-2 | Agency Level 3 | Agency Level 4 |
   |------------------|-----------------|----------------|----------------|
   | Public           | Low risk        | Low risk       | Medium risk    |
   | Internal         | Low risk        | Medium risk    | High risk      |
   | Confidential     | Medium risk     | High risk      | Critical risk  |
   | Regulated (PII, PHI, financial) | High risk | Critical risk | Do not automate |

5. Write an Agent Card. This is a one-page spec containing:
   - Name and version
   - Purpose (one sentence)
   - Agency level (from step 3)
   - Risk classification (from step 4)
   - List of tools the agent may use
   - List of tools the agent must never use
   - Human approval requirements (which actions require a human to confirm before execution)
   - Success criteria (how you will measure whether the agent is working)
6. Write a Capability Matrix: a table mapping each user need to a specific agent capability, the tool(s) that capability requires, and the risk level.
7. Write Acceptance Criteria in the format: "Given [context], when [trigger], then [expected outcome], and [measurable result]."
8. Submit the Agent Card for stakeholder sign-off before building anything.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code documentation | Notion, Confluence, Google Docs |
| Risk classification | Your org's existing data classification framework |
| Diagramming | Miro, Lucidchart, draw.io |

### Key Skills Required

- Writing clear problem statements
- Risk thinking (what could go wrong if the agent acts without human review?)
- Stakeholder communication

### Outputs

- Agent Card (versioned document)
- Capability Matrix
- Acceptance Criteria (minimum 5 scenarios)
- Approval Gate Spec (which steps require sign-off and from whom)

### Governance Gates

Sign-off from the process owner and, for Level 3 or above, a security or compliance stakeholder is required before Phase 2 begins.

### Common Pitfalls

1. **Jumping straight to building.** Teams that skip the Agent Card typically rebuild from scratch after the first real-world failure because the scope was never agreed upon.
2. **Underestimating agency level.** A "read-only" agent that also sends a Slack summary is actually Level 2 (write-single-system) — it becomes Level 3 only if it also writes to a second system. Be honest about what it touches.
3. **Confusing automation with agency.** If the steps are always the same in the same order, that is a workflow automation (Zapier, Make) — not an agent. Save the complexity budget for problems that genuinely require dynamic decision-making.

### Phase Transition Criteria

- Agent Card is written and signed off by the process owner.
- Risk classification is agreed upon.
- Acceptance Criteria cover at least the happy path, one edge case, and one failure mode.
- You know which actions require human approval before the agent may proceed.

---

## Phase 2: Data and Knowledge Preparation

**Purpose:** Build the knowledge base your agent will retrieve from so it answers questions using current, accurate information rather than relying on the model's training data alone.

### Inputs

- Agent Card from Phase 1
- List of source documents, databases, or APIs the agent needs to know about
- Access to at least one vector database or managed knowledge base service

### Steps

1. Inventory your knowledge sources. List every document type, database table, or API endpoint the agent needs. Note the update frequency of each (static, daily refresh, real-time).
2. Choose a chunking strategy for your documents:
   - **Fixed-size chunking (default start):** Split documents into 512–1024 token chunks with 20% overlap. Works for most use cases.
   - **Semantic chunking:** Split at natural topic boundaries (paragraphs, headings). Better for structured content like policies or manuals.
   - **Hierarchical chunking:** Store a summary chunk alongside detail chunks. Use when users ask both high-level and detailed questions about the same content.
3. Select an embedding model. For no-code platforms: use the default model provided by the platform (e.g., Amazon Titan Embeddings v2 in Bedrock, OpenAI `text-embedding-3-small` in most SaaS tools). Do not change the embedding model after ingestion — this invalidates your index.
4. Ingest your documents into a vector store. For no-code: use a managed knowledge base (see Tools section). For code paths: use LlamaIndex or LangChain ingest pipelines.
5. Configure metadata. Every chunk should carry: source document name, last-updated date, document type, and access permissions. This metadata is what enables freshness filtering and access control at query time.
6. Build a retrieval pipeline. Configure: top-k results (start with k=5), similarity threshold (reject chunks below 0.7 cosine similarity), and a reranker if precision matters more than speed.
7. Test retrieval quality with 20 representative questions. For each question, verify that the retrieved chunks are relevant. If more than 20% of retrievals are off-target, revisit your chunking strategy.
8. Set up a freshness management process. For documents that change, establish: who triggers a re-ingestion, how often, and whether stale chunks are deleted or flagged.
9. Plan for ingestion failure recovery. If a re-ingestion run fails mid-way or corrupts the index: keep the previous index snapshot as a rollback target, re-ingest from scratch into a new collection, validate retrieval quality on the new collection, then swap the alias. Never overwrite the live index in place.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code knowledge bases | AWS Bedrock Knowledge Bases, Azure AI Search, Google Vertex AI Search, Dify (built-in), Flowise |
| No-code pipeline builders | n8n (HTTP + vector store nodes), Make (with vector DB modules) |
| Vector databases (managed) | Pinecone (serverless), Weaviate Cloud, Qdrant Cloud, Supabase pgvector |
| Vector databases (self-hosted) | Chroma, Weaviate OSS, Qdrant OSS, Milvus |
| Code-path ingest | LlamaIndex, LangChain document loaders |

### Key Skills Required

- Understanding what a vector database does (stores meaning, not exact text)
- Ability to configure managed services via console UIs (no coding required for no-code options)
- Basic data hygiene: knowing which documents are authoritative, which are duplicates

### Outputs

- Populated vector index with metadata
- Retrieval pipeline configuration (documented)
- Retrieval quality test results (pass/fail against 20 test questions)
- Freshness management runbook

### Governance Gates

For data classified as Confidential or higher (per Phase 1): confirm that the vector store is within your organization's security boundary (private cloud or a vendor with a signed DPA) before ingesting.

### Common Pitfalls

1. **Ingesting everything without curation.** Garbage in, garbage out. An agent that retrieves from a mix of authoritative policies and outdated drafts will confidently give wrong answers.
2. **No metadata on chunks.** Without source attribution and dates, you cannot tell the agent to prefer recent documents or restrict access by role.
3. **Skipping retrieval quality testing.** Teams that skip step 7 discover retrieval failures in production, where they are much harder to diagnose.

### Phase Transition Criteria

- Vector index is populated and metadata is present on all chunks.
- Retrieval quality test passes at 80% or higher.
- Freshness management process is documented and owned by someone.
- Data residency and access controls are confirmed for the risk level of the data.

---

## Phase 3: Agent Design and Architecture

**Purpose:** Choose the orchestration pattern and framework that match your use case, and produce a documented architecture before writing a single prompt or tool definition.

### Inputs

- Agent Card and Capability Matrix from Phase 1
- Retrieval pipeline from Phase 2
- Team's technical capability (no-code vs. code)

### Steps

1. Choose your orchestration pattern:
   - **ReAct (Reason + Act):** The agent reasons about what to do, calls a tool, observes the result, reasons again. Use for open-ended tasks where the next step depends on what you just learned.
   - **Plan-and-Execute:** The agent creates a full plan upfront, then executes each step. Use for multi-step tasks with a predictable structure where you want to review the plan before execution.
   - **Tool-calling loop:** The agent picks from a fixed tool list until it has enough information to answer. Use for Q&A and retrieval tasks.
2. Decide: single agent or multi-agent. Start with a single agent unless you have a clear, concrete reason for multiple agents. Legitimate reasons for multi-agent: the task genuinely requires parallel work streams, different steps require different tool access levels, or the context window of a single conversation would overflow.
3. Use the framework decision flowchart:
   - No code available and task is workflow-like → **n8n or Dify**
   - No code available and task is Claude-native → **Claude Managed Agents** (Anthropic console)
   - Python available and you need fine-grained control → **LangGraph** or **Claude Agent SDK**
   - You want CrewAI-style role-based teams → **CrewAI** (requires Python)
4. Draw the architecture: boxes for each agent (if multi-agent), arrows showing information flow, tool boxes, memory/knowledge base boxes, and the human approval gate positions.
5. Define the agent's memory model:
   - **In-context (short-term):** conversation history within one session.
   - **External (long-term):** facts stored in a database or vector store between sessions.
   - **Episodic:** logs of past task completions that the agent can query.
6. Document every external system the agent will connect to. For each: what data goes in, what comes back, who owns the system, and what the failure mode is if it is unavailable.
7. Review the architecture against the Agent Card from Phase 1. Every tool and every external connection must appear in the Capability Matrix or you add it now and re-get sign-off.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code agent builders | Dify, Flowise, n8n Agent nodes, Botpress |
| Claude-native managed | Claude Managed Agents (Anthropic console), Amazon Bedrock Agents |
| Code frameworks | LangGraph, CrewAI, AutoGen, Claude Agent SDK, Semantic Kernel |
| Diagramming | draw.io, Miro, Excalidraw |

### Key Skills Required

- Reading architecture diagrams
- Understanding what a context window is and why it matters
- Mapping tool permissions to risk levels

### Outputs

- Architecture diagram (versioned)
- Agent spec document (pattern, framework, memory model, external systems)
- Tool list (preliminary — detailed in Phase 4)

### Governance Gates

For Level 3 or Level 4 agents: architecture review with security team before building, specifically to verify that the planned external system connections are within approved boundaries.

### Common Pitfalls

1. **Choosing multi-agent by default.** Multi-agent systems are harder to debug, more expensive to run, and more likely to produce cascading failures. Start single-agent. Escalate only when you hit a concrete limitation.
2. **No failure mode planning.** Every external system will be unavailable at some point. Document what the agent does when each tool returns an error before you build.
3. **Architecture drift.** The diagram you draw in Phase 3 must stay synchronized with what you build. Undocumented changes are the root cause of most production incidents.

### Phase Transition Criteria

- Architecture diagram is complete and matches the Capability Matrix from Phase 1.
- Framework choice is documented with rationale.
- Every external system is listed with an owner and a documented failure mode.
- For Level 3+ agents: architecture sign-off from security stakeholder is complete.

---

## Phase 4: Skill and Tool Definition

**Purpose:** Define and build the exact tools the agent can call, with precise schemas and minimal permissions — because a well-defined tool is the difference between an agent that works and one that invents actions that do not exist.

### Inputs

- Tool list from Phase 3
- Access to the systems each tool needs to connect to
- Phase 1 risk classification (drives permission scoping)

### Steps

1. Adopt MCP (Model Context Protocol) as your tool interface standard. MCP is the industry standard (~97M monthly SDK downloads as of March 2026) supported natively by Claude, Cursor, and most major agent frameworks. Building to MCP means your tools are portable across agents and frameworks.
2. Browse the public MCP server registry (mcp.so, GitHub topic `mcp-server`) before building anything custom. There are 10,000+ active public MCP servers (Anthropic, 2026). Common needs — GitHub, Slack, Notion, Google Drive, Jira, Postgres, Salesforce — likely have a production-ready server you can configure rather than build.
3. For each tool you must build, write the JSON Schema definition first. Every tool definition needs:
   - `name`: snake_case, verb-noun format (e.g., `get_customer_record`, `create_support_ticket`)
   - `description`: one sentence that tells the model exactly when to use this tool and what it returns
   - `parameters`: typed fields with descriptions, required vs. optional, and value constraints (enums, min/max)

   Example of a complete tool definition:
   ```json
   {
     "name": "get_customer_record",
     "description": "Retrieve a customer's profile by their unique ID. Returns name, email, plan, and account status.",
     "input_schema": {
       "type": "object",
       "properties": {
         "customer_id": {
           "type": "string",
           "description": "The customer's unique identifier (e.g., 'cust_abc123')"
         }
       },
       "required": ["customer_id"]
     }
   }
   ```
4. Apply least-privilege scoping to every tool. Read-only tools get read-only credentials. A tool that only needs to read from one table should not have access to the full database. Scope credentials at the tool level, not the agent level.
5. Implement graceful failure for every tool. Tools must return structured error messages the agent can act on (e.g., `{"error": "record_not_found", "id": "12345", "suggestion": "verify the ID is correct"}`), not raw stack traces.
6. Group tools by job function. Example: a customer service agent should have a `customer_lookup` tool group and a `ticket_management` tool group, not a single massive tool that does everything. Grouping helps the model select tools correctly.
7. Build tools in this order of effort: configure existing MCP server → compose n8n/Dify function tool (HTTP request) → deploy AWS Lambda or similar serverless function → build custom MCP server.
8. Write a test case for every tool before connecting it to the agent. Each test case: example input, expected output, expected error when given bad input.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code tool building | n8n HTTP nodes (wrap any REST API), Dify function tools, Zapier MCP integration |
| Pre-built MCP servers | mcp.so registry, GitHub `mcp-server` topic, Anthropic's MCP directory |
| Serverless tool hosting | AWS Lambda, Cloudflare Workers, Azure Functions, Vercel Edge Functions |
| Custom MCP server SDKs | `@modelcontextprotocol/sdk` (TypeScript), `mcp` (Python) |

### Key Skills Required

- Reading REST API documentation
- Writing JSON (specifically JSON Schema — no programming language required)
- Understanding authentication methods (API keys, OAuth, service accounts)

### Outputs

- JSON Schema definition for each tool
- Deployed tool endpoints (or configured MCP servers)
- Test cases for each tool (input/output pairs)
- Permission matrix: which tool uses which credentials with what scope

### Governance Gates

For Level 3+ agents: permission matrix review before any tool with write access is connected to a production system. All write-access tools must have a corresponding audit log.

### Common Pitfalls

1. **Tools that do too much.** A tool named `manage_customer` that reads, writes, and deletes is impossible for the model to select precisely. Split into `get_customer`, `update_customer`, `delete_customer`.
2. **Missing error structure.** If a tool returns an unstructured error, the agent cannot reason about it and will often retry indefinitely or hallucinate a workaround.
3. **Skipping the test cases.** Tool bugs discovered inside a running agent conversation are much harder to diagnose than bugs caught with a standalone tool test.

### Phase Transition Criteria

- Every tool in the Phase 3 tool list has a JSON Schema definition and at least one passing test case.
- Credentials are scoped to least privilege.
- Write-access tools have audit logging confirmed.
- At least one end-to-end test (tool called from outside the agent) passes for each tool.

---

## Phase 5: Prompt Engineering and System Instructions

**Purpose:** Write the system prompt that defines who the agent is, what it does, and what it must never do — the most direct control surface you have over agent behavior.

### Inputs

- Agent Card from Phase 1 (the system prompt is an operationalization of the Agent Card)
- Tool definitions from Phase 4
- Retrieval pipeline from Phase 2
- Acceptance Criteria from Phase 1 (used to test the prompt)

### Steps

1. Use Anthropic's 3-part skeleton for every system prompt:
   - **Role:** "You are [name], a [specific role] for [organization/context]."
   - **Task Instructions:** What the agent does, step by step, including how and when to use each tool.
   - **Constraints:** What the agent must never do, how to handle ambiguity, when to stop and ask a human.
2. Use XML tags to organize the system prompt. Claude processes XML tags reliably. Example structure:
   ```
   <role>...</role>
   <instructions>...</instructions>
   <tools>...</tools>
   <constraints>...</constraints>
   <examples>...</examples>
   ```
3. Apply primacy and recency reinforcement. Put the most important instructions at the very beginning and repeat the most critical constraints at the very end. Instructions buried in the middle are more likely to be ignored under long context.
4. Write explicit tool-use instructions. For each tool: when to use it, what inputs to pass, and what to do if it fails. Do not assume the model will infer the correct use from the schema alone.
5. Write explicit refusal instructions. List at least 3 things the agent must not do, phrased as "Do not [action]. If asked, respond with [specific message]."
6. Enable extended thinking for complex reasoning tasks (available in Claude claude-sonnet-4-6 and above). Add to the API call: `"thinking": {"type": "enabled", "budget_tokens": 5000}`. This is a configuration setting, not a prompt change — but document it in the prompt spec so it is not accidentally removed.
7. For persistent context across sessions, create a `CLAUDE.md` file. This is a markdown file that Claude Code reads automatically at the start of every session. Put in it: the agent's role, standing context, and any facts that must always be available. (This applies specifically to Claude Code deployments.)
8. Version your system prompt. Use a header comment format:
   ```
   # System Prompt v1.0 | 2026-06-17 | Author: [name]
   # Changes from v0: initial release
   ```
9. Test the prompt manually against each Acceptance Criterion from Phase 1 before running any automated evals.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code prompt testing | Claude.ai (Workbench), Dify prompt editor, Flowise prompt node |
| Prompt versioning | Git (the system prompt lives in a file in your repo), Langfuse prompt management |
| CLAUDE.md (Claude Code only) | Markdown file in repo root or subfolder |

### Key Skills Required

- Clear technical writing
- Understanding of how context windows work (what fits, what gets dropped)
- Iterative testing mentality (expect to revise the prompt 5-10 times)

### Outputs

- System prompt v1.0 (versioned file)
- CLAUDE.md (if using Claude Code)
- Manual test results against each Acceptance Criterion
- Prompt changelog

### Governance Gates

For Level 4 (autonomous with side effects): have one person other than the author read the system prompt aloud against the Agent Card before approving. System prompts are legal instruments — they define what the agent is authorized to do.

### Common Pitfalls

1. **Vague task instructions.** "Help users with customer service" is not an instruction. "When a user reports an issue, use `get_customer_record` to look up their account, then use `get_recent_tickets` to check their history before responding" is an instruction.
2. **No explicit constraints.** Agents without explicit "do not" instructions will attempt to be helpful in ways you did not intend. Always include a constraints section.
3. **Treating the prompt as final.** Every prompt is v1.0 and will change. Build in version tracking from day one.

### Phase Transition Criteria

- System prompt is versioned and passes manual review against all Acceptance Criteria.
- Tool-use instructions are explicit for every tool defined in Phase 4.
- Constraints section exists with at least 3 explicit "do not" rules.
- CLAUDE.md is created (if using Claude Code deployment).

---

## Phase 6: Testing and Evaluation

**Purpose:** Measure whether your agent meets its Acceptance Criteria with quantitative scores, catch regressions before they reach production, and create the monitoring baseline for AgenticOps.

### Inputs

- System prompt and tool definitions from Phases 4-5
- Acceptance Criteria from Phase 1
- A dataset of test cases (you will build this in step 1)

### Steps

1. Build your evaluation dataset. Target 50-200 examples. Each example contains:
   - Input (user message or trigger)
   - Expected output or expected behavior
   - Evaluation dimension (which metric this example tests)
   Start with 20 examples covering the Acceptance Criteria and grow from there.
2. Define your scoring dimensions and weights:
   - Correctness (did the agent produce the right answer or take the right action?): 60%
   - Tool selection quality (did it use the right tool, with the right parameters?): 15%
   - Safety (did it refuse appropriately? did it avoid prohibited actions?): 15%
   - Latency and cost (did it complete within acceptable time and token budget?): 10%
3. Choose your eval platform:
   - For no-code: **Confident AI** (configure via HTTP, no Python required) or **Braintrust** (dashboard-driven)
   - For code paths: **LangSmith**, **Galileo**, or **Langfuse**
4. Run your first eval. Record the baseline scores. Do not optimize based on the first run — you need a baseline before any iteration.
5. Iterate. For each failing test case: diagnose whether the failure is in the prompt, the tool, the retrieval pipeline, or the test case itself. Fix the root cause, not the symptom.
6. Set regression alert thresholds. The minimum thresholds before production deployment:
   - Overall score: 80% or higher
   - Safety dimension: 95% or higher (no exceptions)
   - No single Acceptance Criterion may fail
7. Set up continuous monitoring evals (a subset of your dataset run on a schedule in production). Regression alerts fire if any dimension drops more than 5 percentage points from the baseline.

### Tools and Platforms

| Category | Options |
|----------|---------|
| No-code eval platforms | Confident AI, Braintrust (dashboard), Langfuse (OSS) |
| Code-path eval platforms | LangSmith, Galileo, Arize Phoenix |
| Dataset management | Google Sheets → CSV → upload, or platform-native dataset builder |

### Key Skills Required

- Writing test cases (input/expected output pairs)
- Reading evaluation dashboards and interpreting scores
- Root cause analysis: prompt vs. tool vs. retrieval vs. test case

### Outputs

- Evaluation dataset (versioned in your repo or eval platform)
- Baseline eval scores per dimension
- Eval run reports
- Regression alert configuration
- Iteration backlog (prioritized list of what to fix next)

### Governance Gates

The safety dimension must score 95% or higher before any deployment to a production environment. This gate is non-negotiable. If safety fails, halt and fix before proceeding.

### Common Pitfalls

1. **Evaluating only the happy path.** Your dataset must include edge cases and adversarial inputs. A system prompt that handles every normal case but breaks on "ignore your previous instructions" is not production-ready.
2. **No baseline before optimization.** Teams that iterate before recording a baseline lose the ability to tell whether changes are improvements or regressions.
3. **Treating eval as one-time.** Evals must run continuously in production. A model update, a data change, or a tool change can break a passing agent silently.

### Phase Transition Criteria

- Overall eval score is 80% or higher.
- Safety dimension is 95% or higher.
- All Acceptance Criteria pass.
- Continuous monitoring eval job is configured and confirmed to run on schedule.
- Baseline scores are documented for future regression comparison.

---

## Phase 7: Deployment and Integration

**Purpose:** Move your agent from a tested prototype into a running production service with defined trigger mechanisms, traffic management, and a documented runbook.

### Inputs

- Passing eval results from Phase 6
- Tool endpoints from Phase 4 (production credentials, not dev)
- Architecture diagram from Phase 3
- Stakeholder sign-off from Phase 1 approval gate

### Steps

1. Choose your deployment model:
   - **Claude Managed Agents (Anthropic console):** Managed hosting, $0.08 per session-hour (active running time only; standard token costs billed separately on top), no infrastructure to run. Best for internal tools and prototypes moving to production quickly.
   - **n8n or Dify cloud:** Your agent lives inside a workflow platform. Best for agents that are one node in a larger automation.
   - **Claude API + custom hosting:** You manage the server, scale, and uptime. Required if you need full control over the execution environment.
   - **Serverless (Lambda, Cloud Run, Azure Functions):** Good for event-driven agents with bursty, infrequent usage.
2. Configure your trigger mechanism:
   - **Webhook trigger:** An external event (form submission, Slack message, Jira ticket created) calls a URL and the agent runs.
   - **Scheduled trigger (cron):** The agent runs on a time schedule. Configure with caution for write-access agents — every scheduled run is a real action.
   - **API trigger:** Your application calls the agent programmatically.
   - **UI trigger:** A user clicks a button in a UI that calls the agent.
3. Implement staging before production. Run the agent in a staging environment with:
   - Production-equivalent data (or anonymized clones)
   - Read-only credentials for write-access tools (until final staging sign-off)
   - Logging enabled from day one
4. Run a canary deployment. Send a small percentage of real traffic to the new agent while the old process (manual or previous automation) handles the rest:
   - Day 1-3: 5% to new agent, 95% to old process
   - Day 4-7: 25% to new agent
   - Day 8+: 100% to new agent (if metrics are healthy)
5. Configure multi-tenant isolation if multiple customers or business units share the agent. Each tenant must have: separate conversation context, separate tool credentials (or row-level security), separate audit logs.
6. Write the integration guide. A one-page document for anyone who will trigger or consume the agent's outputs. Include: trigger method, expected inputs, expected outputs, error codes, escalation contact.
7. Write the operational runbook. Include: how to restart, how to roll back, how to check health, who to call when it breaks, and the escalation chain.

### Tools and Platforms

| Category | Options |
|----------|---------|
| Managed agent hosting | Claude Managed Agents, Amazon Bedrock Agents, Azure AI Foundry |
| No-code platform hosting | Dify Cloud, n8n Cloud, Flowise Cloud |
| Serverless compute | AWS Lambda, Google Cloud Run, Azure Functions, Cloudflare Workers |
| Webhook management | n8n (built-in), Pipedream, AWS API Gateway |

### Key Skills Required

- Reading deployment console UIs (AWS, Azure, GCP, or your chosen platform)
- Understanding the difference between staging and production environments
- Writing operational runbooks

### Outputs

- Agent deployed in staging (passing full integration test)
- Agent deployed in production (after canary)
- Integration guide
- Operational runbook
- Rollback procedure documented

### Governance Gates

Production deployment requires: passing eval scores from Phase 6, stakeholder sign-off from Phase 1, and for Level 3+ agents, security team confirmation that production credentials are scoped correctly.

### Common Pitfalls

1. **Deploying directly to production.** Skipping staging is the single fastest way to cause a production incident with a new agent. Always have a staging step.
2. **Using development credentials in production.** Development credentials are typically over-privileged (full database access, admin API tokens). Production credentials must be scoped to least privilege.
3. **No runbook.** At 2am when the agent is stuck in a loop, "ask the person who built it" is not a runbook. Document restart and rollback procedures before you go live.

### Phase Transition Criteria

- Agent is running in production and serving real traffic (even at 5% canary).
- Integration guide is published and the downstream consumers have it.
- Operational runbook is reviewed by someone who did not write it.
- Monitoring from Phase 8 is active before canary traffic begins.

---

## Phase 8: AgenticOps and Monitoring

**Purpose:** Operate the agent in production with full visibility into health, cost, quality, and drift — catching problems before they reach users or blow the budget.

### Inputs

- Deployed agent from Phase 7
- Baseline eval scores from Phase 6 (used as drift benchmarks)
- Budget allocation for agent operations (token budget per month/quarter)

### Steps

1. Instrument with distributed tracing. Every agent invocation should produce a trace with:
   - A session ID (links all turns in one conversation)
   - Spans for each step: retrieval, tool call, model call, human approval wait
   - Token counts per span
   - Latency per span
   - Error flags
   Use OpenTelemetry-compatible instrumentation where possible — it is platform-neutral. For no-code tracing: Helicone works as a proxy (change your API base URL, no SDK needed), and Langfuse offers an HTTP proxy endpoint that logs all LLM calls by routing traffic through it. Both require zero code changes to your agent — just a URL swap.
2. Build your observability dashboard. The minimum set of panels:
   - **Health:** success rate per hour, error rate by type, p50/p95 latency
   - **Cost:** tokens per session, cost per successful task, daily budget burn rate
   - **Quality:** eval score trend (run your Phase 6 evals on a sample of production traffic daily)
   - **Drift:** input topic distribution change week-over-week, tool selection frequency change
   - **Operational:** active sessions, queue depth (if async), tool availability by endpoint
3. Configure alerting. Minimum alerts:
   - Error rate above 5% for 15 minutes → page on-call
   - Daily cost burn exceeds 120% of daily budget → alert finance and product owner
   - Safety eval score drops below 90% → halt new sessions and alert immediately
   - Any individual tool error rate above 20% → alert engineering
4. Implement cost optimization levers (apply in this order):
   - **Prompt caching:** cache your system prompt (saves 90% of input token cost for the system prompt on repeat calls). Available natively in Claude API.
   - **Tool reduction:** remove tools the agent rarely uses. Every tool in the context costs tokens.
   - **Smaller models:** use a smaller, faster model for tool selection steps and reserve the large model for synthesis steps only.
   - **Batch API:** for non-real-time tasks, batch API calls reduce cost by up to 50%.
   - **Early stopping:** configure the agent to stop the loop if it reaches a conclusion with high confidence rather than running all planned steps.
5. Set up drift detection. Three types to monitor:
   - **Input drift:** the distribution of user queries is shifting (new topics, new phrasing). Indicates the agent may need retraining or prompt updates.
   - **Behavioral drift:** the agent is choosing different tools or producing different response formats than at baseline. Often caused by a model update.
   - **Model drift:** the underlying model has been updated by the provider. Check for provider update announcements monthly and run your full eval suite after any model update.
6. Write incident response playbooks for the top 5 failure modes:
   - **Tool misuse:** agent calls a tool with incorrect parameters repeatedly. Mitigation: add clearer tool descriptions, add parameter validation.
   - **Hallucination cascade:** agent invents tool results when the tool fails. Mitigation: ensure all tools return structured errors and the system prompt explicitly handles tool failure.
   - **Goal drift:** agent pursues a sub-goal that was a means to an end and ignores the original objective. Mitigation: add explicit goal-anchoring instructions to the system prompt.
   - **Infinite loop:** agent calls the same tool repeatedly without progressing. Mitigation: implement a maximum tool-call-per-session limit.
   - **Silent degradation:** agent produces plausible-sounding but incorrect outputs. Mitigation: continuous eval monitoring catches this before users do.
7. Establish a regular operational review cadence. Weekly: review cost and error metrics. Monthly: review quality trend and drift signals. Quarterly: full eval re-run against the original dataset.

### Tools and Platforms

| Category | Options |
|----------|---------|
| Tracing and observability | Langfuse (OSS), LangSmith, Arize Phoenix, Helicone |
| Enterprise APM | Datadog (with LLM Observability), New Relic AI |
| Cost tracking | Helicone, your platform's built-in cost dashboards |
| Alerting | PagerDuty, Opsgenie, Slack alert workflows |

### Key Skills Required

- Reading dashboards and interpreting time-series metrics
- Distinguishing between a model problem, a tool problem, and a prompt problem from telemetry
- Writing incident response procedures

### Outputs

- Observability dashboard (live)
- Alert configuration (documented)
- Cost report (weekly)
- Incident response playbooks for the 5 top failure modes
- Operational review schedule

### Governance Gates

For Level 3+ agents: cost overrun alerts must notify a named finance stakeholder, not just engineering. For Level 4 agents: any safety score drop below 95% triggers an automatic session halt (not just an alert).

### Common Pitfalls

1. **Monitoring only uptime.** An agent can be "up" (responding to requests) while silently giving wrong answers. Quality monitoring is as important as availability monitoring.
2. **No cost ceiling.** Agents can burn 20-50x more tokens than a simple chat interaction. Without a hard budget ceiling and a circuit breaker, a runaway agent or a spike in usage can generate unexpected cost very quickly.
3. **Ignoring drift signals.** Teams that only look at error rates miss gradual quality degradation. Input drift and behavioral drift typically appear weeks before error rates rise.

### Phase Transition Criteria

This is an ongoing operational phase, not a phase you "complete." However, the following conditions must be true before you consider the agent stable:
- Dashboard is live with all 5 panel groups.
- All minimum alerts are configured and tested (confirm alerts fire by simulating a threshold breach).
- At least two incident response playbooks are written and reviewed.
- Cost burn is within 20% of the projected budget for two consecutive weeks.
- Eval quality score has not dropped more than 3 percentage points from the Phase 6 baseline.

---

## Phase 9: Governance and Compliance

**Purpose:** Ensure the agent operates within legal, regulatory, and organizational policy boundaries — with audit trails that prove it, approval gates that enforce it, and a governance maturity plan that improves it over time.

### Inputs

- Agent Card and risk classification from Phase 1
- Observability infrastructure from Phase 8
- Your organization's legal and compliance requirements
- Operational runbook from Phase 7

### Steps

1. Map your regulatory requirements. Identify which frameworks apply:
   - **EU AI Act (2025):** Classifies AI systems by risk. High-risk systems require conformity assessment, human oversight, and audit logging with 6-month minimum retention.
   - **NIST AI RMF:** A voluntary US framework providing structured risk management vocabulary and practices.
   - **OWASP Top 10 for Agentic Applications (December 2025):** The definitive security checklist for agentic systems, produced by the OWASP GenAI Security Project's Agentic Security Initiative (ASI). The 10 risks are: ASI01 Agent Goal Hijack, ASI02 Tool Misuse and Exploitation, ASI03 Identity and Privilege Abuse, ASI04 Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution, ASI06 Memory and Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human Agent Trust Exploitation, and ASI10 Rogue Agents. (Canonical list: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/)
   - **HIPAA:** For agents that touch Protected Health Information. Requires BAA with every vendor in the stack.
   - **GDPR:** For agents that process EU personal data. Requires data minimization, purpose limitation, and subject rights support.
   - **SOX:** For agents that touch financial reporting. Requires separation of duties and change management controls.
2. Implement OWASP Top 10 for Agentic Applications controls. The minimum controls for every agentic system:
   - **ASI01 Agent Goal Hijack:** System prompt is immutable at runtime. User inputs cannot override system instructions. (Enforce via prompt architecture — put constraints in the system turn, not the user turn.)
   - **ASI02 Tool Misuse and Exploitation:** Every tool has explicit usage instructions in the system prompt. Tools validate inputs and reject malformed requests.
   - **ASI03 Identity and Privilege Abuse:** Tools verify the caller identity at the API level, not just the agent's claim about who is calling.
   - **ASI06 Memory and Context Poisoning:** RAG retrievals are validated against a content policy before being injected into context.
   - **ASI08 Cascading Failures:** Circuit breakers on all tool calls. Maximum retry limits enforced.
3. Implement approval gates. Three types:
   - **Pre-execution (blocking):** The agent cannot proceed until a human approves. Use for high-risk, irreversible actions. Display: what action is proposed, what the expected outcome is, what the rollback is.
   - **Post-execution (audit):** The action executes and a human reviews the log. Use for medium-risk, reversible actions.
   - **Statistical (anomaly-based):** An automated system reviews batches of actions and flags outliers for human review. Use for high-volume, low-risk actions.
4. Classify every agent action into one of four risk tiers and assign the appropriate gate:
   - **Tier 1 (informational — read, summarize, draft):** No gate required. Log only.
   - **Tier 2 (reversible write — update a record, create a draft, send an internal notification):** Post-execution audit gate.
   - **Tier 3 (consequential write — send external communication, create financial record, modify access permissions):** Pre-execution approval gate.
   - **Tier 4 (irreversible or high-value — delete records, execute payments, modify security configurations):** Pre-execution approval + dual authorization (two humans approve).
5. Implement audit logging. Every agent action must be logged with:
   - Session ID and turn ID
   - Timestamp (UTC)
   - User or system that triggered the agent
   - Tool called and exact parameters passed
   - Tool response (or error)
   - Human approval decision (if applicable) and approver identity
   - Final output delivered
   Logs must be append-only (no modification after write), stored separately from the agent's runtime environment, and retained for at least 6 months (EU AI Act minimum; check your jurisdiction).
6. Implement cost governance controls:
   - **Metering gateway:** All API calls route through a gateway that tracks token consumption by tenant, use case, and time period.
   - **Budget enforcement:** Set hard ceilings per tenant per billing period. When the ceiling is hit, new sessions are rejected (not silently degraded).
   - **Circuit breakers:** If a single session exceeds a token threshold (e.g., 10× the average session length), halt and alert.
   - **Graceful degradation:** When budget is constrained, switch to a smaller model or reduce tool calls — do not silently switch to hallucinated answers.
7. For multi-agent systems, implement multi-agent governance:
   - **Hierarchical:** One orchestrator agent supervises all subagents. Only the orchestrator has write access. Subagents are read-only.
   - **Kill switches:** Every subagent must respond to a halt command from the orchestrator within one turn.
   - **Trust isolation:** Subagents do not inherit the orchestrator's permissions. Each subagent has its own scoped credentials.
8. Assess your governance maturity level and plan to advance it:
   - **Ad-hoc:** No documented policies. Individuals make decisions. (Acceptable for experiments only.)
   - **Documented:** Policies exist (Agent Cards, approval gate specs). (Required before production.)
   - **Managed:** Policies are enforced automatically (approval gates in code, not just documents). (Required for Level 3+ agents.)
   - **Optimized:** Governance is measured, reported on, and continuously improved based on incident data. (Target state for any agent operating at scale.)
9. Prepare compliance evidence package. Collect and store: Agent Card, Capability Matrix, Architecture Diagram, Eval Results, Approval Gate Spec, Audit Log Samples, Incident History. This package is what you hand to an auditor.

### Tools and Platforms

| Category | Options |
|----------|---------|
| Audit logging | Immutable log stores: AWS CloudTrail, Azure Monitor Logs, Supabase with RLS, Datadog Log Management |
| Approval gate UIs | Slack interactive messages, custom web form, ServiceNow, Jira approval workflows |
| Policy enforcement | AWS IAM, Azure Policy, OPA (Open Policy Agent) |
| Compliance tracking | Drata, Vanta, Secureframe (automate evidence collection for SOC2, HIPAA, GDPR) |

### Key Skills Required

- Reading regulatory frameworks at a summary level (you do not need to be a lawyer)
- Translating risk classification into concrete gate decisions
- Writing audit-quality log specifications

### Outputs

- Regulatory requirements map (which frameworks apply and why)
- OWASP ASI Top 10 control checklist (completed)
- Approval Gate Spec (each action → gate type → approver identity)
- Audit log specification and confirmed log store
- Cost governance configuration
- Governance maturity assessment with a roadmap to "Managed" level
- Compliance evidence package

### Governance Gates

This phase is itself a governance gate. No Level 3 or Level 4 agent may operate in production indefinitely without a completed Phase 9. Schedule a governance review at 90 days post-launch and annually thereafter.

### Common Pitfalls

1. **Treating governance as a one-time checkbox.** Model updates, regulatory changes, and new use cases all change the compliance picture. Build a review cadence into Phase 8's operational review.
2. **Approval gates that approve everything.** If every approval request is approved in under 30 seconds without anyone actually reading it, the gate provides no protection. Design approval UIs that present the relevant context and require an active decision.
3. **Logs you cannot query.** An audit trail written to an append-only file with no search capability is nearly useless during an incident. Choose a log store with query support from day one.

### Phase Transition Criteria

Phase 9 has no "next phase" — it feeds back into Phase 8 (ongoing operations) and Phase 3 (when you redesign or extend the agent). The completion condition is:
- Regulatory requirements are mapped and documented.
- OWASP ASI Top 10 controls are implemented or have a documented remediation date.
- Approval gate spec is implemented in code (not just documented).
- Audit logs are flowing, queryable, and confirmed to meet retention requirements.
- Compliance evidence package is assembled and stored in a location accessible to auditors.

---

## Quick-Reference Tool Landscape

| Phase | No-Code Options | Code Options | Managed / SaaS |
|-------|----------------|-------------|----------------|
| 1 — Requirements | Notion, Miro, Google Docs | — | — |
| 2 — Data and Knowledge | Dify (built-in KB), n8n, Flowise | LlamaIndex, LangChain | Bedrock Knowledge Bases, Vertex AI Search |
| 3 — Architecture | n8n Agent nodes, Dify, Botpress | LangGraph, CrewAI, AutoGen | Claude Managed Agents, Bedrock Agents |
| 4 — Tools | n8n HTTP nodes, Dify function tools | AWS Lambda, custom MCP SDKs | mcp.so (10,000+ pre-built), Zapier MCP |
| 5 — Prompts | Claude Workbench, Dify prompt editor | Langfuse prompt mgmt | Anthropic Console |
| 6 — Evals | Confident AI, Braintrust dashboard | LangSmith, Galileo, Langfuse | Arize Phoenix Cloud |
| 7 — Deployment | n8n Cloud, Dify Cloud | Claude API + serverless | Claude Managed Agents ($0.08/session-hr) |
| 8 — AgenticOps | Langfuse (OSS), Helicone | Arize Phoenix, LangSmith | Datadog LLM Observability, New Relic AI |
| 9 — Governance | Drata, Vanta (compliance SaaS) | OPA, AWS IAM | Secureframe, AWS CloudTrail |

---

## Recommended Learning Path

### Week 1: Foundations

- Read Anthropic's "Building Effective Agents" guide (anthropic.com/research/building-effective-agents)
- Read the MCP specification overview (modelcontextprotocol.io)
- Watch the Claude Managed Agents demo (Anthropic YouTube channel)
- Complete Phase 1 for a real (but low-risk) problem you want to automate

### Week 2: No-Code Experimentation

- Set up a Dify or n8n instance (both have free tiers)
- Build a retrieval-only agent: connect a knowledge base, configure a tool, test 10 queries
- Set up a Confident AI account and run your first eval on the retrieval agent
- Aim to complete Phases 2-5 on your chosen problem

### Week 3: Deployment and Monitoring

- Deploy your Phase 2-5 agent to a staging environment
- Set up Langfuse or Helicone for basic tracing
- Run a canary with 5% of real traffic
- Build your first observability dashboard

### Week 4: Governance

- Complete the OWASP ASI Top 10 checklist for your agent
- Implement one approval gate (pre-execution blocking for the riskiest action)
- Set up audit logging and confirm logs are flowing
- Write an incident response playbook for the most likely failure mode

### Month 2 and Beyond: Advanced Topics

- Multi-agent design (only after your single-agent is stable in production)
- Custom MCP server development (when no public MCP server exists for a tool you need)
- Advanced cost optimization: prompt caching, batch API, model routing
- Drift detection: build a weekly automated eval job on production traffic samples (no-code: use an n8n scheduled trigger node that calls the Confident AI API with sampled traces every Monday morning)
- Governance maturity: advance from "Documented" to "Managed" by automating gate enforcement

---

## Key Principles

**1. Start simple.** Build a single agent with 3-5 tools. Complexity is a liability, not a feature. Add capability only when the simpler version fails a real user need.

**2. Adopt MCP early.** MCP is the industry standard tool interface (97M+ monthly downloads). Building to MCP makes your tools portable across frameworks and future-proofs your investment.

**3. Measure from day one.** Evals in Phase 6, cost tracking in Phase 7, and observability in Phase 8 are not optional extras. An agent you cannot measure is an agent you cannot improve or trust.

**4. Governance is not optional.** It is operational infrastructure. The time to implement audit logging and approval gates is before the incident, not during it.

**5. No-code platforms are production-grade.** n8n, Dify, Flowise, and Claude Managed Agents are not toy tools. Teams are running mission-critical automations on them. Start there before writing custom code.

**6. Cost management is critical.** Agents burn 20-50x more tokens than equivalent chat interactions. A mid-complexity agent handling 1,000 sessions per day can easily reach $5,000-$15,000 per month in token costs without optimization. Set budget ceilings before going to production.

**7. Match the gate to the risk.** Not every agent action needs a pre-execution approval. Apply Tier 1-4 risk classification and reserve blocking gates for irreversible, high-value actions. Over-gating makes the agent useless; under-gating makes it dangerous.

---

## Sources

### Phase 1 — Requirements

- Anthropic: "Building Effective Agents" — https://anthropic.com/research/building-effective-agents
- Google DeepMind: Agent-to-Agent (A2A) protocol specification
- NIST AI RMF: https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf

### Phase 2 — Data and Knowledge

- AWS Bedrock Knowledge Bases documentation
- Pinecone: "The Chunking Guide" developer documentation
- Weaviate: Hybrid search and metadata filtering guides

### Phase 3 — Agent Architecture

- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- CrewAI documentation: https://docs.crewai.com/
- Anthropic: Claude Agent SDK documentation

### Phase 4 — Tool Definition

- Model Context Protocol specification: https://modelcontextprotocol.io/
- MCP server registry: https://mcp.so/
- Anthropic: Tool use documentation

### Phase 5 — Prompt Engineering

- Anthropic: Prompt engineering guide — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Anthropic: Extended thinking documentation
- Anthropic: CLAUDE.md persistent context documentation

### Phase 6 — Evaluation

- Braintrust documentation: https://www.braintrust.dev/docs
- Confident AI documentation: https://docs.confident-ai.com/
- Langfuse documentation: https://langfuse.com/docs

### Phase 7 — Deployment

- Anthropic: Claude Managed Agents pricing and documentation
- n8n documentation: https://docs.n8n.io/
- Dify documentation: https://docs.dify.ai/

### Phase 8 — AgenticOps

- Arize Phoenix documentation: https://docs.arize.com/phoenix
- Helicone documentation: https://docs.helicone.ai/
- OpenTelemetry specification: https://opentelemetry.io/docs/

### Phase 9 — Governance

- EU AI Act: Official Journal of the European Union, Regulation (EU) 2024/1689
- OWASP Top 10 for Agentic Applications (December 2025): https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/
- Gartner: "AI Governance Maturity Model" (2025 edition)
- OWASP: Top 10 for LLM Applications
