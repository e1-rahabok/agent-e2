# Health check

## What it is
- A check of one object or system across every pillar: is it up, is it fast, is it secure, will it be enough. The what: is the object healthy, at risk, or wasteful.
- The unit is the object, not the pillar. Health is a property of a system; a pillar is one aspect of it.
- No single-pillar health check. A capacity-only check misses a cluster that has room for 50 VMs and has lost HA; a performance-only check misses a host that runs fast on an unsupported version. One pillar answers one question (can this cluster take more VMs?): a step of the health check, or a decision, not a health check.
- Proactive: no complaint and no alert starts it. It runs on a schedule (daily, twice a day; weekly and monthly with a longer data range) or on request (before a change, after a migration, on an estate seen for the first time). Cadence: `sp5-framework/concepts/proactive-operations`.

## Superset of troubleshooting
- Troubleshooting starts from a known problem. A complaint, an alert or a failed health check step gives the object and the problem type (down or slow). The question is only why.
- A health check starts with no known problem. It must first find out whether there is one, on which pillar, on which object, and how bad. Only then does a failed step open its troubleshooting flow.
- So a health check contains troubleshooting: detection across every pillar, then troubleshooting for each step that fails.
- The availability, performance and security steps use the same order of checks as the reactive flows (down, slow, breached). Reactive enters one pillar directly; the health check walks all four.
- Detection is the harder half. There is no symptom to anchor on, most metrics are fine, and the object count is large. KPIs and models (0-100%, colour coded) keep the check to about 5 minutes when nothing is wrong.
- Capacity and efficiency are checked but never troubleshot: there is no incident to explain, only a plan to compare with.

## Order of checks
```mermaid
flowchart TD
  S0([Health check of one object]) --> A1
  subgraph AV["1. Is it up? Availability"]
    A1[Log] --> A2[Saturation] --> A3[Configuration] --> A4[Known bug]
  end
  subgraph PF["2. Is it fast? Performance"]
    P1[Contention] --> P2[Consumption] --> P3[Configuration] --> P4[Known bug] --> P5[Log]
  end
  subgraph SC["3. Is it secure? Security"]
    S1[Configuration] --> S2[Known bug] --> S3[Log]
  end
  subgraph CP["4. Will it be enough? Capacity"]
    C1[Consumption] --> C2[Configuration] --> C3[Contention] --> C4[Inventory]
  end
  A4 --> P1
  P5 --> S1
  S3 --> C1
  C4 --> D([Done: a failed step opens its troubleshooting flow])
```
- Is it up? Availability first: a system that is down has no performance problem and cannot be attacked.
- Is it fast? Up does not mean fast.
- Is it secure? Running well does not mean safe from attack.
- Will it be enough? A healthy present does not mean a healthy future. Efficiency (waste) is read here.
- Within each pillar, the what before the why: establish the fact, then explain it.
- Configuration and known bugs sit inside each pillar, not after them: a configuration issue or a bug can cause an outage, slowness or a security loophole.

## How to read the result
- Three verdicts, read separately: present health, risk (future health) and efficiency. Never one score (`sp5-framework/concepts/health-risk-efficiency`).
- Each failed step names the KPI or model, its band, and the troubleshooting flow it opens.
- Release 1.0 checks availability, performance and capacity. Security and compliance steps are a future phase: state them as not checked.

## Object health checks
- VM: `vsphere/object-types/vm/health-check/vm-health-check`.
- ESXi host: `vsphere/object-types/esxi/health-check/esxi-health-check`.
- vSphere cluster: `vsphere/object-types/cluster/health-check/cluster-health-check`. Its capacity step uses the closure decision `sp5-framework/capacity/health-check/can-cluster-take-more-vms`.

## Traps
- "Run a capacity health check on this cluster" → a health check covers the cluster on every pillar. For capacity alone, name the question (can it take more VMs, how long until full) and say the other pillars were not checked.
- "Health check and troubleshooting are the same thing" → troubleshooting starts from a known problem and asks why; the health check first finds out whether there is a problem.
- "The VM is slow: run its health check" → a complaint is reactive. Start the troubleshooting flow (`sp5-framework/performance/troubleshooting/vm-slow`).
- "No alert fired, so the object is healthy" → alerts are guard rails for what humans miss; most risk and waste never raise one.
- "Performance is green, so the object is healthy" → availability, security and capacity are checked separately; up and fast today is not safe or enough tomorrow.
- "Troubleshoot the capacity problem" → capacity is planned and monitored; only down and slow are troubleshot.

## Metadata
```yaml
id: sp5-framework/concepts/health-check
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- performance
- compliance
- capacity
- value
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- sp5-framework/concepts/proactive-operations
- sp5-framework/concepts/health-risk-efficiency
- sp5-framework/concepts/monitoring-vs-troubleshooting
related:
- vsphere/object-types/cluster/health-check/cluster-health-check
- vsphere/object-types/vm/health-check/vm-health-check
- vsphere/object-types/esxi/health-check/esxi-health-check
- sp5-framework/performance/troubleshooting/vm-slow
source:
  document: Knowledge base synthesis of the files in internal_derive; order of checks from the health check template (2026-11-09)
  path: 'Your Private Cloud > SP5 Framework > Health; Monitor | Troubleshoot; Proactive Operations'
corrections: []
review_notes: []
status: draft
```
