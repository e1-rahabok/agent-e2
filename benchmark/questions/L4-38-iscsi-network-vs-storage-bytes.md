# iSCSI: network bytes do not match storage bytes

## Prompt
- ESXi host esx-21 uses iSCSI only, through software iSCSI adapter vmhba64 on a dedicated 10 GbE VMkernel port with MTU 9,000, carried by vmnic4.
- The workload is almost all 8 KB reads.
- [The attached export](0084/esx-21-iscsi-storage-and-vmnic4.csv) joins two vCenter charts of esx-21 for 4 hours of 5-minute samples: the storage adapter chart (read and write requests per second, read and write rates) and the vmnic4 network chart (packets as a sum per sample, data rates). KB is 1,024 bytes in this export.
- The storage team asks two things: why vmnic4 receives more data than the adapter reads, and why vmnic4 transmits millions of packets per sample during a read-only workload.

Which statements about the two counters and the busiest sample are correct?

- A. Storage counters measure the logical payload; network counters measure whole frames, with headers and acknowledgements.
- B. Reads go out as network transmit, because the host sends the data request.
- C. The extra receive bytes on vmnic4 are retransmissions or a counter error.
- D. A read arrives mostly as network receive; transmit carries only the read command and the acknowledgement of the data.
- E. With MTU 9,000, each 8 KB read comes back in one data frame.
- F. The millions of transmitted packets per sample show that the host also writes data.
- G. At 10:00, network receive is expected about 2% above the read rate: about 27,200 KBps.
- H. At 10:00, network transmit is expected at about 550 KBps.
- I. About two packets per read go each way: about 2 million packets per sample in each direction at 10:00.
- J. The vmnic4 data rates are in kilobits per second, so receive is far below the adapter's read rate.
- K. The vmnic4 packet counts are per second, so 2 million packets per second put the 10 GbE link near its limit.
- L. With MTU 1,500, each 8 KB read would need several frames, each with its own headers.
- M. The export matches the frame model: receive and transmit at 10:00 are within 1% of the expected values.
- N. Each data frame adds about 106 bytes of Ethernet, IP, TCP and iSCSI headers to the 8 KB payload.

## Likely wrong answer
- B: "Reads go out as network transmit, because the host sends the data request."
- C: "The extra receive bytes are retransmissions or a counter error."

## Expected key points
- Answer: A, D, E, G, H, I, L, M, N.
- A true: storage read bytes count 8,192 per read; the network counts every frame in both directions.
- B false: only the command is transmit; the data returns as receive.
- C false: the extra is headers and the acknowledgement of each command; network bytes are not storage throughput.
- D true: per read, transmit is the command (106 bytes) and the acknowledgement of the data (64 bytes). A write reverses the pattern.
- E true: MTU 9,000 allows a TCP segment of up to 8,960 bytes, so 8 KB fits one jumbo frame. TCP can combine or delay acknowledgements, so 1-2 small frames each way per read.
- F false: writes are near 0; the transmitted packets are read commands and acknowledgements, about two per read.
- G true: about 3,333 reads per second (26,666 KBps); 8,362 bytes received per read: 3,333 x 8,362 / 1,024 is about 27,200 KBps.
- H true: 3,333 x 170 bytes / 1,024 is about 553 KBps.
- I true: 3,333 x 2 x 300 s is about 2 million packets per sample each way.
- J false: KB is 1,024 bytes in this export; vCenter network rates labelled Kbps are kilobytes per second.
- K false: vCenter packet counters are totals per sample, not per second: about 6,700 packets per second each way.
- L true: more packets and more overhead per I/O.
- M true: 27,270 KBps against about 27,220, and 553.8 against about 553: the export matches.
- N true: 14 + 20 + 20 + 48 + 4 = 106 bytes; the data frame is 8,298 bytes.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the 2,016-row workbook became a 48-row CSV; after the independent review, packets are sums per sample, as vCenter shows them, and the key accepts 1-2 packets per read each way. The CSV is synthetic, generated with a fixed seed from the frame model of ip-storage-network-accounting, with ±0.2% noise.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Knowledge added: vcenter-statistics (network rates in kilobytes per second; packet counts as totals per interval).

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
answer_type: deterministic
answer: [A,D,E,G,H,I,L,M,N]
misconception: [B,C]
input: [table]
knowledge:
  - vsphere/technology/storage/concepts/ip-storage-network-accounting
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/storage/concepts/ip-storage-network-accounting
attachments:
  - 0084/esx-21-iscsi-storage-and-vmnic4.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [unit-and-normalization]
status: draft
```
