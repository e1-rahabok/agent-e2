# Busy but healthy hosts and the loss of one

## Prompt
- Cluster prod-cl07: four identical ESXi 9.1 hosts, 2 sockets of 32 cores, Hyper-Threading off, 1 TB of memory each. DRS fully automated.
- vSphere HA admission control: cluster resource percentage, 25% for CPU and memory. Reservations are small: the VMs reserve 8% of the cluster CPU.
- Over four weeks, in business hours, every host shows Core Utilization of 70% to 74%, flat from day to day. Memory Consumed is 60%.
- On every host, the worst VM shows a 20-second peak Ready below 0.9% while its Net Run stays above 80%. No VM shows memory or disk contention.
- Colleague 1: "72% is below the 80% ceiling in the vendor guidance, so nothing to do." Colleague 2: "Hosts at 72%: add a fifth host."

Which statements about the hosts, the two colleagues and the loss of one host are correct?

- A. The hosts show no performance problem: the worst VM waits under 1% of the time while it runs more than 80% of it.
- B. Every host is below the 80% ceiling in the vendor guidance, so the cluster needs no action.
- C. If one host fails and its load spreads evenly, each of the three hosts left runs at about 96% Core Utilization.
- D. The 80% ceiling and 90% warning for the esxtop PCPU line describe a host in normal operation, not the hosts left after a failure.
- E. With "Performance degradation VMs tolerate" at its default of 100%, vSphere HA raises no warning for this cluster.
- F. With a fifth identical host, the same load runs at about 58% per host, and at about 72% per host with one host lost.
- G. The worst VM Ready below 1% today shows that the cluster has CPU to spare for the loss of one host.
- H. The load after a host failure is judged in each host's own health check, since it is each host's 72% that rises.
- I. The figure to scale for a host failure is the busiest period, not an average taken over the four weeks.

## Likely wrong answer
- B: "72% is under the 80% ceiling, so the hosts are fine: no action."

## Expected key points
- Answer: A, C, D, E, F, I.
- A is correct: the worst VM waits about 1% against 80% or more of Run, so the VMs get what they ask for. High utilization with no VM waiting is a capacity reading, not a performance one.
- B is wrong: the ceiling is for normal operation; after a failure the three hosts left run at 4 x 72% / 3 = 96%, above both esxtop levels. Contention is expected after the failure, even though none exists now.
- C is correct: 4 x 72% / 3 = 96%. With Hyper-Threading off, Core Utilization is the share of cores in use.
- D is correct: Performance Best Practices for vSphere 9.1 gives 80% as a reasonable ceiling and 90% as a warning, and says organizations set their own target. The levels say nothing about the loss of a host.
- E is correct: at the default of 100%, any degradation is tolerated, so no warning; HA admission control itself counts reservations, not usage, so nothing in HA speaks up.
- F is correct: total load 4 x 72% = 288% of one host; over five hosts 57.6%, over four hosts after a failure 72%. The other options are to reduce the load or to accept degraded performance during a failure, as a stated decision.
- G is wrong: today's Ready is read in normal operation; it says nothing about the load of 96% after a failure.
- H is wrong: a host is sized as part of its cluster. The ESXi health check hands capacity over to the cluster check, where the N / (N - 1) arithmetic belongs.
- I is correct: the post-failure load is set by the peak, so check that the flat four-week figure is not an average that hides the busiest days.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1 (revision 20260624), ESX CPU Considerations: PCPU 80% reasonable ceiling, 90% warning, organizations set their own target. Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, page updated 2026-11-09): failover capacity is computed from reservations plus overhead. vSphere HA "Performance degradation VMs tolerate" default 100%.
- The arithmetic 4 x 72 / 3 = 96% follows from the prompt; the vendor levels (80, 90) are exceeded.
- Debatable risk: moderate. Whether to add a host, cut load or accept degradation is a business decision, so the key does not require "add a host": it requires the post-failure figure and the reason the host checks and HA stay silent. Hyper-Threading is off in the prompt to keep Core Utilization equal to the share of cores in use.
- Rests on: esxi-health-check (green with high utilization is a capacity question; step 8 hands over to the cluster) and the vendor facts above.
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- 2026-11-15 audit: the stem line "The ESXi health check of each host reads: no contention, high utilization" removed (it interpreted the values). Dropped as copies of facts other questions keep: old D and G (HA admission control counts reservations, not usage: 0290, 0355), old F (busy hosts are not a defect: 0019, 0431), old H (HA admission refuses at a usage level: 0233) and old J (the degradation warning blocks power-ons: 0240). Letters: A, B, C unchanged; D dropped; E -> D; F, G, H dropped; I -> E; J dropped; K -> F; L -> G; M -> H; N -> I.

## Metadata
```yaml
id: "0353"
title: "Busy but healthy hosts and the loss of one"
product: [vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,D,E,F,I]
misconception: [B]
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
source_path: "Synthetic, 2026-11-13"
misconception_type: [threshold-transplanted, consumption-as-contention]
status: draft
```
