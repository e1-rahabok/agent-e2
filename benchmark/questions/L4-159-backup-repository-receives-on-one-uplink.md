# Backup repository receives on one uplink

## Prompt
- ESXi 9.1 host esx-31 runs the backup repository VM bkrepo-01: one VMXNET3 adapter, one IP address.
- esx-31 has four 25 GbE uplinks, vmnic0 to vmnic3, in one team on a distributed switch. bkrepo-01's port group uses "Route based on IP hash".
- The four switch ports of esx-31 form a static EtherChannel on a top-of-rack switch stack. That port channel balances on the destination IP address only.
- During the nightly backup, 40 source VMs on other hosts send to bkrepo-01 over TCP. The backup runs past its window.
- esxtop network panel on esx-31, 02:10:

```text
   PORT-ID USED-BY              MbTX/s     MbRX/s
  2214592 vmnic0               182.40     611.25
  2214594 vmnic1               205.73   23816.90
  2214596 vmnic2               176.18     598.04
  2214598 vmnic3               194.66     640.37
  2214630 3812290:bkrepo-01    512.61   23702.33
```

Which statements are correct?

- A. The IP hash policy on esx-31 picks the uplink only for the frames esx-31 sends.
- B. The port channel's hash on the top-of-rack stack decides which uplink receives bkrepo-01's frames.
- C. With a hash on destination IP only, every frame for bkrepo-01 maps to one member port.
- D. A port channel hash that also uses the source IP can spread the 40 streams over the member ports.
- E. IP hash on esx-31 spreads the backup over all four uplinks both ways, so the vmnic1 row is a counter error.
- F. A move to Load Based Teaming can spread bkrepo-01's incoming streams over the four uplinks.
- G. Since the physical switch picks the receive uplink, esxtop cannot show which uplink receives the backup.
- H. Only the teaming policies of the 40 source hosts decide which of esx-31's member ports receives each stream.
- I. With IP hash on both sides, each TCP stream to bkrepo-01 is split over the member ports packet by packet.
- J. A move to Load Based Teaming also means removing the static EtherChannel, which pairs only with IP hash.

## Likely wrong answer
"We set IP hash with an EtherChannel, so ESXi balances the backup over all four links" (E), and its fix, "switch to Load Based Teaming so ESXi balances the load" (F).

## Expected key points
- Answer: A, B, C, D, J.
- A is correct: the virtual switch balances transmit traffic only. The transmit rows are spread (176-206 Mb/s each); IP hash spreads esx-31's own frames across different IP pairs.
- B is correct: receive traffic arrives on the port the physical switch picks; its own policy decides.
- C is correct: bkrepo-01 has one IP address, so a hash on the destination IP alone gives the same member port for every frame to it, whatever the source. vmnic1 receives 23,817 Mb/s, about 95% of 25 Gb/s, while the other uplinks receive about 600 Mb/s each.
- D is correct: with the source IP in the hash, the 40 source-destination pairs hash to different member ports. The change is on the physical switch, not in ESXi.
- E is wrong: the misconception. ESXi balances only what it sends; the vmnic1 row is the physical switch's choice for receive.
- F is wrong: the wrong action. Load Based Teaming maps a whole virtual port to one uplink, so one vNIC never gets more than one uplink's speed in either direction.
- G is wrong: the over-correction. The vmnic rows show where traffic arrives (MbRX/s per vmnic); only the choice is the physical switch's.
- H is wrong: each source host's team decides only the uplink its own frames leave on. The switch in front of esx-31 picks the member port toward esx-31.
- I is wrong: one source-destination pair always hashes to the same uplink; IP hash does not split a stream.
- J is correct: mixing IP hash with no EtherChannel, or an EtherChannel with another policy, disrupts the network: the physical switch sees one MAC on several ports. Load Based Teaming needs no physical switch change.

## Notes
- The port channel hash on destination IP only is a case fact. A source-and-destination hash is the usual alternative on switches that offer it; the exact options depend on the switch vendor.

## Metadata
```yaml
id: "0458"
title: "Backup repository receives on one uplink"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi, network]
tool: [esxtop]
knowledge:
  - vsphere/technology/network/concepts/nic-teaming
  - vsphere/tools/esxtop/network
knowledge_main: vsphere/technology/network/concepts/nic-teaming
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/network/concepts/nic-teaming"
answer: [A, B, C, D, J]
misconception: [E, F]
misconception_type: []
status: draft
```
