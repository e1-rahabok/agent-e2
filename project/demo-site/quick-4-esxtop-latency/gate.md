# Gate: Storage Latency Demo

Run 2026-11-19, Muse Glimmer 30B (reasoning effort low), 3 runs of `steps/step-1.txt`. The answer points and the claims to avoid are in `demo.yaml` (key), written before the runs. Run 1 is shown on the page.

| Answer point | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| GAVG = KAVG + DAVG; QAVG is inside KAVG, so not 9 ms | yes | yes | yes |
| The array and fabric are fine: DAVG 0.8 ms | yes | yes | yes |
| Queueing in the VMkernel: check queue depths and an IOPS limit | yes | yes | yes |
| Below 10 ms is not healthy here | yes | yes | yes |
| A claim to avoid stated as true | none | none | none |

Result: passed, 3 of 3.
Flaws kept in run 1: none found.
