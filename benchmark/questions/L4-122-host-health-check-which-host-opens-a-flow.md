# Host health check: which of four hosts opens a troubleshooting flow

## Prompt
- Cluster prod-cl03: four identical ESXi 9.1 hosts, 2 sockets of 32 cores, Hyper-Threading off, 1 TB of memory each. DRS fully automated. Between 10:00 and 11:00 no user has complained.
- The scheduled host health check reads these values for the hour. The VM columns show the worst VM on the host, taken at the 20-second peak.

| Host | Core Utilization | Host CPU Ready (average of its VMs) | Worst VM: Ready / Net Run | Memory Consumed | Balloon | Memory state | Worst VM memory Contention | Worst VM peak disk latency |
|---|---|---|---|---|---|---|---|---|
| esx-01 | 88% | 0.4% | 1.2% / 92% | 62% | 0 | clear | 0% | 14 ms |
| esx-02 | 31% | 0.8% | 22% / 30% | 55% | 0 | clear | 0% | 9 ms |
| esx-03 | 64% | 0.3% | 0.9% / 70% | 94% | 0 | clear | 0% | 11 ms |
| esx-04 | 57% | 0.2% | 0.8% / 55% | 99.4% | 14 GB | soft | 0% | 12 ms |

- On esx-02, the worst VM has 8 vCPUs and sits in a resource pool with a CPU limit. The other 11 VMs of esx-02 show Ready below 0.3%.

Which reading of the check is correct?

- A. esx-01 first: at 88% it is the busiest host, so its CPU flow opens, and the other three hosts are healthy.
- B. esx-02 opens the CPU contention flow, starting from limits and resource pools; esx-04 is a capacity warning; esx-01 and esx-03 have no finding.
- C. esx-03 opens the memory flow because Consumed is 94%, and esx-02 is a capacity issue because its average Ready is low.
- D. esx-02 and esx-04 both open a flow: a ballooning host is already short of memory, and esx-02 needs another host added to the cluster.
- E. No host opens a flow: every host Ready average is below 1%, so the four hosts are healthy and only esx-01 needs a capacity note.

## Likely wrong answer
A (busiest host first) or D (balloon read as a current wait).

## Expected key points
- Answer: B.
- A host is a provider: its contention is its VMs' contention. Read performance from the worst VM at the 20-second peak, not from the host average (E is wrong: esx-02's average of 0.8% hides one VM at 22% Ready against 30% Run, which is about 42% of the time it wanted to run).
- esx-01 at 88% Core Utilization with its worst VM at 1.2% Ready against 92% Run: the host works hard and serves its VMs. That is a capacity reading, not a performance one (A is wrong).
- esx-02 has the lowest utilization and the only contention: the cause is not load. The flow starts at the configuration items that create contention without load: the CPU limit or the resource pool of the worst VM, then shares, then NUMA placement. Adding a host does not remove a limit (D is wrong on the second half).
- Memory Consumed holds guest cache, so 94% or 99.4% alone is not a problem (C is wrong). esx-04 shows the leading warnings, Balloon and the soft state: ESXi is reclaiming. Past reclamation is not a wait: the worst VM memory Contention is 0%. It goes to the capacity step as a warning, with the swap-in and compression counters to watch.
- The order inside the host check is contention (through the worst VM), then consumption, then configuration, then capacity.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1 (revision 20260624) on esxtop CPU load readings as utilization levels; Broadcom TechDocs vSphere 9.1 Monitoring and Performance for the ESXi memory states and counters; the esxtop %RDY description (the ready time includes time held back by a CPU limit, shown as %MLMTD). Soft state: ballooning starts (same fact as the host memory state question 0144).
- Why one answer: only one VM waits (Ready 22% against Run 30%), and the vendor definitions make the other findings either utilization (esx-01, esx-03) or reclamation without wait (esx-04).
- Debatable risk: moderate on the wording "capacity warning" for esx-04. The question does not ask what to do about it, only that it is not a contention flow; B is the only option that matches the table. Whether esx-04 deserves action at all is left out.
- Rests on: the design logic of the ESXi health check (Principle: provider, worst VM, utilization is capacity; Interpretation: contention with low utilization points to limits and placement) and the vendor definitions above.

## Metadata
```yaml
id: "0352"
title: "Host health check: which of four hosts opens a troubleshooting flow"
product: [vsphere]
technology: [cpu, memory, storage, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/esxi/esxi-health-check
  - vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
  - vsphere/technology/memory/metrics/comparisons/host-memory-metrics
  - vsphere/architecture/provider-consumer
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/esxi/esxi-health-check
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, D]
misconception_type: [average-hides-worst, consumption-as-contention, reclamation-as-contention, provider-vs-consumer]
status: draft
```
