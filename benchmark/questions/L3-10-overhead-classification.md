# What counts as overhead

## Prompt
- A capacity report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, vSAN FTT=1 storage, ESXi kernel memory, and VM log files.

Is this classification correct?

## Likely wrong answer
"Yes, all of these are overhead."

## Expected key points
- **Overhead** = mandatory (cannot be avoided) **and** has negative impact.
- **Not overhead** = optional, and brings a capability you choose to use.
- Overhead: ESXi kernel, VM log files (also VMM overhead, vSAN processes' CPU/memory).
- Not overhead: VM snapshots, HA spare host, vSAN FTT policy.
- Buffers (capacity, cost, DR, security) are a separate category again.
- Bonus: vMotion is not overhead, but can raise VM Consumed on the destination (swap or compressed pages become regular pages).

## Notes
- Previous id: vsphere-foundations-004 (renamed 2026-11-05).
- Tests: Principle: overhead vs not overhead.

## Metadata
```yaml
id: "0017"
title: "What counts as overhead"
product: [vsphere]
technology: [system]
input: [text]
task: decide-capacity
knowledge:
  - vsphere/architecture/overhead
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Overhead vs Not Overhead."
answer_type: judged
level: 300                      # author 2026-11-05
object: [cluster, esxi]
tool: [none]
knowledge_main: vsphere/architecture/overhead
misconception_type: []
status: draft
```
