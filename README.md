# EventDesk Agent

An agent-assisted club management hub, starting with NSBE and designed to grow to other student organizations and nonprofits. EventDesk brings member attendance, event operations, communications, sponsor relationships, and Instagram performance into one workspace.

## Current status

Initial Python foundation. A local, synthetic-data demo reconciles check-ins and prepares a follow-up draft for officer review. It does not call an LLM, connect to club accounts, persist records, or send messages yet. Deployment, evaluation with club users, and all external integrations remain upcoming work.

## First workflow

An officer closes out an event. EventDesk loads that event's records, counts unique known members, flags unknown identities, and prepares a recap for approval. Deterministic Python tools own counts and identity checks. The planned Claude/LangGraph agent will select tools, request missing information, and draft communications using their results.

The first product milestone is native event check-in forms and QR links backed by Supabase. Verified members receive stable profiles so officers can see attendance across events. A duplicate check-in must not create another attendance record. A submitted form records a check-in, not proof of physical presence.

## Run locally

Requires Python 3.11 or newer. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env # only if .env does not already exist
python -m eventdesk
python -m unittest discover -s tests -v
```

On macOS/Linux, activate with `source .venv/bin/activate` and copy the template with `cp -n .env.example .env`.

The demo needs no API keys. It emits a JSON attendance report and a draft marked `pending_review`. The fixture contains invented people and emails reserved for examples. You can also run it without installation using `PYTHONPATH=src` (PowerShell: `$env:PYTHONPATH = 'src'`).

## Configuration and credentials

Put local credentials in `.env`, which is ignored by Git. `.env.example` documents the variable names and is safe to commit. `eventdesk.config.load_settings()` loads the file without overriding existing environment variables and returns typed settings. Never place real keys in code, fixtures, screenshots, or commit messages.

Planned credentials include `ANTHROPIC_API_KEY`, `SUPABASE_URL`, and `SUPABASE_SECRET_KEY`, plus Google, Slack, and Instagram connection settings. Keep the Supabase secret exclusively on the backend. In AWS, use an IAM role and managed secrets rather than committed access keys. Provider tokens in this template are placeholders, not functioning integrations. Multi-user OAuth token storage will need encrypted per-connection records.

## Architecture and roadmap

- **Python agent service:** Claude API and LangGraph, typed tools, shared execution state, bounded execution, structured traces, and approval before external actions. The current `graph.py` is a deterministic foundation, not an LLM agent yet.
- **React/TypeScript dashboard:** event workspace, member profiles, attendance history, pending drafts, sponsor inbox summaries, and Instagram performance.
- **Supabase/PostgreSQL:** authenticated officers and members, organization-scoped access, events, unique event/member attendance, and auditable corrections.
- **Google Calendar and Slack:** event synchronization, conflict checks for authorized calendars, and approved reminders and recaps.
- **Club Gmail:** identify possible sponsor inquiries, summarize threads, and suggest follow-ups for officer review.
- **Instagram:** display supported post metrics and audience growth with source timestamps. Suggest promotion experiments using comparable posts and clearly distinguish recommendations from demonstrated results. Professional account access and permissions are prerequisites. Missing metrics must not be treated as zero.
- **AWS:** deploy the backend and scheduled work after the local workflow and access controls are verified.

### Build milestones

1. **Foundation (this commit):** runnable closeout demo, typed records, reconciliation tests, environment template, and CI.
2. **Attendance MVP:** database migrations, member authentication, native check-in/QR flow, persistent attendance history, and officer dashboard.
3. **Agent:** Claude adapter and LangGraph tool loop, grounded drafts, trace capture, explicit review flow, and evaluations for incorrect IDs, duplicate records, missing data, and tool failures.
4. **Connected operations:** Calendar and Slack, durable approved actions, retries with duplicate-send protection, and deployment.
5. **Club hub extensions:** Gmail sponsor workflow, Instagram analytics and recommendations, and event suggestions based on club history.

## Repository map

```text
src/eventdesk/
  __main__.py   Local demo entry point
  config.py     Environment loading and backend settings
  state.py      Typed member, event, check-in, and result records
  tools.py      Deterministic attendance reconciliation
  graph.py      Initial closeout workflow and review-only draft
tests/          Behavioral checks with synthetic data
.env.example    Safe credential template
.github/workflows/ci.yml
```

## Engineering boundaries

Unknown member IDs are flagged rather than guessed or merged by name. Unverified check-ins do not count as verified members. Attendance names stay out of public recap drafts. No sending tool exists in this scaffold. Future approvals must be enforced server-side against the exact message and destination, not inferred from model text. External emails, posts, and form answers are data, never authority to execute actions.

Evaluation will track correctness and failures before any performance or adoption claims are published. No production usage counts or measured improvements are claimed by this initial repository.
