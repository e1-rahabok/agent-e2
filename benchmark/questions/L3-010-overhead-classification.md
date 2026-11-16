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
- G. Anything that consumes host resources is overhead.
- H. A capacity buffer is a kind of overhead and belongs on the same line of the report.
- I. A vMotion is overhead to the VM it moves.
- J. The VM swap file (.vswp) belongs in such a report as overhead.
- K. The CPU and memory that vSAN processes use on each host are overhead.

## Answers
A, B, F, K

## Explanation
- A is correct: the ESXi kernel is not optional and not negligible; it reduces usable capacity.
- B is correct: the VM is a layer of its own, and its logs give necessary observability.
- C is wrong: a snapshot is optional; you choose it for a capability the Guest OS does not have.
- D is wrong: the HA spare host is optional availability protection.
- E is wrong: the FTT policy is chosen availability protection (vSAN does not use hardware redundancy); FTT can even be 0.
- F is correct: overhead is mandatory and has a negative impact; a capability you choose to use is not overhead, even though it consumes resources.
- G is wrong: consuming resources does not make an item overhead; a capability you choose (three of the five items) consumes resources and is still not overhead.
- H is wrong: buffers (capacity, cost, DR, security) are a separate category from overhead.
- I is wrong: vMotion is not overhead to the VM. It can change VM metrics on the destination (swapped or compressed pages can become regular pages), which is a metric effect, not overhead.
- J is wrong: the swap file enables memory overcommit at ESXi level; it is not overhead.
- K is correct: ESXi memory consumed and CPU used by vSAN processes are overhead, although the FTT copy they manage is not.
- Misconception: G: "Everything on that list is overhead: it all eats capacity."

## Notes
- Tests: principle, overhead vs not overhead.
- Open (2026-11-15 audit): the key rests on the knowledge base's definition of overhead (mandatory and with a negative impact), which the prompt does not state (design.md 6.1, F3). Stating it does not settle B: vSphere 9.1 lets VM logging be turned off (vSphere Virtual Machine Administration, Enable Virtual Machine Logging, PDF p. 1024), so "cannot be avoided" reads B as false while overhead.md lists VM log files as overhead. Options left unchanged for the author's decision.

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
misconception: [G]
level: 300                      # author 2026-11-05
object: [cluster, esxi]
tool: [none]
misconception_type: []
knowledge_main: vsphere/architecture/overhead
status: draft
```
