# vMotion downtime in VCF Operations Log Management

## Prompt
- VM db-orders: 16 vCPUs, 64 GB of memory, a write-heavy order database.
- In VCF Operations Log Management, you query the vMotion entries of the last week and chart the field `vmw_esxi_vmdowntime` for this VM.
- Most migrations show values between 90,000 and 160,000.
- On Tuesday at 02:10, during the nightly batch load, one migration shows 1,450,000.
- Your team's guide for vMotion switchover downtime: under 200 ms is expected; above 1 second, investigate.
- The application owner says the database was frozen for 24 minutes on Tuesday night.

Which statements are correct?

- A. Most migrations paused the VM for 90-160 ms at switchover: within the guide.
- B. The Tuesday migration paused the VM for about 1.45 seconds at switchover: above the guide, worth investigating.
- C. The Tuesday value means the database was frozen for about 24 minutes, as the owner says.
- D. A longer pause during the batch load fits: a write-heavy VM leaves more changed pages to send while paused.
- E. Switchover downtime is set by the configured memory size, so a 64 GB VM shows about the same downtime on each migration.
- F. A pause of 1.45 seconds is too short for the database or its clients to notice.
- G. Set db-orders to DRS manual mode, so that vMotion no longer freezes it for minutes at a time.

## Likely wrong answer
C: the value read as milliseconds (1,450,000 ms is about 24 minutes) instead of microseconds.

## Expected key points
- Answer: A, B, D.
- A is true: the downtime value is in microseconds, so 90,000-160,000 is 90-160 ms, within the guide (under 200 ms).
- B is true: 1,450,000 microseconds is 1.45 seconds, above 1 second, so investigate: the guest was paused for 1.45 s.
- C is false: it reads microseconds as milliseconds.
- D is true: at switchover the VM is quiesced on the source, the last changed pages are copied, and it resumes on the target. A high page-change rate during the copy (the batch load) leaves more to copy at the pause.
- E is false: downtime varies per migration with the page-change rate, the vMotion network and host load, not only with memory size.
- F is false: the switchover pause is the largest guest impact of a vMotion, a sudden latency rise, and above 1 second it is worth investigating.
- G is false: it rests on reading the value as 24 minutes; the pause was 1.45 seconds, and its cause (the page-change rate during the batch load) is what to look at.

## Notes
- The guide values are stated in the prompt (benchmark/design.md, section 6.1, F3).
- Changed in the 2026-11-15 audit: level 400 -> 300 (convert a unit and apply a guide given in the stem; design.md 3.2); product name VCF Operations Log Management (vSphere 9.1 name, as in the vmotion file); E without "only ... same on every"; D shortened; key points one per option. G kept: the review's stun-time replacement is undecidable while vmotion.md describes stun time two ways.
- Unit: Broadcom KB 436882, How to identify vMotion stun time for a vMotion (https://knowledge.broadcom.com/external/article/436882): downtime and stun time are logged in microseconds.

## Metadata
```yaml
id: "0077"
title: "vMotion downtime in VCF Operations Log Management"
product: [vcf-operations, vsphere]
technology: [system]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/vm/vmotion
knowledge_main: vsphere/object-types/vm/vmotion
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05; revised 2026-11-12"
answer: [A, B, D]
misconception: [C, G]
misconception_type: [unit-and-normalization]
status: draft
```
