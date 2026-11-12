# High %RDY in esxtop on a quiet host

## Prompt
- ESXi 9.1 host: 2 sockets of 16 cores at 2.5 GHz, Hyper-Threading on.
- The owner of batch-07 (4 vCPUs) says its nightly jobs now take twice as long.
- esxtop, CPU panel, with batch-07 expanded (e) to show its worlds. Per-PCPU values are not shown.

```text
 2:14:06am up 41 days  3:02, 812 worlds, 14 VMs, 38 vCPUs; CPU load average: 0.28, 0.27, 0.29
PCPU USED(%): (64 values) AVG: 24
PCPU UTIL(%): (64 values) AVG: 27

      GID NAME               NWLD   %USED    %RUN    %SYS   %WAIT    %RDY   %IDLE  %OVRLP   %CSTP  %MLMTD  %SWPWT
 52741011 batch-07              8  160.50  162.10    0.20  405.10  232.40    0.00    0.70    0.40  224.80    0.00
 52741011 vmx                   1    0.10    0.10    0.00   99.90    0.00    0.00    0.00    0.00    0.00    0.00
 52741011 vmast.52741011        1    0.00    0.00    0.00  100.00    0.00    0.00    0.00    0.00    0.00    0.00
 52741011 vcpu-0:batch-07       1   40.10   40.50    0.10    1.30   58.10    0.00    0.20    0.10   56.20    0.00
 52741011 vcpu-1:batch-07       1   40.10   40.50    0.10    1.30   58.10    0.00    0.20    0.10   56.20    0.00
 52741011 vcpu-2:batch-07       1   40.10   40.50    0.00    1.30   58.10    0.00    0.10    0.10   56.20    0.00
 52741011 vcpu-3:batch-07       1   40.10   40.50    0.00    1.30   58.10    0.00    0.20    0.10   56.20    0.00
 52741011 mks:batch-07          1    0.00    0.00    0.00  100.00    0.00    0.00    0.00    0.00    0.00    0.00
 52741011 svga.batch-07         1    0.00    0.00    0.00  100.00    0.00    0.00    0.00    0.00    0.00    0.00
```

Which statements are correct?

- A. A CPU limit holds the VM back: %MLMTD makes up almost all of %RDY.
- B. The host is short of physical CPU.
- C. Co-stop between the vCPUs causes the wait.
- D. Each vCPU is ready about 58% of the time. The group row adds up the VM's worlds, so 232% is not a per-vCPU value.
- E. Look for the limit on the VM and on every parent resource pool, then remove or raise it.
- F. Add vCPUs so the jobs finish faster.

## Likely wrong answer
B: a high %RDY read as a host short of CPU. Or F: more vCPUs for a VM that waits.

## Expected key points
- Answer: A, D, E.
- A: %MLMTD is time the vCPU was ready but not scheduled because running it would break a CPU limit. It is counted inside %RDY: 56.2 of 58.1 per vCPU.
- B is wrong: PCPU UTIL averages 27%. The host has free threads.
- C is wrong: %CSTP is about 0.1%.
- D: esxtop group values are sums over the VM's worlds (NWLD 8), so they pass 100%. Read the vcpu rows, or divide by the vCPU count.
- E: a limit can sit on the VM or on any parent resource pool. Each vCPU runs about 40% of the time: about 4 vCPUs × 40% × 2.5 GHz = 4 GHz, which looks like a 4,000 MHz limit.
- F is wrong: more vCPUs would share the same limit.

## Notes
- Previous id: question-0066 (renamed 2026-11-05).
- Revised 2026-11-12: the screenshot it waited for became an esxtop excerpt typed in the prompt (no new screenshots in 1.0).
- esxtop CPU panel fields (%MLMTD is counted inside %RDY; %RDY is summed over the worlds): vSphere 9.1 documentation, vSphere Monitoring and Performance > resxtop and esxtop > CPU Panel.

## Metadata
```yaml
id: "0066"
title: "High %RDY in esxtop on a quiet host"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, resource-pool, esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/tools/esxtop/overview
knowledge_main: vsphere/tools/esxtop/cpu
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6); revised 2026-11-12"
answer: [A, D, E]
misconception: [B, F]
misconception_type: [unit-and-normalization, provider-vs-consumer]
status: draft
```
