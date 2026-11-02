# The Interpretation Challenge

**Source**: Chapter 1 – The World of Metrics → Metrics Nuances  
**Last Updated**: 2026-11-02

## Core Difficulty

At the end of the day, what matters is the **interpretation** of the value. What is considered good?

The honest answer is: **it depends**.

- Different applications have different tolerances.
- The same software can have different tolerances depending on the use case.
- Even with identical use cases, different end users can have different tolerances.

This makes universal, out-of-the-box thresholds very difficult to set well.

- Set too low → constant false alarms (red when there is no real complaint)
- Set too high → real problems are missed

## Example: Disk Latency

Microsoft guidance for SQL Server often cites 10–15 ms.  
However:

- That number is at the SQL Server layer.
- At the Windows layer the value needs to be lower (to account for stack processing and queuing).
- At the vSphere VM layer it needs to be even lower.

This raises practical questions:

- What threshold should be used at the VM level?
- Should read and write latency be treated differently?

There is no simple universal answer.
