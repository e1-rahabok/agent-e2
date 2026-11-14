# Resource pool alert: microbursts and the 5-minute average

## Prompt
- VCF Operations collects every 5 minutes. A cycle holds 15 real-time samples of 20 seconds. The resource pool Web holds 40 VMs with 2 vCPUs each.
- The pool alert "Resource pool CPU contention" uses one symptom set over the VMs of the pool: more than 25% of the VMs must meet both conditions, in the same cycle. Wait cycle 1.
  - Red: highest 20-second vCPU Ready in the cycle above 24%, and CPU Contention (%) of the cycle above 6%.
  - Orange: highest 20-second vCPU Ready above 12%, and CPU Contention (%) above 3%.
- Last cycle (11:05), the data of the pool:
  - 14 VMs sat behind a short CPU storm on their hosts in the same 20-second sample: Ready 80% on both vCPUs in that sample, about 0% in the other 14 samples. Co-stop and Other Wait are negligible.
  - 4 VMs had a steady Ready of 7% to 8% in all 15 samples, with 11% as the highest sample.
  - 22 VMs were quiet.
- The application owner of Web sees that 14 VMs had 80% Ready and asks which pool alerts fired in this cycle, and why.

Which statements are correct?

- A. The red alert fires, because 14 of 40 VMs (35%) had 80% Ready in a sample, far above 24%.
- B. One 80% sample among 15 gives a 5-minute Ready of about 5.3%.
- C. The orange alert fires for the pool; the red alert does not.
- D. The 4 VMs with a steady 7% to 8% Ready count toward red, since their 5-minute value is above 6%.
- E. No alert fires, because averaging over the cycle leaves the storm VMs with too little Ready.
- F. The 4 steady VMs count toward neither alert, because their highest sample, 11%, is below 12%.
- G. The 80% sample shows that these VMs waited for CPU for most of the 5-minute cycle.
- H. The 20-second peak condition catches a stall that the 5-minute average dilutes about 15 times.
- I. The 5-minute condition keeps one short spike from firing the alert unless it moves the cycle's value.
- J. 14 VMs hit in the same 20-second sample point to one common cause on the hosts, not a steady CPU shortage.
- K. The remedy is to add vCPUs to the 14 VMs that the storm hit, so they ride out the next one.

## Likely wrong answer
- A: "Red fires: 35% of the VMs had 80% Ready, far over 24%."
- E: "Nothing fires: once averaged over 5 minutes the storm is gone."

## Expected key points
- Answer: B, C, F, H, I, J.
- A is false: the misconception; red also needs CPU Contention above 6%, and the storm VMs reach only about 5.3%. No VM meets both red conditions: 0 of 40.
- B is true: 80 / 15 = 5.3% Ready over the cycle; with Co-stop and Other Wait negligible, CPU Contention is about 5.3% too (it is never below Ready).
- C is true: the 14 storm VMs meet both orange conditions (peak 80% above 12%, Contention 5.3% above 3%): 14 of 40 = 35%, over 25%. For red, 5.3% is below 6%.
- D is false: their highest sample, 11%, is below the red 24% (and the orange 12%), so they fail the peak condition. A condition on the 5-minute value alone would count them and miss the burst.
- E is false: the misconception; 5.3% is above the orange 3%, and the peak (80%) is above both 12% and 24%.
- F is true: both conditions must hold for the same VM in the same cycle; a steady 7% to 8% with an 11% peak fails the orange peak value of 12%.
- G is false: one sample is 20 seconds; the VMs were near 0% Ready in the other 14 samples and recovered inside the cycle.
- H is true: a 5-minute average dilutes one 20-second sample 15 times; the peak keeps the acute stall visible.
- I is true: the sustained condition shows the burst was big enough to move the cycle's value, so a one-off frozen sample alone does not fire the alert.
- J is true: many VMs hit in the same sample point to a burst on the hosts (a batch job, a vMotion or backup storm, another pool); check the time alignment, the hosts and the busiest VMs of that sample, and follow the VM CPU contention flow for the VMs hit.
- K is false: adding vCPUs to a VM with CPU contention makes its performance worse; the cause is a common burst, not the VM size.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped key point: which team receives orange and red (infrastructure team red and orange, application team red only). It is the site's alert design, not stated in the prompt, so no option can rest on it. Sharpened stem: the storm hit both vCPUs of each of the 14 VMs in the same 20-second sample, so the VM-level Ready of that sample is 80%. The last bullet no longer says that a notification arrived and red did not fire: in a multiple-choice question that would give the answer away.
- Public source: Real-time statistics are sampled every 20 seconds, and the 5-minute (past day) interval rolls up 15 samples (vSphere Monitoring and Performance, "Data Collection Intervals", Broadcom TechDocs, vSphere 9.0). The arithmetic 80 / 15 follows from the 300 / 20 = 15 samples. VCF Operations Ready (%) definition: Ready as a share of the sample interval.
- Knowledge file logic: vsphere/object-types/resource-pool/resource-pool-alerts, "Resource pool CPU contention": "a burst (VM Peak vCPU Ready) and sustained contention (VM CPU Contention) together"; vcf-operations/features/peak-20-second-metrics: the peak is the highest of the 15 20-second values. Receivers follow vm-alerts (infrastructure team red and orange, application team red only); the pool and ESXi alerts exist so the infrastructure team can act before the application team is alerted.
- Why one answer: with the thresholds in the prompt, the arithmetic leaves exactly one result (orange only), and the reasons for two conditions follow from dilution.
- Debatable risk: the receiver rule is the author's design (a red-only application team alert); the key marks it as part of the design logic and the prompt does not ask for it directly. The remedy (look for a common cause such as a burst on the hosts) is a lead, not a cause the prompt fixes; the judge should accept any equivalent first check of what ran on the hosts in that sample.

## Metadata
```yaml
id: "0341"
title: "Resource pool alert: microbursts and the 5-minute average"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, C, F, H, I, J]
misconception: [A, E]
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
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [rollup-and-interval, average-hides-worst]
status: draft
```
