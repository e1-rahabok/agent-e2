# iSCSI: network bytes do not match storage bytes

## Prompt
- ESXi host esx-21 uses iSCSI only, through software iSCSI adapter vmhba64 on a dedicated 10 GbE VMkernel port with MTU 9,000, carried by vmnic4.
- The workload is almost all 8 KB reads.
- [The attached export](0084/esx-21-iscsi-storage-and-vmnic4.csv) joins two vCenter charts of esx-21 for 4 hours of 5-minute samples: the storage adapter chart (read and write requests, read and write rates) and the vmnic4 network chart (packets received and transmitted, data rates), with the counter names as vCenter shows them.
- The storage team asks two things: why vmnic4 receives more data than the adapter reads, and why vmnic4 transmits millions of packets during a read-only workload.

Which statements about the two counters and the busiest sample are correct?

- A. In every sample, the gap between vmnic4 receive and the adapter's read rate moves in step with the number of reads.
- B. Reads go out as network transmit, because the host sends the data request.
- C. The extra receive bytes on vmnic4 are retransmissions or a counter error.
- D. Per read, transmit carries only the read command and the acknowledgement of the data.
- E. With MTU 9,000, each 8 KB read comes back in one data frame.
- F. The millions of transmitted packets per sample show that the host also writes data.
- G. At 10:00, network receive is expected about 2% above the read rate: about 27,200 KBps.
- H. At 10:00, network transmit is expected at about 550 KBps.
- I. At 10:00, the packet counts show about two packets per read in each direction.
- J. The vmnic4 data rates are in kilobits per second, so receive is far below the adapter's read rate.
- K. The vmnic4 packet counts are per second, so 2 million packets per second put the 10 GbE link near its limit.
- L. With MTU 1,500, each 8 KB read would return in six data frames instead of one.
- M. The export matches the frame model: receive and transmit at 10:00 are within 1% of the expected values.
- N. Each data frame adds about 106 bytes of Ethernet, IP, TCP and iSCSI headers to the 8 KB payload.

## Answers
A, D, E, G, H, I, L, M, N

## Explanation
- A is correct: receive counts 8,362 bytes per read against 8,192 of storage payload, about 170 bytes of headers and acknowledgement per read at MTU 9,000. The gap is about 335 KBps at 08:00 (1,837 reads per second), about 604 KBps at 10:00 (3,333) and about 305 KBps at 11:55 (1,781): 1.9-2.3% of the read rate in every sample, about 170 bytes per read within the export's noise.
- B is wrong: only the command is transmit; the data returns as receive.
- C is wrong: the extra is headers and the acknowledgement of each command; network bytes are not storage throughput.
- D is correct: per read, transmit is the command (106 bytes) and the acknowledgement of the data (64 bytes). A write reverses the pattern.
- E is correct: MTU 9,000 allows a TCP segment of up to 8,960 bytes, so 8 KB fits one jumbo frame. TCP can combine or delay acknowledgements, so 1-2 small frames each way per read.
- F is wrong: writes are near 0; the transmitted packets are read commands and acknowledgements, about two per read.
- G is correct: about 3,333 reads per second (26,666 KBps); 8,362 bytes received per read: 3,333 x 8,362 / 1,024 is about 27,200 KBps.
- H is correct: 3,333 x 170 bytes / 1,024 is about 553 KBps.
- I is correct: 3,333 reads per second x 2 x 300 s is about 2 million packets per sample each way; the export shows 2,003,440 received and 2,001,545 transmitted.
- J is wrong: vCenter network data rates are kilobytes per second (KB of 1,024 bytes), like the adapter's read rate, so the two columns compare directly.
- K is wrong: vCenter packet counters are totals per sample, not per second: about 6,700 packets per second each way. 2 million packets per second of 8 KB frames would also be far more than the 27,270 KBps received.
- L is correct: MTU 1,500 allows a TCP segment of up to 1,460 bytes; 8,192 bytes of data plus the 48-byte iSCSI header are 8,240 bytes, which need six segments (8,240 / 1,460 is about 5.6), each with its own headers.
- M is correct: 27,270 KBps against about 27,220, and 553.8 against about 553: the export matches.
- N is correct: 14 + 20 + 20 + 48 + 4 = 106 bytes; the data frame is 8,298 bytes.
- Misconception: B: "Reads go out as network transmit, because the host sends the data request." - C: "The extra receive bytes are retransmissions or a counter error."

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Counts only after author approval.
- Revised 2026-11-12: the 2,016-row workbook became a 48-row CSV; after the independent review, packets are sums per sample, as vCenter shows them, and the key accepts 1-2 packets per read each way. The CSV is synthetic, generated with a fixed seed from the frame model of ip-storage-network-accounting, with ±0.2% noise.
- Knowledge added 2026-11-14: vcenter-statistics (network rates in kilobytes per second; packet counts as totals per interval).
- Audit 2026-11-15: A (payload against frames) and L (several frames at MTU 1,500) restated the theory half 0410; A is now a reading of the export over the 4 hours (the gap moves with the read rate) and L a frame count for this workload. D shortened. Key unchanged.
- Re-review 2026-11-16: the stem and the CSV header no longer state the units ("sum per sample", "KBps", "KB is 1,024 bytes"), so J and K test the vCenter units, not reading; headers renamed to the vCenter form "<counter> for <object>", values unchanged. I no longer states the packet unit beside K. A no longer says "fixed" (the gap per read spans 154-187 bytes per sample). Key unchanged.

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
misconception: [B,C]
input: [table]
knowledge:
  - vsphere/technology/storage/concepts/ip-storage-network-accounting
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/storage/concepts/ip-storage-network-accounting
attachments:
  - 0084/esx-21-iscsi-storage-and-vmnic4.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [unit-and-normalization]
pair: "0410"
status: draft
```
