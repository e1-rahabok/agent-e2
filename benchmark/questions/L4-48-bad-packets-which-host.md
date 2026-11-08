# Bad network packets: find the host and the cause

## Prompt
The screenshot is the VCF Operations view of one cluster: Cluster Performance with Highest ESXi Bad Network Packets in the yellow range. The attached table is an export of the vmnics of the 64 hosts in that cluster, for the same day: speed, duplex, driver and firmware version, packets received and transmitted, errors and drops received and transmitted.

Which host causes the sub-metric, what is the likely cause, and what do you do?

## Input to supply
- Screenshot: VCF Operations 9.1, cluster > Metrics, `vCommunity|Cluster Performance|Highest ESXi Bad Network Packets` and the score, one day.
- Table: export of 64 hosts × their vmnics (about 256 rows): host, vmnic, speed, duplex, driver, firmware, packetsRx, packetsTx, errorsRx, errorsTx, droppedRx, droppedTx (sums per 5-minute cycle at the peak).
- Condition for the key: one host (record its name in the Notes) has errorsRx above 0 on one vmnic, and that vmnic has a different driver or firmware version from the others; all other hosts have 0 errors and 0 drops.
- Save as `benchmark/questions/88/host-vmnic-stats-64-hosts.xlsx` and `benchmark/questions/88/vcf-operations-cluster-performance-bad-packets.png`.

## Likely wrong answer
"The sub-metric is an average of all hosts, so the cluster network is degraded everywhere."

## Expected key points
- The sub-metric takes the highest host, not a sum or average: (errorsRx + errorsTx + droppedRx + droppedTx) / (packetsRx + packetsTx) × 100, in the last 5-minute cycle.
- The host named in the Notes: errors on one vmnic whose driver or firmware differs from the others.
- Action: check the vmnic driver and firmware, the cable and the physical switch port.
- Any bad packet is yellow: green is exactly 0 and is Excluded from the KPI.
- Packets Received and Transmitted totals are deactivated by default in VCF Operations: they must be activated in the policy, or the sub-metric has no data.

## Notes
- Previous id: question-0088 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0088"
title: "Bad network packets: find the host and the cause"
product: [vsphere, vcf-operations]
technology: [network]
task: troubleshoot
level: 400
answer_type: judged
input: [table, screenshot]
knowledge:
  - vcf-operations/kpis/cluster-performance
  - vsphere/object-types/cluster/troubleshooting/cluster-vm-contention
  - vsphere/technology/network/metrics/host/errors
attachments:
  - 0088/host-vmnic-stats-64-hosts.xlsx
  - 0088/vcf-operations-cluster-performance-bad-packets.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
