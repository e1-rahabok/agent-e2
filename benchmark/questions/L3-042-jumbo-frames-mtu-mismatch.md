# iSCSI trouble after enabling jumbo frames

## Prompt
- Last night the team set MTU 9,000 on the distributed switch and on vmk1, the iSCSI VMkernel port of host esx-03.
- Since then the iSCSI sessions log in and every path shows Active, but VMs on the iSCSI datastore see IO timeouts and long stalls.
- Tests from esx-03 to the array port 10.20.0.50:

```text
vmkping -I vmk1 -d -s 1472 10.20.0.50   → replies, 0% loss
vmkping -I vmk1 -d -s 1473 10.20.0.50   → no reply, 100% loss, no error message
vmkping -I vmk1 -d -s 8972 10.20.0.50   → no reply, 100% loss, no error message
```

Which statements are correct?

- A. A hop on the path to the array, a switch port or the array port, still has a 1,500-byte MTU.
- B. With -d nothing may be fragmented, so the path cannot carry a frame above 1,500 bytes whole.
- C. The iSCSI sessions log in and the paths are Active, so the MTU cannot be the cause here.
- D. The lost frames show as Receive packets dropped on the VMs that use the iSCSI datastore.
- E. The fault is on the host itself: vmk1 cannot send any frame that is larger than 1,500 bytes.
- F. Set MTU 9,000 on every hop of the path to the array, the physical side first.
- G. The 8972 test is too small for a 9,000-byte MTU: the full-size test uses -s 9000.

## Likely wrong answer
C: "the sessions are up, so the network is fine". Or D: looking for the loss in the VM counters. Or G: "test 9,000 with -s 9000".

## Expected key points
- Answer: A, B, F.
- A is correct: 1472 is the ICMP payload that fills a 1,500-byte MTU (28 bytes of IPv4 and ICMP headers); 1472 passes and 1473 times out with no error, so a hop between the host and the array, a switch port or the array port, still carries only 1,500 bytes. The 1472 reply shows the array answers ping.
- B is correct: with the don't-fragment flag set, a frame above a hop's MTU is dropped at that hop instead of being fragmented; the largest frame the path carries whole is 1,500 bytes.
- C is wrong: logins, discovery and small reads use small frames, which pass a mismatch; large data frames are lost, so IO stalls and times out.
- D is wrong: iSCSI runs on the VMkernel port, not on the VMs' network adapters; the VMs see slow or failed disk IO, not network drops.
- E is wrong: if vmk1 or the virtual switch could not send the frame, vmkping would fail at once with a local error ("Message too long"), not time out.
- F is correct: jumbo frames work only end to end (switch ports, any router, the array ports); raise the physical side first, then the virtual switch and the VMkernel ports.
- G is wrong: -s is the ICMP payload, so 8972 plus 28 bytes of headers fills 9,000 exactly; -s 9000 would need a 9,028-byte MTU and fail even on a correct jumbo path.

## Notes
- 2026-11-14: options B, C and E were not decidable from the knowledge base; the vmkping facts (don't-fragment flag, 28 bytes of IPv4 and ICMP headers, a local Message too long error against a time-out, small frames passing a mismatch) were added to network-configuration-review from the Broadcom KB articles below (project/question-pairing-2026-11-14.md). Key unchanged: A, B, F.
- Review 2026-11-15: A names the hops it covers (a switch port or the array port). Key unchanged.
- Audit 2026-11-15: F made one fact (the "or set back to 1,500" alternative removed); G added from network-configuration-review Misconceptions (the -s payload); the key point on TCP segment size was removed, as the knowledge base does not state it: A is decided by the ping, not by the symptom.
- Vendor sources: Broadcom KB 313061, Testing jumbo frame pings from ESXi over the network (1472, 1473 and 8972; 28 bytes of overhead), https://knowledge.broadcom.com/external/article/313061/testing-jumbo-frame-pings-from-esxi-over.html; Broadcom KB 419088, Risks and potential impacts of changing the MTU on a virtual switch ("Message too long"; change the physical path first), https://knowledge.broadcom.com/external/article/419088/risks-and-potential-impacts-of-changing.html; Broadcom KB 448714, iSCSI storage connectivity issues due to MTU mismatch, https://knowledge.broadcom.com/external/article/448714/iscsi-storage-connectivity-issues-or-slo.html.

## Metadata
```yaml
id: "0213"
title: "iSCSI trouble after enabling jumbo frames"
product: [vsphere]
technology: [network, storage]
object: [esxi, network]
tool: [none]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/configuration/network-configuration-review
  - sp5-framework/concepts/configuration-management
knowledge_main: vsphere/technology/network/configuration/network-configuration-review
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, B, F]
misconception: [C, D, G]
misconception_type: [layer-confusion, unit-and-normalization]
status: draft
```
