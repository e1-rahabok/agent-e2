# Gate: CPU Demand Demo

Run 2026-11-19, Muse Glimmer 30B (reasoning effort low), 3 runs of `steps/step-1.txt` with its two screenshots (VCF Operations and vCenter, the same host and hour; from the author's lab, also the attachments of benchmark question L4-120). The answer points and the claims to avoid are in `demo.yaml` (key), written before the runs. Run 1 is shown on the page. The first, text-only version and its runs are in project/archive/demo-quick-2-text-version-2026-11-19/.

| Answer point | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| No: the gap is not unmet demand, no host from it | yes | yes | yes |
| Same name, two formulas: vCenter VMs only; VCF Operations adds the kernel reservation and, per VM, the higher of demand and reservation | yes | yes | yes |
| On a quiet host the gap is reserved capacity | yes | yes | yes |
| Contention from Ready and Co-stop, not Demand minus Usage | yes | yes | yes |
| A claim to avoid stated as true | none | none | none |

Result: passed, 3 of 3. All three read the screenshots: VCF Operations Demand about 2.9 GHz, Usage about 324-484 MHz, vCenter Demand about 200 MHz.
Flaws kept in run 1: none found.
