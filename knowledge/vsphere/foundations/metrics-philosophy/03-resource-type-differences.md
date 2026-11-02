# Fundamental Differences Across Resource Types

**Source**: Chapter 1 – The World of Metrics → Metrics Nuances  
**Last Updated**: 2026-11-02

Metrics for CPU, Memory, Storage, and Network are not just different numbers — they have different natures.

## CPU
- Tends to be about time and scheduling.
- Demand is a meaningful concept.
- High utilization has a relatively clear meaning, but must still be correlated with Ready time and other signals.

## Memory
- Functions largely as a cache.
- Counters often sit near 100%, and that can be expected and desirable.
- 95% memory utilization can be perfectly healthy, while 85% CPU utilization may already be high.
- There is no true equivalent of “VM Memory Demand” in the same way that CPU Demand exists, because memory behaves more like storage space than like a schedulable time resource.

## Storage
- Has two distinct dimensions: **space** and **speed**.
- Speed itself has two components: IOPS and Throughput.
- Throughput depends on block size and is measured in bytes/second (not bits/second).
- Disk throughput focuses on the amount of data moved for the node, unlike network throughput which is more about the link.

## Network
- Primarily concerned with the link / path.
- Different measurement philosophy from storage throughput.

## Key Takeaway

You cannot apply the same mental model or the same threshold philosophy across CPU, Memory, Storage, and Network. Each resource type has its own nature.
