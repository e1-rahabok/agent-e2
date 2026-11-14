# iSCSI: network bytes do not match storage bytes

## Prompt
- ESXi host esx-21 uses iSCSI only, through software iSCSI adapter vmhba64 on a dedicated 10 GbE VMkernel port with MTU 9,000, carried by vmnic4.
- The workload is almost all 8 KB reads.
- [The attached export](0084/esx-21-iscsi-storage-and-vmnic4.csv) joins two vCenter charts of esx-21 for 4 hours of 5-minute samples: the storage adapter chart (read and write requests per second, read and write rates) and the vmnic4 network chart (packets as a sum per sample, data rates). KB is 1,024 bytes in this export.
- The storage team asks two things: why vmnic4 receives more data than the adapter reads, and why vmnic4 transmits millions of packets per sample during a read-only workload.

Explain both. Then, for the busiest sample, estimate the network receive and transmit data rates and packet counts you expect, and compare them with the export.

## Likely wrong answer
"Reads go out as network transmit, because the host sends the data request; the extra receive bytes are retransmissions or a counter error."

## Expected key points
- Storage counters measure the logical payload. Network counters measure whole frames: headers on every frame, and acknowledgements in both directions.
- A read is mostly receive: the data comes back from the array. Transmit carries only the read command and the acknowledgement of the data. A write reverses the pattern.
- Per 8 KB read with MTU 9,000: one data frame of about 8.3 KB comes back (8 KB fits one jumbo frame), plus 1-2 small frames each way for the command and the acknowledgements (TCP can combine or delay them). Each frame carries about 54 bytes of Ethernet, IP and TCP headers plus the iSCSI header.
- Busiest sample, 10:00: about 3,333 reads per second (26,666 KBps). Expected receive about 2% above the read rate, about 27,200 KBps, and about 2 packets per read; transmit only about 550 KBps, also about 2 packets per read, about 2 million packets per sample each way. The export matches.
- With MTU 1,500 each 8 KB read would need several frames, each with its own headers: more packets and more overhead per IO.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the 2,016-row workbook became a 48-row CSV; after the independent review, packets are sums per sample, as vCenter shows them, and the key accepts 1-2 packets per read each way. The CSV is synthetic, generated with a fixed seed from the frame model of ip-storage-network-accounting, with ±0.2% noise.

## Metadata
```yaml
id: "0084"
title: "iSCSI: network bytes do not match storage bytes"
product: [vsphere]
technology: [network, storage]
object: [esxi, network]
tool: [vcenter]
task: explain-mechanism
level: 400
answer_type: judged
input: [table]
knowledge:
  - vsphere/technology/storage/concepts/ip-storage-network-accounting
knowledge_main: vsphere/technology/storage/concepts/ip-storage-network-accounting
attachments:
  - 0084/esx-21-iscsi-storage-and-vmnic4.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [unit-and-normalization]
status: draft
```
