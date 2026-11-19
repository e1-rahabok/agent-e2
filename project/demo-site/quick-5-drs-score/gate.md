# Gate: DRS Score Demo

Run 2026-11-19, Muse Glimmer 30B (reasoning effort low), 3 runs of `steps/step-1.txt`. The answer points and the claims to avoid are in `demo.yaml` (key), written before the runs. Run 1 is shown on the page.

| Answer point | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Not a valid conclusion | yes | yes | yes |
| Cluster DRS Score is a weighted average of the VM DRS Scores; it can hide one VM | yes | yes | yes |
| Read the VM DRS Score of pay-db-01 itself | yes | yes | yes |
| VM DRS Score is execution efficiency, not contention: read the VM's contention counters | yes | yes | yes |
| A claim to avoid stated as true | none | none | none |

Result: passed, 3 of 3.
Flaws kept in run 1: two side paragraphs that the question does not need (ESXi CPU Demand, and how Co-stop works).
