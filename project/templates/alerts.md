# <Object type> alerts

## Coverage and receivers
- Consumer or provider, and who receives the alerts (application team, infrastructure team, sub-persona).
- Alerted: the resources and metric types (contention, consumption) this object type alerts on.
- Every value (threshold, population, wait, gate) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file.
- What every alert of this object shares (a gate, how members are read).

## <Alert name, exactly as the catalog row's name>
- Detects: the problem, in one line.
- One line per symptom: which metric, which interval (acute or sustained, issue or gate), and why it is in the alert. No values.
- Criticality and wait: why red only, or why a longer wait. No values.
- Remediation: the flow to open, or numbered steps.

## Not alerted, and why
- One line per resource or metric type left out: not yet in the set, or why a daily check or the NOC screen serves better.

## Misconceptions
- "Wrong belief, in the user's words (a number is allowed here)" → correction, without alert values.

## Metadata
```yaml
id: vsphere/object-types/<object>/<object>-alerts   # Guest OS: guest-os/guest-os-alerts
retriever_guide: what-to-set
scope: vsphere
technology: [cpu, memory]
pillar: [performance]
product: [vsphere, vcf-operations]
object: [HostSystem]
internal_derive: [sp5-framework/outputs/alert-design]   # and the metric files the symptoms test
related: []                        # the flows the alerts open; the alert files of related object types
source:
  document: <document name, version, revision>
  path: <heading path and pages>
corrections: []
review_notes: []
status: draft
```

- Rules: [project/knowledge-rules/placement.md](../knowledge-rules/placement.md) (Alerts have three parts) and [project/knowledge-rules/thresholds.md](../knowledge-rules/thresholds.md). Each catalog alert row: `kb` this file, `name` in a `##` heading here. Lint rejects a value in an alert's section.
