# Gate: Balloon and Swap Demo

Run 2026-11-19, Muse Glimmer 30B (reasoning effort low), 3 runs of `steps/step-1.txt`. The answer points and the claims to avoid are in `demo.yaml` (key), written before the runs. Run 1 is shown on the page.

| Answer point | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| No counter is wrong | yes | yes | yes |
| Swap consumed and Compressed are held now, left from past reclamation | yes | yes | yes |
| Rates at 0: nothing moves now; a VM waits only when a page comes back | yes | yes | yes |
| State High: no pressure now, so no balloon | yes | yes | yes |
| No VMs need to move | yes | yes | yes |
| A claim to avoid stated as true | none | none | none |

Result: passed, 3 of 3. Flaws kept in run 1: it says the host is well above the Soft threshold without naming Soft as where ballooning starts (run 2 does); it does not say that the balloon deflates once its target falls.
