# Retrieval check 2026-11-14, reading plan, hybrid

The reading plan of the expert-led agent ([harness/AGENT.md](../../../harness/AGENT.md), section 4.2). The column Classic context holds the reading plan's context. Command: `python3 benchmark/runner/retrieval_eval.py --embeddings --set planner=true`. Index: knowledge base at e8fa738 (merge of e1-rahabok/agent-e2#301). How to read: [benchmark/retrieval-check.md](../../retrieval-check.md).

| Question | Needed | Search top 6 | Classic context | Missed in context |
|---|---|---|---|---|
| 0029 | 2 | 2/2 | 2/2 | - |
| 0032 | 2 | 2/2 | 2/2 | - |
| 0034 | 2 | 0/2 | 1/2 | [`vsphere/technology/storage/concepts/storage-layers`](../../../knowledge/vsphere/technology/storage/concepts/storage-layers.md) |
| 0035 | 1 | 1/1 | 1/1 | - |
| 0036 | 2 | 2/2 | 2/2 | - |
| 0037 | 2 | 0/2 | 0/2 | [`vsphere/architecture/metric-sources`](../../../knowledge/vsphere/architecture/metric-sources.md) (main), [`vsphere/architecture/vm-vs-guest-os`](../../../knowledge/vsphere/architecture/vm-vs-guest-os.md) |
| 0038 | 2 | 2/2 | 2/2 | - |
| 0187 | 3 | 3/3 | 3/3 | - |
| 0039 | 3 | 2/3 | 2/3 | [`vsphere/architecture/vm-vs-guest-os`](../../../knowledge/vsphere/architecture/vm-vs-guest-os.md) |
| 0040 | 2 | 2/2 | 2/2 | - |
| 0041 | 3 | 3/3 | 3/3 | - |
| 0042 | 2 | 1/2 | 1/2 | [`vsphere/technology/network/metrics/host/errors`](../../../knowledge/vsphere/technology/network/metrics/host/errors.md) |
| 0043 | 1 | 1/1 | 1/1 | - |
| 0044 | 3 | 3/3 | 3/3 | - |
| 0045 | 2 | 2/2 | 2/2 | - |
| 0046 | 2 | 2/2 | 2/2 | - |
| 0047 | 1 | 1/1 | 1/1 | - |
| 0048 | 2 | 2/2 | 2/2 | - |
| 0049 | 3 | 2/3 | 2/3 | [`vsphere/technology/storage/concepts/snapshot-impact`](../../../knowledge/vsphere/technology/storage/concepts/snapshot-impact.md) |
| 0051 | 2 | 1/2 | 1/2 | [`vsphere/architecture/metric-sources`](../../../knowledge/vsphere/architecture/metric-sources.md) |
| 0052 | 3 | 2/3 | 2/3 | [`vsphere/technology/memory/metrics/virtual-motherboard/latency`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md) |
| 0053 | 2 | 2/2 | 2/2 | - |
| 0149 | 2 | 1/2 | 2/2 | - |
| 0271 | 3 | 1/3 | 3/3 | - |
| 0273 | 1 | 1/1 | 1/1 | - |
| 0001 | 1 | 1/1 | 1/1 | - |
| 0007 | 4 | 3/4 | 3/4 | [`vsphere/object-types/esxi/configuration/bios-settings`](../../../knowledge/vsphere/object-types/esxi/configuration/bios-settings.md) |
| 0009 | 7 | 2/7 | 6/7 | [`vsphere/architecture/vm-vs-guest-os`](../../../knowledge/vsphere/architecture/vm-vs-guest-os.md) |
| 0010 | 4 | 3/4 | 4/4 | - |
| 0011 | 3 | 3/3 | 3/3 | - |
| 0013 | 4 | 1/4 | 1/4 | [`vsphere/technology/cpu/decision-tree/oversized-vm-downsizing`](../../../knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md), [`vsphere/technology/cpu/concepts/idle-and-unused-vcpus`](../../../knowledge/vsphere/technology/cpu/concepts/idle-and-unused-vcpus.md), [`vsphere/technology/memory/concepts/memory-as-storage`](../../../knowledge/vsphere/technology/memory/concepts/memory-as-storage.md) |
| 0014 | 1 | 1/1 | 1/1 | - |
| 0015 | 1 | 1/1 | 1/1 | - |
| 0016 | 3 | 3/3 | 3/3 | - |
| 0017 | 1 | 1/1 | 1/1 | - |
| 0019 | 3 | 1/3 | 2/3 | [`sp5-framework/observability/metric-perspectives`](../../../knowledge/sp5-framework/observability/metric-perspectives.md) |
| 0021 | 4 | 3/4 | 4/4 | - |
| 0022 | 4 | 2/4 | 3/4 | [`vsphere/technology/memory/metrics/virtual-motherboard/usage`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/usage.md) |
| 0027 | 1 | 1/1 | 1/1 | - |
| 0028 | 3 | 1/3 | 3/3 | - |
| 0050 | 3 | 2/3 | 2/3 | [`vsphere/tools/esxtop/overview`](../../../knowledge/vsphere/tools/esxtop/overview.md) |
| 0089 | 3 | 1/3 | 1/3 | [`vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`](../../../knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md), [`vsphere/technology/storage/concepts/guest-os-vs-vm-storage`](../../../knowledge/vsphere/technology/storage/concepts/guest-os-vs-vm-storage.md) |
| 0094 | 3 | 2/3 | 3/3 | - |
| 0095 | 3 | 2/3 | 3/3 | - |
| 0105 | 2 | 2/2 | 2/2 | - |
| 0107 | 3 | 1/3 | 2/3 | [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../../knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md) |
| 0110 | 2 | 1/2 | 2/2 | - |
| 0111 | 3 | 3/3 | 3/3 | - |
| 0114 | 3 | 2/3 | 2/3 | [`vsphere/technology/cpu/concepts/idle-and-unused-vcpus`](../../../knowledge/vsphere/technology/cpu/concepts/idle-and-unused-vcpus.md) (main) |
| 0143 | 3 | 3/3 | 3/3 | - |
| 0144 | 3 | 2/3 | 3/3 | - |
| 0145 | 2 | 2/2 | 2/2 | - |
| 0151 | 3 | 2/3 | 3/3 | - |
| 0181 | 2 | 1/2 | 0/2 | [`vsphere/technology/storage/concepts/vm-files`](../../../knowledge/vsphere/technology/storage/concepts/vm-files.md) (main), [`vsphere/technology/storage/datastore-space-headroom`](../../../knowledge/vsphere/technology/storage/datastore-space-headroom.md) |
| 0182 | 3 | 3/3 | 3/3 | - |
| 0185 | 4 | 3/4 | 3/4 | [`vsphere/technology/storage/concepts/vm-files`](../../../knowledge/vsphere/technology/storage/concepts/vm-files.md) |
| 0211 | 4 | 3/4 | 4/4 | - |
| 0213 | 2 | 0/2 | 1/2 | [`sp5-framework/concepts/configuration-management`](../../../knowledge/sp5-framework/concepts/configuration-management.md) |
| 0214 | 4 | 3/4 | 3/4 | [`vsphere/technology/network/configuration/rss-and-interrupt-coalescing`](../../../knowledge/vsphere/technology/network/configuration/rss-and-interrupt-coalescing.md) |
| 0231 | 2 | 2/2 | 2/2 | - |
| 0232 | 3 | 1/3 | 1/3 | [`vsphere/tools/vsphere-client/vcenter-statistics`](../../../knowledge/vsphere/tools/vsphere-client/vcenter-statistics.md), [`vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`](../../../knowledge/vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention.md) |
| 0233 | 3 | 3/3 | 3/3 | - |
| 0263 | 2 | 1/2 | 2/2 | - |
| 0268 | 3 | 2/3 | 3/3 | - |
| 0270 | 2 | 2/2 | 2/2 | - |
| 0002 | 3 | 1/3 | 3/3 | - |
| 0003 | 3 | 3/3 | 3/3 | - |
| 0004 | 5 | 4/5 | 5/5 | - |
| 0005 | 4 | 2/4 | 3/4 | [`vsphere/technology/cpu/configuration/host-power-management`](../../../knowledge/vsphere/technology/cpu/configuration/host-power-management.md) |
| 0006 | 3 | 2/3 | 2/3 | [`sp5-framework/capacity/overcommit`](../../../knowledge/sp5-framework/capacity/overcommit.md) |
| 0008 | 5 | 4/5 | 5/5 | - |
| 0012 | 4 | 4/4 | 4/4 | - |
| 0018 | 5 | 3/5 | 5/5 | - |
| 0020 | 3 | 2/3 | 3/3 | - |
| 0023 | 4 | 2/4 | 4/4 | - |
| 0293 | 3 | 3/3 | 3/3 | - |
| 0294 | 1 | 1/1 | 1/1 | - |
| 0295 | 1 | 1/1 | 1/1 | - |
| 0296 | 2 | 2/2 | 2/2 | - |
| 0297 | 2 | 1/2 | 2/2 | - |
| 0298 | 6 | 2/6 | 2/6 | [`vsphere/technology/memory/concepts/memory-overhead`](../../../knowledge/vsphere/technology/memory/concepts/memory-overhead.md), [`vsphere/object-types/cluster/concepts/drs-overview`](../../../knowledge/vsphere/object-types/cluster/concepts/drs-overview.md), [`vsphere/object-types/cluster/concepts/dpm`](../../../knowledge/vsphere/object-types/cluster/concepts/dpm.md), [`vsphere/technology/memory/configuration/host-level-swapping`](../../../knowledge/vsphere/technology/memory/configuration/host-level-swapping.md) |
| 0310 | 2 | 1/2 | 2/2 | - |
| 0311 | 4 | 2/4 | 3/4 | [`guest-os/guest-os-alerts`](../../../knowledge/guest-os/guest-os-alerts.md) |
| 0313 | 3 | 2/3 | 2/3 | [`vcf-operations/features/peak-20-second-metrics`](../../../knowledge/vcf-operations/features/peak-20-second-metrics.md) (main) |
| 0314 | 3 | 3/3 | 3/3 | - |
| 0024 | 4 | 3/4 | 3/4 | [`vsphere/technology/memory/concepts/memory-as-storage`](../../../knowledge/vsphere/technology/memory/concepts/memory-as-storage.md) |
| 0330 | 2 | 1/2 | 1/2 | [`vsphere/object-types/cluster/cluster-health-check`](../../../knowledge/vsphere/object-types/cluster/cluster-health-check.md) |
| 0331 | 3 | 2/3 | 2/3 | [`vsphere/technology/cpu/metrics/host/utilization`](../../../knowledge/vsphere/technology/cpu/metrics/host/utilization.md) |
| 0340 | 3 | 2/3 | 2/3 | [`vcf-operations/alert-definitions`](../../../knowledge/vcf-operations/alert-definitions.md) |
| 0341 | 3 | 2/3 | 2/3 | [`vcf-operations/features/peak-20-second-metrics`](../../../knowledge/vcf-operations/features/peak-20-second-metrics.md) |
| 0342 | 3 | 1/3 | 2/3 | [`vsphere/technology/storage/metrics/host/datastore`](../../../knowledge/vsphere/technology/storage/metrics/host/datastore.md) |
| 0343 | 2 | 1/2 | 1/2 | [`vsphere/object-types/datastore/datastore-alerts`](../../../knowledge/vsphere/object-types/datastore/datastore-alerts.md) |
| 0344 | 3 | 2/3 | 3/3 | - |
| 0345 | 3 | 3/3 | 3/3 | - |
| 0346 | 3 | 2/3 | 3/3 | - |
| 0347 | 3 | 2/3 | 3/3 | - |
| 0025 | 5 | 3/5 | 4/5 | [`vsphere/technology/memory/metrics/host/swap-used`](../../../knowledge/vsphere/technology/memory/metrics/host/swap-used.md) |
| 0350 | 5 | 2/5 | 1/5 | [`vsphere/object-types/vm/vm-health-check`](../../../knowledge/vsphere/object-types/vm/vm-health-check.md) (main), [`vsphere/technology/memory/metrics/comparisons/vm-memory-metrics`](../../../knowledge/vsphere/technology/memory/metrics/comparisons/vm-memory-metrics.md), [`vsphere/technology/cpu/metrics/comparisons/consumption-metrics`](../../../knowledge/vsphere/technology/cpu/metrics/comparisons/consumption-metrics.md), [`vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`](../../../knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md) |
| 0351 | 3 | 2/3 | 1/3 | [`vsphere/object-types/vm/vm-health-check`](../../../knowledge/vsphere/object-types/vm/vm-health-check.md), [`vcf-operations/vcf-operations-role`](../../../knowledge/vcf-operations/vcf-operations-role.md) |
| 0352 | 5 | 1/5 | 2/5 | [`vsphere/technology/cpu/metrics/comparisons/host-contention-metrics`](../../../knowledge/vsphere/technology/cpu/metrics/comparisons/host-contention-metrics.md), [`vsphere/architecture/provider-consumer`](../../../knowledge/vsphere/architecture/provider-consumer.md), [`vsphere/architecture/resource-controls`](../../../knowledge/vsphere/architecture/resource-controls.md) |
| 0353 | 5 | 3/5 | 3/5 | [`vsphere/object-types/cluster/cluster-health-check`](../../../knowledge/vsphere/object-types/cluster/cluster-health-check.md), [`vsphere/tools/esxtop/cpu`](../../../knowledge/vsphere/tools/esxtop/cpu.md) |
| 0354 | 4 | 3/4 | 4/4 | - |
| 0355 | 4 | 2/4 | 3/4 | [`vsphere/object-types/cluster/cluster-health-check`](../../../knowledge/vsphere/object-types/cluster/cluster-health-check.md) (main) |
| 0356 | 4 | 2/4 | 2/4 | [`vcf-operations/vcf-operations-role`](../../../knowledge/vcf-operations/vcf-operations-role.md) (main), [`vsphere/object-types/vm/vm-health-check`](../../../knowledge/vsphere/object-types/vm/vm-health-check.md) |
| 0357 | 5 | 1/5 | 4/5 | [`vcf-operations/vcf-operations-role`](../../../knowledge/vcf-operations/vcf-operations-role.md) (main) |
| 0358 | 2 | 1/2 | 1/2 | [`vcf-operations/vcf-operations-role`](../../../knowledge/vcf-operations/vcf-operations-role.md) |
| 0359 | 4 | 2/4 | 3/4 | [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 0026 | 2 | 1/2 | 2/2 | - |
| 0360 | 4 | 2/4 | 3/4 | [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 0361 | 4 | 3/4 | 2/4 | [`vsphere/technology/storage/concepts/esxi-storage-io-path`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-io-path.md) (main), [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 0054 | 3 | 1/3 | 3/3 | - |
| 0056 | 2 | 2/2 | 2/2 | - |
| 0057 | 2 | 1/2 | 2/2 | - |
| 0058 | 4 | 3/4 | 4/4 | - |
| 0059 | 4 | 2/4 | 4/4 | - |
| 0060 | 4 | 3/4 | 4/4 | - |
| 0061 | 1 | 1/1 | 1/1 | - |
| 0062 | 4 | 3/4 | 3/4 | [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 0063 | 3 | 3/3 | 3/3 | - |
| 0065 | 2 | 2/2 | 2/2 | - |
| 0066 | 3 | 1/3 | 2/3 | [`vsphere/tools/esxtop/cpu`](../../../knowledge/vsphere/tools/esxtop/cpu.md) (main) |
| 0067 | 4 | 2/4 | 3/4 | [`vsphere/technology/cpu/concepts/virtual-numa`](../../../knowledge/vsphere/technology/cpu/concepts/virtual-numa.md) |
| 0068 | 3 | 2/3 | 3/3 | - |
| 0069 | 3 | 2/3 | 2/3 | [`vsphere/technology/network/configuration/network-configuration-review`](../../../knowledge/vsphere/technology/network/configuration/network-configuration-review.md) |
| 0070 | 3 | 3/3 | 2/3 | [`vsphere/technology/storage/metrics/host/adapter-and-path`](../../../knowledge/vsphere/technology/storage/metrics/host/adapter-and-path.md) |
| 0072 | 2 | 1/2 | 1/2 | [`vsphere/architecture/vm-vs-guest-os`](../../../knowledge/vsphere/architecture/vm-vs-guest-os.md) |
| 0073 | 2 | 1/2 | 2/2 | - |
| 0074 | 1 | 1/1 | 1/1 | - |
| 0077 | 1 | 1/1 | 1/1 | - |
| 0079 | 5 | 2/5 | 3/5 | [`sp5-framework/capacity/rightsizing`](../../../knowledge/sp5-framework/capacity/rightsizing.md), [`vsphere/technology/memory/metrics/virtual-motherboard/consumed`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/consumed.md) |
| 0080 | 4 | 1/4 | 4/4 | - |
| 0081 | 2 | 2/2 | 2/2 | - |
| 0082 | 1 | 1/1 | 1/1 | - |
| 0083 | 4 | 2/4 | 4/4 | - |
| 0084 | 1 | 1/1 | 1/1 | - |
| 0085 | 3 | 3/3 | 3/3 | - |
| 0086 | 4 | 1/4 | 3/4 | [`vsphere/technology/storage/storage-configuration-review`](../../../knowledge/vsphere/technology/storage/storage-configuration-review.md) |
| 0088 | 3 | 2/3 | 2/3 | [`vsphere/object-types/esxi/configuration/esxi-configuration-review`](../../../knowledge/vsphere/object-types/esxi/configuration/esxi-configuration-review.md) |
| 0090 | 7 | 0/7 | 3/7 | [`vsphere/technology/storage/concepts/snapshot-impact`](../../../knowledge/vsphere/technology/storage/concepts/snapshot-impact.md) (main), [`vsphere/technology/cpu/troubleshooting/vm-other-wait-high`](../../../knowledge/vsphere/technology/cpu/troubleshooting/vm-other-wait-high.md), [`vsphere/technology/cpu/concepts/numa`](../../../knowledge/vsphere/technology/cpu/concepts/numa.md), [`vsphere/technology/network/vnic-rx-drops`](../../../knowledge/vsphere/technology/network/vnic-rx-drops.md) |
| 0097 | 3 | 1/3 | 2/3 | [`vsphere/technology/cpu/metrics/host/reserved-capacity`](../../../knowledge/vsphere/technology/cpu/metrics/host/reserved-capacity.md) |
| 0100 | 3 | 2/3 | 3/3 | - |
| 0101 | 3 | 1/3 | 2/3 | [`vsphere/technology/cpu/concepts/cpu-frequency`](../../../knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md) |
| 0102 | 4 | 1/4 | 2/4 | [`vsphere/technology/cpu/metrics/virtual-motherboard/latency`](../../../knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md), [`vsphere/technology/cpu/concepts/hyper-threading`](../../../knowledge/vsphere/technology/cpu/concepts/hyper-threading.md) |
| 0103 | 3 | 2/3 | 3/3 | - |
| 0104 | 4 | 2/4 | 4/4 | - |
| 0106 | 2 | 1/2 | 2/2 | - |
| 0108 | 3 | 2/3 | 3/3 | - |
| 0109 | 4 | 1/4 | 4/4 | - |
| 0112 | 2 | 1/2 | 2/2 | - |
| 0113 | 2 | 2/2 | 2/2 | - |
| 0115 | 4 | 1/4 | 3/4 | [`vsphere/technology/cpu/metrics/comparisons/host-contention-metrics`](../../../knowledge/vsphere/technology/cpu/metrics/comparisons/host-contention-metrics.md) (main) |
| 0140 | 5 | 1/5 | 3/5 | [`vsphere/technology/memory/metrics/virtual-motherboard/overhead`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/overhead.md), [`vsphere/architecture/resource-controls`](../../../knowledge/vsphere/architecture/resource-controls.md) |
| 0141 | 5 | 3/5 | 3/5 | [`vsphere/technology/memory/metrics/virtual-motherboard/overhead`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/overhead.md), [`vsphere/technology/memory/metrics/virtual-motherboard/consumed`](../../../knowledge/vsphere/technology/memory/metrics/virtual-motherboard/consumed.md) |
| 0142 | 5 | 2/5 | 5/5 | - |
| 0146 | 4 | 2/4 | 3/4 | [`vsphere/technology/memory/metrics/host/shared`](../../../knowledge/vsphere/technology/memory/metrics/host/shared.md) (main) |
| 0147 | 2 | 2/2 | 2/2 | - |
| 0148 | 3 | 2/3 | 3/3 | - |
| 0150 | 3 | 2/3 | 3/3 | - |
| 0152 | 3 | 1/3 | 2/3 | [`vsphere/technology/memory/concepts/memory-overhead`](../../../knowledge/vsphere/technology/memory/concepts/memory-overhead.md) (main) |
| 0153 | 3 | 2/3 | 2/3 | [`vsphere/architecture/resource-controls`](../../../knowledge/vsphere/architecture/resource-controls.md) |
| 0180 | 3 | 0/3 | 2/3 | [`vsphere/technology/storage/concepts/storage-dimensions`](../../../knowledge/vsphere/technology/storage/concepts/storage-dimensions.md) |
| 0183 | 3 | 1/3 | 2/3 | [`vsphere/technology/storage/metrics/virtual-motherboard/iops`](../../../knowledge/vsphere/technology/storage/metrics/virtual-motherboard/iops.md) |
| 0184 | 4 | 2/4 | 3/4 | [`vsphere/technology/storage/concepts/guest-os-vs-vm-storage`](../../../knowledge/vsphere/technology/storage/concepts/guest-os-vs-vm-storage.md) |
| 0186 | 2 | 2/2 | 2/2 | - |
| 0188 | 4 | 2/4 | 2/4 | [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../../knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md), [`vsphere/architecture/provider-consumer`](../../../knowledge/vsphere/architecture/provider-consumer.md) |
| 0210 | 2 | 2/2 | 2/2 | - |
| 0212 | 3 | 1/3 | 2/3 | [`vsphere/technology/network/configuration/rss-and-interrupt-coalescing`](../../../knowledge/vsphere/technology/network/configuration/rss-and-interrupt-coalescing.md) (main) |
| 0215 | 3 | 3/3 | 3/3 | - |
| 0216 | 4 | 2/4 | 3/4 | [`vsphere/technology/network/metrics/distributed-switch/packets`](../../../knowledge/vsphere/technology/network/metrics/distributed-switch/packets.md) (main) |
| 0217 | 4 | 3/4 | 4/4 | - |
| 0230 | 2 | 2/2 | 2/2 | - |
| 0234 | 3 | 1/3 | 3/3 | - |
| 0235 | 3 | 2/3 | 3/3 | - |
| 0236 | 4 | 1/4 | 4/4 | - |
| 0237 | 3 | 1/3 | 2/3 | [`vsphere/tools/esxtop/units-vs-vsphere-client`](../../../knowledge/vsphere/tools/esxtop/units-vs-vsphere-client.md) |
| 0238 | 4 | 2/4 | 3/4 | [`vsphere/object-types/cluster/concepts/cluster-operations`](../../../knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md) |
| 0239 | 5 | 1/5 | 3/5 | [`vsphere/object-types/resource-pool/resource-pool-design`](../../../knowledge/vsphere/object-types/resource-pool/resource-pool-design.md) (main), [`vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`](../../../knowledge/vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention.md) |
| 0240 | 1 | 1/1 | 1/1 | - |
| 0260 | 4 | 1/4 | 1/4 | [`guest-os/cpu/metrics/run-queue`](../../../knowledge/guest-os/cpu/metrics/run-queue.md), [`vsphere/tools/esxtop/cpu`](../../../knowledge/vsphere/tools/esxtop/cpu.md), [`vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu`](../../../knowledge/vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu.md) |
| 0261 | 4 | 2/4 | 2/4 | [`guest-os/cpu/metrics/processor-time`](../../../knowledge/guest-os/cpu/metrics/processor-time.md), [`vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu`](../../../knowledge/vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu.md) |
| 0262 | 5 | 1/5 | 5/5 | - |
| 0264 | 3 | 3/3 | 3/3 | - |
| 0265 | 4 | 0/4 | 1/4 | [`guest-os/memory/windows-memory`](../../../knowledge/guest-os/memory/windows-memory.md) (main), [`vsphere/technology/memory/concepts/guest-os-vs-vm-memory`](../../../knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md), [`guest-os/system/troubleshooting/ms-windows-slow`](../../../knowledge/guest-os/system/troubleshooting/ms-windows-slow.md) |
| 0266 | 3 | 3/3 | 3/3 | - |
| 0267 | 3 | 2/3 | 2/3 | [`vsphere/tools/esxtop/memory`](../../../knowledge/vsphere/tools/esxtop/memory.md) |
| 0269 | 5 | 2/5 | 4/5 | [`guest-os/system/concepts/guest-os-configuration-review`](../../../knowledge/guest-os/system/concepts/guest-os-configuration-review.md) |
| 0272 | 1 | 1/1 | 1/1 | - |
| 0274 | 1 | 1/1 | 1/1 | - |
| 0275 | 1 | 1/1 | 1/1 | - |
| 0276 | 1 | 1/1 | 1/1 | - |
| 0277 | 1 | 1/1 | 1/1 | - |
| 0278 | 1 | 1/1 | 1/1 | - |
| 0279 | 1 | 1/1 | 1/1 | - |
| 0290 | 3 | 1/3 | 2/3 | [`vsphere/object-types/cluster/configuration/cluster-configuration-review`](../../../knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md) |
| 0291 | 5 | 2/5 | 2/5 | [`vsphere/object-types/vm/configuration/resource-settings-guidance`](../../../knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (main), [`vsphere/architecture/resource-controls`](../../../knowledge/vsphere/architecture/resource-controls.md), [`vsphere/object-types/resource-pool/resource-pool-design`](../../../knowledge/vsphere/object-types/resource-pool/resource-pool-design.md) |
| 0292 | 4 | 2/4 | 3/4 | [`vsphere/object-types/cluster/concepts/drs-overview`](../../../knowledge/vsphere/object-types/cluster/concepts/drs-overview.md) |

Questions: 196. Recall@6 search: 60%. Recall classic context: 80%. Questions with every needed file in context: 115/196 (59%). Main file missing from context: 19 of 196 questions with a main file (0037, 0114, 0181, 0313, 0350, 0355, 0356, 0357, 0361, 0066, 0090, 0115, 0146, 0152, 0212, 0216, 0239, 0265, 0291). Mode: hybrid, reading plan (harness/planner.py).
Complete by number of needed files: 1 file 24/24 (100%), 2 files 32/42 (76%), 3 files 39/69 (57%), 4 files 15/42 (36%), 5+ files 5/19 (26%).
Release levels (benchmark/retrieval-check.md): main file 100%, context recall at least 95%, complete at least 90%.
