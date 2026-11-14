# Consultations

Agent E2 as a consultant: it leads a conversation, asks for what the advice needs, computes with code, and explains. Not indexed. Release 1.0 ships one consultation, capacity planning (C00); the others are the plan after 1.0, for the author to edit and review as one set (author, 2026-11-14).

How each consultation works ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 4.7):

- The user asks to be guided. The one-round limit on clarifying questions does not apply.
- Code holds a checklist of inputs. Each turn it asks only for what is missing, and offers a default from the catalog, named as a default.
- Code computes (calculator, catalog, decision tree); the model explains the result and the trade-off.
- One shared consultation runner serves every entry: a new consultation is a checklist and its knowledge files, not new code.
- Not in the benchmark: a benchmark question states its inputs and tests the method. The live test measures consultations ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), step 9).

Each entry: status; the user's prompt; why a consultant beats a plain LLM; the checklist; what code computes; what the model explains; the knowledge files; gaps and blockers; a line for your notes.

## Release 1.0

### C00 · Capacity planning for a new cluster
- Status: Release 1.0 (author, 2026-11-14). Calculator built ([harness/capacity.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/capacity.py)); the conversation to build ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 4.7)
- Prompt: "Can you guide me over capacity planning for a vSphere cluster? What should I consider? You're my expert consultant."
- Why a consultant: a plain LLM sizes from GHz and an overcommit ratio per core, forgets HA and what ESXi, vSAN and NSX take, and checks one model instead of six.
- Checklist (code asks only for what is missing): host specification (cores, base clock, Hyper-Threading, DRAM, memory tiering); VM classes with overcommit per physical thread, reservation and expected concurrent peak; typical VM size per class; HA hosts; threads and memory taken by ESXi, vSAN and NSX; CPU that cannot be reserved. Each missing input is offered from the catalog default and named as one.
- Code computes: per host the six numbers (CPU and memory: allocation, reservation, utilization at the expected peak); the binding one; VMs per host and per cluster with HA added on top; the RAM that matches the CPU when RAM is not given.
- The model explains: what each number means, which one limits the host and what would move it (more DRAM, a different ratio, fewer reservations).
- Knowledge: [class-of-service-planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md), [host-spec-from-class-of-service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md), [supply](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md), [overcommit](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/overcommit.md), [class-of-service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md)
- Gaps and blockers: none for the knowledge; the conversation code is the work. Benchmark: L4-43 tests the method; the live test measures the consultation (step 9).
- Author notes:

## After 1.0

### C01 · Can this cluster take more VMs?
- Status: After 1.0
- Prompt: "We need to add 40 VMs to PROD-CL02 next month. Can the cluster take them?"
- Why a consultant: a plain LLM reads Consumed or CPU Usage against total capacity; the answer depends on performance, consumption and risk together, on HA and on reservations.
- Checklist (code asks only for what is missing): the cluster (hosts, HA admission control, failover capacity); Cluster Performance, Cluster Consumption and Cluster Risk, or the counters behind them; the new VMs (count, size, class, reservations); the time horizon.
- Code computes: the decision tree step by step: each score against its band; the new VMs added to allocation, reservation and the expected peak; the HA admission result.
- The model explains: the answer (yes, yes with a condition, no) and the score that decides it; what to fix first when it is no.
- Knowledge: [can-cluster-take-more-vms](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md), [cluster-consumption](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [cluster-risk](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [cluster-performance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/cluster-performance.md), [admission-control-and-cluster-state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md)
- Gaps and blockers: the decision tree runs as code only once flows are executable (Q166). Step 6 (one orange and one green) is open in the tree.
- Author notes:

### C02 · Can I take a host out?
- Status: After 1.0
- Prompt: "I want to put two hosts in maintenance mode on Saturday, or decommission one. Is it safe?"
- Why a consultant: a plain LLM checks average utilization; the limits are HA failover capacity, memory reservations that stop DRS from moving VMs, affinity rules and the peak of the remaining hosts.
- Checklist (code asks only for what is missing): hosts and their load at the business peak; HA admission control policy; VM and pool reservations; DRS rules; how long the hosts stay out.
- Code computes: the cluster with N-1 or N-2 hosts: utilization at the peak, reservations against the unreserved memory of each remaining host, HA failover capacity left.
- The model explains: whether it is safe, and if not, which VMs or settings block it.
- Knowledge: [can-cluster-take-a-host-out](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out.md), [admission-control-and-cluster-state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md), [drs-overview](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/drs-overview.md), [resource-controls](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md)
- Gaps and blockers: Q166 (executable steps). Q222 (does a host in maintenance mode lower availability).
- Author notes:

### C03 · Rightsize a VM, or reclaim capacity across many VMs
- Status: After 1.0
- Prompt: "The capacity team wants to cut our VMs. Which ones, and by how much, without hurting the applications?"
- Why a consultant: a plain LLM sizes from VM Active or Consumed and cuts vCPUs from CPU Usage; Agent E2 sizes the Guest OS, treats applications that manage their own memory apart, and reclaims idle and powered-off VMs first.
- Checklist (code asks only for what is missing): the VMs and what is collected (Guest OS memory used and page-out, Net Run, run queue); the applications (SQL Server, Java, Oracle); the business cycle; the risk appetite per class.
- Code computes: per VM the Guest OS footprint and the proposed size; the idle, powered-off and orphaned VMs; the total reclaimed.
- The model explains: which VMs to change first and why; what to watch after the change; where an application needs its own method.
- Knowledge: [guest-os-sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md), [rightsizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md), [oversized-vm-downsizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md), [reclamation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/reclamation.md), [unused-vm](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/unused-vm.md), [vm-footprint-sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-footprint-sizing.md)
- Gaps and blockers: Q193 (SQL Server max server memory steps). A table tool for exports of many VMs (After 1.0 list).
- Author notes:

### C04 · Design classes of service (Gold, Silver, Bronze)
- Status: After 1.0
- Prompt: "We want to offer Gold, Silver and Bronze VMs to our business units. How do we design and price them?"
- Why a consultant: a plain LLM gives overcommit per core and prices by GHz; Agent E2 sets ratios per physical thread, ties them to the KPI each class must meet, and derives the host specification and the price from them.
- Checklist (code asks only for what is missing): the tenants and what they buy; the performance each class must meet; storage tiers; the cost of a host; HA and maintenance policy.
- Code computes: per class the ratios, reservations and expected peaks; VMs per host (planning calculator); the price per VM from the cost per host.
- The model explains: the trade-off of each ratio, and what Gold buys over Silver.
- Knowledge: [class-of-service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md), [class-of-service-planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md), [host-spec-from-class-of-service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md), [overcommit](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/overcommit.md), [vm-size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md)
- Gaps and blockers: builds on C00; the price formula in class-of-service is to check (review note).
- Author notes:

### C05 · Guided health check of a cluster, host or VM
- Status: After 1.0
- Prompt: "Walk me through a health check of cluster PROD-CL01."
- Why a consultant: a plain LLM lists counters; Agent E2 follows the order of the check, reads each value against its band and goes down only where a value is out.
- Checklist (code asks only for what is missing): the object; each value the next step needs, one at a time (Ready, Co-stop, memory contention, disk latency, drops, consumption).
- Code computes: each value against its KPI band and threshold row; the branch to the next step.
- The model explains: what is healthy, what is not and why, and which flow opens next.
- Knowledge: [cluster-health-check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/cluster-health-check.md), [esxi-health-check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/esxi-health-check.md), [vm-health-check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/vm-health-check.md)
- Gaps and blockers: Q166 (executable steps; thresholds for flow tests, point 4). Availability is after 1.0 in the checks themselves.
- Author notes:

### C06 · Configuration review
- Status: After 1.0
- Prompt: "Review the configuration of our ESXi hosts and VMs against best practice."
- Why a consultant: a plain LLM repeats generic hardening lists; Agent E2 checks what affects performance and capacity, with the reason and the trade-off of each setting.
- Checklist (code asks only for what is missing): the object types in scope; the settings per object (BIOS, power policy, NUMA, VM hardware, reservations and limits, network and storage settings, Guest OS).
- Code computes: each setting against its guidance; consistency across the hosts of a cluster.
- The model explains: each finding with its reason and its risk; what to change first.
- Knowledge: [esxi-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/configuration/esxi-configuration-review.md), [vm-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md), [cluster-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md), [network-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/configuration/network-configuration-review.md), [storage-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/storage-configuration-review.md), [guest-os-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-configuration-review.md), [bios-settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/configuration/bios-settings.md), [host-power-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/host-power-management.md)
- Gaps and blockers: the settings are typed or exported by the user until the live connection (After 1.0 list). Known bugs need web search.
- Author notes:

### C07 · Monster VM and NUMA design
- Status: After 1.0
- Prompt: "We are moving a 40-vCPU, 600 GB SQL Server to vSphere 9.1. How do we size and place it?"
- Why a consultant: a plain LLM sets cores per socket by licensing and ignores the NUMA node size, CPU Hot Add and the host CPU architecture.
- Checklist (code asks only for what is missing): the host CPU model (cores per CCD or compute tile, L3 domains, NPS or SNC mode), memory per NUMA node; the VM vCPUs and memory; licensing; CPU Hot Add; latency sensitivity.
- Code computes: the largest VM that fits one node; the vNUMA layout; whether the VM spans nodes.
- The model explains: the layout and its cost; when to split the VM.
- Knowledge: [virtual-numa](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/virtual-numa.md), [numa-settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/numa-settings.md), [cpu-topology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-topology.md), [latency-sensitivity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/latency-sensitivity.md), [vm-size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md)
- Gaps and blockers: Q198 (NPS-1 or the setting that matches the silicon); Q216 (`numa.*` options in 9.1). The VM size calculator (After 1.0 list).
- Author notes:

### C08 · Memory tiering: adopt it, and on which hosts?
- Status: After 1.0
- Prompt: "Should we turn on NVMe memory tiering to fit 50% more VMs?"
- Why a consultant: a plain LLM reads Consumed as demand and promises the full ratio; Agent E2 reads active memory against DRAM, NVMe latency and CPU headroom.
- Checklist (code asks only for what is missing): per host active memory, Consumed, DRAM; the NVMe device; the workload types (VDI, databases, write-heavy caches); CPU utilization.
- Code computes: active memory as a share of DRAM; the density gain at the chosen ratio; which hosts qualify.
- The model explains: where tiering helps, where it hurts, and what to watch after (NVMe read bandwidth and latency per VM).
- Knowledge: [memory-tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md), [is-memory-tiering-slowing-host](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host.md), [cluster-risk](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md)
- Gaps and blockers: the vendor thresholds have no catalog row for a flow test (Q166, point 4).
- Author notes:

### C09 · Resource pool and reservation design
- Status: After 1.0
- Prompt: "How should we set up resource pools and reservations for production and test?"
- Why a consultant: a plain LLM uses pools as folders and High shares as priority; Agent E2 computes share dilution per VM and the effect of reservations on admission control and DRS.
- Checklist (code asks only for what is missing): the pools, their VMs and vCPUs; shares, reservations, limits, expandable reservations; Scalable Shares; HA policy.
- Code computes: the share each VM gets under contention; reservations against the cluster after a host failure; pools whose reservations block power-on.
- The model explains: the design, the traps it avoids, and the simplest setup that meets the goal.
- Knowledge: [resource-pool-design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/resource-pool/resource-pool-design.md), [resource-settings-guidance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md), [resource-controls](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md), [admission-control-and-cluster-state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md)
- Gaps and blockers: share and reservation arithmetic is not in the calculator yet. Q218 (is a CPU reservation inside Demand).
- Author notes:

### C10 · Design monitoring: KPIs, alerts, dashboards and reports
- Status: After 1.0
- Prompt: "Help us design the alerts and dashboards for our VCF Operations."
- Why a consultant: a plain LLM alerts on utilization; Agent E2 alerts on contention, separates risk from slowness, and sets wait cycles and receivers.
- Checklist (code asks only for what is missing): the teams and what each acts on; the objects; the VCF Operations version; current alert noise.
- Code computes: the alert set from the catalog (symptoms, sets, wait cycles) for the chosen objects.
- The model explains: why each alert exists, who receives it, and what it leaves to dashboards and reports.
- Knowledge: [performance-kpi-design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md), [alert-design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md), [dashboard-design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/dashboard-design.md), [report-design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/report-design.md)
- Gaps and blockers: the full alert catalog waits on the alert overhaul (After 1.0 list).
- Author notes:

### C11 · IaaS SLA and the operating model
- Status: After 1.0
- Prompt: "We are writing the SLA for our private cloud. What should it promise, and how do we run operations to meet it?"
- Why a consultant: a plain LLM puts performance in the SLA and averages availability; Agent E2 keeps performance in the KPI, excludes the maintenance window, and ties daily operations to the pillars.
- Checklist (code asks only for what is missing): what is sold; the tenants; availability target; maintenance windows; the teams.
- Code computes: availability minutes per period for the target; the KPI levels per class.
- The model explains: the SLA text, the KPIs behind it, and the daily and weekly routine.
- Knowledge: [sla-metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md), [kpi-vs-sla](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md), [iaas-business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/iaas-business.md), [proactive-operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/proactive-operations.md), [health-risk-efficiency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-risk-efficiency.md)
- Gaps and blockers: Q222 (does a host in maintenance mode lower Operational Availability).
- Author notes:

### C12 · Hardware refresh and host specification
- Status: After 1.0
- Prompt: "We are replacing our hosts next year. Fewer large hosts or more small ones? Which CPU and how much DRAM?"
- Why a consultant: a plain LLM compares GHz and core counts; Agent E2 compares threads, the clock under load, NUMA size, licensing per core and the HA cost of large hosts.
- Checklist (code asks only for what is missing): the current estate and its peak; candidate CPUs; licensing; HA policy; growth.
- Code computes: hosts needed per option (planning calculator); the HA capacity lost per option.
- The model explains: the trade-off of each option.
- Knowledge: [supply](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md), [host-spec-from-class-of-service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md), [cpu-frequency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md), [memory-hardware](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/configuration/memory-hardware.md)
- Gaps and blockers: thin: no file compares processor generations or the throughput per core under load.
- Author notes:

### C13 · Network design for a cluster
- Status: After 1.0
- Prompt: "How should we lay out the uplinks, teaming and NetIOC for VM, vMotion and vSAN traffic?"
- Why a consultant: a plain LLM adds bandwidth; Agent E2 knows that one vNIC uses one uplink, the switch balances transmit only, and NetIOC shares apply per physical NIC.
- Checklist (code asks only for what is missing): uplinks and speeds; traffic types and their peaks; distributed or standard switch; physical switch capabilities (LACP).
- Code computes: traffic per uplink under each teaming policy; NetIOC shares under contention.
- The model explains: the layout and how it fails over.
- Knowledge: [nic-teaming](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/nic-teaming.md), [netioc](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/netioc.md), [network-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/configuration/network-configuration-review.md)
- Gaps and blockers: thin: no flow or design guide for the whole network; the NIC teaming file is new (2026-11-14).
- Author notes:

### C14 · Storage design
- Status: After 1.0
- Prompt: "How large should our datastores be, how far can we overcommit thin disks, and what queue depths should we set?"
- Why a consultant: a plain LLM raises queue depths and trusts the array latency; Agent E2 reads the queues along the IO path and sizes overcommit from growth and snapshots.
- Checklist (code asks only for what is missing): the array and protocol; VMs per datastore; thin share; snapshot policy; growth; queue depth settings.
- Code computes: the thin overcommit ratio and the runway; the outstanding IO each queue allows.
- The model explains: the design and its risks.
- Knowledge: [storage-configuration-review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/storage-configuration-review.md), [esxi-storage-io-path](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-io-path.md)
- Gaps and blockers: thin: Q195 (Paravirtual SCSI queue limit, KAVG and DAVG values); no datastore sizing guidance.
- Author notes:
