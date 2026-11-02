# The Volume of Metrics Problem

**Source**: Chapter 1 – The World of Metrics → Metrics Nuances  
**Last Updated**: 2026-11-02

## The Scale Problem

vCenter exposes a large number of metrics. At the VM level there are many CPU metrics (some also available per vCPU) and many memory metrics.

Example calculation from the book:

- 17 CPU metrics at VM level
- 12 of them also available per vCPU
- 28 memory metrics
- A VM with 4 vCPUs → 17 + (4 × 12) + 28 = 93 metrics

In an environment with 1,000 VMs (average 4 vCPUs):

- ~93,000 metrics per collection cycle
- If collected every minute → ~134 million metrics per day
- Retained for 6 months → 24+ billion metrics

## The Real Question

With this volume, the amount of actual business value received becomes a valid concern.

**You are not in the business of collecting metrics.**

The goal is insight and problem-solving, not metric accumulation.
