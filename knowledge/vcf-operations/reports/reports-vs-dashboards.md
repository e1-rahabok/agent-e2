# When a report beats a dashboard

## Where a report fits
- A report is static. It complements dashboards where a dashboard cannot reach:
  - Offline: the user is travelling, such as on a plane. Typical audience: senior IT leaders. With limited bandwidth but a connection, a text-based AI chat can serve better than a report.
  - No access: the user has no network access or security clearance for VCF Operations. Typical audience: external users.
  - Casual user: a PDF or CSV file takes less training than a system and needs no login.
  - Export: data for a spreadsheet or slides, typically for finance or audit. Where it makes sense, teach them the dashboard instead; they then filter tables and transform data themselves.
  - Legal requirement: the law may require the information to be pushed to the user. Politically, a delivered report counts as done, read or not. Typical audience: another legal entity, a paying customer.
  - Printed document: easier to pass around in some meetings; some government policies require a signed report. Widget sizes must be designed by hand to fit the paper.
  - Historical copies: an external copy of the data, for capacity and compliance management. Fixed, regular periods (each week Monday 00:00 to Sunday 00:00, each month) compare more easily in reports. Use a simple CSV with a fixed layout so files compare in a spreadsheet; a format change breaks comparison.
  - Attachment: a file attaches easily to email or another system.

## Where a report does not fit
- Daily use: an interactive dashboard gives more. Even for weekly use, a personalized dashboard adapts better as needs change.
- Detail: large data that needs analysis is served by a set of interactive dashboards, unless free-form spreadsheet analysis is the goal.
- Dynamic time period: a dashboard lets the user change the period; a report is fixed. Changing a report from 1 day to 1 week means editing each widget, with designer access.
- So a report is not where management happens. It suits planning and overall review, above all long-term planning without distracting detail.

## Read or explained
- A report is consumed in one of two ways: read, or presented and explained.
- A report to be read must explain itself.
- A report to be presented keeps to strategic conversation. The lack of drill-down keeps the focus on the big picture. For detail, use a dashboard and drill down to answer questions live.

## Reports per pillar
- Inventory: the big picture.
- Availability: overall availability only. Individual ESXi host availability does not belong in a report.
- Performance: not for monitoring or troubleshooting. It proves that performance was good, so it shows overall performance; individual VM performance does not belong in a report.
- Compliance: reporting for compliance, not remediation.
- Capacity: planning, not managing; the big picture, looking ahead, ideally one quarter.
- Configuration: background on why there are configuration issues and what can be done.
- Security: reporting only, not remediation.

## Who reads reports
- A report is purpose-built for one persona and use case. A persona can need several reports, each with its own frequency and content; do not merge them into one. Find the real end reader and meet them.
- VCF Operations ships building blocks and some sample reports; combining and customizing them is expected.
- Questions for the reader:
  - Purpose: action or information? Senior management may only want the report available, in case detail is needed.
  - Next step: a report for action must not be time sensitive within the day; daily information belongs on a dashboard, unless it must go to a spreadsheet.
  - Timeline: the longer the interval, the staler the data, so the focus moves to the big picture; the reader forgets the last value, so show current against previous.
  - Past or future: users ask for history while their intent is the future. Work out which.
  - The period is hard-coded per widget; a report has no date control at report level.
- Personas:
  - IT senior management: the most common reader (`vcf-operations/dashboards/it-leaders-dashboards`).
  - Auditor: most needs are better met by dashboards. Wants to know the environment is secure, and whether privileged users (the system administrators) made unauthorised changes. Weekly to monthly.
  - Capacity planning team: most needs are better met by dashboards. Reports keep history for years for long-term planning: a record per data centre, cluster and datastore, as simple CSV files. Weekly to monthly.
  - Finance: prefers a spreadsheet for its own analysis. Cares about assets, so hardware only: for example ESXi hosts with purchase date, warranty end and cost. Weekly to quarterly.
  - Tenant: a regular reclamation email to the VM owner, copied to their senior leadership and the CFO office, gets a different reaction from a self-service portal. Example content: the top 10 VMs with the largest saving, with owner names. Weekly to monthly.
  - Consultant: comprehensive, covering all of operations management, for an assessment done rarely, such as once a year.

## Traps
- "Send a daily report" → daily information belongs on a dashboard; a report is fixed and has no drill-down.
- "Put VM performance in the monthly report" → reports prove overall performance; individual VMs are for dashboards.
- "One report for all of the auditor's needs" → one report per persona and use case; several reports if needed.
- "Users asked for history, so give history" → their intent is often the future; ask.
- "Change the report period on the fly" → the period is hard-coded per widget.
- "A delivered report was read" → a pushed report proves delivery, not reading. Dashboard use can be tracked.
- "Finance needs VM metrics" → finance cares about hardware assets: purchase date, warranty, cost.

## Metadata
```yaml
id: vcf-operations/reports/reports-vs-dashboards
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- availability
- performance
- compliance
- capacity
- value
product:
- vcf-operations
internal_derive:
- vcf-operations/concepts/system-engagement
related:
- vcf-operations/reports/report-design
- vcf-operations/reports/report-suite
- vcf-operations/dashboards/it-leaders-dashboards
- sp5-framework/capacity/reclamation
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Reports > Report | Dashboard (Suitability); Target Audience (Auditor, Capacity Planning Team, Finance Department, Tenant, Consultant) (pp. 49-53)'
corrections: []
review_notes:
- 'Section ''Who reads reports'': the source points to a Role-based Contents chapter for IT senior management; linked to vcf-operations/dashboards/it-leaders-dashboards instead.'
status: draft
```
