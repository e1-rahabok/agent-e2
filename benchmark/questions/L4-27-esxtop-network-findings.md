# Which esxtop network findings need action?

## Prompt
- ESXi 9.1 host esx-07 in a vSAN cluster. vmk0 is management, vmk1 is vSAN, vmk2 is vMotion.
- The data uplinks vmnic0, vmnic1 and vmnic2 are 25 GbE ports in one team. vmnic3 is a 1 GbE port for out-of-band management.
- Your team's standard: VM ports may show receive drops up to a few tenths of a percent at peak; VMkernel ports for vSAN and vMotion must show none.
- esxtop network panel (n), busiest minute of the day, columns selected:

```text
   PORT-ID USED-BY              TEAM-PNIC DNAME         UP  SPEED FDUPLX  MbTX/s  MbRX/s %DRPTX %DRPRX
  67108866 vmnic0               -         DvsPortset-0   Y  25000      Y 2410.33 2876.51   0.00   0.00
  67108868 vmnic1               -         DvsPortset-0   Y  25000      Y 2295.70 2711.04   0.00   0.00
  67108870 vmnic2               -         DvsPortset-0   Y  10000      Y  890.12  934.80   0.00   0.00
  67108872 vmnic3               -         vSwitch1       Y   1000      N    4.10    3.95   0.00   0.00
  67108874 vmk0                 vmnic3    vSwitch1     n/a    n/a    n/a    1.22    0.98   0.00   0.00
  67108875 vmk1                 vmnic1    DvsPortset-0 n/a    n/a    n/a 1650.40 1702.13   0.00   0.31
  67108876 vmk2                 vmnic2    DvsPortset-0 n/a    n/a    n/a    0.00    0.00   0.00   0.00
  67108880 2451873:web-01.eth0  vmnic0    DvsPortset-0 n/a    n/a    n/a  410.20  388.65   0.00   0.10
  67108881 2459012:app-02.eth0  vmnic1    DvsPortset-0 n/a    n/a    n/a  205.77  240.19   0.00   0.00
  67108882 2460558:db-03.eth0   vmnic0    DvsPortset-0 n/a    n/a    n/a  611.03  702.44   0.00   0.00
```

Which findings need action?

- A. vmk1, the vSAN VMkernel port, drops 0.31% of the packets it receives.
- B. web-01, a busy web VM, drops 0.10% of the packets it receives.
- C. vmnic3, the out-of-band management port, runs at half duplex.
- D. vmk2, the vMotion port, shows 0 Mb/s: its link or its uplink is down.
- E. vmnic2 runs at 10,000 Mb/s while its team peers run at 25,000 Mb/s.

## Likely wrong answer
B: applying the zero-drop rule of a VMkernel network to a VM port. Or D: reading an idle port as a broken one.

## Expected key points
- Answer: A, C, E.
- A: a dedicated vSAN network should drop nothing. Receive drops on the vSAN VMkernel port need action: the host's CPU for packet processing, the uplink, and the physical path.
- B is within the stated standard for a VM port at peak: watch it, no action now.
- C: half duplex (FDUPLX N) is a fault on any link: check the port settings on both sides, the cable and the switch port.
- D is not a fault: no vMotion runs in that minute, so the port is idle. Its uplink vmnic2 is up (UP Y) and carries other traffic; a down link would show UP N on the vmnic.
- E: one team member negotiated down to 10 Gb/s: check the cable, the transceiver and the switch port. Every port mapped to it (here vMotion) gets less bandwidth.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12 (question set 1.0): the screenshot became an esxtop excerpt in the prompt; the team standard is stated in the prompt (fairness F3); a negotiated-speed finding added. After the independent review, the units option was replaced (question 0029 owns that fact).

## Metadata
```yaml
id: "0069"
title: "Which esxtop network findings need action?"
product: [vsphere, vsan]
technology: [network]
object: [esxi, network, vm]
tool: [esxtop]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/tools/esxtop/network
  - vsphere/technology/network/configuration/network-configuration-review
  - vsphere/object-types/esxi/configuration/esxi-configuration-review
knowledge_main: vsphere/tools/esxtop/network
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [threshold-transplanted]
status: draft
```
