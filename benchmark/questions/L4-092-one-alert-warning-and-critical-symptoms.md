# One alert for a warning and a critical symptom

## Prompt
- In VCF Operations 9.1 a new alert definition is being built for VMs. It will have symptom sets defined on Self.
- Three symptom definitions exist:
  - S1: VM CPU Usage (%) above 80, severity Warning.
  - S2: VM CPU Usage (%) above 95, severity Critical.
  - S3: VM CPU Ready (%) above a set value, severity Warning.
- Operations wants one alert definition, not two or three. Required behaviour:
  - no alert when CPU usage is high and CPU Ready is normal (a nightly backup job drives VMs to 97% usage with no contention);
  - no alert when CPU Ready is high and CPU usage is below 80;
  - an alert with Warning criticality when usage is above 80 and CPU Ready is high;
  - an alert with Critical criticality when usage is above 95 and CPU Ready is high.
- Other alert definitions already use S1, S2 and S3 on their own, and must not change.

Which configurations of the new alert definition give that behaviour?

- A. One symptom set with S1, S2 and S3 that matches Any; the alert criticality is Symptom Based.
- B. One symptom set with S1, S2 and S3 that matches All; the alert criticality is Symptom Based.
- C. Set 1 with S1 and S2 that matches Any, and set 2 with S3; the alert needs all sets; the alert criticality is Symptom Based.
- D. Set 1 with S1 and S2 that matches Any, and set 2 with S3; the alert needs all sets; the alert criticality is fixed to Warning.
- E. Set 1 with S1 and S2 that matches Any, and set 2 with S3; the alert needs any set; the alert criticality is Symptom Based.

## Likely wrong answer
B or A. B: All is read as "the strongest evidence" and the Warning and Critical symptoms are put in one set. A: the vendor pattern for Warning plus Critical (one set, Any, Symptom Based) is copied without the contention condition.

## Expected key points
- Answer: C.
- The vendor pattern for one alert with two severities is a single set holding the Warning and the Critical symptom with Any, and criticality Symptom Based. That covers the usage side (S1 or S2).
- The contention condition must be true as well, so it goes into a second set, and the alert must need all sets (Boolean AND across sets). Any alert needs both sets: usage high and CPU Ready high.
- Symptom Based criticality takes the severity of the triggered symptoms (the most critical one counts). S3 is Warning, so with S1 the alert is Warning and with S2 it is Critical. A Critical S3 would make every alert Critical.
- A is wrong: usage alone or CPU Ready alone creates an alert; the backup job would alert.
- B is wrong: All in one set needs S1, S2 and S3 together. S2 implies S1, but the Warning-only state (usage between 80 and 95) never creates an alert.
- D is wrong: a fixed criticality ignores the symptom severity and never shows Critical.
- E is wrong: the sets are combined with Any, so usage alone or CPU Ready alone creates an alert.
- S1, S2 and S3 are reused as they are; nothing in the other alert definitions changes.

## Notes
- Public source: Broadcom TechDocs, VCF Operations (VCF 9.0 and later), "Alert Definition Best Practices" (page last updated 2026-11-09): include the Warning and Critical symptom definitions in a single alert definition with an Any condition and set the alert criticality to Symptom Based; the alert is generated with the right criticality if either symptom is triggered. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Alert Definitions in VCF Operations" (updated 2026-11-12), section Symptoms in Alert Definitions: an alert definition can require all of its symptom sets, or only one of several, before an alert is generated; criticality value "Symptom" displays symptom based criticality. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/alert-definitions.html
- Public source: Broadcom TechDocs, Aria Operations 8.18, "Creating Alert Definitions": All and Any for symptom sets and for the symptoms inside a set (Boolean AND, OR); criticality of the alert is determined by the most critical of the triggered symptoms.
- Why one answer: the behaviour list is a Boolean expression, (S1 OR S2) AND S3, and only C builds it with the documented operators. The severity rule rules out a fixed criticality.
- Debatable risk: other designs exist (three alert definitions, or conditions written inside the alert). The prompt fixes one alert definition and says the symptom definitions stay as they are. The "most critical wins" wording is from the Aria Operations 8.18 page; the VCF 9 pages describe the same behaviour more loosely. No page was found for VCF 9.1 that spells out both operators in one place.
- Rewritten 2026-11-13 to raise difficulty: a third symptom (contention) forces two sets with Any inside the first and All between sets; the severity of S3 matters for Symptom Based; the vendor pattern alone (A) is the trap.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which configuration ... gives that behaviour?"

## Metadata
```yaml
id: "0275"
title: "One alert for a warning and a critical symptom"
product: [vcf-operations]
technology: [system]
task: judge-setting
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
misconception_type: []
status: draft
```
