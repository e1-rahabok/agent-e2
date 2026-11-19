# Gate: CPU Demand Demo

Run 2026-11-19, Muse Glimmer 30B (reasoning effort low), 3 runs of `steps/step-1.txt`. The answer points and the claims to avoid are in `demo.yaml` (key), written before the runs. Run 1 is shown on the page.

| Answer point | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| No: the gap is not unmet demand, no host from it | yes | yes | yes |
| Same name, two formulas: vCenter VMs only; VCF Operations adds the kernel reservation and, per VM, the higher of demand and reservation | yes | yes | yes |
| On a quiet host the gap is reserved capacity | yes | yes | yes |
| Contention from Ready and Co-stop, not Demand minus Usage | yes | yes | yes |
| A claim to avoid stated as true | none | none | none |

Result: passed, 3 of 3.
Flaws kept in run 1: "Thread Utilization below about 80-90%" is a loose level the knowledge base does not state that way.
