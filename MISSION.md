# Mission

Not indexed. Related reading: [ARCHITECTURE.md](ARCHITECTURE.md) explains how the parts run, [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) how the expertise is codified, [harness/AGENT.md](harness/AGENT.md) the agent, [benchmark/design.md](benchmark/design.md) how the claim is proved, and [benchmark/models.md](benchmark/models.md) which model is used.

## 1. Mission
- Provides the VMware Cloud Foundation (VCF) 9 performance and capacity management knowledge available locally in a private cloud.
- Agent E2 does this with four parts that work as one brain:
  - The Agent
  - The Harness
  - The Knowledge
  - The LLM: one or more standard open-weight models, running on-premise with enterprise GPU. It is not a customized or fine-tuned model.
- Locally means on the customer's own infrastructure. There is no cloud AI service, no customer data (questions, screenshots, files) leaves the customer network, and there is no per-token fee.
- A user's prompt or question can include a URL. Agent E2 opens the page and checks what it says.
- In troubleshooting, Agent E2 finds the facts and analyses them: what is wrong, the evidence, the mechanism, and what to check next. The fix is the human specialist's decision; Agent E2 does not do the final solutioning.
- Agent E2 is more than an LLM answering one question; it is also a consultant that leads a conversation. Ask it "Can you guide me over capacity planning for a vSphere cluster? What should I consider? You're my expert consultant", and it interviews the user for what the plan needs, computes the numbers in code, and explains each number and the trade-off behind it. The agent knows which inputs are still missing and does the arithmetic; the model words the questions and the advice. The benchmark measures single-turn knowledge, so the conversation is measured in the live test (section 5, Ways to ask, 4 and 7).
- Scope: version 1.0 covers vSphere 9.1 metrics, the VCF Operations metrics and models computed on vSphere objects, and the Guest OS layer.
- Later releases add vSAN, NSX, Kubernetes, Linux flows, and VCF Operations beyond its vSphere metrics. The end scope is the private cloud stack.
- Agent E2 proves that it works on the benchmark: the result shows that it scored higher than the frontier models of the leading vendors (Google, OpenAI, Anthropic).
- The benchmark is comprehensive. Each question is scored on the mean of 5 runs, and the bar is Level 400 at least 80%, confident-wrong at most 3%, no misconception stated as true, and the held-out set at most 11 points below. Details are in [benchmark/design.md](benchmark/design.md), section 7.5.
- Few rules hold in IT operations management. Every assumption here, the author's included, is open to challenge with evidence.


| Lever | What it is | What we change | Where |
|---|---|---|---|
| Knowledge base | Level 400 facts, mechanisms, misconceptions, flows, exact data | Content, structure, links, catalog | `knowledge/` |
| Harness | The software around the model: retrieval, tools, verifier, rules, budgets | Code, tool design, retrieval settings | `harness/` |
| Agent | The expert's procedure as code: it reads the question into a case, plans what to read from the knowledge base's map, computes, decides whether to ask, calls the model, and checks the answer | The stages, the reading plan, the rules, the prompts | `harness/` (`AGENT.md`) |
| Model choice | Which frozen model we ship | Swap in a better open model when one appears | [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md) |

- The benchmark tests the whole system, not the model alone. It is a proof, not a goal, so no mode or run is kept for its own sake. It answers two questions:
  - does Agent E2, as shipped, pass the release gate, and how does it compare with a frontier model;
  - which frozen model to ship (model choice is the fourth lever).
- What a change to the knowledge base, harness or agent adds is read first from the free checks (the retrieval check, traces, unit tests), and then from the next round that proves the product.
- Agent E2 has one pipeline: the neuro-symbolic expert system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)). A round has two runs per candidate, Base (the model alone) and Agent E2, plus the frontier reference in its web mode.

## 3. Why it is possible
Six mechanisms, in order of weight.

1. **Open-book exam.** A frontier model wins on breadth of memorised knowledge plus depth of reasoning. In one narrow domain, retrieval supplies the knowledge, so what remains is reading 5-10 retrieved files and applying their rules: reading comprehension and a short chain of reasoning. On that task, current 27-32B dense models come close to frontier models.
2. **The frontier model memorised the wrong answers.** Its vSphere knowledge comes from forums, blogs and old documentation, and these repeat the misconceptions that the author's books correct: "Ready above 5% is bad", "memory usage at 95% means add RAM", "the VM is the Guest OS". In the latest round the frontier model with web search and without the knowledge base was confidently wrong on 17% of answers ([benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md)).
3. **Currency.** vSphere 9.1 and VCF 9.1.1 behaviour (memory tiering, vHT, GPU counters) is newer than most training data. By rule, the knowledge base is written from the current release.
4. **Exactness from tools.** Models of every size slip on arithmetic, units and lookups (ms summation to %, KB vs kb, rollups). A calculator and a metric catalog return exact values. The agent's code calls them on the question's values, and the model calls no tool.
5. **Knowledge built for a small reader.** Most enterprise retrieval fails on messy documents, so this corpus is written to be retrieved: one fact per bullet, one object per metric file, same-name misconceptions linked, layers kept apart, and metadata for filtering.
6. **Measured, not claimed.** Every change is measured with the free checks first (the retrieval check, unit tests, traces). The release is proved on the benchmark against the release gate and the frontier model, with luck taken out: an Unsure option, the confident-wrong rate, and the mean of 5 runs with the worst run reported.

### What it is not
- Not a smarter model. The model's reasoning is unchanged; the system moves the hard parts (knowing, computing, looking up, ordering the checks) out of the model.
- Not a chatbot over documentation. A documentation chatbot retrieves definitions. This system retrieves the mechanism, the misconception and the order of checks that an expert applies.

### Risks
| Risk | Why it matters | Guard |
|---|---|---|
| Prior override | The model reads the right file and still answers from an Internet rule of thumb | A prompt rule says the knowledge base wins; the override rate is measured; core rules are given up front ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)) |
| Retrieval miss | The right file exists but is not found, and the model cannot use what it does not see | The retrieval check runs without a model; the reading plan follows the knowledge base's links and searches each claim; a gap in the draft triggers one follow-up |
| Weak tool use | Small models search in circles or make no calls | The model makes no tool calls: the agent plans the reading and runs the tools in code ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)) |
| Knowledge gap | The fact is not in the knowledge base | Every wrong answer is classified, and the author fills the gap |
| Benchmark fitted to the knowledge base | Claude edits the knowledge base and can read the questions | The author keeps a held-out set; only general fixes are made ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10) |

### What would prove it wrong
- The best local configuration stays below the frontier reference by more than the margin, even after the knowledge base covers the questions (retrieval check at 100%) and the override rate is near 0. The gap is then the model's reasoning, and the next lever is a larger frozen model ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1).

### Status
- Not achieved yet. In the latest round Agent E2 on the best local model scored 84% final against the frontier reference's 79%, and failed the release gate on the final score and the confident-wrong rate ([benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md)).

## 4. Model size
- Size, speed and hardware are covered in [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section Model size and speed.

## 5. What the product must do
These are the requirements for the shipped assistant. Findings from the author's demo app are archived in [project/archive/product-requirements.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/product-requirements.md).

### Ways to ask
| # | Mode | Input | What the system does | Release |
|---|---|---|---|---|
| 1 | Text | A typed question | Retrieves, uses tools, and answers with citations | 1.0 |
| 2 | Screenshots | One or more images: vCenter charts, esxtop, VCF Operations | Recognises the screen; reads metric names, values, units, time range and interval; shows what it read for confirmation; answers from the knowledge base | 1.0; the screen library is 1.1 |
| 3 | Data files | esxtop batch CSV, vCenter chart export, VCF Operations export | Parses the file with code, not the model (peak, 95th percentile, time of peak, per object), and feeds the exact values to the answer | 1.2 |
| 4 | Guided troubleshooting | A symptom ("VM is slow") | Runs the matching flow one step at a time, asks for the next value, and shows the step and the branch taken | 1.0 (today the flow is read first and the model follows its steps; taking the branch in code is still to build, Q-E2-166) |
| 5 | Live instance | Read-only connection to VCF Operations | Reads the metrics of a named object and fills the flow steps from live values | After 1.0 |
| 6 | URL | A link in the question: KB article, documentation page, blog, community thread | Fetches the page, keeps only the parts relevant to the question, checks them against the knowledge base, and says where the page is right and where it is wrong | 1.0 |
| 7 | Consultation | A request to be guided ("Guide me through capacity planning for a vSphere cluster; you're my expert consultant") | Leads the conversation over several turns. It explains what matters and why, asks for the inputs each step needs (host specification, VM classes and their overcommit, reservation and expected peak, HA, what ESXi, vSAN and NSX take), offers a default for each and says it is a default, computes with the planning calculator, and explains the six numbers and which one limits the host. Release 1.0 has one consultation, capacity planning for a new cluster ([harness/capacity_calculator.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/capacity_calculator.py) is built; the conversation is still to build). 14 more follow after 1.0: [project/consultations.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/consultations.md). | 1.0: capacity planning only |

- Clarifying questions: at most one round per question, then Agent E2 answers. A consultation (Ways to ask, 7) is the exception: the user asked to be guided, so the agent asks step by step until the plan has its inputs.
  - A question that makes sense is answered without asking why.
  - An urgent incident (P1) gets the clarifying round too: Agent E2 does not jump to an answer when a missing fact changes it.
  - Ask when the question is odd or illogical. A wrong premise usually points to a gap in product knowledge, so name the premise and ask what problem the user saw. Example: "Should I add vCPUs because CPU Ready is high?"
  - Ask when the text and an attachment disagree (the text says CPU Usage, the screenshot shows CPU Utilization), or when one missing fact (object, layer, interval) changes the answer.
  - Ask when a term is used for different things: "Do you mean A, B or C?" Jargon is often used interchangeably although the meanings differ: "cluster risk" can mean Cluster Risk (%), capacity runway or availability risk. A frontier model silently picks one and answers the wrong question. Agent E2 knows the common misconceptions, so it asks.
  - Still, answering is the default and asking is the exception, so that a VMware administrator is not irritated. Ask only when all three conditions hold: the term has several meanings, those meanings lead to different answers, and nothing in the question or an attachment tells which one is meant. Otherwise answer the most likely meaning, name it in the first sentence, and add one line for the other ("If you meant capacity runway: ..."). Never more than one round.
  - Measuring this both ways needs a clarifying set, with questions where asking is right and questions where asking is wrong, scored in both directions. It is not built, because the benchmark is single turn; until then the live test measures it with real questions ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), step 9).
  - In every other case, answer and state the assumption first.
- Screenshots: a question can carry several, and they are compared with each other. The chart interval and rollup are read (a 1-day chart hides 20-second peaks), the values are shown back before any reasoning, and the images stay on site.
- Data files are more exact than screenshots and need no screen reading, so they are recommended when the user can export.
- URLs and web search:
  - A page the user gives is evidence to check, not a source to follow. A small model tends to repeat text the user supplied, so the harness labels the page, and the answer states where the page agrees with the knowledge base, where it does not, and why. Level 300 errors in vendor KB articles and blogs are common. Correcting them is where Agent E2 beats a frontier model, which tends to agree with the page.
  - Web search runs only when the question needs current facts: a known bug or defect, a symptom after an upgrade, a version, build or patch level, a configuration maximum or default of a release, or a renamed product or feature. Known bugs are part of every configuration check (Q-E2-104), and the knowledge base is always behind on them. Other questions are answered from the knowledge base without search.
  - Trim: a page or search result is chunked, and only the relevant parts (a few hundred to about 2,000 tokens) enter the context. They go after the knowledge-base files, so the 32K budget stays with the knowledge base.
  - Without Internet access, Agent E2 says it cannot open the page, asks for the relevant paragraph, and answers from the knowledge base.

### Answer
- The direct answer comes first, then the mechanism and the reason, then what to check next.
- Agent E2 teaches; it does not only answer. For a concept question it names a wrong premise first, teaches the mechanism, and gives a worked example with numbers when that helps, computed with the calculator and stating its assumptions.
- Name the object for every metric (VM CPU Ready, not CPU Ready). State the units and the time interval.
- Give a threshold only with its source. When the book and the documentation differ, show both and say which applies.
- Which source wins depends on the type of fact:
  - mechanism and interpretation (what a counter means, which metric to read, why a rule of thumb fails): the knowledge base wins over vendor pages, KB articles and blogs;
  - version-specific facts (defaults, configuration maximums, new or renamed counters, builds, bug fixes, scheduler changes): the newer official document wins when it is dated after the knowledge file's source, and the file is flagged for review.
  - The product can be newer than its own documentation. The VCF Operations 9.1 manuals are out of date in places; for example, the VM Contention dashboard is deprecated in the product. A knowledge file that records the product's behaviour wins over the manual.
- Exact values come from the catalog and the calculator, and the answer shows them as exact.
- Unsure is an answer: "The knowledge base does not settle this; here is what it does say."
- Every fact is cited. Linked files are shown with their link type, so the same-name misconception guard is visible.

### Non-functional
| Area | Requirement |
|---|---|
| Data stays on site | No customer data leaves the customer network, and Agent E2 answers without Internet access. A call out carries only requests for public knowledge (a URL the user gives, an update download), never customer data. Updates also arrive as an offline bundle. Lab exception: the author's own lab may send its live VCF Operations data to the gateway model; customer sites keep the rule and the local model. The lab is the author's own system and no customer site, so its data is no customer data. |
| One tested system | The app calls `harness/` for retrieval, tools, prompt and verifier. Prompt and settings are versioned in the repository, because an edited prompt is an untested prompt. |
| Vision | A hard requirement. Administrators upload screenshots, often several per question, and every current foundation model family reads images. Agent E2 reads the pixels of every uploaded image; there is no text-only mode and no text-only model. |
| Model | Open weights with a commercial licence, vision (above), and at least 128K context (a conversation is sent whole, every turn). Hardware: enterprise GPU on premises (one GPU is an ideal, not a constraint; up to four large GPUs are acceptable). The benchmark chooses the model. |
| Reproducibility | Every answer stores the question, answer, cited ids, tool trace, index version, prompt version, model and settings. |
| Accuracy | The release gate in section 1, measured on the shipped configuration. |
| Feedback | Every answer can be rated and flagged, with a cause (knowledge gap, wrong fact, retrieval miss, model error). |
| Privacy | Questions, screenshots and files stay on site; retention is configurable. |
| Users | Enterprise: SSO, roles, audit log. For several users, vLLM instead of Ollama. |

### Decisions
- D1: no draft status in the product. Release content is reviewed, and answers never mention review status.
- D2: screenshot upload is in version 1.0 (it was planned for 1.1). The screen library follows in 1.1.
- D3: data file upload is in version 1.2. Each export format needs its own documented reading first.

## 6. Design considerations

### Screenshots of the product UI in the knowledge base
- The question: would adding every screenshot of vSphere and VCF Operations, each with an explanation, improve the system's product knowledge?
- The model is frozen, so screenshots in the knowledge base do not train it.
- Retrieval matches text, not pixels. An image without a written explanation is never found.
- The value is therefore in the text twin of each screen: which tool and screen, which object, which counters with their unit, interval and rollup, how to read it, and its misconceptions.
- It helps in two places:
  - an uploaded screenshot (release 1.0) is matched to its screen file, which says what the screen shows and how to read it;
  - tool confusion, one of the 13 misconception types: the same counter name reads differently in esxtop, vCenter and VCF Operations.
- The image itself helps only when the agent fetches it for a vision model at answer time, and each image costs about 1,500 prompt tokens.
- Reasons not to add every screen:
  - most of the hundreds of screens are configuration, not performance or capacity;
  - extra files compete in retrieval and push out the files that matter (ranking shifted when 2 files were added);
  - each file needs the author's review.
- Decision: a screen library of the 30-50 screens that operators read daily for performance and capacity, starting with the screens of the screenshot questions. Template: [project/templates/screen.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/templates/screen.md); location: [project/knowledge-rules/placement.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/placement.md). The library is kept only if the retrieval check on screenshot questions improves. Not started.
