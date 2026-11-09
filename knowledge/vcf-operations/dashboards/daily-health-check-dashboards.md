# Daily health check dashboards

## Who runs it
- The daily health check is the second proactive view, after the NOC live screen. It is read at the start of each day.
- Level 2 and Level 1 run it at first. As Level 1 gains confidence, they run it at the start of each shift; 24/7 operations have 2-3 shifts, so the dashboard is used several times a day.
- It aims to reduce alerts by finding the issues underneath them. Reading it needs knowledge of how the private cloud performs and of what happens that day that can affect performance and security.
- Order of the check and its steps: `sp5-framework/concepts/health-risk-efficiency` and the object health checks, such as `vsphere/object-types/cluster/health-check/cluster-health-check`.

## Morning routine
- A list of alerts or complaints does not show the big picture.
- The environment is assumed mostly healthy; where it is not, the problem is known, because it must be explained to management. The dashboard therefore shows what needs attention.
- It complements alerts in two ways:
  - insight: situations that have not triggered an alert;
  - the overall picture: before troubleshooting one object, rule out a problem with the whole environment.
- Open two browser windows side by side: the VCF Operations daily dashboard and the log dashboard of VCF Operations for logs.

## vSphere daily log check
- Much information exists only in logs. A daily log dashboard covers basic hygiene:
  - Undesirable VM events: is the count and timing as expected? Harmless events (VM relocation, snapshot, power on) are filtered out.
  - Undesirable VM changes and snapshots: as expected? Taken during office hours? Harmless changes filtered out.
  - Issues: vCenter alarms, vCenter tasks that ended in error, ESXi potential problems.
  - Security: malicious changes, shell commands at the ESXi console, root logins.
  - vMotion: bandwidth lower than expected, downtime longer than expected, or some clusters with many more vMotions than usual.
- vMotion is a leading indicator of a larger performance problem. Metric: `vsphere/object-types/vm/metrics/vmotion`.

## Traps
- "The alert list is the morning check" → alerts show objects above a threshold, one at a time. The daily dashboard shows insight and the whole environment.
- "Metrics cover the daily check" → many changes, security events and failed tasks exist only in logs. Read the log dashboard beside the metrics dashboard.
- "Troubleshoot the VM first" → check the overall picture first; the problem may be the whole environment.
- "Slower vMotion is cosmetic" → it is a leading indicator of a larger performance problem.
- "Show every VM event" → filter harmless events (relocation, snapshot, power on); otherwise the undesirable ones are lost.

## Metadata
```yaml
id: vcf-operations/dashboards/daily-health-check-dashboards
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- availability
- performance
- compliance
product:
- vcf-operations
- vsphere
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- sp5-framework/concepts/proactive-operations
- vcf-operations/concepts/system-engagement
related:
- sp5-framework/alerts/alerts-and-insights
- sp5-framework/concepts/health-risk-efficiency
- vsphere/object-types/vm/metrics/vmotion
- observability/input-types
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Proactive Operations > Daily Health Check (Morning Routine, vSphere Daily Log Check) (pp. 6-7)'
corrections: []
review_notes:
- 'Section ''Morning routine'': the source names Log Insight; in VCF 9 it is VCF Operations for logs. Claude''s knowledge.'
- 'Not copied: the screenshot of the two dashboards side by side (proof screenshot).'
status: draft
```
