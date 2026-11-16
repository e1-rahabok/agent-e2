# What counts as overhead

## Prompt
- You're the VMware Architect, who plan and design your company private cloud. Your IT Leadership forwarded a capacity audit report, that raises a concern that your private cloud has a high degree of overhead.
- The report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, VM swap files, ESXi kernel memory, and VM log files.

Which statements are correct?

- A. ESXi kernel memory belongs in the report as overhead.
- B. VM log files belong in the report as virtualization overhead.
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
A, F, J, K

## Explanation
- A is correct: the ESXi kernel is not optional and not negligible; it reduces usable capacity.
- B is wrong: the logs are mandatory in practice and cost disk and IO, but a physical server has its own logs. They replace logs; virtualization adds no new kind. They belong to Enterprise Readiness (observability), not to virtualization overhead.
- C is wrong: a snapshot is optional; you choose it for a capability the Guest OS does not have.
- D is wrong: the HA spare host is Enterprise Readiness (availability): required by policy and sized by it (N+1 or N+2), and a physical cluster needs spare servers too. It is not added by virtualization.
- E is wrong: the kernel reservation is a minimum that admission control sets aside, not a measure of what the kernel uses; hypervisor use can pass it or stay far below it.
- F is correct: virtualization overhead is mandatory, has a negative impact and is added by virtualization; a capability you choose, or a requirement the enterprise sets, is not, even though it consumes resources.
- G is wrong: consuming resources does not make an item overhead; a capability you choose (snapshots, the HA spare host and VM log files: three of the five items) consumes resources and is still not overhead.
- H is wrong: buffers (capacity, cost, DR, security) are a separate category from overhead and from Enterprise Readiness.
- I is wrong: vMotion is not overhead to the VM. It can change VM metrics on the destination (swapped or compressed pages can become regular pages), which is a metric effect, not overhead.
- J is correct: ESXi creates the swap file at power-on, sized configured memory minus reservation, and it costs datastore space whether or not the host is overcommitted. A physical server has none. It is mandatory, costs resources and is added by virtualization; the overcommit it enables does not make it optional.
- K is correct: the VM Monitor's CPU and memory for each VM are mandatory and cost resources, although small.
- Misconception: G: "Everything on that list is overhead: it all eats capacity."

## Notes
- Tests: principle, overhead vs not overhead.
- 2026-11-16 (author, Q250: vSAN moves to after 1.0): the vSAN items are out. Stem item "vSAN FTT=1 storage" became "VM swap files"; E (vSAN FTT copy, false) became the kernel reservation read as the overhead figure (false; overhead.md, Misconceptions); K (vSAN processes, true) became the VM Monitor's per-VM CPU and memory (true; overhead.md, section Virtualization overhead). Key then: A, B, F, K (B since changed, next note). The vSAN lines of overhead.md stay until the vSAN content is written after 1.0.
- 2026-11-16 (author, Q250): VM log files (B) are not virtualization overhead: physical servers have their own logs. They sit in Enterprise Readiness in overhead.md (mandatory by policy, not added by virtualization). The stem says "virtualization overhead", the term the key tests.
- 2026-11-16 (author, swap file question): the VM swap file (J) is virtualization overhead: mandatory, costs datastore space, no physical equivalent. Key A, F, J, K.

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
