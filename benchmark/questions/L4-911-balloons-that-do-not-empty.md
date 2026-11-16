# Balloons that do not empty

## Prompt
- Three VMs in a vSphere 9.1 cluster show memory in their balloons. The vCenter keeps statistics level 2. No VM in the cluster has a memory reservation.
- app-01: Linux, 24 GB configured, on host esx-07 (512 GB). The VMs on esx-07 have 700 GB of memory configured in total. Host Consumed stays at 97-99% all week, and the esxtop memory state alternates between clear and soft every day.
- rpt-02: Windows, 16 GB configured, VMware Tools running, on host esx-03 (512 GB). Host Consumed is 58% all week, the esxtop memory state stays high, and no other VM on esx-03 shows Ballooned memory.
- db-03: Linux, 32 GB configured, on host esx-05. At 10:20 today DRS moved several VMs off esx-05, and its memory state went from soft to high.
- vCenter values:

| VM | Chart | Balloon target | Ballooned memory | Active |
|---|---|---|---|---|
| app-01 | Past week | 6.0 GB, flat for the last 4 days | 6.0 GB, flat for the last 4 days | about 0.9 GB |
| rpt-02 | Past day | 3.5 GB, flat | 3.5 GB, flat | about 2.1 GB |
| db-03 | Real-time, 10:00-10:40 | 2.0 GB until 10:20, then 0 | 2.0 GB at 10:20, 1.8 GB at 10:30, 1.6 GB at 10:40 | about 6 GB |

- Inside app-01, `free -m` shows 11,200 MB available. Its owner writes: "Linux has 11 GB available and has not needed the ballooned memory. When the application grows, the guest will take those pages back."

Which statements are correct?

- A. ESXi keeps app-01's balloon target equal to the balloon, so it stays inflated whatever Linux reports as available.
- B. app-01's balloon will deflate once Linux needs more memory, because the guest asks the driver for its pages back.
- C. app-01 keeps its balloon for as long as it stays this idle on a host that remains overcommitted.
- D. app-01's balloon has reached the driver's ceiling, so ESXi would compress or swap any further target.
- E. More memory shares for app-01 than for the other VMs on esx-07 can make ESXi lower its target.
- F. A balloon target above 0 on rpt-02, on a host with 42% of its memory free, is a counter error.
- G. A memory limit on rpt-02 or on a resource pool above it is the likely cause of its balloon.
- H. db-03's Ballooned memory of 1.6 GB beside a target of 0 shows the two counters are out of step and cannot be trusted.
- I. ESXi no longer asks db-03 for that memory, and its balloon is deflating toward 0.
- J. A balloon that stays flat for days can only come from a limit; host pressure would have deflated it by now.
- K. Restart the VMware Tools service in app-01, so that the balloon driver releases its pages.

## Likely wrong answer
B: "Linux has plenty available and will ask for the ballooned memory when the application needs it." F and H: "The balloon counters do not match what the host and the target show, so they are wrong."

## Expected key points
- Answer: A, C, E, G, I.
- A is correct: deflating is driven by the target. The balloon deflates when the scheduler lowers the Balloon Target below the balloon size; a target equal to Ballooned, flat for 4 days, means ESXi still wants those pages. The guest's free memory does not move it.
- B is wrong: the misconception of ballooning ("Ballooned stays above 0 after the pressure, so the guest has not asked for the pages back"). The guest asking for memory does not deflate the balloon; only a lower target does.
- C is correct: the allocation target follows shares and the working set and taxes idle memory. An idle VM (Active about 0.9 GB of 24 GB) on a host that stays overcommitted (700 GB configured on 512 GB, Consumed 97-99%, soft every day) keeps its balloon.
- D is wrong: the ceiling is 65% of configured memory by default, 0.65 × 24 = 15.6 GB; 6.0 GB is 25% of 24 GB.
- E is correct: the scheduler's allocation target follows shares, so more shares give app-01 a larger share of host memory and can lower the target set for it.
- F is wrong: the misconception of Balloon Target ("A Balloon Target above 0 on a host with free memory is a data error"). A limit sets the target to the excess above the limit on a host with free memory too.
- G is correct: a balloon has two triggers, host pressure and a limit on the VM or a pool above it. esx-03 is at 58% with its state high and no other VM ballooned: no host pressure, so a limit.
- H is wrong: the misconception "Balloon Target 0, so Ballooned must be 0". The reallocation lags the target; Ballooned falls after the target drops.
- I is correct: a target below Ballooned means the VMkernel deflates the balloon; the target is 0 since 10:20 and Ballooned falls 2.0, 1.8, 1.6 GB.
- J is wrong: over-correction. A flat balloon means the target held: by host pressure, by a limit, or on an idle VM on an overcommitted host, which is app-01's case.
- K is wrong: the wrong action. The driver holds the pages because the target holds; on Linux the balloon driver is the kernel module vmw_balloon, which keeps working with the VMware Tools service stopped, so a restart of the service changes nothing.

## Notes
- Sources: the knowledge base, VM Memory Balloon Target (target above or below Ballooned, a target of 0 with Ballooned still above 0, a limit as the cause on a host with free memory) and Ballooning (deflate driven by the target, idle memory tax, shares, the 65% ceiling, the Linux driver). vSphere 9.1 documentation, Memory (MB) counters, Balloon Target (pp. 2073, 2104); How ESX Hosts Allocate Memory (p. 1838).

## Metadata
```yaml
id: "0450"
title: Balloons that do not empty
product: [vsphere, linux, windows]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter, esxtop, guest-os-tools]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/memory-limit
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/metrics/virtual-motherboard/balloon-target"
answer: [A, C, E, G, I]
misconception: [B, F, H]
misconception_type: [layer-confusion, provider-vs-consumer]
status: draft
```
