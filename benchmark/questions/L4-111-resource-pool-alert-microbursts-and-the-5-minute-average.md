# Resource pool alert: microbursts and the 5-minute average

## Prompt
- VCF Operations collects every 5 minutes. A cycle holds 15 real-time samples of 20 seconds. The resource pool Web holds 40 VMs with 2 vCPUs each.
- The pool alert "Resource pool CPU contention" uses one symptom set over the VMs of the pool: more than 25% of the VMs must meet both conditions, in the same cycle. Wait cycle 1.
  - Red: highest 20-second vCPU Ready in the cycle above 24%, and CPU Contention (%) of the cycle above 6%.
  - Orange: highest 20-second vCPU Ready above 12%, and CPU Contention (%) above 3%.
- Last cycle (11:05), the data of the pool:
  - 14 VMs, spread over four hosts, show Ready 80% on both vCPUs in the same 20-second sample (11:02:40) and about 0% in the other 14 samples; CPU Ready for the cycle about 5.3%.
  - 4 VMs had a steady Ready of 7% to 8% in all 15 samples; their highest 20-second vCPU Ready (the worst vCPU) was 11%.
  - Co-stop, Overlap and Other Wait are negligible on every VM of the pool.
  - 22 VMs were quiet.
- The application owner of Web sees that 14 VMs had 80% Ready and asks which pool alerts fired in this cycle, and why.

Which statements are correct?

- A. The red alert fires, because 14 of 40 VMs (35%) had 80% Ready in a sample, far above 24%.
- B. The orange alert fires for the pool; the red alert does not.
- C. The 4 VMs with a steady 7% to 8% Ready count toward red, since their 5-minute value is above 6%.
- D. No alert fires, because averaging over the cycle leaves those 14 VMs with too little Ready.
- E. The 4 steady VMs count toward neither alert, because their highest vCPU Ready, 11%, is below 12%.
- F. The 80% sample shows that these VMs waited for CPU for most of the 5-minute cycle.
- G. A VM's highest 20-second vCPU Ready can be more than 15 times its 5-minute VM-level Ready.
- H. The 5-minute condition keeps one short spike from firing the alert unless it moves the cycle's value.
- I. 14 VMs hit in the same 20-second sample point to one common cause on the hosts, not a steady CPU shortage.
- J. The remedy is to add vCPUs to the 14 VMs hit at 11:02:40, so they ride out the next such sample.

## Likely wrong answer
- A: "Red fires: 35% of the VMs had 80% Ready, far over 24%."
- D: "Nothing fires: once averaged over 5 minutes the storm is gone."

## Expected key points
- Answer: B, E, G, H, I.
- A is wrong: the misconception; red also needs CPU Contention above 6%, and the 14 VMs reach only about 5.3% (Contention is Ready plus Co-stop, Overlap and Other Wait, all negligible here). No VM meets both red conditions: 0 of 40.
- B is correct: the 14 VMs hit at 11:02:40 meet both orange conditions (peak 80% above 12%, Contention about 5.3% above 3%): 14 of 40 = 35%, over 25%. For red, 5.3% is below 6%.
- C is wrong: their highest sample, 11%, is below the red 24% (and the orange 12%), so they fail the peak condition. A condition on the 5-minute value alone would count them and miss the burst.
- D is wrong: the misconception; 5.3% is above the orange 3%, and the peak (80%) is above both 12% and 24%.
- E is correct: both conditions must hold for the same VM in the same cycle; a steady 7% to 8% with an 11% peak vCPU Ready fails the orange peak value of 12%.
- F is wrong: one sample is 20 seconds; the VMs were near 0% Ready in the other 14 samples and recovered inside the cycle.
- G is correct: for one series the peak is at most 15 times the 5-minute average, but the VM's peak is taken across its vCPUs while the 5-minute value is the VM-level average, so the gap can exceed 15 times (one vCPU stalled, the other idle).
- H is correct: the sustained condition shows the burst was big enough to move the cycle's value, so a one-off frozen sample alone does not fire the alert.
- I is correct: many VMs hit in the same sample point to a burst on the hosts (a batch job, a vMotion or backup storm, another pool); check the time alignment, the hosts and the busiest VMs of that sample, and follow the VM CPU contention flow for the VMs hit.
- J is wrong: adding vCPUs to a VM with CPU contention makes co-scheduling harder and can raise Ready and Co-stop; the cause is a common burst, not the VM size.

## Notes
- 2026-11-16 re-review: the stem no longer calls the event "a short CPU storm on their hosts" (an interpretation that handed over I); it gives the sample time and the host count only.
- The burst hit both vCPUs of each of the 14 VMs in the same 20-second sample, so the VM-level Ready of that sample is 80%; its 5-minute value (80 / 15 = 5.3%) is given in the stem, as the dilution fact is tested by 0047 and 0432. Overlap is named as negligible, because CPU Contention (%) adds Overlap to Ready, Co-stop and Other Wait (vsphere/technology/cpu/metrics/virtual-motherboard/contention). The 4 steady VMs' 11% is the worst vCPU's 20-second Ready.
- Public source: Real-time statistics are sampled every 20 seconds, and the 5-minute (past day) interval rolls up 15 samples (vSphere Monitoring and Performance, "Data Collection Intervals", Broadcom TechDocs, vSphere 9.0). VCF Operations Ready (%) definition: Ready as a share of the sample interval.
- Knowledge file logic: vsphere/object-types/resource-pool/resource-pool-alerts, "Resource pool CPU contention": "a burst (VM Peak vCPU Ready) and sustained contention (VM CPU Contention) together"; vcf-operations/features/peak-20-second-metrics: the peak is the highest of the 15 20-second values, across instances.
- I is a lead (look for a common cause on the hosts), not a cause the prompt fixes.
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- 2026-11-15 audit: the 5.3% cycle value moved into the stem; old B (80 / 15 = 5.3%) dropped and old H (the 15x dilution) replaced by G (a peak across vCPUs can exceed 15x), as the dilution fact is over the cap. Letters: A unchanged; B dropped; C -> B; D -> C; E -> D; F -> E; G -> F; H -> G (new text); I -> H; J -> I; K -> J.

## Metadata
```yaml
id: "0341"
title: "Resource pool alert: microbursts and the 5-minute average"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, E, G, H, I]
misconception: [A, D]
input: [text]
object: [resource-pool, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/resource-pool/resource-pool-alerts
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/object-types/vm/vm-alerts
knowledge_main: vsphere/object-types/resource-pool/resource-pool-alerts
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-13"
misconception_type: [rollup-and-interval, average-hides-worst]
status: draft
```
