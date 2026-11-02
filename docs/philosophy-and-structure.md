# Philosophy and Structure

## Why this repository exists

Most documentation-based AI systems end up as shallow metric dictionaries. They can retrieve a counter definition but cannot reason about *why* the counter behaves the way it does, how it relates to architecture, or how an experienced admin actually thinks.

This repository is an attempt to codify **depth of understanding**, not just facts.

The ultimate goal is an AI assistant that can support real vSphere / VCF administrators with the same quality of reasoning that a seasoned human expert would provide.

## Core Philosophy

1. **Architecture and mental models first**  
   Performance counters are a byproduct. Real mastery comes from understanding how the system works.

2. **Preserve nuance**  
   The same counter name can mean different things on a Host versus a VM. Naming is inconsistent across the industry. Thresholds are rarely universal. These nuances must be explicitly captured.

3. **Cross-cutting foundations matter**  
   Concepts such as “Metrics as accounting”, “VM vs Guest OS”, and “Overhead vs feature” apply across CPU, Memory, Storage, and Network. They deserve their own layer.

4. **Real admin behavior > clean textbook questions**  
   Administrators often submit screenshots, diagrams, or logs and simply say “Explain the problem.” The evaluation system must reflect this reality.

5. **Written for humans first**  
   The repository should feel natural to veteran vSphere admins. AI retrieval is a secondary (but important) concern.

## Why the structure looks the way it does

```text
knowledge/
├── raw-input/                 ← Original source materials (book, diagrams, decks)
├── vsphere/
│   ├── foundations/            ← Cross-cutting mental models
│   ├── cpu/ memory/ storage/ network/
│   │   ├── architecture/
│   │   ├── resource-management/
│   │   ├── counters/host/ and counters/vm/
│   │   └── interpretation/
│   ├── troubleshooting/
│   └── glossary/
```

### Reasoning behind key decisions

| Decision | Why |
|----------|-----|
| Separate `foundations/` | Deep conceptual material (e.g. Metrics Nuances) does not belong under a single resource area. |
| Split counters into `host/` and `vm/` | The same counter name often has different meaning and interpretation depending on the object type. Mixing them destroys clarity. |
| `architecture/` + `resource-management/` before counters | Forces the knowledge base to capture *why* before *what*. |
| `raw-input/` at the knowledge root | Source documents often cut across components. Keeping them separate from derived structured knowledge avoids confusion. |
| Evaluation supports screenshots, diagrams, logs | Matches how real admins actually interact with tools. |

## Limitations (honest)

- Turning deep human expertise into structured files is lossy. Some tacit knowledge is extremely hard to codify.
- The AI does not “understand” the way a human expert does. It retrieves and recombines. High-quality structure and golden cases improve the *appearance* and usefulness of understanding, but it remains statistical pattern matching at its core.
- Maintaining consistency as the knowledge base grows requires discipline. Without regular review, quality will drift.
- Multi-modal inputs (screenshots, diagrams) currently rely on good textual descriptions or future vision capabilities. Pure image understanding is still limited in local/offline setups.
- Coverage is incomplete. This is intentional — we prefer depth in the areas we have touched over shallow coverage of everything.

## How to improve this repository

1. **Add depth before breadth**  
   Prefer one excellent architectural explanation over twenty shallow counter definitions.

2. **Keep Host and VM perspectives strictly separated**  
   Never mix them in the same file.

3. **Use real cases for evaluation**  
   Generate golden cases from the live lab and from actual operational problems.

4. **Document tribal knowledge**  
   If something is only known by experienced admins, write it down explicitly (with appropriate caveats).

5. **Review and prune**  
   Outdated or low-quality files should be improved or removed. Volume is not a virtue.

6. **Preserve the author’s voice when extracting from the book**  
   The value of the source material is often in the thinking style, not just the facts.

## Relationship to RAG / AI systems

This repository is deliberately organized so that a Retrieval-Augmented Generation system can:

- Pull the right conceptual foundation before diving into specific counters
- Distinguish Host vs VM perspectives
- Retrieve interpretation patterns rather than isolated definitions
- Be evaluated against realistic admin interactions

The structure is a compromise between human readability and machine retrievability. When the two conflict, we currently bias toward human clarity and explicitness.
