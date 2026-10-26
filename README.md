# Enterprise AI Knowledge Architecture

An end-to-end learning repository connecting business outcomes, enterprise operations, AI platform capabilities and the digitised enterprise foundation.

**[Open the live site](https://lajirajg.github.io/enterprise-ai/)** · **[Read the architecture](docs/architecture/index.md)** · **[Browse the knowledge base](docs/index.md)** · **[Add a resource](https://github.com/lajirajg/enterprise-ai/issues/new?template=resource.yml)**

## Structure

- Business outcomes and value measurement
- Five operating layers: User Experience; Intelligent Orchestration; Execution; Data & AI for Continuous Improvement; Central Hub for Monitoring & Governance
- Three spines: Knowledge & Memory; Trust & Control; Workforce & Ways of Working
- Intelligent Core: harnesses, LLM kernel, inference, context and platform operations
- Data & Digital Core: digitised processes, ERP/CRM/ITSM, channels, integrations and data
- Industry playbooks, role-based learning paths and practical labs
- Canonical capability and resource catalogues, plus explicit planned-content placeholders
- A separate Modern Operate profile with a clear public/private boundary

## Local setup

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/catalogue.py validate
python scripts/catalogue.py render
python -m unittest discover -v
python -m mkdocs build --strict
python -m mkdocs serve
```

Python 3.9+ works locally; CI uses Python 3.12. `site/` is generated and ignored. Open the local address printed by MkDocs. See [setup and publishing](docs/contributing/setup.md) for Pages and workflow configuration.

## Maintenance

Paste a URL into the resource issue form. Automation validates it without fetching the URL and prepares a candidate artifact. A maintainer can run **Review resource intake** to open a candidate pull request. No resource is auto-approved or auto-merged. See [resource intake](docs/contributing/resource-intake.md).

Canonical metadata lives in `catalogue/`; catalogue pages are generated. Edit substantive narrative under `docs/`. Run the commands above after any change.

## Scope and rights

This is a learning framework under active development, not a product assessment or a compliance certification. [Design decisions](docs/about/design-decisions.md) distinguish confirmed requirements from implementation assumptions. Confidential reference attachments and detailed proprietary inventories are excluded. No project-wide reuse licence has been chosen; linked resources retain their owners’ terms.
