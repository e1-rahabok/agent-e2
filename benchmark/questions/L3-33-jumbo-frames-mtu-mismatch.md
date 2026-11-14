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

- A. A device between the host and the array still has a 1,500-byte MTU and drops larger frames.
- B. With -d nothing may be fragmented, so the path cannot carry a frame above 1,500 bytes whole.
- C. The iSCSI sessions log in and the paths are Active, so the MTU cannot be the cause here.
- D. The lost frames show as Receive packets dropped on the VMs that use the iSCSI datastore.
- E. The fault is on the host itself: vmk1 cannot send any frame that is larger than 1,500 bytes.
- F. Carry MTU 9,000 on every hop of the path, or set vmk1 and the switch back to 1,500 for now.

## Likely wrong answer
C: "the sessions are up, so the network is fine". Or D: looking for the loss in the VM counters.

## Expected key points
- Answer: A, B, F.
- 1472 and 8972 are the ICMP payloads that fill a 1,500-byte and a 9,000-byte frame (28 bytes of IP and ICMP headers). 1472 passes, 1473 fails: the largest frame the path carries is 1,500 bytes.
- A and B: with the don't-fragment flag set, a frame above a hop's MTU is dropped at that hop. A time-out with no error message means the host sent the frame and the path lost it.
- C is wrong: logins, discovery and small reads use small frames, which pass. Large data frames are lost, so IO stalls and times out.
- D is wrong: iSCSI runs on the VMkernel port, not on the VMs' network adapters. The VMs see slow or failed disk IO, not network drops.
- E is wrong: if vmk1 or the virtual switch could not send the frame, vmkping would fail at once with a local error ("Message too long"), not time out.
- F: jumbo frames work only end to end (switch ports, any router, the array ports); set the physical side first, then the virtual switch and VMkernel ports.
- Why the loss is in the middle: an endpoint with a 1,500 MTU would advertise a smaller TCP segment size, and both sides would adapt. A switch port in the middle cannot do that; it drops the jumbo frame.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B, F]
misconception: [C, D]
misconception_type: [layer-confusion]
status: draft
```
