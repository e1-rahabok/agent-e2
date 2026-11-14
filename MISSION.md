# Mission

Not indexed.
How the parts run: [ARCHITECTURE.md](ARCHITECTURE.md). How expertise is codified: [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md). The agent: [harness/AGENT.md](harness/AGENT.md). How the claim is proved: [benchmark/design.md](benchmark/design.md). Which model: [benchmark/models.md](benchmark/models.md).

## 1. Mission
- Agent E2 is built by Iwan 'E1' Rahabok to make his expertise and experience in VCF performance and capacity management available.
- A proof that Agent E2 works is the benchmark result show it scored higher than frontier models from leading players (Google, OpenAI, Anthropic).
- It achieves this with four parts working as one brain:
  - The Agent
  - The Harness
  - The Knowledge
  - The LLM. Standard open-weight model(s), running locally with minimal GPU. It is not a customized, fine tuned model.
- Locally means on the customer's own infrastructure: no cloud AI service, and no customer data (questions, screenshots, files) leaving the customer network. No per-token fee.
- Users' prompt or question can include a URL. Agent E2 will browse and check the content. 
- Agent E2 is more than an LLM answering one question. It is also a consultant that leads a conversation: asked "Can you guide me over capacity planning for a vSphere cluster? What should I consider? You're my expert consultant", it interviews the user for what the plan needs, computes with code, and explains each number and the trade-off behind it. Code knows which inputs are missing and does the arithmetic; the model words the questions and the advice. The benchmark measures single-turn knowledge; a conversation is measured in the live test (section 5, Ways to ask, 4 and 7).
- Scope: version 1.0 covers vSphere 9.1 metrics, the VCF Operations metrics and models computed on vSphere objects, and the Guest OS layer.
- Later: vSAN, NSX, Kubernetes, Linux flows, and VCF Operations beyond its vSphere metrics. The end scope is the private cloud stack.
- Comprehensive Benchmark, each question scored on the mean of 5 runs; Level 400 at least 80%; confident-wrong at most 3%; no misconception stated as true; the held-out set at most 11 points below. Details: [benchmark/design.md](benchmark/design.md), section 7.5.
- Targets, not rules. The smallest hardware (GPU, CPU, Memory) that passes the benchmark.
- Few rules hold in IT operations management; every assumption here, the author's included, is open to challenge with evidence.


| Lever | What it is | What we change | Where |
|---|---|---|---|
| Knowledge base | Level 400 facts, mechanisms, misconceptions, flows, exact data | Content, structure, links, catalog | `knowledge/` |
| Harness | The software around the model: retrieval, tools, verifier, rules, budgets | Code, tool design, retrieval settings | `harness/` |
| Agent | The expert's procedure as code: it reads the question into a case, plans what to read from the knowledge base's map, computes, decides whether to ask, calls the model, checks the answer | The stages, the reading plan, the rules, the prompts | `harness/` (`AGENT.md`) |
| Model choice | Which frozen model we ship | Swap in a better open model when one appears | [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md) |

- The benchmark tests the whole system, not the model. It is a proof, not a goal: no mode or run is kept for its own sake. It answers:
  - whether Agent E2, as shipped, passes the release gate and how it compares with a frontier model;
  - which frozen model to ship (model choice is the fourth lever).
- What a change to the knowledge base, harness or agent adds is read from free checks first (the retrieval check, traces, unit tests), and from the next round that proves the product.
- Agent E2 has one pipeline (author, 2026-11-14): the neuro-symbolic expert system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)); classic and agentic mode are removed. A round has two runs per candidate, Base (the model alone) and Agent E2, and the frontier reference in its web mode.

## 3. Why it is possible
Six mechanisms, in order of weight.

1. **Open-book exam.** A frontier model wins on breadth of memorised knowledge plus reasoning depth. In one narrow domain, retrieval supplies the knowledge. What remains is reading 5-10 retrieved files and applying their rules: reading comprehension plus a short reasoning chain. On that task, current 27-32B dense models are close to frontier models.
2. **The frontier model memorised the wrong answers.** Its vSphere knowledge comes from forums, blogs and old documentation, which repeat the misconceptions the author's books correct: "Ready above 5% is bad", "memory usage at 95% means add RAM", "the VM is the Guest OS". Measured on 196 questions (benchmark 2026-11-13): the frontier model without the knowledge base gave the misconception answer on 2% of multiple-choice answers and 3% of judged answers (4% with web search), and was confidently wrong on 11% of answers (12% with web search).
3. **Currency.** vSphere 9.1 and VCF 9.1.1 behaviour (memory tiering, vHT, GPU counters) is newer than most training data. The knowledge base is written from the current release by rule.
4. **Exactness from tools.** Models of every size slip on arithmetic, units and lookups (ms summation to %, KB vs kb, rollups). A calculator and a metric catalog return exact values; the agent's code calls them on the question's values, and the model calls no tool.
5. **Knowledge built for a small reader.** One fact per bullet, one object per metric file, same-name misconceptions linked, layers separated, metadata for filtering. Most enterprise retrieval fails on messy documents; this corpus is written to be retrieved.
6. **Measured, not claimed.** Every change is measured by free checks first (the retrieval check, unit tests, traces); the release is proved on the benchmark against the release gate and the frontier model, with luck removed (Unsure option, confident-wrong rate, the mean of 5 runs with the worst run reported).

### What it is not
- Not a smarter model: the model's reasoning is unchanged. The system moves the hard parts (knowing, computing, looking up, ordering the checks) out of the model.
- Not a chatbot over documentation: a documentation chatbot retrieves definitions. This system retrieves the mechanism, the misconception and the order of checks an expert applies.

### Risks
| Risk | Why it matters | Guard |
|---|---|---|
| Prior override | The model reads the right file and still answers from an Internet rule of thumb | Prompt rule: knowledge base wins; override rate measured; core rules given up front ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)) |
| Retrieval miss | The right file exists but is not found; the model cannot use what it does not see | Retrieval check without a model; the reading plan follows the knowledge base's links and searches each claim; a gap in the draft triggers one follow-up |
| Weak tool use | Small models search in circles or make no calls | The model makes no tool calls: the agent plans the reading and runs the tools in code ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)) |
| Knowledge gap | The fact is not in the knowledge base | Every wrong answer classified; the author fills the gap |
| Benchmark fitted to the knowledge base | Claude edits the knowledge base and can read the questions | Held-out set kept by the author; general fixes only ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10) |

### What would prove it wrong
- The best local configuration stays below the frontier reference by more than the margin after the knowledge base covers the questions (retrieval check at 100%) and the override rate is near 0. Then the gap is the model's reasoning, and the next lever is a larger frozen model ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1).

### Status
- Not achieved yet. Agent E2 was rebuilt on 2026-11-14 as one pipeline, the neuro-symbolic expert system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)): code plans what the model reads and computes the exact values; the model reads and writes. No round has run on it yet.

## 4. Model size
- Size, speed and hardware: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section Model size and speed.

## 5. What the product must do
Requirements for the shipped assistant. Findings from the author's demo app (2026-11-04) are archived in [project/archive/product-requirements.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/product-requirements.md).

### Ways to ask
| # | Mode | Input | What the system does | Release |
|---|---|---|---|---|
| 1 | Text | A typed question | Retrieve, use tools, answer with citations | 1.0 |
| 2 | Screenshots | One or more images: vCenter charts, esxtop, VCF Operations | Recognise the screen; read metric names, values, units, time range and interval; show what was read for confirmation; answer from the knowledge base | 1.0; the screen library is 1.1 |
| 3 | Data files | esxtop batch CSV, vCenter chart export, VCF Operations export | Parse with code, not the model: peak, 95th percentile, time of peak, per object; feed exact values to the answer | 1.2 |
| 4 | Guided troubleshooting | A symptom ("VM is slow") | Run the matching flow one step at a time; ask for the next value; show the step and the branch taken | 1.0 (today the flow is read first and the model follows its steps; code taking the branch is to build, Q166) |
| 5 | Live instance | Read-only connection to VCF Operations | Read metrics of a named object; fill the flow steps from live values | After 1.0 |
| 6 | URL | A link in the question: KB article, documentation page, blog, community thread | Fetch the page, keep only the parts relevant to the question, check them against the knowledge base, say where the page is right and where it is wrong | 1.0 |
| 7 | Consultation | A request to be guided ("Guide me through capacity planning for a vSphere cluster; you're my expert consultant") | Lead the conversation over several turns: explain what matters and why, ask for the inputs a step needs (host specification, VM classes and their overcommit, reservation and expected peak, HA, what ESXi, vSAN and NSX take), offer the default for each and say it is one, compute with the planning calculator, and explain the six numbers and which one limits the host. Release 1.0 has one consultation, capacity planning for a new cluster ([harness/capacity.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/capacity.py), built; the conversation is to build). 14 more after 1.0: [project/consultations.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/consultations.md). | 1.0: capacity planning only (author, 2026-11-14) |

- Clarifying questions: at most one round per question, then answer. A consultation (Ways to ask, 7) is the exception: the user asked to be guided, so the agent asks step by step until the plan has its inputs.
  - A question that makes sense is answered without asking why.
  - Ask when the question is odd or illogical: a wrong premise usually shows a gap in product knowledge, so name the premise and ask what problem the user saw. Example: "Should I add vCPUs because CPU Ready is high?"
  - Ask when the text and an attachment disagree (the text says CPU Usage, the screenshot shows CPU Utilization), or when one missing fact (object, layer, interval) changes the answer.
  - Ask when a term is used for different things: "Do you mean A, B or C?". Jargon is often used interchangeably although the meanings differ ("cluster risk" can mean Cluster Risk (%), capacity runway or availability risk). A frontier model picks one silently and answers the wrong question; knowing the common misconceptions, Agent E2 asks.
  - But answering is the default; asking is the exception, so a VMware administrator is not irritated. Ask only when all three hold: the term has several meanings, they lead to different answers, and nothing in the question or an attachment tells which. Otherwise answer the most likely meaning, name it in the first sentence, and add one line for the other ("If you meant capacity runway: ..."). Never more than one round.
  - To measure both ways: a clarifying set with questions where asking is right and questions where asking is wrong, scoring both. Not built: the benchmark is single turn; until then the live test measures it with real questions ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), step 9).
  - Otherwise answer and state the assumption first.
- Screenshots: several per question, compared with each other; the chart interval and rollup are read (a 1-day chart hides 20-second peaks); values are shown back before reasoning; images stay on site.
- Data files are more exact than screenshots and need no screen reading; recommended when the user can export.
- URLs and web search:
  - A page the user gives is evidence to check, not a source to follow. A small model tends to repeat text the user supplied, so the harness labels it and the answer states where the page agrees with the knowledge base and where it does not, and why. Level 300 errors in vendor KB articles and blogs are common; correcting them is where Agent E2 beats a frontier model, which tends to agree with the page.
  - Web search runs only when the question needs current facts: a known bug or defect, a symptom after an upgrade, a version, build or patch level, a configuration maximum or default of a release, a renamed product or feature. Known bugs are part of every configuration check (Q104), and the knowledge base is always behind on them. Other questions are answered from the knowledge base without search.
  - Trim: a page or search result is chunked and only the relevant parts (a few hundred to about 2,000 tokens) enter the context, after the knowledge-base files, so the 16K budget keeps the knowledge base.
  - Without Internet access: say the page cannot be opened, ask for the relevant paragraph, answer from the knowledge base.

### Answer
- Direct answer first, then the mechanism and the reason, then what to check next.
- Agent E2 teaches, not only answers. For a concept question: name a wrong premise first; teach the mechanism; give a worked example with numbers when it helps, computed with the calculator, stating its assumptions.
- Name the object for every metric (VM CPU Ready, not CPU Ready). State units and the time interval.
- Thresholds only with their source. When the book and the documentation differ, show both and say which applies.
- Which source wins depends on the type of fact:
  - mechanism and interpretation (what a counter means, which metric to read, why a rule of thumb fails): the knowledge base wins over vendor pages, KB articles and blogs;
  - version-specific fact (defaults, configuration maximums, new or renamed counters, builds, bug fixes, scheduler changes): the newer official document wins when it is dated after the knowledge file's source; the file is flagged for review.
  - The product can be newer than its own documentation: the VCF Operations 9.1 manuals are out of date in places (example: the VM Contention dashboard, deprecated in the product). A knowledge file that records the product's behaviour wins over the manual.
- Exact values come from the catalog and the calculator, and are shown as such.
- Unsure is an answer: "The knowledge base does not settle this; here is what it does say."
- Every fact cited. Linked files shown with their link type, so the same-name misconception guard is visible.

### Non-functional
| Area | Requirement |
|---|---|
| Data stays on site | No customer data leaves the customer network. Agent E2 answers without Internet access. A call out carries only public knowledge requests (a URL the user gives, an update download), never customer data. Updates also arrive as an offline bundle. |
| One tested system | The app calls `harness/` for retrieval, tools, prompt and verifier. Prompt and settings are versioned in the repository; an edited prompt is an untested prompt. |
| Vision | Hard requirement (author, 2026-11-14). Administrators upload screenshots, often several per question, and every current foundation model family reads images. Agent E2 reads the pixels of every uploaded image; there is no text-only mode and no text-only model. |
| Model | Open weights with a commercial licence, vision (above), at least 32K context. Hardware: as little as passes the release gate; one GPU is the stretch target, two to four GPUs are acceptable. Chosen by the benchmark. |
| Reproducibility | Every answer stores question, answer, cited ids, tool trace, index version, prompt version, model, settings. |
| Accuracy | Release gate in section 1, measured on the shipped configuration. |
| Feedback | Rate and flag every answer, with a cause (knowledge gap, wrong fact, retrieval miss, model error). |
| Privacy | Questions, screenshots and files stay on site; retention configurable. |
| Users | Enterprise: SSO, roles, audit log. Several users: vLLM instead of Ollama. |

### Decisions
- D1: no draft status in the product. Release content is reviewed; answers never mention review status.
- D2: screenshot upload is version 1.0 (was 1.1). The screen library follows in 1.1.
- D3: data file upload is version 1.2. Each export format needs its own documented reading first.

## 6. Design considerations

### Screenshots of the product UI in the knowledge base (2026-11-06)
- Question: does adding every screenshot of vSphere and VCF Operations, with an explanation, improve the system's product knowledge?
- The model is frozen: screenshots in the knowledge base do not train it.
- Retrieval matches text, not pixels. An image without a written explanation is never found.
- So the value is the text twin of each screen: which tool and screen, which object, which counters with unit, interval and rollup, how to read it, and its misconceptions.
- Where it helps:
  - an uploaded screenshot (release 1.0) is matched to its screen file, which says what the screen shows and how to read it;
  - tool confusion, one of the 12 misconception types: the same counter name reads differently in esxtop, vCenter and VCF Operations.
- The image itself helps only when the agent fetches it for a vision model at answer time; each costs about 1,500 prompt tokens.
- Why not every screen:
  - most of the hundreds of screens are configuration, not performance or capacity;
  - extra files compete in retrieval and push out the files that matter (ranking shifted when 2 files were added);
  - each file needs the author's review.
- Decision: a screen library of the 30-50 screens operators read daily for performance and capacity, starting with the screens of the screenshot questions. Template: [project/templates/screen.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/templates/screen.md); location: [project/knowledge-rules/placement.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/placement.md). Kept only if the retrieval check on screenshot questions improves. Not started.
