# Which VMs need a network investigation

## Prompt
The attached table is a VCF Operations export of 400 VMs over one week, in 5-minute samples summarized per VM: Packets Dropped (%), received and transmitted packets dropped, packets per second and throughput.

- fw-01 (a firewall appliance) shows receive drops of about 2% at its peak packet rate, every day.
- batch-07 shows Packets Dropped (%) of 95% in one 5-minute sample, at very low throughput, and near 0 otherwise.
- app-12 shows transmit drops above 0 every day.

Which VMs need a network investigation? Choose all that apply.

- A. fw-01: check the vNIC receive ring with vsish on its host.
- B. batch-07: it had a network outage.
- C. app-12: transmit drops count against its VM KPI, even without complaints.
- D. None: Packets Dropped (%) below 99% is normal.

## Input to supply
- Source: VCF Operations 9.1 export, 400 powered-on VMs, 7 days, one row per VM.
- Columns: VM name, Packets Dropped (%) max and p95, received packets dropped (sum), transmitted packets dropped (sum), packets per second (max), throughput KBps (max), time of the max.
- Condition for the key: rows fw-01, batch-07 and app-12 as described in the prompt; most other VMs have 0 drops. Rename VMs if needed and keep these three names.
- Save as `benchmark/questions/82/vm-network-400-vms.xlsx`.

## Likely wrong answer
B: reading 95% dropped as an outage.

## Expected key points
- Answer: A, C.
- fw-01: steady receive drops at peak packet rate on a network VM point to the receive ring; vsish shows the reason (running out of buffers, ring full). Consider a larger ring and NetQ RSS.
- batch-07: Packets Dropped (%) = dropped / (dropped + delivered); at low throughput a few receive drops give a high percentage for a short time. Not an outage.
- app-12: TCP retransmits hide transmit drops; transmit dropped packets is a contention sub-metric of the VM KPI (VM Performance).

## Notes
- Previous id: question-0082 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0082"
title: "Which VMs need a network investigation"
product: [vsphere, vcf-operations]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/troubleshooting/vnic-rx-drops
  - vsphere/object-types/vm/kpis/vm-performance
attachments:
  - 0082/vm-network-400-vms.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
misconception: [B]
status: awaiting-input
```
