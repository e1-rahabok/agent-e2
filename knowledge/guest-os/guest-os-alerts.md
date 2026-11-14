# Guest OS alerts

## Coverage and receivers
- Guest OS alerts are for the application team: whoever runs the application on Windows or Linux. They are not for the infrastructure team.
- The Guest OS is the layer closest to the application, and performance problems can start there without any virtualization cause.
- Without application or transaction monitoring, the application team relies on complaints. A complaint is subjective and correlates weakly and unpredictably with technical counters. These alerts give a counter-based signal.
- Alerted: CPU run queue, disk queue. VCF Operations stores the counters on the VM object, so the alerts are defined on the VM; they still watch the Guest OS layer.
- Every value (threshold, wait, gate) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../catalog/thresholds-alerts.yaml), shown with this file.

## Guest OS CPU run queue
- Goal: catch a long CPU run queue, which is less known than CPU utilization. It is often independent of the virtualization layer: some applications spawn too many threads. It also shows the VM owner that the infrastructure team sees inside Windows and Linux.
- Guest OS Peak CPU Queue, 20-second: the queue itself ([`guest-os/cpu/metrics/run-queue`](cpu/metrics/run-queue.md)).
- VM CPU Net Run: confirms a real workload. The queue counter gives false positives, so Net Run is required and the wait is longer ([`vsphere/technology/cpu/metrics/virtual-motherboard/net-run`](../vsphere/technology/cpu/metrics/virtual-motherboard/net-run.md)).
- Red only, to reduce noise. To add an orange, halve the queue value and keep Net Run: red is 2x orange in the set.
- Use it with the VM CPU contention and VM CPU consumption alerts ([`vsphere/object-types/vm/vm-alerts`](../vsphere/object-types/vm/vm-alerts.md)). Remediation:
  1. VM CPU contention alert also fired → follow its remediation.
  2. VM CPU consumption alert also fired → follow its remediation.
  3. Neither → find why the application creates so many threads. Compare with the other software of the same business application, and with the same software in other applications. For commercial software, ask the vendor. Without an answer, exclude the application from this alert.

## Guest OS disk queue
- Guest OS disk queue, 20-second peak: the queue itself ([`guest-os/storage/disk-queue`](storage/disk-queue.md)).
- VM CPU Usage: the activity gate of the VM alerts.
- Neither Windows nor Linux gives official guidance. The values are set high; adjust them to the environment. With too many false positives, disable orange.

## Other contention: custom alerts
- Other Guest OS problems not caused by virtualization have thresholds that vary widely by application, so no alert is defined. Build your own for:
  - CPU context switches consistently high. Tell the developers it can slow the application. If VM CPU Net Run and the run queue are both low, reduce the vCPU count ([`guest-os/cpu/metrics/context-switch`](cpu/metrics/context-switch.md)).
  - Heavy memory paging with many page faults.
  - Many outstanding disk operations.
  - Network packets dropped (requires the Telegraf agent).

## Consumption: daily checks, no alert
- Consumption alerts at the Guest OS level give false positives. Proactive checks instead:
  - CPU usage disparity consistently high: ask the VM owner why the application cannot use all vCPUs equally. Reduce the vCPU count if the application does not use them, above all when context switches are high and the run queue is low ([`vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity`](../vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity.md)).
  - Free memory consistently near 0 MB with moderate or heavy paging: ask the owner whether performance suffers. Benchmark the application before and after adding memory, because too much memory can reduce performance.
  - Low disk space: not implemented. Some partitions, such as swap, are always near 100%. It cannot be done at the VM virtual disk layer either.

## Misconceptions
- "Guest OS alerts go to the infrastructure team" → they go to the application team; infrastructure has its own VM and host alerts.
- "Run queue above 20 is always a CPU shortage" → check the VM CPU contention and consumption alerts first; if neither fired, the application creates too many threads.
- "Alert on the run queue alone" → the counter gives false positives; the alert also requires Net Run and a longer wait.
- "Alert on low free memory" → the Guest OS uses free memory as cache; check paging and benchmark the application.
- "Alert on low disk space for every partition" → swap partitions are nearly full by design.
- "Disk queue thresholds come from Microsoft or Linux guidance" → neither publishes one; the values in the set are high on purpose.

## Metadata
```yaml
id: guest-os/guest-os-alerts
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
- sp5-framework/outputs/alert-design
- guest-os/cpu/metrics/run-queue
- guest-os/storage/disk-queue
- vsphere/technology/cpu/metrics/virtual-motherboard/net-run
related:
- vsphere/object-types/vm/vm-alerts
- guest-os/cpu/metrics/context-switch
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- guest-os/system/guest-os-performance
source:
  document: Knowledge base
  path: 'Proactive Operations > Alert > Application Team > Guest OS Alerts (CPU Contention, Disk Contention Alert, Other Contention Alerts, Consumption)'
corrections: []
review_notes:
- 'Section ''Guest OS CPU run queue'': the source thanks Darren Farrer for the collaboration on the remediation.'
- 'Section ''Guest OS CPU run queue'': the source gives the optional orange as Peak CPU Queue above 10 with Net Run above 75%, half the red queue value; written as the 2x rule.'
- 'Section ''Consumption: daily checks, no alert'': the source says no alert is defined; the alert count table in Alerts Planning shows Guest OS Disk consumption 1. Parked after 1.0 (Q142).'
- 'Section ''Guest OS disk queue'': the source says CPU Usage above 1 GHz without naming the object; written as VM CPU Usage, as in the VM alerts.'
status: draft
```
