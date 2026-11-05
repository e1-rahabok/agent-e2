# iSCSI: network bytes do not match storage bytes

## Prompt
The attached table is a one-week export, in 5-minute samples, of one ESXi host that uses iSCSI only, on a dedicated 10 GbE VMkernel port with MTU 9,000: storage read and write IOPS and bytes, and network receive and transmit packets and bytes of the iSCSI vmnic.

- The workload is almost all 8 KB reads.
- In the busiest sample the host read 1,000,000 IOs of 8 KB.
- The storage team asks why network receive bytes are higher than storage read bytes, and why there are transmit packets at all during a read-only workload.

Explain the difference. Work out the expected network receive and transmit bytes and packets for the busiest sample.

## Input to supply
- Source: VCF Operations 9.1 export, one host, 7 days, 5-minute samples (2,016 rows).
- Columns: time, storage read IOPS, storage write IOPS, storage read bytes, storage write bytes, network packets received, network packets transmitted, network bytes received, network bytes transmitted (iSCSI vmnic only).
- Condition for the key: a host with iSCSI over MTU 9,000 and an 8 KB read workload; the busiest sample holds about 1,000,000 reads. If the real numbers differ, record them in the Notes and the key is recalculated.
- Save as `benchmark/questions/84/host-iscsi-network-vs-storage-week.xlsx`.

## Likely wrong answer
"Reads go out as network Transmit, because the host sends the read."

## Expected key points
- Storage counters measure the logical payload; network counters measure whole frames: headers and acknowledgements in both directions.
- Per 8 KB read with MTU 9,000: Transmit 2 packets, 170 bytes (the read command 106 bytes + the ACK of the data 64 bytes); Receive 2 packets, 8,362 bytes (the ACK of the command 64 bytes + the data frame 8,298 bytes).
- Busiest sample: storage read 8,192,000,000 bytes; network receive about 8,362,000,000 bytes and 2,000,000 packets; transmit about 170,000,000 bytes and 2,000,000 packets.
- A read is mostly Receive; Transmit carries only the command and the acknowledgement. A write reverses the pattern.
- With MTU 9,000 the 8 KB block fits one frame; with 1,500 it takes several frames, each with its own headers.

## Notes
- Previous id: question-0084 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "84"
title: "iSCSI: network bytes do not match storage bytes"
product: [vsphere]
technology: [network, storage]
task: explain-mechanism
level: 400
answer_type: judged
input: [table]
knowledge:
  - vsphere/technology/storage/concepts/ip-storage-network-accounting
attachments:
  - 84/host-iscsi-network-vs-storage-week.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
