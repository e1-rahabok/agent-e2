# Which dashboard for VM contention

## Prompt
You're an expert in Broadcom VMware vSphere. You're a VCDX, focusing on performance monitoring and troubleshooting.
https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/predefined-dashboards-in-vrealize-operations-manager/performance-dashboards/vm-contention-dashboard.html is this the dashboard I should use to troubleshoot VM contention?

What about the VM Performance dashboard? What's the difference?

## Likely wrong answer
"Yes. VM Contention shows supply (what the VM wants but cannot get: %RDY, %CSTP, ballooning, swapping); VM Performance shows demand (CPU Usage, Active Memory, IOPS). Check VM Contention first; if contention is zero and usage hits 100%, add vCPUs or RAM." (Gemini, Pro, high effort, 2026-11-09.)

## Expected key points
- No: VM Contention is deprecated in VCF Operations 9.1, marked (DEP); VM Performance supersedes it. The linked 9.1 page is out of date.
- There is no supply vs demand split. Performance means contention; VM Performance (%) is a KPI of contention counters. Utilization is context on the same dashboard.
- VCF Operations shows VM CPU Ready and Co-stop per 5 minutes with 20-second peaks, not esxtop %RDY and %CSTP.
- Active Memory is not a performance metric.
- No contention and high usage is not a reason to add vCPUs by itself: check the Guest OS run queue (a batch job runs at 100% by design).

## Notes
- Real exchange: the author's prompt and follow-up to Gemini (Pro, high effort), 2026-11-09. The author built VM Performance to supersede VM Contention.
- URL question (benchmark/design.md, section 3.4). The page is live; check that it still describes VM Contention as current before scoring. Page checked: 2026-11-09 (author).
- Two turns joined into one prompt; the runner is single turn.

## Metadata
```yaml
id: "0091"
title: "Which dashboard for VM contention"
product: [vcf-operations, vsphere]
technology: [cpu, memory]
input: [text]
task: troubleshoot
knowledge:
  - vcf-operations/dashboards/vm-performance-dashboard
  - vsphere/object-types/vm/vm-performance
attachments: []
origin: synthetic
source_path: "Author's Gemini exchange, 2026-11-09"
answer_type: judged
level: 400
status: draft
```
