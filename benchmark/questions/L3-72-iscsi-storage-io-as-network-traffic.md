# iSCSI storage IO as network traffic

## Prompt
- An ESXi host reaches its datastores only through a software iSCSI adapter, on a dedicated VMkernel port with MTU 1,500.
- The VMs read and write 4 KB blocks. The network team compares the vmnic counters of that port with the storage adapter counters.

Which statements about the two sets of counters are correct?

- A. The data of a write leaves the host as network transmit.
- B. The data of a read arrives at the host as network receive.
- C. Storage reads appear as network transmit, because the host sends the read request.
- D. Network bytes run above storage bytes, because every frame carries Ethernet, IP, TCP and iSCSI headers.
- E. During a read-only workload the iSCSI vmnic transmits nothing.
- F. With MTU 1,500, one 4 KB block needs several frames, each with its own headers.
- G. Network receive above the adapter's read rate shows a counter fault: open a case.

## Likely wrong answer
C: reads go out as network transmit because the host issues the command. Or E, the overshoot: reads are pure receive, with no transmit at all.

## Expected key points
- Answer: A, B, D, F.
- A true: a write reverses the read pattern: the data goes out as transmit.
- B true: the array returns the read data in receive frames.
- C false: only the command is transmit; the data returns as receive.
- D true: storage counters measure the logical payload; network counters measure whole frames with headers, and the acknowledgements in both directions.
- E false: the read command and the acknowledgement of the data frame go out as transmit, so a read-only workload still transmits small frames.
- F true: a 1,500-byte MTU leaves less than 4 KB of payload per frame, so the block needs several frames, each with its own headers: more packets and more overhead per IO.
- G false: the gap is headers and acknowledgements; network bytes are not storage throughput.

## Notes
- Theory half of the pair with 0084 (practical; design.md, section 3.9). Different MTU and block size from 0084.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B15 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0410"
title: "iSCSI storage IO as network traffic"
product: [vsphere]
technology: [storage, network]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [esxi, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/ip-storage-network-accounting
knowledge_main: vsphere/technology/storage/concepts/ip-storage-network-accounting
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B15"
answer: [A, B, D, F]
misconception: [C]
misconception_type: [unit-and-normalization]
pair: "0084"
status: draft
```
