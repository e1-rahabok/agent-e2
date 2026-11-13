# One alert for a warning and a critical symptom

## Prompt
- In VCF Operations 9.1 you have two symptom definitions on VM CPU Usage (%): one with severity Warning at a lower value, one with severity Critical at a higher value.
- Operations wants one alert definition, not two. It must be created with Warning criticality while only the lower value is exceeded, and with Critical criticality once the higher value is exceeded.
- The alert definition has one set of symptoms, defined on the VM itself (Self).

Which configuration gives that result?

- A. Put both symptom definitions in the set, match Any of them, and set the alert criticality to Symptom Based.
- B. Put both symptom definitions in the set, match All of them, and set the alert criticality to Symptom Based.
- C. Put both symptom definitions in the set, match Any of them, and set the alert criticality to Critical.
- D. Put both symptom definitions in the set, match All of them, and set the alert criticality to Warning.
- E. Put only the Critical symptom definition in the set, and set the alert criticality to Symptom Based.

## Likely wrong answer
B: "All" feels safer because it needs the full evidence. Then the alert is created only when both symptoms hold, which is the Critical case.

## Expected key points
- Answer: A.
- Any means the alert is created when either symptom is triggered; Symptom Based criticality takes the severity from the symptom that triggered, so the alert shows Warning, then Critical.
- All (B, D) creates the alert only when both symptoms are true. The higher value implies the lower one, so the alert never appears for the Warning-only state.
- A fixed alert criticality (C, D) ignores the severity of the symptoms.
- E has no Warning state.

## Notes
- Public source: Broadcom TechDocs, VCF Operations (VCF 9.0 and later), "Alert Definition Best Practices": include the Warning and Critical symptom definitions in a single alert definition with an Any condition and set the alert criticality to Symptom Based; this generates the alert with the right criticality if either of the symptoms is triggered. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html (page last updated 2026-11-09).
- Public source: Broadcom TechDocs, VCF 9.0, "Create a New Alert Definition": the symptoms pane criteria is set to All by default, so Any must be chosen. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/create-a-new-alert-definition.html (page last updated 2026-11-09).
- Why one answer: the vendor page prescribes exactly this combination for this case, and the alternatives fail by logic (All needs both symptoms; a fixed criticality cannot change with the symptom).
- Debatable risk: two separate alert definitions would also work, but the prompt fixes one alert definition.

## Metadata
```yaml
id: "0275"
title: "One alert for a warning and a critical symptom"
product: [vcf-operations]
technology: [system]
task: judge-setting
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
answer: [A]
misconception: [B]
misconception_type: []
status: draft
```
