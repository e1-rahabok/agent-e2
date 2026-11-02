# Naming Complexity

**Source**: Chapter 1 – The World of Metrics → Metrics Nuances  
**Last Updated**: 2026-11-02

## The Problem

The same concept is often given different names across platforms, vendors, and even within the same product family. This creates unnecessary cognitive load and increases the chance of misinterpretation.

## Examples of Naming Issues

| Pattern | Example |
|---------|--------|
| Same object, same metric, different name | OpenTelemetry uses “Usage” for GB but “Utilization” for %. Kubernetes Pod memory metrics are called Memory Usage (GB) and Memory Utilization (%). |
| Same purpose, different name | Different products use different labels for essentially the same idea (Allocation vs Reservation vs Limit, etc.). |
| Ambiguous or overloaded terms | Words such as Device, Disk, and LUN are often used interchangeably even though they are not identical. |
| Inconsistent use of Reservation / Allocation / Limit | Terms are mixed or poorly chosen across products, making it harder to reason clearly. |

## Why It Matters

When names are inconsistent, people (and AI systems) easily compare the wrong things or apply the wrong thresholds. Clean thinking starts with clean terminology.
