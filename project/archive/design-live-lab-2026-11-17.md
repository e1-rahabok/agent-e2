# Design: live lab (VCF Operations login, two checks)

Status: archived 2026-11-20, superseded (project/plan.md, decision of 2026-11-20): the UI, login, connector and database move to PCM; Agent E2 serves answers through `harness/answer_service.py`. Was: design, not built. Scope: the author's home lab (demo). Customer sites are out of scope here. The lab exception is in [plan.md](plan.md), Decisions of 2026-11-17. Release placement is the author's decision and is not set here.

## 1. What the user gets
- A login screen: VCF Operations user ID and password.
- After login, two features:
  1. Cluster Performance Check. Pick a cluster from a list. Agent E2 runs the check.
  2. VM Health Check. Pick a VM from a list. Agent E2 runs the check.
- The UI design comes later. This document covers the architecture only.

## 2. Components
| Part | What it is | Runs on |
|---|---|---|
| Browser | The UI (login, two lists, check result) | The user's browser, on the home network |
| Web server | One Python process: serves the UI and the JSON API (FastAPI) | Home PC, Linux or container |
| Database | SQLite file: object cache, check results, audit log. No passwords, no tokens | Same host, one file |
| Connector | `harness/connectors/vcf_operations`: calls VCF Operations, GET only | Inside the web server process |
| Check engine | Runs the flow of a check, in code (`harness/`) | Inside the web server process |
| Agent | Writes the explanation of a check result (model call) | Inside the web server process |
| Model | Open-weight model through Vercel AI Gateway | Vercel (cloud) |
| VCF Operations | The instance the user logs in to | Home lab |

- Vercel is used only for the model (AI Gateway). The UI and the database run locally.
- The web server is the only process that talks to VCF Operations and to Vercel.

## 3. Login
- The login form posts the user ID and password to the web server over HTTPS.
- The web server calls the VCF Operations token API with them and gets a session token.
- The password is used once and discarded. It is never stored, logged or returned to the browser.
- The session token stays in server memory, keyed by a random session ID.
- The browser gets only the session ID, in an HttpOnly, SameSite cookie. CSRF protection on every POST.
- The session ends on logout, on token expiry (then the user logs in again), or on server restart.
- Each user acts with their own VCF Operations role. Agent E2 has no service account. A read-only role is recommended for the lab user.
- TLS: the connector verifies the VCF Operations certificate against a CA file set in config. No verification off.
- Login attempts are rate-limited (lab: a few per minute per user ID).

## 4. Connector rules
- GET only. Paths are whitelisted in code. Any other method is refused before the network call.
- Every call uses the logged-in user's token. The connector never uses a token from config.
- Calls are logged with path, user, time and status. No payloads, no tokens.
- Object lists (clusters, VMs) are cached in the database with a short time to live. Metric values are not cached beyond one check run.

## 5. Check flow: Cluster Performance Check
1. The UI calls `GET /api/clusters`. The connector lists clusters. The cache answers if it is fresh.
2. The user picks a cluster. The UI calls `POST /api/checks` with type `cluster-performance` and the cluster ID.
3. The check engine loads the cluster health-check flow from `knowledge/` (the harness reads the file, no model).
4. The connector fetches the metrics the flow names, for the cluster and for its hosts where the flow needs them.
5. The check engine runs the flow steps in code: for each step it compares the value with the threshold from the catalog and takes the branch.
6. The result is stored (check run, steps, values, branches, verdict).
7. The agent writes the explanation: the path taken, step numbers, values, thresholds and their sources. The model sees only the step results and the cited files.
8. The UI shows the steps, the verdicts and the explanation.

## 6. Check flow: VM Health Check
Same as section 5, with the VM health-check flow and the VM as the object. The VM's host and its datastores are fetched when the flow names them.

## 7. Where the decisions sit
- Code decides: what to fetch, the thresholds, each branch, the verdict.
- The model decides nothing. It explains the path the code took.
- The model input is limited to the case, the step results and the cited knowledge files.

## 8. Build dependencies (honest status)
- The flow executor (take the branch in code, Q-E2-166) is not built. It is needed by both checks. It is the first dependency.
- Threshold verdicts in stage 3 are not built ([`project/plan.md`](plan.md), M3a).
- Object lists and metric fetch need the connector (new).
- Check two flows in the knowledge base exist (cluster and VM health check). The cluster flow has to be checked against its steps before the executor uses it.

## 9. Build order
1. Connector: login token and object lists, GET only, tested on recorded fixtures, then against the lab.
2. Web server with login and sessions (no checks yet).
3. Flow executor for one flow (VM CPU Contention or Latency is the first flow per Q-E2-166; cluster and VM health check next).
4. Check engine and the two checks, with the stored results and the audit log.
5. Explanation by the model (gateway).
6. UI (later, after the architecture is accepted).

## 10. Open for later
- The VCF Operations token endpoint and its response are to be confirmed against the lab instance at build time.
- Exact list of metrics per flow: taken from the flow files, not decided here.
- UI design.
- Release placement: the author's decision.
