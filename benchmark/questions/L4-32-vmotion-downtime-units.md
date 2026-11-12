# vMotion downtime in VCF Operations for logs

## Prompt
- VM db-orders: 16 vCPUs, 64 GB of memory, a write-heavy order database.
- In VCF Operations for logs, you query the vMotion entries of the last week and chart the field `vmw_esxi_vmdowntime` for this VM.
- Most migrations show values between 90,000 and 160,000.
- On Tuesday at 02:10, during the nightly batch load, one migration shows 1,450,000.
- Your team's guide for vMotion switchover downtime: under 200 ms is expected; above 1 second, investigate.
- The application owner says the database was frozen for 24 minutes on Tuesday night.

Which statements are correct?

- A. Most migrations paused the VM for 90-160 ms at switchover: within the guide.
- B. The Tuesday migration paused the VM for about 1.45 seconds at switchover: above the guide, worth investigating.
- C. The Tuesday value means the database was frozen for about 24 minutes, as the owner says.
- D. A longer pause during the batch load fits the mechanism: pages changed during the copy must be sent while the VM is paused, and a write-heavy VM leaves more of them.
- E. Switchover downtime depends only on the configured memory size, so a 64 GB VM shows the same downtime on every migration.

## Likely wrong answer
C: the value read as milliseconds (1,450,000 ms is about 24 minutes) instead of microseconds.

## Expected key points
- Answer: A, B, D.
- The downtime value is in microseconds: 90,000-160,000 is 90-160 ms; 1,450,000 is 1.45 seconds.
- A: within the guide (under 200 ms).
- B: above 1 second, so investigate: the guest was paused for 1.45 s, enough to break short application or cluster timeouts.
- C is wrong: it reads microseconds as milliseconds.
- D: at switchover the VM is quiesced on the source, the last changed pages are copied, and it resumes on the target. A high page-change rate during the copy (the batch load) leaves more to copy at the pause.
- E is wrong: downtime varies per migration with the page-change rate, the vMotion network and host load, not only with memory size.

## Notes
- Revised 2026-11-12 (question set 1.0): the screenshot became values as text; the guide values are stated in the prompt (benchmark/design.md, section 6.1, F3); the stun-time table option (a UI detail) replaced by the downtime mechanism.
- Unit: Broadcom KB 436882, How to identify vMotion stun time for a vMotion (https://knowledge.broadcom.com/external/article/436882): downtime and stun time are logged in microseconds.

## Metadata
```yaml
id: "0077"
title: "vMotion downtime in VCF Operations for logs"
product: [vcf-operations, vsphere]
technology: [system]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/vm/vmotion
knowledge_main: vsphere/object-types/vm/vmotion
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation; revised 2026-11-12 (question set 1.0)"
answer: [A, B, D]
misconception: [C]
misconception_type: [unit-and-normalization]
status: draft
```
