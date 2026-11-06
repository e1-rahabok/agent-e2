# Mission: why a small local model can beat a frontier model

Not indexed.
How the parts run: [ARCHITECTURE.md](ARCHITECTURE.md). How expertise is codified: [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md). The agent: [harness/AGENT.md](harness/AGENT.md). How the claim is proved: [benchmark/design.md](benchmark/design.md). Which model: [benchmark/models.md](benchmark/models.md).

## 1. Mission
- An open-weight model, running offline on one GPU (at most 96 GB), answers Level 400 private cloud operations questions better than the best frontier model.
- Offline means a dark site: no Internet, no cloud API, no data leaving the customer. No per-token fee.
- Scope: version 1.0 covers vSphere 9.1 metrics and the Guest OS layer. Later: vSAN, NSX, VCF Operations, Kubernetes, Linux. The end scope is the private cloud stack.
- Release gate: final score at least 85% on the benchmark, each question scored on its worst of 5 runs. Target: 99%. Confident-wrong rate near 0.

## 2. What we can change
- The model is frozen. We do not train or fine-tune it. Its weights are a given.
- The product is not the model. It is a compound system: model + agent + harness + knowledge base.

| Lever | What it is | What we change | Where |
|---|---|---|---|
| Knowledge base | Level 400 facts, mechanisms, traps, flows, exact data | Content, structure, links, catalog | `knowledge/` |
| Harness | The software around the model: retrieval, tools, verifier, rules, budgets | Code, tool design, retrieval settings | `harness/` |
| Agent | The model plus the tool loop: what it is told up front, its rules for choosing tools | System prompt, up-front knowledge, tool rules | `harness/` (`AGENT.md`) |
| Model choice | Which frozen model we ship | Swap in a better open model when one appears | [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md) |

- The benchmark tests the whole system, not the model. It answers three questions:
  - which frozen model to ship (model choice is the fourth lever);
  - what each change to the knowledge base, harness or agent adds: a score delta per change, with everything else fixed;
  - whether the system beats the frontier model.
- Baseline mode (the model alone) is not a test of the model for its own sake. It is the zero point: system score minus baseline score is what our work adds.

## 3. Why it is possible
Six mechanisms, in order of weight.

1. **Open-book exam.** A frontier model wins on breadth of memorised knowledge plus reasoning depth. In one narrow domain, retrieval supplies the knowledge. What remains is reading 5-10 retrieved files and applying their rules: reading comprehension plus a short reasoning chain. On that task, current 27-32B dense models are close to frontier models.
2. **The frontier model memorised the wrong answers.** Its vSphere knowledge comes from forums, blogs and old documentation, which repeat the misconceptions the author's books correct: "Ready above 5% is bad", "memory usage at 95% means add RAM", "the VM is the Guest OS". Measured: the frontier model without the knowledge base gave the trap answer on 16% of answers (benchmark 20261103-093742).
3. **Currency.** vSphere 9.1 and VCF 9.1.1 behaviour (memory tiering, vHT, GPU counters) is newer than most training data. The knowledge base is written from the current release by rule.
4. **Exactness from tools.** Models of every size slip on arithmetic, units and lookups (ms summation to %, KB vs kb, rollups). A calculator and a metric catalog return exact values; the model only chooses the tool.
5. **Knowledge built for a small reader.** One fact per bullet, one object per metric file, same-name traps linked, layers separated, metadata for filtering. Most enterprise retrieval fails on messy documents; this corpus is written to be retrieved.
6. **Measured, not claimed.** Every change is scored on a fixed benchmark against the frontier model, with luck removed (Unsure option, confident-wrong rate, worst of 5 runs).

### What it is not
- Not a smarter model: the model's reasoning is unchanged. The system moves the hard parts (knowing, computing, looking up, ordering the checks) out of the model.
- Not a chatbot over documentation: a documentation chatbot retrieves definitions. This system retrieves the mechanism, the trap and the order of checks an expert applies.

### Risks
| Risk | Why it matters | Guard |
|---|---|---|
| Prior override | The model reads the right file and still answers from an Internet rule of thumb | Prompt rule: knowledge base wins; override rate measured; core rules given up front ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)) |
| Retrieval miss | The right file exists but is not found; the model cannot use what it does not see | Retrieval check without a model; link expansion; a map of the knowledge base given up front |
| Weak tool use | Small models search in circles or make no calls | Classic mode as fallback; tool rules; no-progress stops |
| Knowledge gap | The fact is not in the knowledge base | Every wrong answer classified; the author fills the gap |
| Benchmark fitted to the knowledge base | Claude edits the knowledge base and can read the questions | Held-out set kept by the author; general fixes only ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10) |

### What would prove it wrong
- The best local configuration stays below the frontier baseline by more than the margin after the knowledge base covers the questions (retrieval check at 100%) and the override rate is near 0. Then the gap is the model's reasoning, and the next lever is a larger frozen model ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1).

### Status
- Not achieved yet. On the first 17 questions (old scoring), the best local model with the knowledge base scored 58%; the frontier model without it, 75%.
- Known causes, each tracked: knowledge gaps, answer-key errors, an old prompt rule (knowledge base only, since changed), weak agentic tool use, retrieval reaching 67% of needed files.

## 4. Model size
- Size, speed and hardware: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section Model size and speed.

## 5. What the product must do
Requirements for the shipped assistant. Findings from the author's demo app (2026-11-04) are archived in [project/archive/product-requirements.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/product-requirements.md).

### Ways to ask
| # | Mode | Input | What the system does | Release |
|---|---|---|---|---|
| 1 | Text | A typed question | Retrieve, use tools, answer with citations | 1.0 |
| 2 | Screenshots | One or more images: vCenter charts, esxtop, VCF Operations | Recognise the screen; read metric names, values, units, time range and interval; show what was read for confirmation; answer from the knowledge base | 1.0 (author, 2026-11-06); the screen library is 1.1 |
| 3 | Data files | esxtop batch CSV, vCenter chart export, VCF Operations export | Parse with code, not the model: peak, 95th percentile, time of peak, per object; feed exact values to the answer | 1.2 |
| 4 | Guided troubleshooting | A symptom ("VM is slow") | Run the matching flow one step at a time; ask for the next value; show the step and the branch taken | 1.0 (flow tool exists) |
| 5 | Live instance | Read-only connection to VCF Operations | Read metrics of a named object; fill the flow steps from live values | After 1.0 |

- Clarifying questions are part of every mode: the system asks when the object, the time window or the product version is unclear, because one metric name means different things on different objects.
- Screenshots: several per question, compared with each other; the chart interval and rollup are read (a 1-day chart hides 20-second peaks); values are shown back before reasoning; images stay on site.
- Data files are more exact than screenshots and work on a dark site; recommended when the user can export.

### Answer
- Direct answer first, then the mechanism and the reason, then what to check next.
- Name the object for every metric (VM CPU Ready, not CPU Ready). State units and the time interval.
- Thresholds only with their source. When the book and the documentation differ, show both and say which applies.
- Exact values come from the catalog and the calculator, and are shown as such.
- Unsure is an answer: "The knowledge base does not settle this; here is what it does say."
- Every fact cited. Linked files shown with their link type, so the same-name trap guard is visible.

### Non-functional
| Area | Requirement |
|---|---|
| Dark site | No call outside the customer network to answer, index or update. Updates arrive as an offline bundle. |
| One tested system | The app calls `harness/` for retrieval, tools, prompt and verifier. Prompt and settings are versioned in the repository; an edited prompt is an untested prompt. |
| Model | Open weights with a commercial licence, vision, at least 32K context, one GPU of at most 96 GB. Chosen by the benchmark. |
| Reproducibility | Every answer stores question, answer, cited ids, tool trace, index version, prompt version, model, settings. |
| Accuracy | Release gate in section 1, measured on the shipped configuration. |
| Feedback | Rate and flag every answer, with a cause (knowledge gap, wrong fact, retrieval miss, model error). |
| Privacy | Questions, screenshots and files stay on site; retention configurable. |
| Users | Enterprise: SSO, roles, audit log. Several users: vLLM instead of Ollama. |

### Decisions (author, 2026-11-04)
- D1: no draft status in the product. Release content is reviewed; answers never mention review status.
- D2: screenshot upload is version 1.0 (changed by the author, 2026-11-06; was 1.1). The screen library follows in 1.1.
- D3: data file upload is version 1.2. Each export format needs its own documented reading first.

## 6. Design considerations

### Screenshots of the product UI in the knowledge base (2026-11-06)
- Question: does adding every screenshot of vSphere and VCF Operations, with an explanation, improve the system's product knowledge?
- The model is frozen: screenshots in the knowledge base do not train it.
- Retrieval matches text, not pixels. An image without a written explanation is never found.
- So the value is the text twin of each screen: which tool and screen, which object, which counters with unit, interval and rollup, how to read it, and its traps.
- Where it helps:
  - an uploaded screenshot (release 1.0) is matched to its screen file, which says what the screen shows and how to read it;
  - tool confusion, one of the 12 trap types: the same counter name reads differently in esxtop, vCenter and VCF Operations.
- The image itself helps only when the agent fetches it for a vision model at answer time; each costs about 1,500 prompt tokens.
- Why not every screen:
  - most of the hundreds of screens are configuration, not performance or capacity;
  - extra files compete in retrieval and push out the files that matter (ranking shifted when 2 files were added);
  - each file needs the author's review.
- Decision: a screen library of the 30-50 screens operators read daily for performance and capacity, starting with the screens of the 25 screenshot questions. Template: [project/templates/screen.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/templates/screen.md); location: `KNOWLEDGE-ENGINEERING.md`, section 5. Kept only if the retrieval check on screenshot questions improves. Not started (author, 2026-11-06).
