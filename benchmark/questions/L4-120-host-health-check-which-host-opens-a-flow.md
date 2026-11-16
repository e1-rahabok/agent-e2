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

Which readings of the check are correct?

- A. Only esx-02 needs any step: the other three hosts are up and none of their VMs waits, so they are healthy.
- B. esx-02 opens the CPU contention flow, from limits and resource pools; esx-04 goes to capacity as a warning; esx-01 and esx-03 open no flow.
- C. esx-03 opens the memory flow because Consumed is 94%, and esx-02 is a capacity issue because its average Ready is low.
- D. No host opens a flow: every host Ready average is below 1%, so the four hosts are healthy and only esx-01 needs a capacity note.

## Likely wrong answer
A: the hosts with no waiting VM are read as healthy, and the capacity readings of esx-01 and esx-04 are dropped.

## Expected key points
- Answer: B.
- A is wrong: no wait is present health only; esx-01 at 88% Core Utilization is a capacity reading and esx-04, reclaiming memory (Balloon, soft state), goes to the capacity step as a warning. Capacity and configuration are risk, read apart from present health.
- B is correct: esx-02 has the lowest utilization and the only contention (worst VM 22% Ready against 30% Run), so the cause is not load: the flow starts at the CPU limit or resource pool of that VM, then shares, then NUMA placement. esx-04's balloon and soft state are reclamation, not a wait (worst VM memory Contention 0%): a capacity warning. esx-01 works hard and serves its VMs (1.2% Ready against 92% Run), a capacity reading handed to the cluster check; esx-03 has no finding. Neither opens a troubleshooting flow.
- C is wrong: Memory Consumed holds guest cache, so 94% alone is not a problem; and esx-02's low average hides one VM at 22% Ready, a contention finding.
- D is wrong: a host is a provider and its Ready is an average of its VMs; esx-02's 0.8% hides one VM at 22% Ready, about 42% of the time it wanted to run.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1 (revision 20260624) on esxtop CPU load readings as utilization levels; Broadcom TechDocs vSphere 9.1 Monitoring and Performance for the ESXi memory states and counters; the esxtop %RDY description (the ready time includes time held back by a CPU limit, shown as %MLMTD). Soft state: ballooning starts.
- Only one VM waits (Ready 22% against Run 30%), and the vendor definitions make the other findings either utilization (esx-01, esx-03) or reclamation without wait (esx-04).
- Rests on: esxi-health-check (provider, worst VM, utilization is capacity; contention with low utilization points to limits and placement; present health is not health).
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- 2026-11-15 audit: B reworded to "open no troubleshooting flow" (esx-01 at 88% is a capacity reading, so "no finding" was arguable); old A (busiest host first) replaced by the present-health misconception, as 0019 and 0431 keep the utilization-is-not-contention fact; old D (balloon read as a wait) dropped, as 0149 and 0392 keep it. Letters: A new text; B, C unchanged; D dropped; E -> D.

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
source_path: "Synthetic, 2026-11-13"
answer: [B]
misconception: [A]
misconception_type: [average-hides-worst, consumption-as-contention, provider-vs-consumer]
status: draft
```
