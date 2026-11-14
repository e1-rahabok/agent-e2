# What counts as overhead

## Prompt
- A capacity report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, vSAN FTT=1 storage, ESXi kernel memory, and VM log files.

Which statements are correct?

- A. ESXi kernel memory belongs in the report as overhead.
- B. VM log files belong in the report as overhead.
- C. VM snapshots belong in the report as overhead.
- D. The spare host kept for vSphere HA belongs in the report as overhead.
- E. The extra copy that vSAN FTT=1 keeps belongs in the report as overhead.
- F. An item is overhead only when it cannot be avoided and it costs performance or resources.
- G. Every item in the report is overhead, because each one consumes host resources.
- H. A capacity buffer is a kind of overhead and belongs on the same line of the report.
- I. A vMotion is overhead, because it can raise the VM's Consumed memory on the destination host.
- J. The VM swap file (.vswp) belongs in such a report as overhead.
- K. The CPU and memory that vSAN processes use on each host are overhead.

## Likely wrong answer
- G: "Yes, everything on that list is overhead: it all eats capacity."

## Expected key points
- Answer: A, B, F, K.
- A is true: the ESXi kernel is not optional and not negligible; it reduces usable capacity.
- B is true: the VM is a layer of its own, and its logs give necessary observability.
- C is false: a snapshot is optional; you choose it for a capability the Guest OS does not have.
- D is false: the HA spare host is optional availability protection.
- E is false: the FTT policy is chosen availability protection (vSAN does not use hardware redundancy); FTT can even be 0.
- F is true: overhead is mandatory and has a negative impact; a capability you choose to use is not overhead, even though it consumes resources.
- G is false: consuming resources does not make an item overhead; three of the five are optional capabilities.
- H is false: buffers (capacity, cost, DR, security) are a separate category from overhead.
- I is false: vMotion is not overhead to the VM; it can change VM metrics on the destination (swapped or compressed pages become regular pages).
- J is false: the swap file enables memory overcommit at ESXi level; it is not overhead.
- K is true: ESXi memory consumed and CPU used by vSAN processes are overhead, although the FTT copy they manage is not.

## Notes
- Tests: Principle: overhead vs not overhead.
- The old key point "not overhead: snapshots, HA spare host, FTT policy" is tested by the false options C, D and E; "not overhead = optional" is in the reason for F and G.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Review 2026-11-14: options J and K hold one fact each; K no longer says the FTT copy is not overhead (that gave away E), J no longer says the log files are overhead (that gave away B).

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
answer_type: deterministic
answer: [A, B, F, K]
misconception: [G]
level: 300                      # author 2026-11-05
object: [cluster, esxi]
tool: [none]
misconception_type: []
knowledge_main: vsphere/architecture/overhead
status: draft
```
