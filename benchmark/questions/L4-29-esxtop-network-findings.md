# Which esxtop network findings need action?

## Prompt
The attached screenshot is the esxtop network panel (n) of one ESXi host in a vSAN cluster.

Which findings need action? Choose all that apply.

- A. The vSAN VMkernel port shows %DRPRX above 0.
- B. A busy web VM shows %DRPRX of 0.1%.
- C. One vmnic uplink shows FDUPLX N.
- D. MbTX/s of a VM does not match the KBps shown for it in the vSphere Client.

## Input to supply
- Tool: esxtop on one ESXi 9.1 host in a vSAN cluster, network panel (press n).
- Must show the columns PORT-ID, USED-BY, DNAME, UPLINK, SPEED, FDUPLX, MbTX/s, MbRX/s, %DRPTX, %DRPRX.
- Condition for the key: the vSAN vmk port has %DRPRX above 0 (for example 0.3); one web VM has %DRPRX at 0.1; one vmnic shows FDUPLX N. If a real host has no half-duplex link, the author may edit only that cell and say so in the Notes.
- Mask names if they reveal the customer.
- Save as `benchmark/questions/69/esxtop-network-panel.png`.

## Likely wrong answer
D: treating the bits vs bytes difference as a fault.

## Expected key points
- Answer: A, C.
- On dedicated networks such as vSAN and vMotion, expect 0% drops on every host at all times: any drop on the vSAN port needs action.
- On VM ports, expect at most 0.x%: 0.1% on a busy VM is within that.
- FDUPLX N (half duplex) is a problem: check the link, the physical switch port and the NIC settings.
- D is not a fault: esxtop shows megabits, the vSphere Client shows kilobytes.

## Notes
- Previous id: question-0069 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0069"
title: "Which esxtop network findings need action?"
product: [vsphere, vsan]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/tools/esxtop/network
  - vsphere/tools/esxtop/units-vs-vsphere-client
attachments:
  - 0069/esxtop-network-panel.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [D]
status: awaiting-input
```
