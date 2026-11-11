# Report design in VCF Operations

## Scope, layout, colour, recency
- Scope: the whole environment or a subset? Data volume decides the visualization: a table handles 100 rows, while 10,000 rows become endless pages. With thousands of clusters and datastores, world-level data can be too much; show exceptions or what matters, such as only large VMs in a downsize list.
- The scope objects are usually vSphere World, vCenter or a vCenter Datacenter; the content comes from objects below them.
- Layout: horizontal page orientation for laptop and desktop, so the default reports are horizontal. Portrait (vertical) for a phone. A tablet depends on its size.
- Colour: a colour-coded report reads more easily.
- Recency: the present value shows the latest situation. Past values cover a period and must be reduced to one number (maximum, average or percentile), or drawn as a line chart for a pattern.

## PDF or CSV
- CSV:
  - only the View List widget fits. A Summary List can export CSV but lacks detail for analysis; use it in a PDF with another widget for detail;
  - page orientation does not matter: as deep and wide as needed;
  - one report per object: a CSV file has no tabs, so one file holds one table;
  - no colour: plain CSV drops it;
  - no grouping and no summary row: a spreadsheet groups better and allows a formula per column;
  - at most 50 columns: split an object with many metrics and properties into logical sets;
  - utilization and contention at the 95th percentile: the maximum shows outliers, and the average reacts too late when the goal is to serve everyone almost all the time;
  - events summed, such as the number of Guest OS reboots.
- PDF:
  - horizontal orientation suits laptop, tablet and paper;
  - a phone needs its own design, as a phone app does.
- Context columns for a VM CSV of thousands of rows, placed at the end so the first columns hold the main data for sorting: the parent vCenter Datacenter, the parent cluster, the parent folder. They let the reader group VMs.

## Widget order: summary to detail
- A PDF report has no interaction and a fixed height, so only some widgets fit.
- Order:
  1. headline numbers, large and eye-catching;
  2. the headline broken down by group, focused on relative size or value;
  3. the trend, if the pattern matters;
  4. individual members, limited to the important ones, such as the top 10.
- Check each widget's limits in PDF before building, to avoid redoing the report.

## Widgets and their limits
- Headline:
  - 3-5 numbers fill a portrait page well; more looks crammed, 1-2 looks sparse.
  - Scoreboard. Limit: shows the present value only, so it does not suit performance.
- Summary:
  - Summary View: a simple table summarizing many members at the parent level; adds computation to the Scoreboard.
  - Limit: one filter applies to all rows although each row has its own metric; no count function, only sum, maximum, minimum, average and standard deviation.
- Grouping (the group matters, not the members):
  - Pie Chart: when the number of slices is not known in advance; shows relative distribution, so it suits performance less. Limit: legends truncate unless short.
  - Bar Chart: when you control the range of each bucket, or the quantity per bucket matters; shows absolute distribution. Limit: buckets set by hand.
  - Heat Map: relative size and intensity; the only widget with a continuous colour gradient. Limit: group names are hard to read when there are many groups.
- Trend:
  - Health Chart: when the value can be colour coded. Limits: the shortest height is too small (use medium or tall); suits a fixed number of objects; no control of the y-axis minimum and maximum.
  - View Trend: when values cannot be colour coded and several lines share one y-axis. Limit: tall; put two side by side on a horizontal page.
- Individual (each object by name):
  - Top-N: one metric, where relative values matter and can be colour coded. Use the Percentile function, since the default rollup is average. Limit: a fixed row count, so only where capping does not lose meaning.
  - View List: a multi-column table focused on the object name; can show before and after. Limit: the time setting is hard-coded in the view, and users without designer access cannot change it.

## Present or past data per pillar

| Pillar | Present data | Past data |
|---|---|---|
| Inventory | Yes | Yes |
| Availability | No | Yes |
| Performance | No | Yes |
| Compliance | Yes | Yes |
| Capacity | Yes | Yes |
| Configuration | Yes | Yes |
| Value (cost) | Yes | Yes |

- Past data needs the period hard-coded in each widget.
- Availability and performance need data across time, so Scoreboard and Heat Map do not suit them.

## Misconceptions
- "Export a Summary List to CSV for analysis" → it lacks detail; only View List suits CSV.
- "Colour the CSV" → plain CSV drops colour.
- "Use the maximum for utilization in a CSV" → it shows outliers; the 95th percentile serves the goal of serving everyone almost all the time.
- "Top-N on the default rollup" → the default is average; set Percentile.
- "Scoreboard for performance" → it shows only the present value; performance needs data across time.
- "Pie chart for performance" → it shows relative distribution; performance is judged against absolute values.
- "One CSV with every metric" → the limit is 50 columns; split by logical set.
- "Context columns first" → put them last; the first columns are for the main data and sorting.

## Metadata
```yaml
id: vcf-operations/reports/report-design
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
object:
- VirtualMachine
- ClusterComputeResource
- Datacenter
internal_derive:
- vcf-operations/reports/reports-vs-dashboards
- observability/aggregation
related:
- vcf-operations/dashboards/dashboard-design
- vcf-operations/reports/report-suite
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Reports > Technical Considerations (Output, Context, Widgets); Functional Considerations (pp. 53-58)'
corrections: []
review_notes:
- 'Section ''PDF or CSV'', context columns: the source says the folder column groups the VM by cluster; written as folder.'
- 'To check: Section ''PDF or CSV'': the 50-column limit is from the source (VCF Operations 9.1 documentation).'
- 'To check: Section ''Misconceptions'', pie chart for performance: the reason (judged against absolute values) is a reading of the source, which says relative distribution makes it less suitable for performance.'
status: draft
```
