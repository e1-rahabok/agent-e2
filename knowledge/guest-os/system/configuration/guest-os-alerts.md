# Guest OS alerts

## What to set
- Guest OS alerts are for the application team: whoever runs the application on Windows or Linux. They are not for the infrastructure team.
- The Guest OS is the layer closest to the application, and performance problems can start there without any virtualization cause.
- Without application or transaction monitoring, the application team relies on complaints. A complaint is subjective and correlates weakly and unpredictably with technical counters. These alerts give a counter-based signal.
- Each alert below fires only when all its conditions hold.

## CPU run queue alert
- Goal: catch a long CPU run queue, which is less known than CPU utilization. It is often independent of the virtualization layer: some applications spawn too many threads. It also shows the VM owner that the infrastructure team sees inside Windows and Linux.
- Red: for 15 minutes, Guest OS Peak CPU Queue above 20 and VM CPU Net Run above 75%.
- Orange: not set, to reduce noise. To set one: Guest OS Peak CPU Queue above 10 and VM CPU Net Run above 75%.
- Why 15 minutes and Net Run: the queue counter gives false positives, so the wait is longer and Net Run confirms a real workload.
- Use it with the VM CPU contention and VM CPU consumption alerts (`vsphere/technology/cpu/configuration/cpu-alerts`). Remediation:
  1. VM CPU contention alert also fired → follow its remediation.
  2. VM CPU consumption alert also fired → follow its remediation.
  3. Neither → find why the application creates so many threads. Compare with the other software of the same business application, and with the same software in other applications. For commercial software, ask the vendor. Without an answer, exclude the application from this alert.
- Metrics: `guest-os/cpu/metrics/run-queue`, `vsphere/technology/cpu/metrics/virtual-motherboard/net-run`.

## Disk queue alert
- Red: for 5 minutes, 20-second peak Guest OS disk queue above 10,000 and VM CPU Usage above 1 GHz.
- Orange: for 5 minutes, 20-second peak Guest OS disk queue above 5,000 and VM CPU Usage above 1 GHz.
- Neither Windows nor Linux gives official guidance. The values are set high; adjust them to the environment. With too many false positives, disable orange.
- Metric: `guest-os/storage/metrics/disk-queue`.

## Other contention: build your own
- Other Guest OS problems not caused by virtualization have thresholds that vary widely by application, so no alert is defined. Build your own for:
  - CPU context switches consistently high. Tell the developers it can slow the application. If VM CPU Net Run and the run queue are both low, reduce the vCPU count (`guest-os/cpu/metrics/context-switch`).
  - Heavy memory paging with many page faults.
  - Many outstanding disk operations.
  - Network packets dropped (requires the Telegraf agent).

## Consumption: daily checks, no alert
- Consumption alerts at the Guest OS level give false positives. Proactive checks instead:
  - CPU usage disparity consistently high: ask the VM owner why the application cannot use all vCPUs equally. Reduce the vCPU count if the application does not use them, above all when context switches are high and the run queue is low (`vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity`).
  - Free memory consistently near 0 MB with moderate or heavy paging: ask the owner whether performance suffers. Benchmark the application before and after adding memory, because too much memory can reduce performance.
  - Low disk space: not implemented. Some partitions, such as swap, are always near 100%. It cannot be done at the VM virtual disk layer either.

## Traps
- "Guest OS alerts go to the infrastructure team" → they go to the application team; infrastructure has its own VM and host alerts.
- "Run queue above 20 is always a CPU shortage" → check the VM CPU contention and consumption alerts first; if neither fired, the application creates too many threads.
- "Alert on the run queue alone" → the counter gives false positives; require Net Run above 75% and wait 15 minutes.
- "Alert on low free memory" → the Guest OS uses free memory as cache; check paging and benchmark the application.
- "Alert on low disk space for every partition" → swap partitions sit near 100% by design.
- "Disk queue thresholds come from Microsoft or Linux guidance" → neither publishes one; the values here are set high on purpose.

## Metadata
```yaml
id: guest-os/system/configuration/guest-os-alerts
retriever_guide: what-to-set
scope: guest-os
layer:
- guest-os
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vcf-operations
- windows
- linux
internal_derive:
- sp5-framework/alerts/alert-design
- guest-os/cpu/metrics/run-queue
- guest-os/storage/metrics/disk-queue
- vsphere/technology/cpu/metrics/virtual-motherboard/net-run
related:
- vsphere/technology/cpu/configuration/cpu-alerts
- guest-os/cpu/metrics/context-switch
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- guest-os/system/metrics/guest-os-performance
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Proactive Operations > Alert > Application Team > Guest OS Alerts (CPU Contention, Disk Contention Alert, Other Contention Alerts, Consumption) (pp. 16-18)'
corrections: []
review_notes:
- 'Section ''CPU run queue alert'': the source thanks Darren Farrer for the collaboration on the remediation.'
- 'Section ''CPU run queue alert'', remediation: the source refers to high VM CPU contention and high VM CPU consumption alerts; linked to vsphere/technology/cpu/configuration/cpu-alerts by Claude.'
- 'Section ''Consumption'': the source says no alert is defined; the alert count table in Alerts Planning shows Guest OS Disk consumption 1. Q142.'
- 'Section ''Disk queue alert'': the source says CPU Usage above 1 GHz without naming the object; written as VM CPU Usage, as in the VM alerts.'
status: draft
```
