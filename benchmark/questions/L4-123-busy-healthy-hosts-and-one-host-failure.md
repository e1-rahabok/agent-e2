# Busy but healthy hosts and the loss of one

## Prompt
- Cluster prod-cl07: four identical ESXi 9.1 hosts, 2 sockets of 32 cores, Hyper-Threading off, 1 TB of memory each. DRS fully automated.
- vSphere HA admission control: cluster resource percentage, 25% for CPU and memory. Reservations are small: the VMs reserve 8% of the cluster CPU.
- Over four weeks, in business hours, every host shows Core Utilization of 70% to 74%, flat from day to day. Memory Consumed is 60%.
- On every host, the worst VM shows a 20-second peak Ready below 0.9% while its Net Run stays above 80%. No VM shows memory or disk contention.
- The ESXi health check of each host reads: no contention, high utilization.
- Colleague 1: "72% is below the 80% ceiling in the vendor guidance, so nothing to do." Colleague 2: "Hosts at 72%: add a fifth host."

Which statements about the hosts, the two colleagues and the loss of one host are correct?

- A. The host checks show no performance problem: the worst VM waits under 1% of the time while it runs more than 80% of it.
- B. Every host is below the 80% ceiling in the vendor guidance, so the cluster needs no action.
- C. If one host fails and its load spreads evenly, each of the three hosts left runs at about 96% Core Utilization.
- D. HA admission control keeps 25% of the cluster free, so the three hosts left can run the whole load without contention.
- E. The 80% ceiling and 90% warning for the esxtop PCPU line describe a host in normal operation, not the hosts left after a failure.
- F. Core Utilization of 72% means the hosts are overloaded today, and that alone is the reason to add a fifth host.
- G. HA admission control gives no warning here, because it compares the 8% of CPU that is reserved with the 25% it keeps.
- H. HA admission control refuses new power-ons once host CPU usage passes the 75% left after the failover share.
- I. With "Performance degradation VMs tolerate" at its default of 100%, vSphere HA raises no warning for this cluster.
- J. Set to 0%, "Performance degradation VMs tolerate" would stop new VMs from powering on in this cluster.
- K. With a fifth identical host, the same load runs at about 58% per host, and at about 72% per host with one host lost.
- L. The worst VM Ready below 1% today shows that the cluster has CPU to spare for the loss of one host.
- M. The load after a host failure is judged in each host's own health check, since it is each host's 72% that rises.
- N. The figure to scale for a host failure is the busiest period, not an average taken over the four weeks.

## Likely wrong answer
- B: "72% is under the 80% ceiling, so the hosts are fine: no action."
- D: "HA keeps 25% free, so losing a host is covered."
- F: "The hosts are busy, so they are unhealthy: add capacity now."

## Expected key points
- Answer: A, C, E, G, I, K, N.
- A true: the worst VM waits about 1% against 80% or more of Run, so the VMs get what they ask for. High utilization with no VM waiting is a capacity reading, not a performance one.
- B false: the ceiling is for normal operation; after a failure the three hosts left run at 4 x 72% / 3 = 96%, above both esxtop levels. Contention is expected after the failure, even though none exists now.
- C true: 4 x 72% / 3 = 96%. With Hyper-Threading off, Core Utilization is the share of cores in use.
- D false: with the percentage policy, admission control keeps failover capacity for reservations plus overhead, not for usage. VMs without reservations can fill the cluster past what three hosts can run.
- E true: Performance Best Practices for vSphere 9.1 gives 80% as a reasonable ceiling and 90% as a warning, and says organizations set their own target. The levels say nothing about the loss of a host.
- F false: 72% with no VM waiting is not a defect. Colleague 2 reaches a defensible outcome for the wrong reason: the reason to add capacity is the load after a failure, decided in the cluster check.
- G true: the percentage policy sums reservations plus overhead (8% of CPU) against the 25% kept, so it stays silent while usage is high.
- H false: admission control counts reservations, not usage; a cluster at high usage still admits VMs without reservations.
- I true: at the default of 100%, any degradation is tolerated, so no warning. The setting that compares usage with what survives a failure is this one, not the admission control policy.
- J false: the threshold raises a configuration warning only; it does not block power-ons, migrations or reservation changes.
- K true: total load 4 x 72% = 288% of one host; over five hosts 57.6%, over four hosts after a failure 72%. The other options are to reduce the load or to accept degraded performance during a failure, as a stated decision.
- L false: today's Ready is read in normal operation; it says nothing about the load of 96% after a failure.
- M false: a host is sized as part of its cluster. The ESXi health check hands capacity over to the cluster check, where the N / (N - 1) arithmetic belongs.
- N true: the post-failure load is set by the peak, so check that the flat four-week figure is not an average that hides the busiest days.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1 (revision 20260624), ESX CPU Considerations: PCPU 80% reasonable ceiling, 90% warning, organizations set their own target. Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, page updated 2026-11-09): failover capacity is computed from reservations plus overhead. vSphere HA "Performance degradation VMs tolerate" default 100%.
- Why one answer: the arithmetic 4 x 72 / 3 = 96% follows from the prompt; the vendor levels (80, 90) are exceeded, and the admission-control mechanics are documented.
- Debatable risk: moderate. Whether to add a host, cut load or accept degradation is a business decision, so the key does not require "add a host": it requires the post-failure figure and the reason the host and admission-control checks stay silent. Hyper-Threading is off in the prompt to keep Core Utilization equal to the share of cores in use.
- Rests on: the design logic of the ESXi health check (Interpretation: green with high utilization is a capacity question; step 8 hands over to the cluster) and the vendor facts above.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0353"
title: "Busy but healthy hosts and the loss of one"
product: [vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,E,G,I,K,N]
misconception: [B,D,F]
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
