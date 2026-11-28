# Key check of the answer set

An independent agent answered each question from the knowledge files, the facts and the attachments, without seeing the key (R-E2-004). It was told not to read `benchmark/` or `project/`. The table says whether its answer agrees with the key. A row marked `uncertain` is for the author to review; its decision is then written into the question's key. Not indexed.

| Question | Agreement |
|---|---|
| acme-01-score-dip | agrees |
| acme-02-steady-score | agrees |
| acme-03-capacity-closed | agrees |
| conv-01-more-vcpus | agrees |
| csv-01-swapped-flat | agrees |
| csv-02-host-hides-vm | agrees |
| design-01-install | agrees |
| reader-01-ready-above-100 | agrees |
| reader-02-costop-single-vcpu | agrees |
| reader-03-active-for-sizing | agrees |
| reader-04-link-not-opened | agrees |
| reader-05-memory-limit | agrees |
| shot-01-guest-metrics | agrees |
| shot-02-demand-below-usage | agrees |

## Notes

- acme-01: the agent found the same step at 07:35, the same low of 42 at 13:00 and the same 10 h 30 min below 75%.
- acme-03: the agent gave the same reason: Consumption above 80, with Performance and Risk not deciding.
- csv-01: the agent read the gap to Swap target (about 0.44 GB) as the most ESXi could still swap. The key says the target is not queued memory. Both say ESXi is not swapping now.
- csv-02: the agent found the same window 04:15 to 04:40, the same peak of 9.32% and the host peak of 0.39%.
- design-01: the agent pointed to techdocs.broadcom.com and gave no steps. Its answer ran longer than three sentences: that tests the service, not the key.
- The other ten agree with no difference worth noting.
