# Retrieval check 2026-11-13, hybrid

Baseline after reactivation (Q206). Command: `python3 benchmark/runner/retrieval_eval.py --embeddings`. Index: knowledge base at the merge of e1-rahabok/agent-e2#297. How to read: [benchmark/retrieval-check.md](../../retrieval-check.md).

| Question | Needed | Search top 6 | Classic context | Missed in context |
|---|---|---|---|---|
| 0029 | 2 | 2/2 | 2/2 | - |
| 0032 | 2 | 2/2 | 2/2 | - |
| 0034 | 2 | 0/2 | 1/2 | `vsphere/technology/storage/concepts/storage-layers` |
| 0035 | 1 | 1/1 | 1/1 | - |
| 0036 | 2 | 2/2 | 2/2 | - |
| 0037 | 2 | 0/2 | 0/2 | `vsphere/architecture/metric-sources` (main), `vsphere/architecture/vm-vs-guest-os` |
| 0038 | 2 | 2/2 | 2/2 | - |
| 0187 | 3 | 3/3 | 3/3 | - |
| 0039 | 3 | 2/3 | 2/3 | `vsphere/architecture/vm-vs-guest-os` |
| 0040 | 2 | 2/2 | 2/2 | - |
| 0041 | 3 | 3/3 | 3/3 | - |
| 0042 | 2 | 1/2 | 1/2 | `vsphere/technology/network/metrics/host/errors` |
| 0043 | 1 | 1/1 | 1/1 | - |
| 0044 | 3 | 3/3 | 3/3 | - |
| 0045 | 2 | 2/2 | 2/2 | - |
| 0046 | 2 | 2/2 | 2/2 | - |
| 0047 | 1 | 1/1 | 1/1 | - |
| 0048 | 2 | 2/2 | 2/2 | - |
| 0049 | 3 | 2/3 | 2/3 | `vsphere/technology/storage/concepts/snapshot-impact` |
| 0051 | 2 | 1/2 | 1/2 | `vsphere/architecture/metric-sources` |
| 0052 | 3 | 2/3 | 2/3 | `vsphere/technology/memory/metrics/virtual-motherboard/latency` |
| 0053 | 2 | 2/2 | 2/2 | - |
| 0149 | 2 | 1/2 | 1/2 | `vsphere/tools/esxtop/memory` |
| 0271 | 3 | 1/3 | 2/3 | `guest-os/storage/disk-queue` |
| 0273 | 1 | 1/1 | 1/1 | - |
| 0001 | 1 | 1/1 | 1/1 | - |
| 0007 | 4 | 3/4 | 3/4 | `vsphere/object-types/esxi/configuration/bios-settings` |
| 0009 | 7 | 2/7 | 2/7 | `vsphere/architecture/vm-vs-guest-os`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready`, `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`, `vsphere/technology/cpu/metrics/virtual-motherboard/other-wait`, `vsphere/technology/cpu/metrics/virtual-motherboard/demand` |
| 0010 | 4 | 3/4 | 3/4 | `guest-os/cpu/windows-cpu-scheduling` (main) |
| 0011 | 3 | 3/3 | 3/3 | - |
| 0013 | 4 | 1/4 | 1/4 | `vsphere/technology/cpu/decision-tree/oversized-vm-downsizing`, `vsphere/technology/cpu/concepts/idle-and-unused-vcpus`, `vsphere/technology/memory/concepts/memory-as-storage` |
| 0014 | 1 | 1/1 | 1/1 | - |
| 0015 | 1 | 1/1 | 1/1 | - |
| 0016 | 3 | 3/3 | 3/3 | - |
| 0017 | 1 | 1/1 | 1/1 | - |
| 0019 | 3 | 1/3 | 1/3 | `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`, `sp5-framework/observability/metric-perspectives` |
| 0021 | 4 | 3/4 | 4/4 | - |
| 0022 | 4 | 2/4 | 3/4 | `vsphere/technology/memory/metrics/virtual-motherboard/usage` |
| 0027 | 1 | 1/1 | 1/1 | - |
| 0028 | 3 | 1/3 | 3/3 | - |
| 0050 | 3 | 2/3 | 2/3 | `vsphere/tools/esxtop/overview` |
| 0089 | 3 | 1/3 | 1/3 | `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`, `vsphere/technology/storage/concepts/guest-os-vs-vm-storage` |
| 0094 | 3 | 2/3 | 3/3 | - |
| 0095 | 3 | 2/3 | 3/3 | - |
| 0105 | 2 | 2/2 | 2/2 | - |
| 0107 | 3 | 1/3 | 2/3 | `vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high` |
| 0110 | 2 | 1/2 | 2/2 | - |
| 0111 | 3 | 3/3 | 3/3 | - |
| 0114 | 3 | 2/3 | 3/3 | - |
| 0143 | 3 | 3/3 | 3/3 | - |
| 0144 | 3 | 2/3 | 2/3 | `vsphere/technology/memory/concepts/page-sharing` |
| 0145 | 2 | 2/2 | 2/2 | - |
| 0151 | 3 | 2/3 | 1/3 | `vsphere/technology/memory/metrics/virtual-motherboard/active`, `vsphere/technology/memory/metrics/virtual-motherboard/usage` |
| 0181 | 2 | 1/2 | 0/2 | `vsphere/technology/storage/concepts/vm-files` (main), `vsphere/technology/storage/datastore-space-headroom` |
| 0182 | 3 | 3/3 | 3/3 | - |
| 0185 | 4 | 3/4 | 3/4 | `vsphere/technology/storage/concepts/vm-files` |
| 0211 | 4 | 3/4 | 3/4 | `vsphere/technology/network/metrics/virtual-motherboard/throughput` |
| 0213 | 2 | 0/2 | 0/2 | `vsphere/technology/network/configuration/network-configuration-review` (main), `sp5-framework/concepts/configuration-management` |
| 0214 | 4 | 3/4 | 2/4 | `vsphere/technology/network/concepts/network-characteristics`, `vsphere/technology/network/configuration/rss-and-interrupt-coalescing` |
| 0231 | 2 | 2/2 | 1/2 | `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop` |
| 0232 | 3 | 1/3 | 1/3 | `vsphere/tools/vsphere-client/vcenter-statistics`, `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention` |
| 0233 | 3 | 3/3 | 3/3 | - |
| 0263 | 2 | 1/2 | 2/2 | - |
| 0268 | 3 | 2/3 | 3/3 | - |
| 0270 | 2 | 2/2 | 2/2 | - |
| 0002 | 3 | 1/3 | 3/3 | - |
| 0003 | 3 | 3/3 | 3/3 | - |
| 0004 | 5 | 4/5 | 5/5 | - |
| 0005 | 4 | 2/4 | 4/4 | - |
| 0006 | 3 | 2/3 | 2/3 | `sp5-framework/capacity/overcommit` |
| 0008 | 5 | 4/5 | 4/5 | `vsphere/technology/cpu/metrics/virtual-motherboard/net-run` (main) |
| 0012 | 4 | 4/4 | 4/4 | - |
| 0018 | 5 | 3/5 | 3/5 | `guest-os/storage/disk-queue`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0020 | 3 | 2/3 | 1/3 | `vsphere/technology/memory/metrics/virtual-motherboard/usage` (main), `sp5-framework/observability/resource-nature` |
| 0023 | 4 | 2/4 | 2/4 | `vsphere/technology/memory/metrics/virtual-motherboard/swapped`, `vsphere/technology/memory/vm-memory-latency-high` |
| 0293 | 3 | 3/3 | 3/3 | - |
| 0294 | 1 | 1/1 | 1/1 | - |
| 0295 | 1 | 1/1 | 1/1 | - |
| 0296 | 2 | 2/2 | 2/2 | - |
| 0297 | 2 | 1/2 | 2/2 | - |
| 0298 | 6 | 2/6 | 1/6 | `vsphere/technology/memory/concepts/memory-overhead`, `vsphere/technology/memory/concepts/ballooning`, `vsphere/object-types/cluster/concepts/drs-overview`, `vsphere/object-types/cluster/concepts/dpm`, `vsphere/technology/memory/configuration/host-level-swapping` |
| 0310 | 2 | 1/2 | 2/2 | - |
| 0311 | 4 | 2/4 | 2/4 | `guest-os/guest-os-alerts`, `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency` |
| 0313 | 3 | 2/3 | 2/3 | `vcf-operations/features/peak-20-second-metrics` (main) |
| 0314 | 3 | 3/3 | 3/3 | - |
| 0024 | 4 | 3/4 | 3/4 | `vsphere/technology/memory/concepts/memory-as-storage` |
| 0330 | 2 | 1/2 | 1/2 | `vsphere/object-types/cluster/cluster-health-check` |
| 0331 | 3 | 2/3 | 2/3 | `vsphere/technology/cpu/metrics/host/utilization` |
| 0340 | 3 | 2/3 | 2/3 | `vcf-operations/alert-definitions` |
| 0341 | 3 | 2/3 | 2/3 | `vcf-operations/features/peak-20-second-metrics` |
| 0342 | 3 | 1/3 | 2/3 | `vsphere/technology/storage/metrics/host/datastore` |
| 0343 | 2 | 1/2 | 2/2 | - |
| 0344 | 3 | 2/3 | 3/3 | - |
| 0345 | 3 | 3/3 | 3/3 | - |
| 0346 | 3 | 2/3 | 3/3 | - |
| 0347 | 3 | 2/3 | 1/3 | `vsphere/technology/cpu/metrics/virtual-motherboard/usage`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0025 | 5 | 3/5 | 3/5 | `vsphere/technology/memory/metrics/host/swap-used`, `vsphere/technology/memory/metrics/host/compressed` |
| 0350 | 5 | 2/5 | 2/5 | `vsphere/technology/memory/metrics/comparisons/vm-memory-metrics`, `vsphere/technology/cpu/metrics/comparisons/consumption-metrics`, `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency` |
| 0351 | 3 | 2/3 | 2/3 | `vcf-operations/vcf-operations-role` |
| 0352 | 5 | 1/5 | 2/5 | `vsphere/technology/cpu/metrics/comparisons/host-contention-metrics`, `vsphere/architecture/provider-consumer`, `vsphere/architecture/resource-controls` |
| 0353 | 5 | 3/5 | 3/5 | `vsphere/object-types/cluster/cluster-health-check`, `vsphere/tools/esxtop/cpu` |
| 0354 | 4 | 3/4 | 4/4 | - |
| 0355 | 4 | 2/4 | 3/4 | `vsphere/object-types/cluster/cluster-health-check` (main) |
| 0356 | 4 | 2/4 | 2/4 | `vcf-operations/vcf-operations-role` (main), `vsphere/object-types/vm/vm-health-check` |
| 0357 | 5 | 1/5 | 3/5 | `vcf-operations/vcf-operations-role` (main), `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop` |
| 0358 | 2 | 1/2 | 1/2 | `vcf-operations/vcf-operations-role` |
| 0359 | 4 | 2/4 | 2/4 | `vsphere/technology/storage/concepts/esxi-storage-latency-stack`, `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency` |
| 0026 | 2 | 1/2 | 2/2 | - |
| 0360 | 4 | 2/4 | 3/4 | `vsphere/technology/storage/concepts/esxi-storage-latency-stack` |
| 0361 | 4 | 3/4 | 3/4 | `vsphere/technology/storage/concepts/esxi-storage-latency-stack` |
| 0054 | 3 | 1/3 | 2/3 | `vsphere/technology/memory/metrics/virtual-motherboard/latency` |
| 0056 | 2 | 2/2 | 2/2 | - |
| 0057 | 2 | 1/2 | 2/2 | - |
| 0058 | 4 | 3/4 | 4/4 | - |
| 0059 | 4 | 2/4 | 3/4 | `vsphere/technology/cpu/concepts/hyper-threading` |
| 0060 | 4 | 3/4 | 4/4 | - |
| 0061 | 1 | 1/1 | 1/1 | - |
| 0062 | 4 | 3/4 | 3/4 | `vsphere/technology/storage/concepts/esxi-storage-latency-stack` |
| 0063 | 3 | 3/3 | 3/3 | - |
| 0065 | 2 | 2/2 | 2/2 | - |
| 0066 | 3 | 1/3 | 1/3 | `vsphere/tools/esxtop/cpu` (main), `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0067 | 4 | 2/4 | 3/4 | `vsphere/technology/cpu/concepts/virtual-numa` |
| 0068 | 3 | 2/3 | 3/3 | - |
| 0069 | 3 | 2/3 | 2/3 | `vsphere/technology/network/configuration/network-configuration-review` |
| 0070 | 3 | 3/3 | 2/3 | `vsphere/technology/storage/metrics/host/adapter-and-path` |
| 0072 | 2 | 1/2 | 1/2 | `vsphere/architecture/vm-vs-guest-os` |
| 0073 | 2 | 1/2 | 2/2 | - |
| 0074 | 1 | 1/1 | 1/1 | - |
| 0077 | 1 | 1/1 | 1/1 | - |
| 0079 | 5 | 2/5 | 2/5 | `sp5-framework/capacity/rightsizing`, `vsphere/technology/memory/metrics/virtual-motherboard/active`, `vsphere/technology/memory/metrics/virtual-motherboard/consumed` |
| 0080 | 4 | 1/4 | 4/4 | - |
| 0081 | 2 | 2/2 | 2/2 | - |
| 0082 | 1 | 1/1 | 1/1 | - |
| 0083 | 4 | 2/4 | 2/4 | `vsphere/technology/cpu/metrics/virtual-motherboard/run`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0084 | 1 | 1/1 | 1/1 | - |
| 0085 | 3 | 3/3 | 3/3 | - |
| 0086 | 4 | 1/4 | 2/4 | `vsphere/tools/esxtop/storage` (main), `vsphere/technology/storage/storage-configuration-review` |
| 0088 | 3 | 2/3 | 2/3 | `vsphere/object-types/esxi/configuration/esxi-configuration-review` |
| 0090 | 7 | 0/7 | 0/7 | `vsphere/technology/storage/concepts/snapshot-impact` (main), `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`, `vsphere/technology/cpu/troubleshooting/vm-other-wait-high`, `vsphere/technology/cpu/concepts/numa`, `vsphere/technology/network/vnic-rx-drops`, `vsphere/technology/storage/metrics/virtual-motherboard/datastore`, `vsphere/technology/cpu/metrics/host/core-utilization` |
| 0097 | 3 | 1/3 | 2/3 | `vsphere/technology/cpu/metrics/host/reserved-capacity` |
| 0100 | 3 | 2/3 | 3/3 | - |
| 0101 | 3 | 1/3 | 1/3 | `vsphere/technology/cpu/metrics/virtual-motherboard/net-run`, `vsphere/technology/cpu/concepts/cpu-frequency` |
| 0102 | 4 | 1/4 | 2/4 | `vsphere/technology/cpu/metrics/virtual-motherboard/latency`, `vsphere/technology/cpu/concepts/hyper-threading` |
| 0103 | 3 | 2/3 | 2/3 | `vsphere/technology/cpu/metrics/virtual-motherboard/used` |
| 0104 | 4 | 2/4 | 2/4 | `vsphere/technology/cpu/metrics/virtual-motherboard/run`, `vsphere/technology/cpu/concepts/power-states` |
| 0106 | 2 | 1/2 | 1/2 | `vsphere/technology/cpu/metrics/virtual-motherboard/net-run` |
| 0108 | 3 | 2/3 | 3/3 | - |
| 0109 | 4 | 1/4 | 2/4 | `vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate`, `vsphere/technology/memory/metrics/virtual-motherboard/latency` |
| 0112 | 2 | 1/2 | 2/2 | - |
| 0113 | 2 | 2/2 | 2/2 | - |
| 0115 | 4 | 0/4 | 0/4 | `vsphere/technology/cpu/metrics/virtual-motherboard/ready`, `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`, `vsphere/technology/cpu/metrics/comparisons/host-contention-metrics` (main), `vsphere/architecture/provider-consumer` |
| 0140 | 5 | 1/5 | 2/5 | `vsphere/technology/memory/metrics/virtual-motherboard/granted`, `vsphere/technology/memory/metrics/virtual-motherboard/overhead`, `vsphere/architecture/resource-controls` |
| 0141 | 5 | 3/5 | 3/5 | `vsphere/technology/memory/concepts/ballooning`, `vsphere/technology/memory/metrics/virtual-motherboard/consumed` |
| 0142 | 5 | 2/5 | 3/5 | `vsphere/technology/memory/metrics/virtual-motherboard/granted`, `vsphere/technology/memory/metrics/virtual-motherboard/active` |
| 0146 | 4 | 2/4 | 1/4 | `vsphere/technology/memory/concepts/large-memory-pages`, `vsphere/technology/memory/metrics/host/shared` (main), `vsphere/technology/memory/concepts/page-sharing` |
| 0147 | 2 | 2/2 | 2/2 | - |
| 0148 | 3 | 2/3 | 2/3 | `vsphere/technology/memory/metrics/virtual-motherboard/zero-pages` |
| 0150 | 3 | 2/3 | 2/3 | `vsphere/architecture/resource-controls` |
| 0152 | 3 | 1/3 | 2/3 | `vsphere/technology/memory/concepts/memory-overhead` (main) |
| 0153 | 3 | 2/3 | 2/3 | `vsphere/architecture/resource-controls` |
| 0180 | 3 | 0/3 | 0/3 | `vsphere/technology/storage/concepts/storage-dimensions`, `vsphere/technology/storage/metrics/virtual-motherboard/iops` (main), `vsphere/technology/storage/metrics/datastore/storage-io-control` |
| 0183 | 3 | 1/3 | 2/3 | `vsphere/technology/storage/metrics/virtual-motherboard/iops` |
| 0184 | 4 | 2/4 | 3/4 | `vsphere/technology/storage/concepts/guest-os-vs-vm-storage` |
| 0186 | 2 | 2/2 | 2/2 | - |
| 0188 | 4 | 2/4 | 2/4 | `vsphere/technology/storage/concepts/esxi-storage-latency-stack`, `vsphere/architecture/provider-consumer` |
| 0210 | 2 | 2/2 | 2/2 | - |
| 0212 | 3 | 1/3 | 2/3 | `vsphere/technology/network/configuration/rss-and-interrupt-coalescing` (main) |
| 0215 | 3 | 3/3 | 3/3 | - |
| 0216 | 4 | 2/4 | 3/4 | `vsphere/technology/network/metrics/distributed-switch/packets` (main) |
| 0217 | 4 | 3/4 | 3/4 | `vsphere/technology/network/metrics/host/throughput` |
| 0230 | 2 | 2/2 | 2/2 | - |
| 0234 | 3 | 1/3 | 1/3 | `vsphere/technology/cpu/concepts/hyper-threading`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0235 | 3 | 2/3 | 3/3 | - |
| 0236 | 4 | 1/4 | 1/4 | `vsphere/architecture/resource-controls`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready`, `vsphere/technology/cpu/metrics/virtual-motherboard/demand` |
| 0237 | 3 | 1/3 | 1/3 | `vsphere/tools/esxtop/units-vs-vsphere-client`, `vsphere/technology/storage/metrics/virtual-motherboard/disk` |
| 0238 | 4 | 2/4 | 2/4 | `vsphere/object-types/cluster/concepts/cluster-operations`, `vsphere/technology/cpu/metrics/virtual-motherboard/ready` |
| 0239 | 5 | 1/5 | 2/5 | `vsphere/object-types/resource-pool/resource-pool-design` (main), `vsphere/architecture/resource-controls`, `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention` |
| 0240 | 1 | 1/1 | 1/1 | - |
| 0260 | 4 | 1/4 | 1/4 | `guest-os/cpu/metrics/run-queue`, `vsphere/tools/esxtop/cpu`, `vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu` |
| 0261 | 4 | 2/4 | 3/4 | `guest-os/cpu/metrics/processor-time` |
| 0262 | 5 | 1/5 | 3/5 | `guest-os/memory/windows-memory`, `guest-os/storage/disk-queue` |
| 0264 | 3 | 3/3 | 3/3 | - |
| 0265 | 4 | 0/4 | 1/4 | `guest-os/memory/windows-memory` (main), `vsphere/technology/memory/concepts/guest-os-vs-vm-memory`, `guest-os/system/troubleshooting/ms-windows-slow` |
| 0266 | 3 | 3/3 | 3/3 | - |
| 0267 | 3 | 2/3 | 2/3 | `vsphere/tools/esxtop/memory` |
| 0269 | 5 | 2/5 | 3/5 | `guest-os/system/concepts/guest-os-configuration-review`, `vsphere/technology/memory/metrics/virtual-motherboard/active` |
| 0272 | 1 | 1/1 | 0/1 | `vsphere/technology/memory/concepts/guest-os-vs-vm-memory` (main) |
| 0274 | 1 | 1/1 | 1/1 | - |
| 0275 | 1 | 1/1 | 1/1 | - |
| 0276 | 1 | 1/1 | 1/1 | - |
| 0277 | 1 | 1/1 | 1/1 | - |
| 0278 | 1 | 1/1 | 1/1 | - |
| 0279 | 1 | 1/1 | 1/1 | - |
| 0290 | 3 | 1/3 | 2/3 | `vsphere/object-types/cluster/configuration/cluster-configuration-review` |
| 0291 | 5 | 2/5 | 2/5 | `vsphere/object-types/vm/configuration/resource-settings-guidance` (main), `vsphere/architecture/resource-controls`, `vsphere/object-types/resource-pool/resource-pool-design` |
| 0292 | 4 | 2/4 | 2/4 | `vsphere/object-types/vm/configuration/resource-settings-guidance`, `vsphere/technology/memory/concepts/memory-overhead` |

Questions: 196. Recall@6 search: 60%. Recall classic context: 69%. Questions with every needed file in context: 91/196 (46%). Main file missing from context: 23 of 196 questions with a main file (0037, 0010, 0181, 0213, 0008, 0020, 0313, 0355, 0356, 0357, 0066, 0086, 0090, 0115, 0146, 0152, 0180, 0212, 0216, 0239, 0265, 0272, 0291). Mode: hybrid.
Release levels (benchmark/retrieval-check.md): main file 100%, context recall at least 95%, complete at least 90%.
