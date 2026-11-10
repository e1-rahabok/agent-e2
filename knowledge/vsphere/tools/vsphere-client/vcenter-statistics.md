# vCenter statistics: sampling, rollup and levels

## Definition
- ESXi samples performance counters every 20 seconds. The vSphere Client labels this interval Real-time. It is not real time: each point is a 20-second average (`observability/real-time-metrics`).
- vCenter stores history by rolling the 20-second samples into coarser intervals.
- Two settings decide what history exists: the collection interval and the statistics level.
- Each vCenter counter carries 4 attributes: unit, stat type, rollup type, collection level.

## Collection intervals (default)
| Interval (archive length) | One data point every | Built from | Changeable |
|---|---|---|---|
| Real-time | 20 seconds | ESXi samples | No |
| 1 Day | 5 minutes | 15 real-time samples. 288 points per day. | Interval duration and archive length |
| 1 Week | 30 minutes | 6 points of 1 Day. 336 points per week. | No |
| 1 Month | 2 hours | 4 points of 1 Week. 360 points per 30-day month. | No |
| 1 Year | 1 day | 12 points of 1 Month. 365 points per year. | Archive length only |

- Real-time data exists only for powered-on VMs and connected hosts.
- Each rollup step averages away peaks: a 20-second burst is diluted 15x in the 1 Day interval and 4,320x in the 1 Year interval.
- Longer intervals or archives need more vCenter database storage.

## Rollup delay
- A data point appears only after its interval closes and the rollup job runs.
- 1 Day data can be up to 30 minutes behind the current time.
- 1 Week data can be up to 1 hour behind: 30 minutes for the 1 Week interval plus 30 minutes for 1 Day.
- 1 Month data can be up to 3 hours behind.
- 1 Year data can be up to 1 day and 3 hours behind.
- During the delay the chart for that period is empty.

## Stat type
| Stat type | Meaning | Example counter |
|---|---|---|
| Rate | Value over the current statistics interval | cpu.usagemhz (MHz) |
| Delta | Change from the previous statistics interval | cpu.system (%) |
| Absolute | Value independent of the interval | mem.consumed (MB) |

## Rollup type
| Rollup | How samples in one interval are combined | Consequence |
|---|---|---|
| Average | Mean of the samples | Hides peaks. Most consumption counters. |
| Summation | Sum of the samples | Time counters such as cpu.ready.summation (ms) grow with interval length: 20,000 ms per vCPU per 20-second sample is 100%. Packet counts are totals per interval, not per second. |
| Latest | Last value in the interval | One point in time, not representative of the interval. Space counters (provisioned, used) and Highest Latency (maxTotalLatency). |
| Minimum, Maximum | Lowest, highest value in the interval | Stored only at statistics level 4. For historical data: the minimum or maximum of the aggregated values, not of the raw 20-second samples. |

## Statistics levels
- **1**
  - Adds: Aggregate counters only. CPU: usage, usagemhz, totalmhz, cpuentitlement. Memory: consumed, overhead, swapinRate, swapoutRate, swapused, vmmemctl (balloon), mementitlement, totalmb, usage, total bandwidth (DRAM, PMem, NVMe). Disk: capacity, maxTotalLatency, provisioned, unshared, usage, used. Network: usage. System: heartbeat, uptime. DRS cluster services. VM operations: numChangeDS, numChangeHost, numChangeHostDS. VM power.
  - Intended use: Long-term monitoring. Default for every interval.
- **2**
  - Adds: CPU: idle, reservedCapacity. Disk: all except numberRead and numberWrite. Memory: all except memUsed, min/max rollups and DRAM/PMem/NVMe read and write latency. All VM operations counters.
  - Intended use: Long-term monitoring beyond the basic counters.
- **3**
  - Adds: All counters except min/max rollups. Per-instance (device) counters: per vCPU, per physical CPU, per NIC, per disk.
  - Intended use: Short-term, after a problem appears.
- **4**
  - Adds: Everything, including minimum and maximum rollups.
  - Intended use: Short-term, after a problem appears.

- Contention counters stored at the default level 1: VM CPU Ready, disk maxTotalLatency (Highest Latency, Latest rollup), balloon, swap-in and swap-out rates.
- Storage latency per device (kernelLatency, deviceLatency, queueLatency, totalReadLatency, totalWriteLatency) needs level 2 or higher. The chart tables list these at level 3.
- The VM CPU Ready chart shows the average of all vCPUs at level 1. Ready per vCPU appears only at level 3.
- Per-device GPU counters on the host (utilization, memory used, temperature) are level 4 in the chart tables. Cluster and resource pool GPU counters are level 1 in the vCenter 9.1 API. See `vsphere/technology/gpu/concepts/gpu-monitoring`.
- Levels 3 and 4 raise vCenter load significantly. If vpxd cannot write statistics to the database fast enough, its memory grows until it runs out of memory and crashes. After raising a level, watch the vpxd process size.

## Level 1 counters per object (vCenter 9.1 API)
What the vCenter 9.1 API offered per object type in one inventory (an export of the API). This is the history that exists when nobody raised the statistics level.

| Object | Counters |
|---|---|
| VM | cpu: usage, usagemhz, ready. mem: usage, consumed, overhead, vmmemctl, swapinRate, swapoutRate. disk: usage, maxTotalLatency, used, provisioned, unshared. net: usage. sys: uptime. clusterServices: vmDrsScore |
| ESXi | cpu: usage, usagemhz, ready. mem: usage, consumed, overhead, vmmemctl, swapinRate, swapoutRate, bandwidth.total. disk: usage, maxTotalLatency. net: usage. sys: uptime. clusterServices: cpufairness, memfairness |
| Cluster | cpu: usage, usagemhz, totalmhz. mem: usage, consumed, overhead, vmmemctl, totalmb. clusterServices: effectivecpu, effectivemem, clusterDrsScore, failover. vmop: 20 operation counts. gpu: utilization, mem.used, mem.reserved, mem.total, power.used, temperature |
| Resource pool | cpu: usagemhz. mem: consumed, overhead, vmmemctl. gpu: same 6 as cluster |
| Datastore | disk: used, provisioned, capacity, unshared, numberReadAveraged, numberWriteAveraged. datastore: numberReadAveraged, numberWriteAveraged |
| Datacenter | vmop: 20 operation counts |
| Distributed switch | net.throughput: packets and drops at switch, port and LAG scope; level 3, not level 1 |
| Distributed port group, folder | none |

- At the default level a VM keeps no Co-stop, no per-vCPU Ready, no memory Latency, no per-disk latency and no network drops. Its contention history is Ready, Highest Latency (maxTotalLatency), balloon and swap rates.
- Every counter with its API unit, rollup and summary: `knowledge/catalog/vcenter-api-counters.yaml`.

## Units
- KB in vCenter counters = 1,024 bytes. KBps = 1,024 bytes per second.
- kb (kilobit) = 1,000 bits. kbps = 1,000 bits per second.
- The API and the charts use different units for the same counter. The API returns memory in KB (mem.consumed, mem.vmmemctl, mem.overhead), swap rates in KBps, disk and network usage in KBps, and space in KB. The vSphere Client charts convert: memory to MB, space to GB, network usage to Mbps. A value exported through the API and read as MB is 1,024 times too large.
- Network counters such as net.received are labelled Kbps but measured in kilobytes per second. esxtop network uses megabits. See `vsphere/tools/esxtop/units-vs-vsphere-client`.

## Where history is lost
- Removing an object from vCenter and adding it again deletes its history.
- vMotion across vCenter instances deletes the VM's chart history.
- Objects moved to another site by protection and recovery lose history at the old site; it is not copied.
- Counters newer than the host version do not exist for that host.

## Chart behaviour
- Stacked charts show the 10 child objects with the highest values. Smaller children are not shown.
- Datastore space charts show the latest data only, not history. Space statistics are refreshed every 30 minutes and collected asynchronously across datastores, so they can be up to 30 minutes old.
- Performance charts do not exist for network objects (switches, port groups). The distributed switch still has API counters at level 3 (switch, port, LAG); the distributed port group has none. See `vsphere/technology/network/metrics/distributed-switch/packets`.
- Overview and advanced charts show a subset of the counters. The vSphere API reference lists all counters.

## Traps
- "An API value of 4,194,304 for VM Consumed is 4 TB" → the API unit is KB: 4 GB.
- "The Real-time chart shows real-time data" → it shows 20-second averages, the label is the UI's. A burst of 1-3 seconds needs esxtop or the 2-second tier of VCF Operations 9.1.
- "The 1 Week chart shows the peak" → it shows 30-minute averages. Use real-time or esxtop for bursts.
- "Max rollup is always available" → only at statistics level 4.
- "Ready of 2,000 ms is high" → it depends on the interval: 2,000 ms in 20 seconds is 10% of one vCPU; in a 5-minute point it is 0.67%.
- "No data in the chart, so the VM was idle" → check rollup delay, power state, recent vMotion across vCenter, and statistics level.
- "Raise all intervals to level 4 for better history" → vpxd memory growth and database size. Raise for a short time only.

## Metadata
```yaml
id: vsphere/tools/vsphere-client/vcenter-statistics
retriever_guide: how-it-works
scope: vsphere
technology:
- system
pillar:
- performance
- capacity
product:
- vsphere
object:
- VCenterServer
- VirtualMachine
- HostSystem
internal_derive:
- vsphere/architecture/metric-sources
related:
- observability/real-time-metrics
- vsphere/architecture/metric-sources
- vcf-operations/features/peak-20-second-metrics
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/tools/esxtop/units-vs-vsphere-client
- vsphere/tools/vsphere-client/performance-guidance
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: vSphere Monitoring and Performance > Monitoring Inventory Objects with Performance Charts > Data Counters, Data Collection Intervals, Statistics Levels, Performance Chart Types; Troubleshoot and Enhance Performance > Empty Performance Charts; Hosts > GPU charts (pp. 2025-2031, 2065-2067, 2123-2124)
corrections: []
review_notes:
- 'Sections ''Level 1 counters per object'', ''Units'' (API units), ''Chart behaviour'' (distributed switch) and the GPU line in ''Statistics levels'': from the vCenter 9.1.0 API export (build 25370922), https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv. The chart-unit conversions are from the vSphere 9.1 chart tables (catalog/vcenter-counters).'
- 'Whole file: from the vSphere 9.1 documentation, not the book.'
- 'Section ''Collection intervals'': the document says 1 Week rolls up 12 points of 1 Day every 2 hours (text under 1 Week) and 6 points every 30 minutes (text under 1 Day). The table uses the arithmetic: 6 x 5 min = 30 min; 4 x 30 min = 2 h; 12 x 2 h = 1 day.'
- 'To check: Section ''Rollup type'': the Summation example (20,000 ms per vCPU per 20-second sample = 100%) and the burst dilution factors are arithmetic, not from the document.'
- 'Section ''Statistics levels'': the level 1 contention list is derived from the level 1 table and the chart tables (VM CPU Ready: level 1). The document is inconsistent on disk latency: the level 2 row says all disk metrics except numberRead and numberWrite; the chart tables list deviceLatency, totalReadLatency and totalWriteLatency at level 3.'
- 'Section ''Units'': the document labels net.received and net.transmitted "Kilobytes per second (Kbps)". Kbps is the bit abbreviation; the label says kilobytes.'
status: draft
```
