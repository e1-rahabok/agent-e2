# Repository map

Where each thing lives. For people; not indexed. How the parts work together: [ARCHITECTURE.md](ARCHITECTURE.md), section Repository.

## Root
| File | For |
|---|---|
| [README.md](README.md) | What Agent E2 is, in one page |
| [MISSION.md](MISSION.md) | Why a small local model can win; requirements; risks |
| [ARCHITECTURE.md](ARCHITECTURE.md) | The whole system: repository, parts, modes, query flow |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | How knowledge is written, placed and tagged |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or change a file |
| [CLAUDE.md](CLAUDE.md) | How Claude works in this repository |
| [SECURITY.md](SECURITY.md) | Security policy |

## Product: deployed to the site
| Folder | Holds |
|---|---|
| `knowledge/` | What Agent E2 reads. The only indexed folder |
| `knowledge/catalog/` | Exact data in YAML: vCenter counters, esxtop fields, thresholds, object model |
| `knowledge/foundations/` | True across VCF components and the Guest OS: units, accounting, thresholds |
| `knowledge/operations-management/` | Pillars across products: `performance/`, `capacity/` |
| `knowledge/vsphere/` | `foundations/`, `technology/<cpu, memory, storage, network, gpu>/`, `object-types/<vm, esxi, cluster>/`, `tools/` |
| `knowledge/vcf-operations/` | What VCF Operations computes: `concepts/`, `kpis/`, `models/`, `metrics/` |
| `knowledge/guest-os/` | Windows and Linux, a separate layer |
| `knowledge/glossary.md` | The agent's vocabulary |
| `knowledge/moved.yaml` | Old file ids → current ids |
| `harness/` | Retrieval, catalog, calculator, flow executor, agent loop, verifier. [README](harness/README.md), [AGENT.md](harness/AGENT.md) |

- Flows (order of checks) sit next to their technology or object, in folders named `troubleshooting/` and `health-check/`. The harness finds them by folder name and gives the agent one index of all flows. List them:

```bash
find knowledge -path '*/troubleshooting/*.md' -o -path '*/health-check/*.md' | sort
```

## Proof: not deployed
| Folder | Holds |
|---|---|
| `benchmark/questions/` | Questions with answer keys. Never indexed |
| `benchmark/runner/` | Runner, judge, retrieval check (`retrieval_eval.py`), config |
| `benchmark/results/` | Run results, `results.csv` |
| `benchmark/*.md` | [design](benchmark/design.md), [models](benchmark/models.md), [live test](benchmark/live-test.md), [retrieval check](benchmark/retrieval-check.md) |

## Project: not deployed
| Folder | Holds |
|---|---|
| `project/plan.md` | Milestones, decisions, open work. Read first |
| `project/author-questions.md` | Questions for the author |
| `project/vocabulary.md`, `project/terms.md` | Writing vocabulary; repository terms |
| `project/sources/` | Source documents. Read-only |
| `project/templates/` | Templates for knowledge files |
| `project/tools/` | `lint.py`, `tags.yaml`, `threshold_inventory.py`, `answered.py`, `link_refs.py` |
| `project/archive/` | Retired documents |
