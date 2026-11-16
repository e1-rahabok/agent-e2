# iSCSI storage IO as network traffic

## Prompt
- An ESXi host reaches its datastores only through a software iSCSI adapter, on a dedicated VMkernel port with MTU 1,500.
- The VMs read and write 4 KB blocks. The network team compares the vmnic counters of that port with the storage adapter counters.

Which statements about the two sets of counters are correct?

- A. The data of a write leaves the host as network transmit.
- B. The data of a read arrives at the host as network receive.
- C. A read-heavy iSCSI workload shows mostly as network transmit.
- D. Network bytes run above storage bytes: each frame adds its own headers.
- E. During a read-only workload the iSCSI vmnic transmits nothing.
- F. With MTU 1,500, a 4 KB write leaves the host in three or more frames.
- G. Network receive above the adapter's read rate shows a fault in one of the two counters.

## Likely wrong answer
C: reads go out as network transmit because the host issues the command. Or E, the overshoot: reads are pure receive, with no transmit at all.

## Expected key points
- Answer: A, B, D, F.
- A is correct: a write reverses the read pattern: the data goes out as transmit.
- B is correct: the array returns the read data in receive frames.
- C is wrong: the misconception. Only the read command and the acknowledgement of the data go out as transmit; the data returns as receive, so a read-heavy workload is mostly receive.
- D is correct: storage counters measure the logical payload; network counters measure whole frames, each with Ethernet, IP, TCP and iSCSI headers, and the acknowledgements in both directions.
- E is wrong: the read command and the acknowledgement of the data frame go out as transmit, so a read-only workload still transmits small frames.
- F is correct: MTU 1,500 allows a TCP segment of up to 1,460 bytes (as MTU 9,000 allows 8,960); 4,096 bytes of data plus the 48-byte iSCSI header need three segments, each with its own Ethernet, IP and TCP headers.
- G is wrong: the gap is headers and acknowledgements; network bytes are not storage throughput.

## Notes
- Theory half of the pair with 0084 (practical; design.md, section 3.9). Different MTU and block size from 0084.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B15 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: C and F reworded away from 0084 (F is now a frame count for a write). Key unchanged: A, B, D, F.
- Audit 2026-11-15: D lost its reason clause and its length (D was the only correct option with a reason); G no longer ends in "open a case", a wrong-only cue in the bank. Key unchanged.

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
