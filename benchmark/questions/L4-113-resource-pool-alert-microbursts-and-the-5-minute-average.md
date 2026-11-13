# Resource pool alert: microbursts and the 5-minute average

## Prompt
- VCF Operations collects every 5 minutes. A cycle holds 15 real-time samples of 20 seconds. The resource pool Web holds 40 VMs with 2 vCPUs each.
- The pool alert "Resource pool CPU contention" uses one symptom set over the VMs of the pool: more than 25% of the VMs must meet both conditions, in the same cycle. Wait cycle 1.
  - Red: highest 20-second vCPU Ready in the cycle above 24%, and CPU Contention (%) of the cycle above 6%.
  - Orange: highest 20-second vCPU Ready above 12%, and CPU Contention (%) above 3%.
- Last cycle (11:05), the data of the pool:
  - 14 VMs sat behind a short CPU storm on their hosts for one 20-second sample each: Ready 80% in that sample, about 0% in the other 14 samples. Co-stop and Other Wait are negligible.
  - 4 VMs had a steady Ready of 7% to 8% in all 15 samples, with 11% as the highest sample.
  - 22 VMs were quiet.
- The infrastructure team asks why it received a notification, and the application owner of Web asks why the red alert did not fire when 14 VMs had 80% Ready.

Which alerts fire for the pool Web in this cycle? Explain how the numbers decide, why the alert needs two conditions, and what the team should check.

## Likely wrong answer
Red fires, because 14 of 40 VMs (35%) had 80% Ready, far over 24%. Or nothing fires, because no VM reached 6% Contention. Both ignore that an 80% sample is diluted to 5.3% over 15 samples, which is under red and over orange.

## Expected key points
- Orange fires, red does not.
- The 5-minute value of one 80% sample is 80 / 15 = 5.3% Ready (Contention is at least the Ready, with negligible other terms, so about 5.3%). That is above the orange 3% and below the red 6%. The highest sample (80%) is above both 24% and 12%.
- Orange: the 14 VMs hit by the storm meet both conditions, 14 of 40 = 35%, over 25%, so orange fires. Red: no VM meets both red conditions, so 0 of 40.
- The 4 steady VMs do not count: their highest sample, 11%, is under the orange 12%, although their 5-minute Ready (7% to 8%) is high. A condition on the 5-minute value alone would count them and miss the burst; a condition on the 20-second peak alone would fire on any one-off frozen sample.
- Two conditions: the peak shows an acute stall that a 5-minute average dilutes 15 times; the 5-minute value shows it was not a single sample. Together they fire on bursts that are big enough to move the average.
- Orange goes to the infrastructure team only; red would also go to the application team (receivers follow the severity). The application owner is correctly not alerted: the VMs recovered inside the cycle.
- Check: 14 VMs hit in the same 20-second sample point to one common cause (a burst on the hosts: a batch job, a vMotion or backup storm, another pool), not to a steady lack of CPU in the pool. Look at the time alignment, the hosts and the busiest VMs of that sample, and follow the VM CPU contention flow for the VMs hit; do not add vCPUs.

## Notes
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
answer_type: judged
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
