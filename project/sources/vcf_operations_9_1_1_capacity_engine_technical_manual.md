# VCF Operations 9.1.1 Capacity Engine Technical Manual

## 1. Architectural Overview

Starting in **VMware Cloud Foundation (VCF) Operations 9.1.1**, Broadcom replaced the legacy parallel multi-model capacity forecasting architecture (which ran linear regression, autoregressive moving average [ARMA], and competing statistical models simultaneously) with a single unified algorithm based on **time-decay weighted linear regression** and **asymmetric quantile distribution** bounds.

| Architectural Dimension | Legacy Engine (VCF Operations $\le$ 9.1.0) | Updated Engine (VCF Operations $\ge$ 9.1.1) |
| :--- | :--- | :--- |
| **Core Forecasting Approach** | Multi-model ensemble evaluated in parallel | Unified **Time-Decay Weighted Linear Regression** |
| **Historical Data Weighting** | Evaluated across multiple competing trend models | Time-decay weighting prioritizing recent observations |
| **Confidence / Risk Envelope** | Symmetric dispersion bands around the trendline | Independent upper and lower **Asymmetric Quantile Bounds** |
| **Policy Slider Mapping** | Indirect heuristic adjustments | Direct mapping to defined upper and lower data percentiles |
| **Step-Change Handling** | Gradual adjustment over the full historical window | Automated **Jump Point Detection** with Recommended Reset Date |
| **Upgrade Auditability** | No automated post-upgrade comparison export | Automated delta CSV (`/storage/log/vcops/log/capacityMetricsUpgradeChanges.csv`) |

---

## 2. Core Forecasting Logic

*(Note: Broadcom/VMware has not published the proprietary closed-form mathematical equations or internal weighting constants used by the engine. The sections below describe the documented algorithmic logic.)*

### 2.1 Time-Decay Weighted Linear Regression
For core capacity metrics (**CPU**, **Memory**, and **Storage**), the engine fits a single linear trendline to historical utilization data and projects that trajectory forward:

* **Recency Prioritization (Time-Decay):** Rather than treating every historical data point equally across the entire lookback window, the engine applies a temporal decay factor. Recent telemetry carries higher influence on the projected slope than older data, ensuring forecasts reflect current operational behavior rather than outdated workload patterns.
* **Cross-Workload Consistency:** Standardizing on a single regression model eliminates cases where structurally similar workloads produced divergent trendlines because the legacy engine selected different winning models behind the scenes.

### 2.2 Dual-Horizon Lookback Windows
The engine separates long-term capacity planning from short-term placement optimization by applying two distinct historical lookback and forecast horizons:

| Operational Consumer | Historical Lookback Window | Projection Horizon | Functional Objective |
| :--- | :--- | :--- | :--- |
| **Capacity Forecasts & Time Remaining** | Up to **90 days** | Policy-defined provisioning window | Long-term runway planning, hardware procurement, and VM rightsizing. |
| **Workload Placement (WLP)** | **7 days** | **~2 hours** | Tactical inter-cluster placement and balancing without unnecessary migration churn. |

---

## 3. Asymmetric Risk Envelope & Policy Mapping

### 3.1 Asymmetric Quantile Distribution
Instead of wrapping a symmetrical margin above and below the trendline, the 9.1.1 engine evaluates the upper and lower forecast boundaries independently using **asymmetric quantile distribution**:

* **Tighter Fit to Actual Patterns:** Upper and lower bounds track real workload distributions independently, hugging actual usage patterns more closely.
* **Spike and Dip Absorption:** Temporary usage bursts or brief idle periods are absorbed accurately without artificially inflating the entire forecast envelope or triggering premature *Time Remaining* exhaustion alerts.

### 3.2 Predictable Policy Risk Levels
Capacity policy risk sliders map directly to defined upper and lower data percentiles, giving administrators predictable control over how aggressively or conservatively capacity headroom is calculated:

| Policy Risk Setting | Envelope Behavior | Operational Use Case |
| :--- | :--- | :--- |
| **Most Aggressive** | Tightens upper and lower bounds closely around the trendline. | High-density consolidation environments tolerating narrower headroom buffers. |
| **Standard / Default (Conservative Level 3)** | Balances typical operational variance while shielding against unexpected spikes. | General production clusters requiring balanced efficiency and safety headroom. |
| **Most Conservative** | Expands bounds outward to encompass extreme historical peak usage. | Mission-critical or strict-SLA workloads requiring maximum protection against contention. |

---

## 4. Built-In Baseline Stabilization Controls

To prevent non-physical projections or erratic slopes when historical telemetry is incomplete or noisy, the engine automatically defaults to a **flat baseline** (zero projected growth) under three specific conditions:

1. **Limited Collection History:** Fewer than **7 days** of historical metric data have been collected for the object.
2. **Low Statistical Correlation:** Data variability is too high for a linear trendline to represent the workload pattern with statistical validity.
3. **Negative Utilization Trends:** Historical consumption exhibits a downward slope. Rather than projecting resource usage down toward zero, the engine levels out the forecast to a flat baseline to prevent false assumptions of long-term surplus capacity.

---

## 5. Behavioral Jump Point Detection & Baseline Resets

When a cluster or virtual machine undergoes a sudden step-level change—such as a major workload migration, application scale-out, or vCPU/memory reconfiguration—pre-change historical data no longer represents current demand.

* **Automated Detection:** The engine identifies abrupt step-level shifts (jump points) in historical utilization.
* **Recommended Reset Date:** When a jump point is detected, the UI highlights a **Recommended Reset Date**.
* **Administrator Action:** Applying the recommended reset truncates stale pre-change telemetry so that trendlines and asymmetric bounds are calculated strictly from post-change operational behavior.

---

## 6. Upgrade Validation & Operational Verification

Upgrading an existing deployment to **VCF Operations 9.1.1** automatically generates an object-level comparison report so administrators can audit how capacity metrics shifted between the legacy engine and the updated model.

### 6.1 Upgrade Delta Comparison File
* **File Path:** `/storage/log/vcops/log/capacityMetricsUpgradeChanges.csv`
* **Purpose:** Records differences between legacy capacity calculations and the 9.1.1 time-decay weighted regression outputs (including *Time Remaining* and *Rightsizing* recommendations).

### 6.2 Post-Upgrade Verification Workflow
1. **Retrieve the Audit File:** Connect via SSH to the VCF Operations primary node and inspect `/storage/log/vcops/log/capacityMetricsUpgradeChanges.csv`.
2. **Review Material Deltas:** Identify clusters or VMs with notable shifts in *Time Remaining* or *Rightsizing* recommendations.
3. **Evaluate Jump Points:** For objects showing significant baseline changes, check whether a historical migration or reconfiguration occurred and apply the **Recommended Reset Date** if appropriate.
4. **Confirm Policy Risk Settings:** Verify that active policies align with **Conservative Level 3** (or your intended custom risk tier) before sharing updated capacity forecasts with stakeholders.

---

## 7. Primary References

* [A Smarter, More Transparent Way to Forecast Capacity in VMware Cloud Foundation 9.1.1 (VMware Cloud Foundation Blog)](https://blogs.vmware.com/cloud-foundation/2026/10/20/a-smarter-more-transparent-way-to-forecast-capacity-in-vcf/)
* [VMware Cloud Foundation 9.1.1.0 Release Notes (Broadcom TechDocs)](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/vmware-cloud-foundation-9-1-1-0-release-notes.html)