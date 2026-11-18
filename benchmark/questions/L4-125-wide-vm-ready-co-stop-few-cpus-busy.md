# A 16-vCPU app server waits while a third of it works

## Prompt
- The owner of app-java-04, a 16-vCPU Java application server on Linux, wants it doubled before the quarter-end peak: "It already waits for CPU, and the developers say Co-stop means our threads block each other."
- The VM fits within one NUMA node of its host and has no snapshot.
- From VCF Operations: [the VM's hourly CPU for the last 7 days](0373/app-java-04-cpu-hourly-7-days.csv) and [the VMs on its host with their 7-day maximum Ready](0373/host-vms-cpu-ready-7-days.csv).
- Inside the guest, at a peak hour, `mpstat -P ALL 60 1` printed:

```text
Linux 5.14.0-427.13.1.el9_4.x86_64 (app-java-04) 	11/13/2026 	_x86_64_	(16 CPU)

02:16:01 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
02:16:01 PM  all   34.33    0.00    2.78    0.09    0.00    0.20    0.64    0.00    0.00   61.95
02:16:01 PM    0    5.90    0.00    0.86    0.03    0.00    0.02    0.18    0.00    0.00   93.01
02:16:01 PM    1    6.51    0.00    0.75    0.09    0.00    0.18    0.08    0.00    0.00   92.39
02:16:01 PM    2    6.12    0.00    1.08    0.06    0.00    0.13    0.07    0.00    0.00   92.54
02:16:01 PM    3   83.71    0.00    5.00    0.02    0.00    0.55    1.46    0.00    0.00    9.26
02:16:01 PM    4   81.35    0.00    4.44    0.28    0.00    0.21    1.43    0.00    0.00   12.29
02:16:01 PM    5    6.33    0.00    1.64    0.02    0.00    0.06    0.01    0.00    0.00   91.94
02:16:01 PM    6    7.02    0.00    0.90    0.04    0.00    0.15    0.11    0.00    0.00   91.78
02:16:01 PM    7   84.16    0.00    6.39    0.06    0.00    0.60    1.06    0.00    0.00    7.73
02:16:01 PM    8   80.73    0.00    6.84    0.30    0.00    0.47    1.87    0.00    0.00    9.79
02:16:01 PM    9    5.49    0.00    0.73    0.08    0.00    0.10    0.23    0.00    0.00   93.37
02:16:01 PM   10   78.47    0.00    4.90    0.23    0.00    0.25    1.32    0.00    0.00   14.83
02:16:01 PM   11    7.65    0.00    1.10    0.05    0.00    0.06    0.20    0.00    0.00   90.94
02:16:01 PM   12    2.70    0.00    1.49    0.06    0.00    0.06    0.07    0.00    0.00   95.62
02:16:01 PM   13   80.89    0.00    5.49    0.07    0.00    0.19    1.83    0.00    0.00   11.53
02:16:01 PM   14    7.71    0.00    1.23    0.01    0.00    0.07    0.29    0.00    0.00   90.69
02:16:01 PM   15    4.49    0.00    1.67    0.04    0.00    0.18    0.09    0.00    0.00   93.53

Average:     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
Average:     all   34.33    0.00    2.78    0.09    0.00    0.20    0.64    0.00    0.00   61.95
Average:       0    5.90    0.00    0.86    0.03    0.00    0.02    0.18    0.00    0.00   93.01
Average:       1    6.51    0.00    0.75    0.09    0.00    0.18    0.08    0.00    0.00   92.39
Average:       2    6.12    0.00    1.08    0.06    0.00    0.13    0.07    0.00    0.00   92.54
Average:       3   83.71    0.00    5.00    0.02    0.00    0.55    1.46    0.00    0.00    9.26
Average:       4   81.35    0.00    4.44    0.28    0.00    0.21    1.43    0.00    0.00   12.29
Average:       5    6.33    0.00    1.64    0.02    0.00    0.06    0.01    0.00    0.00   91.94
Average:       6    7.02    0.00    0.90    0.04    0.00    0.15    0.11    0.00    0.00   91.78
Average:       7   84.16    0.00    6.39    0.06    0.00    0.60    1.06    0.00    0.00    7.73
Average:       8   80.73    0.00    6.84    0.30    0.00    0.47    1.87    0.00    0.00    9.79
Average:       9    5.49    0.00    0.73    0.08    0.00    0.10    0.23    0.00    0.00   93.37
Average:      10   78.47    0.00    4.90    0.23    0.00    0.25    1.32    0.00    0.00   14.83
Average:      11    7.65    0.00    1.10    0.05    0.00    0.06    0.20    0.00    0.00   90.94
Average:      12    2.70    0.00    1.49    0.06    0.00    0.06    0.07    0.00    0.00   95.62
Average:      13   80.89    0.00    5.49    0.07    0.00    0.19    1.83    0.00    0.00   11.53
Average:      14    7.71    0.00    1.23    0.01    0.00    0.07    0.29    0.00    0.00   90.69
Average:      15    4.49    0.00    1.67    0.04    0.00    0.18    0.09    0.00    0.00   93.53
```

Which statements are correct?

- A. In `mpstat`, the guest keeps about 5-6 of its 16 CPUs busy at the peak hour.
- B. Double the VM to 32 vCPUs: the work spreads and each vCPU waits less.
- C. A narrower VM, nearer the guest's use, would tend to show less Ready and less Co-stop.
- D. The Co-stop in the export shows the application's threads waiting on each other's locks inside the guest.
- E. Co-stop on this VM follows from Ready on its siblings: one vCPU waits, the others are held back.
- F. In the hourly export, Co-stop stays above Ready in the peak hours all week.
- G. The other VMs on the host wait as much as this one: the host is short of CPU.
- H. A downsize mainly lowers Co-stop; this VM's Ready follows the load of the host.
- I. Net Run in the hourly export matches the busy CPUs in `mpstat`: about a third of 16 vCPUs.

## Answers
A, C, E, I

## Explanation
- A is correct: reading. In the `mpstat` block, 5 or 6 CPU rows have %idle below 20 and the other rows above 80.
- B is wrong: the misconception and wrong action. More vCPUs need more threads free at about the same time: Ready and Co-stop tend to rise.
- C is correct: the guest uses about a third of its vCPUs; a narrower VM needs fewer threads free at once and fits free threads more easily.
- D is wrong: Co-stop is a wait in the ESXi scheduler that keeps the vCPUs in step; the guest does not see it, and its own locks do not cause it.
- E is correct: with the VM inside one NUMA node and no snapshot, the remaining cause of Co-stop is Ready on a sibling vCPU; co-stopped vCPUs stop even when threads are free.
- F is wrong: reading. In every hourly row CPU|Co-stop (%) is below CPU|Ready (%); in the peak hours Ready is 1.5-4 and Co-stop 0.5-2.
- G is wrong: reading. In the host list every other VM has CPU|Ready (%) (Max) below 0.5, against more than 2 for app-java-04: the wait comes from this VM's width, not the host.
- H is wrong: over-correction. Downsizing usually lowers Ready too: fewer vCPUs fit free threads more easily, and the other VMs' low Ready shows the host load is not what drives this VM's Ready.
- I is correct: CPU|Net Run (%) is normalised to the whole VM (16 vCPUs = 100%). At the peak hours it reads 28-40%, about 4.5-6.5 vCPUs of work; in the hour of the `mpstat` sample the busy CPUs add up to Net Run x 16 within about one CPU (the guest also counts Ready and Co-stop time as busy, so it reads slightly higher).
- Misconception: B: the VM waits for CPU, so give it more vCPUs. Or D: Co-stop means the application's threads block each other.

## Reasoning path
1. `mpstat` and Net Run: about a third of the 16 vCPUs work.
2. The other VMs barely wait: the host is not the problem.
3. Ready and Co-stop come from the VM's width: narrow it, do not double it.

## Notes
- Paired with the theory question 0107 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C11). Counts only after author approval.
- Review 2026-11-15: new situation (16-vCPU Linux application server, a request to double it, the developers' reading of Co-stop) and new wording, away from 0107; NUMA fit and no snapshot added so E is decidable; screen readings F, G (false) and I (true) added. Key changed from A, C, F to A, C, E, I (options relettered).
- Converted 2026-11-16 from screenshots to a VCF Operations hourly list export, a host list export and `mpstat -P ALL` text, generated by a seeded script (project/practical-questions-as-exports-2026-11-15.md). A and I name `mpstat` instead of `top`; D, F and I say export instead of chart. Truth values unchanged. The list view CSV format is assumed (not captured yet; project/tools/export_generator/README.md).
- 2026-11-15 audit: C shortened (no longer the longest option) and H reworded without "only" and "alone" (truth kept). Not done: a CPU|Usage (%) column and an option on Usage above Net Run (needs a generator change).

## Metadata
```yaml
id: "0373"
title: "A 16-vCPU app server waits while a third of it works"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [table]
object: [vm, esxi, guest-os]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments:
  - 0373/app-java-04-cpu-hourly-7-days.csv
  - 0373/host-vms-cpu-ready-7-days.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C11"
misconception: [B, D]
misconception_type: [provider-vs-consumer]
pair: "0107"
status: draft
```
