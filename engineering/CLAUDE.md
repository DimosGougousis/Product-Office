# Engineering Folder

Technical design, architecture, and bug post-mortems.

## Doc Index
- `rfc/` — Request-for-comment technical design documents
- `bug-investigations/` — Root-cause analyses (RCAs) and post-mortems, linked from `observability/incidents/`
- `architecture/` — System diagrams, service maps, dependency graphs

## Instructions for Claude
- Use `rfc/_template.md` for new technical designs.
- Bug investigations follow `bug-investigations/_template.md`: Timeline → Root Cause → Fix → Prevention → Linked PRs/Issues.
- When an incident is opened in `observability/incidents/`, create a corresponding RCA in `bug-investigations/` and cross-link.
- Architecture diagrams: prefer Mermaid (renders in GitHub + VS Code mermaid extension) or Graphviz `.dot` files.
