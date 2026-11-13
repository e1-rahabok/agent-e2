# Alert wait cycles: symptom level and alert level

## Prompt
- VCF Operations 9.1 monitors a vCenter through its vCenter adapter instance, which collects every 5 minutes.
- A symptom definition on the metric VM CPU Usage (%) has a wait cycle of 3.
- The alert definition that uses this symptom has an alert-level wait cycle of 2.
- A VM goes above the symptom's value at 10:00 and stays above it continuously.

Which statement describes how the two wait cycles work together?

- A. The symptom triggers at the first collection above the value; the alert-level wait cycle of 2 is the only delay before the alert is created.
- B. The symptom triggers only after its condition has held for 3 collection cycles; the alert-level wait cycle then adds further delay before the alert is created.
- C. The two wait cycles run in parallel, so the alert is created when the longer one has passed, after 3 collection cycles (15 minutes).
- D. Wait cycles count minutes, so the symptom triggers after 3 minutes and the alert after 2 more minutes.
- E. The alert-level wait cycle replaces the symptom's wait cycle, so the alert is created after 2 collection cycles.

## Likely wrong answer
C or E: the two settings are read as alternatives of the same delay, so only one of them counts. Or D: the cycle number is read as minutes.

## Expected key points
- Answer: B.
- A wait cycle counts collection cycles, not minutes: the condition must be true for that number of collection cycles.
- The alert-level wait cycle goes into effect after the symptom's wait cycle has produced a triggered symptom. The two delays follow each other; they do not replace each other and do not run in parallel.
- So the alert is created later than the symptom triggers. Vendor guidance is to set the sensitivity on the symptom and keep the alert-level wait cycle at 1, so there is one place to tune and no stacked delay.

## Notes
- Public source: Broadcom TechDocs, VCF Operations (VCF 9.0 and later), "Alert Definition Best Practices": the wait cycle for the alert definition goes into effect after the wait cycle for the symptom definition results in a triggered symptom; in most alert definitions, configure the sensitivity at the symptom level and the alert wait cycle to 1. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html (page last updated 2026-11-09).
- Public source: Broadcom TechDocs, VCF 9.1, "Add a Virtual Machine CPU Usage Symptom to the Alert Definition": the wait cycle requires the symptom condition to be true for 3 collection cycles before the symptom is triggered. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/create-a-problem-alert-definition/add-a-virtual-machine-cpu-usage-symptom-to-the-alert-definition.html (page last updated 2026-11-12).
- Why one answer: the documented order (alert wait after symptom wait) rules out parallel and replacement; the cycle is defined in collection cycles. The question asks for no total time, so an off-by-one count cannot be argued.
- Debatable risk: the Aria Operations 8.18 page words it as "added to"; that agrees with B. The 5-minute collection interval is given in the prompt as a fact of the scenario, not as a product default.

## Metadata
```yaml
id: "0274"
title: "Alert wait cycles: symptom level and alert level"
product: [vcf-operations]
technology: [system]
task: explain-mechanism
level: 300
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
answer: [B]
misconception: [C, E]
misconception_type: [rollup-and-interval]
status: draft
```
