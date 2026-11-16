# What counts as overhead

## Prompt
- You're the VMware Architect, who plan and design your company private cloud. Your IT Leadership forwarded a capacity audit report, that raises a concern that your private cloud has a high degree of overhead.
- The report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, VM swap files, ESXi kernel memory, and VM log files.

Which statements are correct?

- A. ESXi kernel memory belongs in the report as overhead.
- B. VM log files belong in the report as overhead. It is an additional files that the Guest OS wouldn't have generated if it were a physical server.
- C. VM snapshots belong in the report as overhead.
- D. The spare host kept for vSphere HA belongs in the report as overhead.
- E. The kernel memory reservation of a host is the size of the kernel's overhead and goes in the report as that figure.
- F. An item is overhead only when it cannot be avoided and it costs performance or resources.
- G. Anything that consumes host resources is overhead.
- H. A capacity buffer is a kind of overhead and belongs on the same line of the report.
- I. A vMotion is overhead to the VM it moves.
- J. The VM swap file (.vswp) belongs in such a report as overhead.
- K. The CPU and memory that the VM Monitor uses for each VM are overhead.

## Answers
A, B, F, K

## Explanation
- A is correct: the ESXi kernel is not optional and not negligible; it reduces usable capacity.
- B is wrong: the VM is a layer of its own, and its logs give necessary observability. While it is an overhead, it is not a virtualization overhead as physical servers would have similar log. It is a replacement, not an addition. Virtualization technology does not add a new type of logs. It merely changes the content.
- C is wrong: a snapshot is optional; you choose it for a capability the Guest OS does not have.
- D is wrong: the HA spare host is optional availability protection.
- E is wrong: the kernel reservation is a minimum that admission control sets aside, not a measure of what the kernel uses; hypervisor use can pass it or stay far below it.
- F is correct: overhead is mandatory and has a negative impact; a capability you choose to use is not overhead, even though it consumes resources.
- G is wrong: consuming resources does not make an item overhead; a capability you choose (snapshots, the HA spare host and swap files: three of the five items) consumes resources and is still not overhead.
- H is wrong: buffers (capacity, cost, DR, security) are a separate category from overhead.
- I is wrong: vMotion is not overhead to the VM. It can change VM metrics on the destination (swapped or compressed pages can become regular pages), which is a metric effect, not overhead.
- J is wrong: the swap file enables memory overcommit at ESXi level; it is not overhead.
- K is correct: the VM Monitor's CPU and memory for each VM are mandatory and cost resources, although small.
- Misconception: G: "Everything on that list is overhead: it all eats capacity."

## Notes
- Tests: principle, overhead vs not overhead.
- 2026-11-16 (author, Q250: vSAN moves to after 1.0): the vSAN items are out. Stem item "vSAN FTT=1 storage" became "VM swap files"; E (vSAN FTT copy, false) became the kernel reservation read as the overhead figure (false; overhead.md, Misconceptions); K (vSAN processes, true) became the VM Monitor's per-VM CPU and memory (true; overhead.md, Overhead table). Key unchanged: A, B, F, K. The vSAN lines of overhead.md stay until the vSAN content is written after 1.0.
- VM log files (B): vSphere 9.1 lets VM logging be turned off, but the vSphere 9.1 documentation (p. 228, advanced configuration parameters, `logging`) says not to, because it makes support difficult or impossible; so the logs are mandatory in practice and cost disk space and IO. B stays true (author question Q250, the logging part, is open).
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
