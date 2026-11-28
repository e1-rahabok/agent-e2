# Key check of the answer set

An independent agent answered each question from the knowledge files, the facts and the attachments, without seeing the key (R-E2-004). It was told not to read `benchmark/` or `project/`. The table says whether its answer agrees with the key. A row marked `uncertain` is for the author to review; its decision is then written into the question's key. Not indexed.

| Question | Agreement | Note |
|---|---|---|
| acme-01-score-dip | agrees | Same step at 07:35, same low of 42 at 13:00, same 10 h 30 min below 75%. It added that the dip alone would not close the cluster. |
| acme-02-steady-score | agrees | Same figures. It also named what the page does not show. |
| acme-03-capacity-closed | agrees | Same reason (Consumption above 80), Performance and Risk do not decide. |
| conv-01-more-vcpus | agrees | Same: more vCPUs raise Ready and Co-stop; find the cause first. |
| csv-01-swapped-flat | agrees | Same: nothing swapped in the hour, Swapped is history. It read the gap to Swap target (about 0.44 GB) as the most ESXi could still swap; the key says the target is not queued memory. Both say it is not swapping now. |
| csv-02-host-hides-vm | agrees | Same window 04:15 to 04:40, same peak 9.32%, host peak 0.39%. |
| design-01-install | agrees | Same pointer to techdocs.broadcom.com and no steps. Its answer was longer than three sentences: that tests the service, not the key. |
| reader-01-ready-above-100 | agrees | Same: summation across vCPUs. |
| reader-02-costop-single-vcpu | agrees | Same: always 0 on one vCPU; read Ready. |
| reader-03-active-for-sizing | agrees | Same: neither Active nor Consumed suits sizing; use Guest OS counters. |
| reader-04-link-not-opened | agrees | Same: link not opened, ballooning alone is no problem. |
| reader-05-memory-limit | agrees | Same: enforced at all times, guest cannot see it, size the VM instead. |
| shot-01-guest-metrics | agrees | Same split by the layer that produces each counter. |
| shot-02-demand-below-usage | agrees | Same legend values (199 and 342 MHz) and the two formulas of Demand. |
