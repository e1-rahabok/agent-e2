# VM memory usage near 100% every night

## Prompt
- A Linux VM with 8 GB of memory runs a PostgreSQL reporting database. VMware Tools is running and current.
- An ETL job loads the database every night from 01:00 to about 03:30.
- [The attached vSphere Client export](0151/vm-memory-past-day.csv) is the VM's Past Day memory chart (5-minute samples).
- Inside Linux, `free -m` during the job (02:00): total 7,962, used 5,214, free 188, buff/cache 2,560, available 2,402. At 14:00: used 4,436, free 402, buff/cache 3,124, available 3,188.
- `sar -W` for the same night: `pswpin/s` and `pswpout/s` are 0.00 in every sample.
- The database owner asks for 8 GB more memory "because vCenter shows memory usage near 100% every night".

Which statements are correct?

- A. Usage near 100% every night shows that the VM runs out of memory during the job and needs the extra 8 GB.
- B. In this chart, Usage (%) is Active divided by the VM's configured memory.
- C. Linux was not short of memory during the nightly job.
- D. Consumed near the configured 8 GB all day shows that the VM was short of memory all along.
- E. The Usage (%) in this chart is Linux's own used memory, as VMware Tools reports it.
- F. No VM counter in vCenter can show whether this VM waited for memory during the job.

## Likely wrong answer
- A: "Memory usage is near 100% every night: the VM runs out of memory. Add the 8 GB."

## Expected key points
- Answer: B, C.
- A is false: the guest counters show no shortage; the nightly 100% is the Active estimate of recently touched pages, not memory the guest lacks.
- B is true: vCenter VM memory Usage (%) maps to Active: in every row of the export, Usage (%) = Active (KB) / 8,388,608 KB × 100 (for example 7,829,308 KB at 02:00 gives 93.33%).
- C is true: about 2.4 GB stayed available during the job and Linux swapped nothing in or out; free memory near 0 is normal, since Linux uses it as page cache.
- D is false: Consumed holds every page the guest has touched, cache included, and does not drop when the guest frees memory; it is not the guest's need.
- E is false: vCenter Usage (%) is Active, an ESXi estimate; it does not use Linux counters. At 14:00 it reads about 13% while Linux uses about 4.4 of 7.8 GB.
- F is false: VM memory Latency (Memory Contention in VCF Operations) is the share of time the VM waited for memory; it shows the wait that Usage does not. This is the over-correction of A.

## Notes
- Rewritten 2026-11-14 (project/question-pairing-2026-11-14.md, pair A2): the old scenario (a domain controller, an agent collecting every 5 minutes, Active at 100% for over 12 hours, a vCenter alarm) was a near-copy of the knowledge example in Guest OS memory vs VM memory, section Example: Guest OS more accurate. New scenario and a new CSV from a seeded script (seed 15120261114): a nightly ETL job on a Linux database VM.
- Removed with the old scenario: the alarm option, and the option on VCF Operations VM memory Usage (%) (Guest OS Needed Memory, falling back to Active), which the new pair D2 tests.
- Paired with 0020 (theory and practical; design.md, section 3.9). Key changed from B, C, D, E, G, H to B, C.

## Metadata
```yaml
id: "0151"
title: "VM memory usage near 100% every night"
product: [vsphere, linux]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
answer: [B, C]
misconception: [A]
input: [table]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - guest-os/system/troubleshooting/linux-os-slow
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments:
  - 0151/vm-memory-past-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion, consumption-as-contention]
pair: "0020"
status: draft
```
