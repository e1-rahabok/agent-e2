# Linux shows no steal, vCenter shows Ready

## Prompt
- A Linux administrator says: "`top` shows no steal all afternoon, so the hypervisor takes no CPU from this VM. The slowness must be elsewhere."
- The VM app-lnx-03 runs RHEL 9 (kernel 5.14) with 4 vCPUs, virtual hardware version 21. It was deployed from a template with default VM settings; nobody changed its advanced parameters.
- He pastes the summary of `top` at the end of the slow period:

```text
top - 14:10:00 up 12 days,  3:12,  1 user,  load average: 4.65, 4.45, 3.32
Tasks: 287 total, 5 running, 282 sleeping, 0 stopped, 0 zombie
%Cpu(s): 69.4 us,  6.6 sy,  0.0 ni, 22.3 id,  0.8 wa,  0.3 hi,  0.6 si,  0.0 st
MiB Mem :  15731.4 total,   2210.6 free,   9876.3 used,   3644.5 buff/cache
MiB Swap:   4096.0 total,   4096.0 free,      0.0 used.   5402.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   2214 appsvc     20   0 6876544 742131  30212 S 295.5   4.6 1832:41.07 java
   1088 root       20   0   19876  11024   9472 S   0.7   0.1   0:12.44 sshd
    711 root       20   0   52140  21980  20112 S   0.3   0.1   1:02.18 systemd-journal
```

- And `sar -u ALL 60 10` for the same 10 minutes:

```text
Linux 5.14.0-427.13.1.el9_4.x86_64 (app-lnx-03) 	11/10/2026 	_x86_64_	(4 CPU)

02:00:00 PM     CPU      %usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
02:01:00 PM     all     69.60      0.00      7.54      1.21      0.00      0.27      0.65      0.00      0.00     20.73
02:02:00 PM     all     68.84      0.00      8.19      1.30      0.00      0.44      0.75      0.00      0.00     20.48
02:03:00 PM     all     70.94      0.00      6.64      0.84      0.00      0.48      0.43      0.00      0.00     20.67
02:04:00 PM     all     67.60      0.00      7.71      0.33      0.00      0.45      0.59      0.00      0.00     23.32
02:05:00 PM     all     71.79      0.00      6.55      1.35      0.00      0.35      0.80      0.00      0.00     19.16
02:06:00 PM     all     71.70      0.00      8.64      1.21      0.00      0.42      0.65      0.00      0.00     17.38
02:07:00 PM     all     72.34      0.00      8.40      0.33      0.00      0.40      0.44      0.00      0.00     18.09
02:08:00 PM     all     70.26      0.00      9.03      1.27      0.00      0.51      0.54      0.00      0.00     18.39
02:09:00 PM     all     63.58      0.00      9.57      0.53      0.00      0.30      0.83      0.00      0.00     25.19
02:10:00 PM     all     64.54      0.00      8.72      1.46      0.00      0.52      0.35      0.00      0.00     24.41
Average:        all     69.12      0.00      8.10      0.98      0.00      0.41      0.60      0.00      0.00     20.79
```

- You export [the vCenter CPU chart of the VM](0381/vcenter-vm-cpu-realtime.csv), Real-time, for the same 10 minutes.

Which statements are correct?

- A. `st` 0.0 shows the vCPUs were never held off a physical thread.
- B. In the vCenter export, Ready is more than a fifth of Run in every row.
- C. In the vCenter export, Readiness stays below 2%.
- D. vCenter's Readiness must be a collection error, since the guest sees no steal.
- E. With this VM's default settings the steal clock is off, so the guest has no counter for the frozen time.
- F. With `stealclock.enable = "TRUE"` set on this VM, `st` would follow its Ready.
- G. The us and sy figures in `top` include time the vCPUs were frozen.
- H. `top` shows `wa` above 10%, so the guest is waiting on storage.
- I. Add 2 vCPUs to the VM to absorb the wait.

## Likely wrong answer
A: `st` is 0.0, so the hypervisor takes nothing from this VM. Or D: the tools disagree, so vCenter is wrong.

## Expected key points
- Answer: B, E, F, G.
- A false: the misconception. Without the steal clock `st` cannot show the wait at all; the vCenter export shows it (`Readiness for app-lnx-03` 14-28% in every row, while `st` and sar `%steal` are 0.0 and 0.00).
- B true: reading. `Ready for app-lnx-03` divided by `Run for app-lnx-03` is above 0.2 in every row (Ready about 12,000-21,600 ms against Run about 40,000-50,000 ms): the vCPUs wait a large share of the time they run.
- C false: reading. `Readiness for app-lnx-03` stays between 14% and 28% in every row.
- D false: the tools count at different layers. The guest kernel is not told about the frozen time; vCenter counts it.
- E true: on vSphere, steal accounting needs the VM's steal clock (`stealclock.enable`); default settings leave it off, so the steal counter stays 0.
- F true: RHEL 9's kernel 5.14 has the VMware steal clock (mainline 5.7 or later) and hardware version 21 is above 13; with the option, `st` follows Ready.
- G true: reading and mechanism. A frozen vCPU stays in the state it was in, so a busy vCPU's frozen time counts as us or sy: `us` + `sy` in `top` is 60 or more, and sar `%usr` + `%sys` stays near Run plus Ready of the vCenter export, above Run alone.
- H false: reading. `wa` in `top` and sar `%iowait` stay below 2.
- I false: wrong action. The vCPUs wait for physical threads on a busy host; more vCPUs add demand and tend to raise Ready.

## Reasoning path
1. vCenter: Readiness of 14-28%: the vCPUs wait.
2. `top` and sar: `st` and `%steal` 0 with defaults: the guest does not count the wait.
3. The wait is real; enable the steal clock to see it in the guest, and fix the host load or placement.

## Notes
- Paired with the theory question 0380 (theory and practical; design.md, section 3.9).
- Vendor sources for general VMs: Broadcom TechDocs, Tanzu GemFire 10.1, High CPU Steal, section VMware ESXi (steal time needs `stealclock.enable = "TRUE"` except on Photon OS; without it `/proc/stat` steal stays 0), https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-gemfire/10-1/gf/managing-checklist-cpu-steal-high.html; Broadcom KB 376609, https://knowledge.broadcom.com/external/article/376609; Broadcom KB 434983 (hardware version 13 or later).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D12). Counts only after author approval.
- Review 2026-11-15: kernel 5.14 in the stem (F needs it); B without the range; screen readings C and H (false) added; options reworded away from 0380. Key changed from B, D, E, G to B, E, F, G (options relettered).
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): `top` and `sar` as guest text, vCenter as CSV. B (the Ready definition, over the cap of two: also 0009, 0376, 0368) became a reading of Ready against Run; still true. sar `%guest` 0.00 is a neighbour column only: no option rests on it, because the knowledge base does not state what `%guest` counts yet (guest-os-vs-vm-cpu, Linux metrics).

## Metadata
```yaml
id: "0381"
title: "Linux shows no steal, vCenter shows Ready"
product: [vsphere, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments:
  - 0381/vcenter-vm-cpu-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D12"
answer: [B, E, F, G]
misconception: [A, D]
misconception_type: [layer-confusion, tool-confusion]
pair: "0380"
status: draft
```
