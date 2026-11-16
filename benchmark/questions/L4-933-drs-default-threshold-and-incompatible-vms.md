# DRS ignores bursts and incompatible VMs

## Prompt
- vCenter 9.1. Cluster batch-cl02: 8 hosts, DRS fully automated, migration threshold at its default. No DRS advanced options have been set.
- A group of 30 ETL VMs runs a burst every 15 minutes that lasts about 4 minutes. During each burst esx-03 runs at 95-98% CPU utilization while the other hosts stay at 50-60%; several ETL VMs on esx-03 show high CPU Ready in those minutes. Between bursts all hosts sit at 40-50%.
- DRS moved 2 VMs in the last 24 hours.
- Separately, last Thursday from 09:10 to 09:30 an NSX component on esx-06 was down. vCenter showed the VMs on esx-06 as incompatible with their host for those 20 minutes. DRS moved none of them.
- A colleague says: "DRS is broken twice. It should react to every spike, and it should have evacuated esx-06 after its 10-minute tolerance."

Which statements are correct?

- A. The default threshold is tuned for mostly stable workloads, so not chasing 4-minute bursts is designed behaviour.
- B. Level 4 is tuned for bursty workloads with occasional spikes and fits this ETL group better than the default.
- C. Level 1 makes DRS the most responsive to load changes, so setting it moves the ETL VMs during each burst.
- D. At the default threshold DRS reacts to every load change, so two moves in a day show that DRS is not working.
- E. Since vCenter 8.0 Update 3 the default no longer moves a VM only because it became incompatible with its current host.
- F. DRS tolerates 600 seconds of incompatibility and then evacuates, so the VMs on esx-06 should have moved by about 09:20.
- G. DRS evaluates the cluster about once an hour, so no threshold can react to a burst of 4 minutes.
- H. The VM Distribution option spreads the CPU load of the bursts across the hosts, so turning it on removes the hot spot.

## Likely wrong answer
D and F: "The default threshold reacts to every spike, and DRS evacuates incompatible VMs after 600 seconds, so DRS failed twice." C and H are the wrong fixes; G is the over-correction.

## Expected key points
- Answer: A, B, E.
- A is correct: since vSphere 7.0 the threshold is workload-focused; level 3, the default, is tuned for mostly stable workloads.
- B is correct: level 4 is for bursty workloads, where occasional spikes may require DRS to react to sudden load changes (level 5 for workloads whose utilization varies significantly).
- C is wrong: level 1 makes only mandatory moves (rule violations, maintenance mode); DRS then makes no move to improve resource availability.
- D is wrong: reacting to workload changes every time is level 5, not the default.
- E is correct: since vCenter 8.0 Update 3 the default of CompatCheckTransientFailureTimeSeconds is -1, so incompatibility with the current host alone no longer triggers a move; no advanced option was set here.
- F is wrong: 600 seconds was the default tolerance before vCenter 8.0 Update 3.
- G is wrong: DRS scans the cluster every minute for load-balancing recommendations.
- H is wrong: VM Distribution spreads the number of VMs evenly across hosts, for availability; it does not balance their CPU load.

## Notes
- Source of the incompatibility default: vSphere 9.1 documentation, VM migrations initiated by DRS due to incompatibility (pp. 1954-1955). Threshold levels: Performance Best Practices for vSphere 9.1 (revision 20260624), DRS Performance Tuning (pp. 78-79).

## Metadata
```yaml
id: "0466"
title: "DRS ignores bursts and incompatible VMs"
product: [vsphere, nsx]
technology: [system, cpu]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/drs-migration-levels
knowledge_main: vsphere/object-types/cluster/configuration/drs-migration-levels
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/object-types/cluster/configuration/drs-migration-levels"
answer: [A, B, E]
misconception: [D, F]
misconception_type: [threshold-transplanted]
status: draft
```
