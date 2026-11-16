# Side-Channel-Aware Scheduler turned on after an L1TF audit

## Prompt
- Cluster prod-03, ESXi 9.1, 8 hosts. Each host: 2 sockets of 24 cores, Hyper-Threading on (96 logical processors).
- A security audit flagged the L1TF (CVE-2018-3646) concurrent-context attack vector on the cluster. The hosts carry every current patch.
- On Saturday the team set `VMkernel.Boot.hyperthreadingMitigation` to TRUE on every host, left every other advanced setting at its default, and rebooted the hosts.
- The VMs and their load did not change. vCenter, busiest host, weekday 10:00-11:00:

| Counter | Week before | Week after |
|---|---|---|
| Host Utilization (%) | 62 | 48 |
| Host Core Utilization (%) | 85 | 96 |
| VM CPU Readiness (%), mean of the VMs | 1.2 | 5.5 |

Which statements about the change and the readings are correct?

- A. The hosts now run the first version of the Side-Channel-Aware Scheduler, which uses one thread per core.
- B. The current patches had already closed the concurrent-context vector, so the setting added no protection.
- C. `hyperthreadingMitigationIntraVM` = FALSE gives SCAv2, which never runs two VMs on one core at once.
- D. Utilization of 48% with Core Utilization of 96% matches a scheduler that runs one thread on each core.
- E. Utilization of 48% shows that about half of each host's thread capacity is still free for more VMs.
- F. Readiness rose because the scheduler now has about half as many logical processors to place vCPUs on.
- G. Side-channel mitigations in the hypervisor have no measurable performance cost on fully patched hosts.
- H. Add vCPUs to the VMs whose Readiness rose, so that each of them gets more CPU time in every second.
- I. The Side-Channel-Aware Scheduler turns on by itself once the sequential-context updates are installed.
- J. SCAv1 and SCAv2 cost about the same performance, since both keep different VMs off a shared core.

## Likely wrong answer
"The hosts were patched, so this was only a formality (B); mitigations cost nothing on current hardware (G); and Utilization fell to 48%, so half the host is now free (E)." B, E and G are the misconceptions.

## Expected key points
- Answer: A, C, D, F.
- A is correct: `hyperthreadingMitigation` TRUE enables the Side-Channel-Aware Scheduler after a reboot; `hyperthreadingMitigationIntraVM` defaults to TRUE, which gives SCAv1, and SCAv1 limits the scheduler to one thread per core.
- B is wrong: for L1TF the updates address the sequential-context vector automatically, but the concurrent-context vector only once the Side-Channel-Aware Scheduler is enabled, which is not the default in any release, 9.x included.
- C is correct: `hyperthreadingMitigationIntraVM` FALSE gives SCAv2 (from ESXi 6.7 Update 2): it keeps multithreading but never schedules threads of different VMs on the same core at the same time.
- D is correct: with one thread per core, every busy core has one busy thread, so Utilization is half of Core Utilization: 96% / 2 = 48%. Before the change, 62% of 96 threads (about 60) ran on 85% of 48 cores (about 41): many cores ran both threads.
- E is wrong: under SCAv1 the second thread of each core is not used for VMs, so the 100% of Utilization (both threads) cannot be reached; with Core Utilization at 96% the host is nearly full.
- F is correct: SCAv1 leaves the scheduler 48 of 96 logical processors; with the same load, vCPUs wait longer for a free one, which shows as Ready.
- G is wrong: some mitigations have a significant performance impact, and the concurrent-context mitigation can have one; hardware mitigations on newer CPUs cost little or nothing.
- H is wrong: more vCPUs add demand on the halved number of usable threads and raise Ready further; the cause is the scheduler mode.
- I is wrong: the Side-Channel-Aware Scheduler stays off until `VMkernel.Boot.hyperthreadingMitigation` is set to TRUE; the sequential-context updates do not enable it.
- J is wrong: SCAv2 has a lower performance penalty than SCAv1 in nearly all cases, because it keeps both threads of a core in use.

## Notes
- Broadcom KB 317621 (legacy 55806) is the current guidance for the ESX scheduler (ESXi 5.5 to 9.x), cited in the knowledge file.

## Metadata
```yaml
id: "0443"
title: "Side-Channel-Aware Scheduler turned on after an L1TF audit"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm, cluster]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/configuration/side-channel-scheduling
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/technology/cpu/configuration/side-channel-scheduling
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/configuration/side-channel-scheduling"
answer: [A, C, D, F]
misconception: [B, E, G]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
