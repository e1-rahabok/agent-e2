# Setting a vNIC speed

## Prompt
- An application owner asks for their VM to be limited to 500 Mbps of network bandwidth.

Can you set the VM's vNIC speed to 500 Mbps? If not, what controls exist?

## Likely wrong answer
"Yes, set the vNIC speed in Edit Settings."

## Expected key points
- No: a vNIC speed cannot be set. It takes the speed of the vmnic behind its port group (1, 10 or 25 GbE, with the right driver).
- Network allocation per VM is coarse; physical bandwidth is shared and typically oversubscribed.
- Network I/O Control (NIOC) and traffic shaping exist, but they are set on the switch or port group, not as VM configuration properties.

## Notes
- Previous id: question-0041 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "41"
title: "Setting a vNIC speed"
product: [vsphere]
technology: [network]
task: judge-setting
level: 200
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/concepts/netioc
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
status: draft
```
