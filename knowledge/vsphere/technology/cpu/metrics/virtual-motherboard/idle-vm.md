# VM Idleness Indicator and Reclaimable Idle (VCF Operations)

## Meaning
- Two VCF Operations metrics on the VM that decide whether it is an idle VM.
- Idleness Indicator: is the VM idle over the last 24 hours. Rolling: computed every 5 minutes, each value over the last 24 hours of data.
- Reclaimable Idle: 1 (true) when the VM met the idle definition on every day of the idle window. A daily metric.
- List an idle VM only when both are true.
- Principles behind the definition (absolute MHz, CPU only, per day): `operations-management/capacity/reclamation`, section Idle VM.

## Policy defaults
| Setting | Default |
|---|---|
| Idle for at least | 7 days |
| Within each day it consumes no more than | 100 MHz CPU |
| For this share of the time | 100% |
| Exclude VMs provisioned in the last | 30 days |

- 7 days: the result shows within a week. Longer windows protect month-end VMs and delay detection of retired ones.
- 100% of the time: any 5-minute period above the MHz threshold in a day makes that day not idle.
- New VMs are excluded: they often wait before use.

## Reading it
- Idleness Indicator is rolling, so a VM is classified without waiting for a daily run.
- Its value is stored only when it changes: the chart shows steps, which makes it easy to see when the state changed.
- Reclaimable Idle alone can be stale: it is daily, and a VM that became busy today still shows 1 until the next daily value. Idleness Indicator shows the recent activity.
- Tightening the threshold (for example 100 MHz to 50 MHz) restarts the count from day 1: past days are not recomputed, because recomputation costs performance. A VM that was idle under both thresholds waits a full window again. With a 2-week window, 2 weeks.

## Traps
- "Reclaimable Idle = 1, so power it off" → check Idleness Indicator (recent activity) and the VM creation date.
- "The threshold was lowered and idle VMs disappeared, so they became busy" → the count restarted from day 1 after the change.
- "A VM idle 6 days of 7 is idle" → every day of the window must be idle.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/idle-vm
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- capacity
- value
product:
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: context
internal_derive:
- operations-management/capacity/reclamation
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- operations-management/capacity/unused-vm
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Capacity Management > Reclamation > Idle VM. Pages 114-116.'
corrections: []
review_notes:
- 'Section ''Policy defaults'': values from the book screenshot of the VCF Operations policy (Idle VMs: 7 days, 100 MHz, 100% of the time, exclude VMs provisioned in the last 30 days). Not checked against VCF Operations 9.1 documentation; the screenshot is not copied.'
- 'Section ''Policy defaults'': "any 5-minute period above 100 MHz makes the day not idle" is Claude''s reading of 100% of the time with 5-minute collection.'
- 'Metric keys of Idleness Indicator and Reclaimable Idle are not in the book; to add from the VCF Operations 9.1 metric reference (plan, M1 VCF Operations).'
status: draft
```
