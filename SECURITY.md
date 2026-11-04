# Security

How Isvara handles the risks of an AI application, and how to report a problem. Not indexed.

## Reporting a vulnerability
- Use GitHub private vulnerability reporting on this repository (Security tab, Report a vulnerability), or contact the repository owner directly.
- Do not open a public issue for a vulnerability.
- Include: what you found, the file or component, and how to reproduce it.

## What the system is
- A local model, a harness and a knowledge base, running on the customer's own server with no Internet access. See [ARCHITECTURE.md](ARCHITECTURE.md).
- It answers questions. It does not change any system: no write access to vCenter, ESXi, VCF Operations or any other product.

## AI application risks and how each is handled
| Risk | Applies? | How it is handled |
|---|---|---|
| Prompt injection hidden in the knowledge base | Guarded | Every knowledge file is plain markdown, reviewed by the author before release, and versioned in git. Lint rejects instruction-like text, hidden HTML comments and invisible Unicode characters in `knowledge/` and in benchmark prompts (patterns in `tools/tags.yaml`, `injection_patterns`). |
| Prompt injection in the user's question | Guarded | The system prompt tells the model to answer only from the knowledge base and to treat the question as data. Tools are read-only, so an injected instruction cannot cause an action. The answer verifier checks the format and the cited files. |
| Prompt injection in an uploaded screenshot or file | Not applicable in 1.0 | Screenshot upload is release 1.1, data files 1.2. Both will be treated as untrusted data; extracted values are shown to the user for confirmation. |
| Data leaving the customer site | Not applicable | The model, the embedding model and the harness run locally. Nothing calls out. Updates arrive as an offline bundle. The test site uses a model gateway only for benchmarking with public questions. |
| Unsafe tool execution | Guarded | Tools only search, read files, look up the catalog, follow flows and calculate. The calculator evaluates arithmetic through a whitelist parser (no `eval`, no imports, no file or network access). No tool runs shell commands or writes files. |
| Harmful or destructive actions | Not applicable | The system has no credentials and no write access to any managed system. The planned VCF Operations connection (after 1.0) is read-only. |
| Confidently wrong answers (hallucination) | Guarded | Answers must come from retrieved files with citations. Thresholds only with a source. An Unsure option; the confident-wrong rate is measured. The verifier flags numbers not found in the retrieved text. See [benchmark/test-design.md](benchmark/test-design.md). |
| Sensitive data in the knowledge base | Guarded | Knowledge is generic product behaviour. Screenshots in the book are masked (host and customer names) before commit. |
| Sensitive data in logs and traces | Customer controlled | Questions and traces stay on the customer's server. Retention is a customer setting. Benchmark traces are not committed to git. |
| Secrets in the repository | Guarded | The gateway API key is read from an environment variable and never committed. |
| Supply chain: model weights | Customer verified | Open-weight models with Apache 2.0 or MIT licences, downloaded from the publisher and checked by hash before deployment. |
| Supply chain: code dependencies | Low | Python standard library plus `pyyaml` and `requests`. No other runtime dependencies. |
| Training-data poisoning | Not applicable | The model is not trained or fine-tuned on customer data or on this repository. Knowledge is supplied at run time by retrieval. |
| Benchmark contamination | Guarded | Answer keys are never indexed and never sent to the model; a held-out question set is kept outside the repository. |
| Resource exhaustion | Guarded | Tool calls, tool output and context size are capped per question. |

## What a security reviewer can check
- `knowledge/` holds only markdown and YAML: no executable content.
- `python3 tools/lint.py` reports 0 problems, including the injection pattern scan.
- `harness/calc.py` (whitelist expression parser) and `harness/modes.py` (tool list) show that no tool executes code or changes a system.
- `harness/llm.py` is the only network client; at a customer site it points at the local model server.
