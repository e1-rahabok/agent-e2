# Busy but healthy hosts and the loss of one

## Prompt
- Cluster prod-cl07: four identical ESXi 9.1 hosts, 2 sockets of 32 cores, Hyper-Threading off, 1 TB of memory each. DRS fully automated.
- vSphere HA admission control: cluster resource percentage, 25% for CPU and memory. Reservations are small: the VMs reserve 8% of the cluster CPU.
- Over four weeks, in business hours, every host shows Core Utilization of 70% to 74%, flat from day to day. Memory Consumed is 60%.
- On every host, the worst VM shows a 20-second peak Ready below 0.9% while its Net Run stays above 80%. No VM shows memory or disk contention.
- The ESXi health check of each host reads: no contention, high utilization.
- Colleague 1: "72% is below the 80% ceiling in the vendor guidance, so nothing to do." Colleague 2: "Hosts at 72%: add a fifth host."

Give the result of the host health checks and say what each colleague gets right or wrong. What do you hand to the cluster check, and what does it show for the loss of one host?

## Likely wrong answer
"72% is under 80%, so the hosts are fine, no action" (or "the hosts are busy, so they are unhealthy: add capacity now"). Both read host utilization as the answer, and neither does the failure arithmetic.

## Expected key points
- Host result: no performance finding. The worst VM waits about 1% of the time against 80% or more of Run, so the VMs get what they ask for. High utilization with no VM waiting is a capacity reading, not a performance one.
- The 80% reasonable ceiling and 90% warning of Performance Best Practices for vSphere 9.1 (esxtop PCPU) are utilization levels for a host in normal operation, and the document says organizations set their own target. They do not say what happens when a host is lost.
- A host is sized as part of its cluster. With four hosts and one failure to tolerate, the three remaining hosts carry the whole load: 4 x 72% / 3 = 96% Core Utilization, above both esxtop levels. Contention is expected after the failure, even though none exists now.
- HA admission control gives no warning: with the percentage policy it compares reservations (8% of CPU against the 25% kept), not usage. The setting that compares usage with what survives a failure is "Performance degradation VMs tolerate"; at its default of 100% it never warns.
- Colleague 1 is wrong about the failure case; colleague 2 reaches a defensible outcome for the wrong reason (72% on its own is not a defect). The decision belongs to the cluster capacity step: with five hosts the same load is 57.6% in normal operation and 72% with one host lost; the other options are to reduce the load or to accept degraded performance during a failure, as a stated decision.
- Check that the flat four-week figure is not an average of peaks: read the busiest days, as the post-failure load is set by the peak.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1 (revision 20260624), ESX CPU Considerations: PCPU 80% reasonable ceiling, 90% warning, organizations set their own target. Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, page updated 2026-11-09): failover capacity is computed from reservations plus overhead. vSphere HA "Performance degradation VMs tolerate" default 100%.
- Why one answer: the arithmetic 4 x 72 / 3 = 96% follows from the prompt; the vendor levels (80, 90) are exceeded, and the admission-control mechanics are documented.
- Debatable risk: moderate. Whether to add a host, cut load or accept degradation is a business decision, so the key does not require "add a host": it requires the post-failure figure and the reason the host and admission-control checks stay silent. Hyper-Threading is off in the prompt to keep Core Utilization equal to the share of cores in use.
- Rests on: the design logic of the ESXi health check (Interpretation: green with high utilization is a capacity question; step 8 hands over to the cluster) and the vendor facts above.

## Metadata
```yaml
id: "0353"
title: "Busy but healthy hosts and the loss of one"
product: [vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: judged
input: [text]
object: [esxi, cluster]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/esxi/esxi-health-check
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
knowledge_main: vsphere/object-types/esxi/esxi-health-check
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [threshold-transplanted, consumption-as-contention]
status: draft
```
