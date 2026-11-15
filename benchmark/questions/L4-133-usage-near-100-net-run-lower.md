# CPU Usage near 100%, a request for more vCPUs

## Prompt
- The owner of a 4-vCPU VM asks for 2 more vCPUs: "VCF Operations shows the CPU maxed out every afternoon this week."
- See [the VCF Operations chart](0371/vcf-operations-vm-cpu-7-days.png) of the VM for the last 7 days.
- The host runs the Balanced power policy with Turbo Boost on.

Which statements are correct?

- A. Usage (%) above Net Run comes from Turbo Boost: Usage counts cycles against the base clock.
- B. Usage at or above 100% shows the vCPUs ran without a pause at those hours.
- C. Net Run is the share of time the vCPUs ran, less the time the kernel interrupted them.
- D. For sizing the guest's vCPUs, Net Run is a better input than Usage.
- E. CPU Demand is the counter to size on, since it adds the CPU the VM asked for and did not get.
- F. Usage has no use once Net Run is available: drop it from the VM's views.
- G. Ready and Co-stop stay low on the chart: the vCPUs rarely waited for a physical thread.
- H. Add the 2 vCPUs: the VM runs at its limit every afternoon.
- I. Net Run can pass 100% with Turbo Boost, just as Usage does.
- J. Before any change to the vCPU count, check the guest's CPU run queue at the busy hours.
- K. On the chart, Net Run reaches 100% at the afternoon peaks.
- L. At the afternoon peaks, Usage sits 20 points or more above Net Run.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1. Host power policy Balanced, Turbo Boost on in the BIOS.
- Object: one VM with 4 vCPUs, no CPU limit.
- Screen, VCF Operations > the VM > Metrics: CPU|Usage (%), CPU|Net Run (%), CPU|Ready (%), CPU|Co-stop (%) on one chart, last 7 days, 5-minute points, with the values of one afternoon peak visible on hover. Save as `0371/vcf-operations-vm-cpu-7-days.png`.
- How to produce it in a lab: run a 3-thread CPU burner in the 4-vCPU guest each afternoon (or a steady load that keeps each vCPU about three quarters busy) on a host with enough free cores that the cores run at All-Core Turbo; keep other load low so Ready stays low.
- Condition the key depends on: at the afternoon peaks, Usage (%) 100-115% and Net Run (%) 72-82%, Usage at least 20 points above Net Run; Ready (%) below 1% and Co-stop (%) below 0.5% throughout.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B or H: Usage at about 100% means the VM is at its limit, so add vCPUs.

## Expected key points
- Answer: A, C, D, G, J, L.
- A true: Usage (MHz and %) counts cycles completed, against the base clock; Turbo pushes it above the time-based counters.
- B false: the misconception. Net Run at 72-82% shows the vCPUs were idle a fifth to a quarter of the time.
- C true: Net Run = Run - Overlap; it counts time, not speed.
- D true: the guest is sized in vCPUs of run time; Usage moves with frequency and Hyper-Threading.
- E false: Demand is an internal counter of the scheduler, in MHz, and moves with the clock speed like Usage; it is not unmet demand (under a limit it equals Usage) and not the guest's need.
- F false: over-correction. Usage is the throughput counter: the one to read for speed, not for sizing.
- G true: reading. Ready below 1% and Co-stop below 0.5%: the vCPUs were rarely held back.
- H false: wrong action. The vCPUs have idle time left; the extra points of Usage are clock speed.
- I false: Net Run is time-based and cannot pass 100%.
- J true: the guest run queue is the primary sign that the guest cannot keep up; it decides whether more vCPUs help.
- K false: reading. Net Run peaks at 72-82%.
- L true: reading. The gap is 20 points or more: frequency, not work.

## Reasoning path
1. Compare Usage with Net Run at the peaks: the gap is frequency.
2. Read Ready and Co-stop: no wait.
3. Size on Net Run and the guest run queue, not on Usage.

## Notes
- Paired with the theory question 0008 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C6). Counts only after author approval.
- Review 2026-11-15: Co-stop added to the screen and the condition (G now reads both waits); screen readings K (false) and L (true) added; stem no longer quotes a value; condition ranges moved off knowledge-base examples. Key changed from A, C, D, G, J to A, C, D, G, J, L.

## Metadata
```yaml
id: "0371"
title: "CPU Usage near 100%, a request for more vCPUs"
product: [vsphere, vcf-operations]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
  - guest-os/system/guest-os-sizing
  - sp5-framework/capacity/rightsizing
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/net-run
attachments:
  - 0371/vcf-operations-vm-cpu-7-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C6"
answer: [A, C, D, G, J, L]
misconception: [B, H]
misconception_type: [frequency-and-hyper-threading]
pair: "0008"
status: awaiting-input
```
