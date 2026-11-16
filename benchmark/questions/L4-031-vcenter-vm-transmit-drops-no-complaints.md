# Transmit drops with no complaints

## Prompt
- app-12 is a Linux application server with one VMXNET3 adapter. The vCenter statistics level of the 1-day interval was raised to 3 last month.
- [The attached chart export](0074/app-12-network-packets-past-day.csv) is the vSphere Client advanced chart of its network packets, past day, 06:00-18:00, one row per 5-minute sample.
- Nobody has reported a problem with the application. The owner says the drops can be ignored.

Which statements are correct?

- A. TCP in the guest resends the lost packets, so no complaint does not prove there is no impact.
- B. The drops repeat every 15 minutes: look with the network team for something with that rhythm.
- C. At full-size frames, the drops of one of the 15-minute bursts are well under 1 MB of data to resend.
- D. Receive packets dropped is 0, so the VM's traffic is lost in neither direction on the path.
- E. The drops are well under 1% of the packets sent, so the owner is right that they can be ignored.

## Likely wrong answer
E: "a small share and no complaints, so it does not matter". Or D: reading 0 receive drops as a clean path in both directions.

## Expected key points
- Answer: A, B.
- A is correct: a dropped transmit is recovered by TCP retransmission in the guest. The application sees delay, not an error, so the lack of complaints says nothing about the impact.
- B is correct: a regular pattern points to something scheduled (a job, a backup, a device on the path). Repeating drops are worth raising with the network team even when the share is small.
- C is wrong: the export shows about 2,300-2,700 transmit drops in each burst sample (at :00, :15, :30 and :45, near 0 in between); at about 1.5 KB per full-size frame that is about 3.5-4 MB to resend per burst.
- D is wrong: the two directions are counted apart; the transmit side drops every 15 minutes while the receive side is clean.
- E is wrong: the share is small, but the drops are regular and their cost is resend delay.

## Notes
- Audit 2026-11-15: the stem states the raised statistics level (at the default level a VM keeps no network drop history, vcenter-statistics); level 400 -> 300 (its theory half 0404 is 300 on the same fact; the practical adds reading a 15-minute rhythm); C (a receive ring causing transmit drops, a throwaway with receive drops at 0) replaced with the resend volume of a burst (packets-dropped, Profile transmit drops; shared with the pair 0404 H). The Distributed Firewall and top-of-rack replacements were not used: each would be a third question on its fact.
- Revised 2026-11-12: the screenshot became a CSV chart export; the management pack score removed (fairness); the question now tests transmit drops hidden by TCP and a regular drop pattern; after the independent review, the top-of-rack option was removed (that fact belongs to a Guest OS question). The CSV is synthetic, generated with a fixed seed.

## Metadata
```yaml
id: "0074"
title: "Transmit drops with no complaints"
product: [vsphere, linux]
technology: [network]
object: [vm]
tool: [vcenter]
task: troubleshoot
level: 300
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
attachments:
  - 0074/app-12-network-packets-past-day.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [A, B]
misconception: [E, D]
misconception_type: [average-hides-worst]
pair: "0404"
status: draft
```
