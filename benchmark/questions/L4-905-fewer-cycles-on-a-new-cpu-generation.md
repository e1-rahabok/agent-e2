# Fewer cycles for the same job on a new CPU generation

## Prompt
- rpt-batch-03, a 4-vCPU VM, runs the same nightly report job on the same data volume every night.
- Until October it ran on cluster old-01: Intel Xeon of 2021, base clock 2.8 GHz. In November it moved to cluster new-01: Intel Xeon 6, base clock 2.0 GHz. Same power policy; both clusters lightly loaded; the vCPU count did not change.
- vCenter, means over the job window, one night on each cluster:

| Reading | old-01 | new-01 |
|---|---|---|
| Job duration | 4 h 00 min | 3 h 20 min |
| VM CPU Usage (MHz) | 8,000 | 7,500 |
| VM CPU Run, per vCPU | 66% | 68% |
| VM CPU Readiness | 0.3% | 0.2% |

- The capacity planner sizes new-01 for the next migration wave from each VM's CPU Usage (MHz) on old-01, against the Total Capacity (GHz) of new-01.

Which statements are correct?

- A. The job did the same work in about 22% fewer CPU cycles on new-01: 25,000 against 32,000 MHz-hours.
- B. The lower base clock of new-01 means that each vCPU completes less work per second than it did on old-01.
- C. VM CPU Usage (MHz) counts cycles, adjusted for frequency and Hyper-Threading, and no counter adjusts for the work per cycle.
- D. The cycle saving must come from Turbo: new-01 runs further above its base clock than old-01 did.
- E. Run of 66% and 68% shows that the VM got about the same CPU performance on both clusters.
- F. Usage (MHz) measured on old-01 is not a like-for-like demand on new-01, as a cycle there does a different amount of work.
- G. Add a vCPU to rpt-batch-03 on new-01 to make up for its lower base clock.
- H. The CPU Latency of the VM on old-01 shows the work per cycle it lost on the older processor.
- I. A vCPU at 2.0 GHz and one at 3.0 GHz that both ran the whole sample show the same Run.

## Likely wrong answer
"The new hosts have a lower clock, so each vCPU does less (B), and the Run is the same, so performance is the same (E)." B and E are the misconceptions.

## Expected key points
- Answer: A, C, F, I.
- A is correct: cycles = Usage × time. old-01: 8,000 MHz × 4 h = 32,000 MHz-hours; new-01: 7,500 MHz × 3.33 h = 25,000 MHz-hours; 25,000 / 32,000 = 0.78, about 22% fewer, for the same job. Each cycle on new-01 did about 1.28 times the work.
- B is wrong: the same job finished 40 minutes sooner on the same 4 vCPUs at about the same Run, so each vCPU completed more work per second. A newer generation does more work per cycle (efficacy), so a lower clock can still run faster.
- C is correct: the cycle count mixes frequency and the Hyper-Threading charge; efficacy, the work per cycle from the core architecture (cache, pipelines, branch prediction), is in no counter.
- D is wrong: Usage (MHz) already counts the cycles at the clock the cores ran, Turbo included. Turbo adds cycles per second; it cannot make the same work take fewer cycles.
- E is wrong: Run is time, not throughput; the work each running second completes depends on frequency, Hyper-Threading and the core architecture.
- F is correct: MHz figures carry the old clock and the old work per cycle; the same MHz is not the same work across CPU generations, so, as rpt-batch-03 shows, old-01 Usage overstates what the same work takes on new-01.
- G is wrong: the job already runs faster on new-01 with Readiness at 0.2%; nothing calls for more vCPUs.
- H is wrong: no metric accounts for efficacy; CPU Latency counts the Hyper-Threading and frequency effects only.
- I is correct: Run is binary per moment (running or not) and counts duration only; the clock speed changes the cycles in Usage, not Run.

## Metadata
```yaml
id: "0447"
title: "Fewer cycles for the same job on a new CPU generation"
product: [vsphere]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [vm, cluster]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/run-time-vs-run-quality
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/concepts/run-time-vs-run-quality
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/concepts/run-time-vs-run-quality"
answer: [A, C, F, I]
misconception: [B, E]
misconception_type: [frequency-and-hyper-threading, unit-and-normalization]
status: draft
```
