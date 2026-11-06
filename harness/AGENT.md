# Agent

What the agent is, what it knows when a question arrives, what it decides, and how it is improved. Not indexed.
Why the system can win: [DESIGN.md](../DESIGN.md). Run-time flow and modes: [ARCHITECTURE.md](../ARCHITECTURE.md). Harness parts: [README.md](README.md). How knowledge is found: [KNOWLEDGE-ENGINEERING.md](../KNOWLEDGE-ENGINEERING.md), section How the agent finds knowledge.

## 1. What it is
- The agent is the model plus the tool loop, in agentic mode only. It is not a separate program.
- The model makes the decisions: which tool next, with which query, which file to read, when to stop and answer.
- The harness hosts the loop and constrains it: it runs the tools, enforces the rules and the budgets, and checks the answer.
- Code: `harness/modes.py`, function `agentic`, with the prompts `SYSTEM_AGENT` and `PROMPTS`. The tools are in `harness/` (`retrieval.py`, `catalog.py`, `calc.py`, `flows.py`); the verifier in `verify.py`.
- The model is frozen. What we change is what the agent is told, which tools it has, and the rules around them.

## 2. Why an agent
- A Level 400 question often needs a chain across files: metric → the same-named metric on another object → the concept behind it → the troubleshooting flow → a calculation.
- One search cannot predict that chain. Classic mode (one lookup, then answer) is capped by what that lookup finds: 67% of needed files reach its context (2026-11-04).
- The agent can go back for more: read a file, follow its links, look up a value, compute, then answer.
- Classic mode stays as the reference point and the fallback (`ARCHITECTURE.md`, section Classic mode).

## 3. What it knows when a question arrives
### Today
- The system prompt: knowledge base first, and it wins on conflict; own knowledge only where the knowledge base is silent, said so in the reason; mechanism before definition; same-name metrics; thresholds only when the knowledge base states them; Unsure over a guess.
- The tool rules (section 5) and the tool descriptions.
- The question and its images.
- Nothing about the knowledge base itself. The agent discovers what exists only by searching.

### The gap
- Searching helps only when the model knows it does not know. Its worst errors are Internet rules of thumb it believes, so it never searches for them.
- Without a map, the agent searches blind: it does not know that a diagnosis file answers "what do I check" or that a comparison file sets two tools side by side.

### Planned: five up-front blocks
Each is small (together about 1-3K tokens), needed on most questions, and changes behaviour. Each is generated from the repository, so it cannot drift, and each has its own on/off switch for the benchmark.

| # | Block | Content | Built from |
|---|---|---|---|
| 1 | Map of the knowledge base | What each folder covers, what each file type answers, which tool serves which question | Folder layout, `retriever_guide`, file counts |
| 2 | Core rules | 10-15 short rules, each with its reason, that undo Internet priors: VM is not Guest OS; utilization is not contention; provider and consumer views differ; a counter means what its layer measures | The trap types (`KNOWLEDGE-ENGINEERING.md`, section Traps and Level 400) and the architecture rules |
| 3 | Confusable terms | Only the pairs public text mixes up: Usage, Utilization and Demand; Ready and Latency; Consumed and Active; Ballooned and Swapped | `knowledge/glossary.md` |
| 4 | Symptom → flow index | One line per diagnosis file: its name and when to use it | `diagnosis/` files |
| 5 | Procedure rules | Troubleshooting starts with the flow; a number comes from the catalog, never from memory; cite the files read | The tool rules |

### Kept behind tools
| Content | Why not up front |
|---|---|
| Full glossary | Long; most entries never matter for one question. Looked up when met. |
| Metrics and thresholds | Hundreds of rows. Up front, the model recalls a value instead of looking it up, and a recalled number cannot be checked or cited. |
| Full flowcharts | Long; one applies per question. The index points to it; the `flow` tool serves it step by step. |

- Reason for the size limit: a small model's attention thins as the prompt grows; rules buried in 20K tokens of reference are ignored. Every token is also sent on every question and run.

## 4. What it decides
| Decision | Example |
|---|---|
| What to look up first | `search("cpu.ready.summation")` or `catalog("cpu.ready")` |
| Which file to read | `read_file` on the metric file, not the snippet |
| Which links to follow | `follow_links(same_name)` before answering about a metric |
| Which exact tool | `catalog` for unit and rollup, `calculate` for the conversion, `flow` for a troubleshooting question |
| When to stop | Answer once the files settle the question, or Unsure |

## 5. Rules the harness enforces
| Rule | How | Why |
|---|---|---|
| Look up before answering | The first call must be `search` or `catalog`; any other tool is refused | Answers from memory are the main failure |
| No repeats | An identical call is refused | Small models search in circles |
| Same-name check | Before the answer, a reminder to call `follow_links(same_name)` on each metric file read | Same label, different object, is the commonest trap |
| Budget | At most `agent_max_calls` (8) tool calls and `agent_tool_tokens` (12K) of tool output; then "answer now" | Context window and time; benchmark cost |
| Format | Two malformed tool calls: fall back to classic mode | A broken loop must still answer |
| Verify | The final answer goes through `verify.py`; a hard issue gets one repair turn | A wrong format scores as wrong |

- The limits are budgets, not design values. Deployment rule (stop on token budget, time budget or no progress): `ARCHITECTURE.md`, section Tool-call limit.

## 6. Observed behaviour (2026-11-03, 17 questions)
- Agentic scored below classic for 7 of 8 small models (33% vs 45% exact on average). The frontier model was slightly ahead in agentic (67% vs 62%).
- Causes seen in traces: few or no tool calls (qwen-3-32b averaged 1.8); searching in circles until the limit (answers that hit the limit were mostly wrong); one model broke the answer format.
- So today the weakest step is the agent's first lookups, not the knowledge base. The up-front blocks (section 3) and a primed start (agentic mode that starts from the classic context) target that step.

## 7. How it is improved
- One change at a time, scored on the benchmark against the same model and questions: a score delta per change.
- Levers, in expected order of effect:
  1. up-front blocks 1-5 (section 3), each switched on alone and then together;
  2. a primed start from the classic context;
  3. tool descriptions and tool rules;
  4. the budgets, re-run on the answers that hit the limit with 16 calls.
- Kept: a change that raises the final score or lowers the confident-wrong or override rate by more than the margin. Otherwise dropped.
- Planned code split: the loop moves from `modes.py` to `harness/agent.py`, so the code matches this document.
