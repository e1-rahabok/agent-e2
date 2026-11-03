# What counts as overhead

## Prompt
A capacity report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, vSAN FTT=1 storage, ESXi kernel memory, and VM log files. Is this classification correct?

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
- Tests: Principle: overhead vs not overhead.

## Metadata
```yaml
id: vsphere-foundations-004
title: "What counts as overhead"
scope: vsphere
area: foundations
input: text
tests: concept
knowledge:
  - vsphere/foundations/overhead
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Overhead vs Not Overhead."
format: free-text
status: draft
```
