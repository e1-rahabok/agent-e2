# Three VM size requests, three reports

## Prompt
- A team builds report sets in VCF Operations for each object type. For the VM, the set has three reports: Inventory, Configuration and Capacity. They are designed together, so that no two reports show the same view of the same data.
- Three requests for the VM size arrive in the same week:
  - R1: "How many different VM sizes (vCPU and memory combinations) exist in our estate, and which are the most common? Are they larger or smaller than we expect?" A pie chart of the relative distribution is wanted.
  - R2: "Rank the VMs by configured size, so that we can focus on the monster VMs." A bar chart whose buckets leave out the small VMs is wanted.
  - R3: "Which VMs are undersized or oversized for what they actually use?" A bar chart with the buckets undersized, rightsized and oversized is wanted, with a table of the top 10 VMs to act on.

Which report holds each request? The answer lists R1, R2, R3 in that order.

- A. Inventory, Configuration, Capacity
- B. Configuration, Inventory, Capacity
- C. Inventory, Capacity, Configuration
- D. Capacity, Configuration, Inventory
- E. Configuration, Configuration, Capacity

## Likely wrong answer
B or E: "VM size" is read as a configuration item, so both the variety of sizes (R1) and the ranking (R2) are put in the Configuration report.

## Expected key points
- Answer: A.
- Inventory counts what exists and how much it varies. R1 asks how many sizes exist and which are common: a count of variation, shown as a relative distribution (pie).
- Configuration shows the settings of the object. R2 ranks the VMs by the configured size, in order, to focus on the largest.
- Capacity compares size with use. R3 sets the configured size against the demand actually used to find undersized and oversized VMs; configured size alone cannot say that.
- B and E merge R1 into configuration, so two reports would show the same view of the same data, which the set was built to avoid. C and D give the "used against configured" comparison to the wrong report or leave it out.
- The reports are run as a set: one report alone misses what another holds.

## Notes
- Public source: none. This question rests only on the design logic of the knowledge file (report-suite, section Example: VM configured size, and Reports as a set), which is the author's own report design; there is no vendor page for the split. The VCF Operations report functionality itself is vendor documented, but the Inventory, Configuration and Capacity split is a design choice.
- Why one answer: each request is matched by what it asks (count of variation, ranking by a setting, comparison of size with use). The prompt gives the set's design principle (no overlap) and the chart types that appear in the file's example.
- Debatable risk: HIGH. The mapping of R1 to Inventory and R2 to Configuration is the author's design; another team could put "VM size distribution" in the Configuration report (the shipped Operations Management set even has a VM Size Distribution section under Configuration). The author should decide whether to keep this question. A frontier model may pick B or E for that reason.
- Rests on: the knowledge file's design logic only.

## Metadata
```yaml
id: "0358"
title: "Three VM size requests, three reports"
product: [vcf-operations, vsphere]
technology: [cpu, memory, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/report-suite
  - vcf-operations/vcf-operations-role
knowledge_main: vcf-operations/report-suite
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, E]
misconception_type: [tool-confusion]
status: draft
```
