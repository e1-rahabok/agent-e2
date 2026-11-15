# Alert wait cycles: symptom level and alert level

## Prompt
- VCF Operations 9.1 monitors a vCenter through its vCenter adapter instance, which collects every 5 minutes.
- An alert definition on VMs has one symptom set, defined on Self. It holds one symptom definition: VM CPU Usage (%) above 90. No other alert definition uses this symptom definition.
- Current settings: symptom Wait Cycle 2 and Cancel Cycle 1; alert-level Wait Cycle 3 and Cancel Cycle 1.
- Every night from 22:00 to 02:00 an 8-vCPU batch VM runs a job. In every group of three collection cycles, its VM CPU Usage (%) is above 90 in two cycles and below 90 in the third. The pattern is the same all four hours: above, above, below, above, above, below, and so on.
- No alert is generated during the job window, although the VM is above 90 for two thirds of it.
- The application owner asks for exactly one alert per job. It must stay open while the pattern continues and close within about 15 minutes after the job ends. The value 90 must stay as it is.

Which changes, each made alone, meet the request?

- A. Set the alert-level Wait Cycle to 1 and leave every other setting.
- B. Set the symptom Wait Cycle to 1 and leave every other setting.
- C. Set the symptom Cancel Cycle to 2 and leave every other setting.
- D. Set the symptom Wait Cycle to 3 and the symptom Cancel Cycle to 3.
- E. Set the alert-level Cancel Cycle to 3 and leave every other setting.

## Likely wrong answer
A: the vendor guidance is to keep the alert-level wait cycle at 1 and tune sensitivity on the symptom, so it looks like the fix. Or B: a shorter wait looks like more sensitivity.

## Expected key points
- Answer: C.
- Symptom level, as it is now: two cycles above 90 in a row meet the symptom Wait Cycle of 2, so the symptom triggers. The single cycle below 90 meets the Cancel Cycle of 1, so the symptom is cancelled. It is triggered for one collection cycle at a time and never for the 3 cycles the alert-level Wait Cycle requires (the symptoms must stay triggered for that many cycles). So no alert is generated.
- C: with Cancel Cycle 2, one cycle below 90 does not cancel the symptom, and the next cycle above 90 resets the count. The symptom stays triggered through the whole window, the alert-level Wait Cycle of 3 is met after a few cycles, and one alert stays open. After the job ends, two cycles below 90 cancel the symptom and the alert-level Cancel Cycle of 1 closes the alert, about 10 to 15 minutes later.
- A is wrong: the alert would be generated at the first trigger, but the symptom is cancelled one cycle later and the alert with it. The result is a new alert every 15 minutes, not one.
- B is wrong: with Wait Cycle 1 the symptom is triggered for two cycles and cancelled for one, so it never stays triggered for 3 cycles. No alert.
- D is wrong: the condition holds for at most 2 cycles in a row, so a Wait Cycle of 3 never triggers the symptom.
- E is wrong: the alert-level Cancel Cycle acts only on an alert that exists. No alert is ever generated, so it changes nothing.
- The two layers are not alternatives: Wait Cycle and Cancel Cycle exist on both, and the alert level counts triggered and cancelled symptoms, not metric samples. Flapping is fixed with the Cancel Cycle of the symptom.

## Notes
- Public source: Broadcom TechDocs, VCF Operations (VCF 9.0 and later), "Alert Definition Best Practices" (page last updated 2026-11-09): the wait cycle and the cancel cycle of the alert definition go into effect after the wait and cancel cycle of the symptom definition result in a triggered or cancelled symptom; sensitivity is set at the symptom level and the alert-level cycles are 1. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html
- Public source: Broadcom TechDocs, Aria Operations 8.18, "Creating Alert Definitions": symptom Wait Cycle, the trigger condition should remain true for this number of collection cycles before the symptom is triggered; symptom Cancel Cycle, the symptom is cancelled after the condition is false for this number of cycles; alert-level Wait Cycle, the symptoms remain triggered for this number of cycles before the alert is generated; alert-level Cancel Cycle, the symptoms are cancelled for this number of cycles after which the alert is cancelled. VCF 9.1, "Add a Virtual Machine CPU Usage Symptom to the Alert Definition" (updated 2026-11-12): Wait Cycle 3 requires the condition true for 3 collection cycles.
- Public source: Broadcom KB 427996: the Wait Cycle is the number of consecutive collection cycles a condition must remain true.
- Why one answer: the timeline is fixed by the pattern, and each option can be computed from the quoted definitions. Only C keeps the symptom triggered long enough for the alert-level Wait Cycle and still gives one alert. A creates an alert that is cancelled and created again; B and D never reach 3 cycles; E acts on a non-existing alert.
- Debatable risk: the sources state "consecutive" for the Wait Cycle only. The question assumes the Cancel Cycle counts consecutive cycles too (the mirror case), and that the alert-level Wait Cycle counts cycles in which the symptom is in the triggered state. Both are the natural reading of the quoted sentences, but no page works an example like this one. The pattern is chosen so that off-by-one counting does not change any option: the symptom is triggered for 1 cycle (current), 2 cycles (B) or all cycles (C) against a requirement of 3.
- Rewritten 2026-11-13 to raise difficulty: the single documented fact (wait cycles are stacked) is replaced by a flapping metric where the symptom Wait Cycle, the symptom Cancel Cycle and the alert-level Wait and Cancel Cycle interact. The vendor rule of thumb (alert-level wait 1) is the tempting wrong answer.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which single change meets the request?"

## Metadata
```yaml
id: "0274"
title: "Alert wait cycles: symptom level and alert level"
product: [vcf-operations]
technology: [system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/alert-definitions
knowledge_main: vcf-operations/alert-definitions
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [C]
misconception: [A, B]
misconception_type: [rollup-and-interval]
status: draft
```
