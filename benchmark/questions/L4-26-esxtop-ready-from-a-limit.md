# High %RDY in esxtop on an idle host

## Prompt
The attached screenshot is the esxtop CPU panel (c) of one ESXi host, with the VM of interest expanded.

- The host PCPU UTIL (%) is low.
- The application owner of the VM reports slow batch jobs.

What is the most likely cause of the high %RDY of this VM?

- A. A CPU limit on the VM or its resource pool: %MLMTD makes up most of %RDY.
- B. The host is short of physical CPU.
- C. Co-stop between the vCPUs of the VM.
- D. NUMA migrations of the VM.

## Input to supply
- Tool: esxtop on one ESXi 9.1 host, CPU panel (press c), VM expanded with e so the vcpu worlds show.
- Must show the summary lines (PCPU UTIL) and the columns %USED, %RUN, %RDY, %MLMTD, %CSTP, %WAIT for the VM.
- Condition for the key: the host PCPU UTIL AVG is below 50%; the VM has %RDY above 10% per vCPU, and %MLMTD is most of %RDY; %CSTP is near 0.
- How to produce it: set a CPU limit on a test VM well below its demand, and run a CPU load inside the Guest OS.
- Mask VM and host names if they reveal the customer.
- Save as `benchmark/questions/66/esxtop-cpu-panel-max-limited.png`.

## Likely wrong answer
B: reading high Ready as a host short of CPU.

## Expected key points
- Answer: A.
- %MLMTD (Max Limited) is time the vCPU was halted by a limit, not by lack of physical CPU. It is counted inside %RDY.
- With low PCPU UTIL the host has free cores: the Ready is not caused by the host.
- Find the limit on the VM and on every parent resource pool, and remove it. Limits should not be set.
- C is wrong: %CSTP is near 0. D is wrong: NUMA migrations do not show as %RDY.

## Notes
- Previous id: question-0066 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0066"
title: "High %RDY in esxtop on an idle host"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/tools/esxtop/overview
attachments:
  - 0066/esxtop-cpu-panel-max-limited.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
