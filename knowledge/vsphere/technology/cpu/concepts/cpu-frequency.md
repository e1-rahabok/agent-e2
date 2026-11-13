# CPU frequency and Turbo

## Three speeds
| Speed | Meaning | Facts |
|---|---|---|
| Base (nominal) | The frequency vSphere uses for its total CPU capacity in GHz. Most commonly shown. | The CPU rarely runs at it. It runs above it. |
| Single-Core Turbo | Marketing figure. Single-thread benchmarks use it. | AMD EPYC 9000 series: 7%-64% above base. Intel Xeon Platinum 8593Q: 77% above base. |
| All-Core Turbo | The speed that matters for a loaded host. | AMD publishes All-Core Boost. Intel no longer does. AMD EPYC 9000 series: 1%-48% above base. |

- Intel does not expose All-Core Turbo via API. So it cannot be used in throughput calculations such as vSphere's GHz total.
- Intel Turbo Boost raises clock speed dynamically, with no installation or configuration.
- Intel Turbo Boost inputs: the heat the system tolerates and the number of active cores. It boosts to the maximum safe level.

## Per-core frequency
- Each core can run at its own frequency.
- Rolling up to ESXi level is therefore complex.
- One throughput counter cannot be derived from another. Each must be calculated at core level.

## Clock speed and throughput
- Frequency sets throughput (work per second), not capacity. Capacity is space, counted in physical threads where a vCPU can run: [`vsphere/technology/cpu/concepts/cpu-measurement-levels`](cpu-measurement-levels.md), section CPU capacity: Rules.
- All else equal, a CPU at 1 GHz is 50% slower than at 2 GHz.
- Turbo raises the clock above the stated frequency.
- Turbo works with power saving in the same socket: some cores sleep, and the saved power boosts other cores.
- The power envelope of the socket stays the same.
- The gap between base and highest Turbo is about 2x.

## History
| Year | Change |
|---|---|
| 2008 | Intel Nehalem introduces Turbo. Early Turbo forced all active cores to the same frequency. |
| 2014 | Intel Per-Core P-States (PCPS), Haswell-EP (Xeon E5-2600 v3). Each core has its own power state and frequency. |
| 2017 | AMD Zen (EPYC, Ryzen). Hundreds of sensors adjust clock speed per core in 25 MHz steps. |

| Attribute | 2006 | 2026 |
|---|---|---|
| Examples | Intel Xeon 5160, AMD Opteron 2220 | Intel Xeon 6, AMD EPYC 9005 |
| Typical base clock | 3.0 GHz | 2.0-2.3 GHz |
| Max Turbo clock | None (locked at base) | 3.9-5.0 GHz |
| Core count | 2 | 128-192 |
| Turbo / base ratio | 1.0x | about 1.7x-2.2x |

## Turbo
- Turbo is large enough that every throughput figure (Usage, Demand, vSphere's GHz total) must account for it.
- Within a core: the frequency cannot be predicted. It depends on the instructions and on what other cores do.
- Within a socket: which cores run faster cannot be predicted. A 20-core socket runs at more than one frequency in practice.
- Example, Intel Xeon Platinum 8260 (base 2.4 GHz):
  - all cores: 1.29x (3.1 GHz).
  - one core: 1.62x.
- The High Performance policy is static: the same frequency throughout. Weigh the Turbo benefit before disabling power management.
- Power, Xeon Platinum 8260 (165 W):
  - at 2.4 GHz base: under 165 W for standard math; up to 165 W for heavy math.
  - at 3.1 GHz all-core Turbo: the full 165 W budget.
  - heavy instructions such as AVX-512: 3.1 GHz cannot be held within 165 W. The CPU lowers the frequency to stay under the limit.
- Example, Intel Xeon 6520P (base 2.4 GHz): 3.4 GHz, 42% above base.
- ESXi has no setting to enable or disable Turbo Boost directly. Turbo is on by default. Control it through the power management policy.
- Turbo can still engage with the BIOS set to static high performance. Field observation: esxtop %A/MPERF showed all cores at 129%.

## All-Core Turbo
- A loaded CPU runs above base frequency: more throughput than vSphere's GHz total shows.
- All-Core Turbo is not always exposed via the CPU API.
- A CPU rarely runs at base clock. Under load it spends most of its time at All-Core Turbo.
- All-Core Turbo is the frequency every core can hold at the same time. Single-Core Turbo is reached only when few cores are active and the rest are idle.
- Turbo works under the Balanced policy too. Balanced also reaches Max Turbo, and is likely to, because power per core is more flexible.
- Balanced does not mean lower performance for every workload. Most workloads suit it.

## Likely vCPU speed on a busy cluster
- Scenario: many cores busy, most running 2 threads, Balanced policy, OS Controlled BIOS.
- Starting point: All-Core Turbo, not base and not Single-Core Turbo.
- Hyper-Threading delivers 1.25x per core in total. Each vCPU on a shared core realistically gets 80% (1 / 1.25) of All-Core Turbo.
- Formula: likely vCPU speed = All-Core Turbo × 0.8.
- Example: base 2.0 GHz, All-Core Turbo 3.0 GHz, Single-Core Turbo 4.0 GHz → about 2.4 GHz, as reported by VM CPU Usage (MHz).
- Base 2.0 GHz understates it. 3.0 GHz ignores Hyper-Threading: VM CPU Usage is Hyper-Threading aware. 4.0 GHz does not apply while most cores are busy.

## TDP
- TDP is Thermal Design Power, not maximum power draw.
- Intel definition: the average power the processor dissipates at Base Frequency with all cores active, under an Intel-defined high-complexity workload.
- Power and frequency are not linear. At Single-Core Turbo, total power can be below TDP because the other cores are idle.

## Impacts on ESXi
![Core Utilization vs actual usage with 20% All-Core Turbo](../images/esxi-cpu-core-utilization-vs-actual-usage-with-turbo.png)
- Example with All-Core Turbo at 20% above base.
- The table shows actual values.
- Older releases capped the reported Usage (%) at 100%, hiding actual usage above it. Current vCenter and VCF Operations no longer cap it (Broadcom KB 417702, KB 431027).

| Core Utilization | Actual usage | Analysis |
|---|---|---|
| 25% | 30% | No performance impact on VMs: no HT pair running. The gap is Turbo. |
| 50% | 60% | Same. |
| 67% | 80% | Same. |
| 75% | 90% | Same. |
| 100% | 120% | Same. |
| 125% | 150% | Performance impact from Hyper-Threading. |

## Sample CPU
![Sample CPU: 1 GHz nominal, 1.3 GHz all cores, 1.7 GHz single core](../images/cpu-turbo-boost-example-nominal-all-core-single-core.png)
- 20 cores. Nominal clock speed 1 GHz, for ease of calculation.
- All 20 cores busy: 30% above nominal (1.3 GHz).
- One core busy: up to 70% above nominal (1.7 GHz).
- The vSphere Client shows the nominal speed and treats it as 100%.
- Using nominal speed as the 100% mark understates throughput.
- A real CPU with this boost profile: AMD EPYC 9634.

## Scenarios
![Throughput per vCPU: 1 core runs vs all cores run, 1 vs 2 vCPU](../images/vcpu-throughput-one-core-vs-all-cores-running.png)
- Assumption: the vCPU runs 100% with 0% contention.
- 2-vCPU cases assume both vCPUs land on the 2 threads of one core.

| Socket load | vCPUs | Throughput per vCPU | VM CPU Demand | Total |
|---|---|---|---|---|
| 1 core of 20 busy | 1 | 1.7 GHz | 170% | 1.7 GHz |
| 1 core of 20 busy | 2, same core | 1.06 GHz (1.7 × 0.625) | - | 2.12 GHz, not 3.4 GHz |
| All cores busy | 1 | 1.3 GHz | 130% | 1.3 GHz |
| All cores busy | 2, same core | 812 MHz (1.3 × 0.625) | about 81% | 1.625 GHz |

## Impact on a VM: Mechanism
- VM CPU Demand is based on the 1 GHz nominal speed. So it reports 170% or 130%.
- Demand above 100% suggests more vCPUs. Adding a vCPU can make it worse: the Hyper-Threading penalty applies when both vCPUs share a core.
- When all cores are busy, the chance that 2 vCPUs of one VM share a core rises.
- In the last case each vCPU runs at about 81% and the VM seems maxed out.

## Over time
![Run stays 100% while Usage falls 1.7, 1.3, 0.8 GHz](../images/vm-cpu-run-flat-while-usage-falls-with-frequency.png)
- Run stays at 100% throughout.
- Throughput falls: 1.7 GHz → 1.3 GHz → 1.06 GHz → 0.81 GHz.
- Cause: VMs are added to the cluster over time, and the ESXi scheduler maximizes total throughput.
- A VM can run 100% for hours while the work it completes varies by the second. This is why VM performance feels unpredictable.
- CPU Usage (%) masks this degradation.

## Misconceptions
- "Base frequency × cores is the most work the host can do" → the CPU runs above base most of the time. Base understates throughput.
- "Turbo raises host capacity" → Turbo raises throughput. Capacity is counted in threads and does not change with frequency.
- "Turbo can be turned off in ESXi" → no direct setting. Use the power policy or BIOS.
- "BIOS static high performance means no Turbo" → Turbo was observed at 129% (%A/MPERF).
- "All cores run at the same frequency" → frequency is per core and changes with load.
- "A busy vCPU runs at base speed" → it runs near All-Core Turbo; with Hyper-Threading, about 80% of it.
- "TDP is the maximum power the CPU draws" → TDP is thermal design power at base frequency.
- "Only High Performance reaches Max Turbo" → Balanced reaches it too.
- "Usage (%) above Core Utilization means a problem" → the gap is Turbo.
- "Usage (%) at 100% means the host is at its limit" → the metric is capped. Actual usage can be higher due to Turbo.
- "Demand 170%, so add vCPUs" → the vCPU already runs on a boosted core. A second vCPU on the same core gets 0.625x.
- "Run 100% means constant performance" → throughput varies with frequency and Hyper-Threading.
- "2 vCPUs give 2x the throughput of 1 vCPU" → 2.12 GHz vs 1.7 GHz in the single-core case.
- "Usage (%) stable, so performance stable" → Usage (%) masks the drop in GHz.

## Metadata
```yaml
id: vsphere/technology/cpu/concepts/cpu-frequency
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive:
- vsphere/technology/cpu/concepts/run-time-vs-run-quality
- vsphere/technology/cpu/concepts/hyper-threading
related:
- vsphere/technology/cpu/concepts/power-states
- vsphere/technology/cpu/configuration/host-power-management
- vsphere/technology/cpu/concepts/cpu-measurement-levels
- vsphere/technology/cpu/metrics/host/usage
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/virtual-motherboard/run
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
images:
- path: ../images/esxi-cpu-core-utilization-vs-actual-usage-with-turbo.png
  product:
  - vsphere
  object:
  - HostSystem
  metric:
  - ESXi CPU Core Utilization
  - ESXi CPU Usage
  topic: Turbo Boost
  image_type: diagram
- path: ../images/cpu-turbo-boost-example-nominal-all-core-single-core.png
  product:
  - vsphere
  object:
  - HostSystem
  topic: Turbo Boost
  image_type: diagram
- path: ../images/vcpu-throughput-one-core-vs-all-cores-running.png
  product:
  - vsphere
  object:
  - VirtualMachine
  topic: Turbo Boost
  image_type: table
- path: ../images/vm-cpu-run-flat-while-usage-falls-with-frequency.png
  product:
  - vsphere
  object:
  - VirtualMachine
  metric:
  - VM CPU Run
  - VM CPU Usage
  image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > Architecture > CPU Frequency; Total Capacity; Turbo; All Cores Turbo; Impacts on ESXi; CPU > Architecture > Impacts on VM (from former vsphere/technology/cpu/concepts/cpu-frequency)
corrections: []
review_notes:
- 'Section ''Turbo'': whitepaper ''Host Power Management in VMware vSphere 7.0'' (2021), pp. 12 and 24: https://www.vmware.com/docs/hpm-vsphere7-perf. A search on 2026-11-02 found no newer standalone version; vSphere 8 and 9 cover host power management inside Performance Best Practices.'
- 'To check: Section ''Turbo'': %A/MPERF as the esxtop ratio of actual to nominal frequency (APERF/MPERF registers).'
- 'To check: Section ''Three speeds'': figures for AMD EPYC 9000 series and Intel Xeon Platinum 8593Q (from the book) against vendor pages.'
- 'Section ''Turbo'': Intel Xeon 6520P spec page from the book: https://www.intel.com/content/www/us/en/products/sku/242640/intel-xeon-6520p-processor-144m-cache-2-40-ghz/specifications.html'
- 'Section ''Three speeds'': Intel Turbo Boost description from https://www.intel.com/content/www/us/en/gaming/resources/cpu-clock-speed.html (quoted in the book).'
- 'Section ''All-Core Turbo'': the book cites https://ioflood.com/blog/what-is-all-cores-turbo-base-clock-max-turbo-and-all-cores-turbo-explained/ (third-party).'
- 'To check: Section ''Likely vCPU speed on a busy cluster'': relationship between the 62.5% charge per thread when both threads run (`vsphere/technology/cpu/metrics/virtual-motherboard/used` and `usage`) and the 80% tenant-facing likely speed; not yet written.'
- 'Section ''Scenarios'': the ''Total'' column is computed from the book''s per-vCPU values (2 × 0.8125 = 1.625 GHz); the book gives no total.'
- 'Section ''Sample CPU'': example CPU from the book: AMD EPYC 9634, https://www.amd.com/en/products/processors/server/epyc/4th-generation-9004-and-8004-series/amd-epyc-9634.html'
status: draft
```
