# cpu.usage.average (VM perspective)

**Counter**: `cpu.usage.average`  
**Object Type**: VirtualMachine  
**Unit**: percent  
**Rollup**: average  
**Last Updated**: 2026-11-02

## Description
CPU usage of the virtual machine as a percentage of its entitled resources during the interval.

This is **not** the same thing as the host counter with the same name.

## Interpretation Notes
- High values on a VM must be interpreted together with `cpu.ready.summation`.
- A VM can show high usage while still being constrained (high ready time).
- A VM can show moderate usage but still suffer from co-stopping or scheduling delays.

## Related Counters (VM)
- `cpu.ready.summation` (critical)
- `cpu.costop.summation`
- `cpu.overlap.summation`
- `cpu.system.summation`
- `cpu.used.summation`

## Notes
This is the **VirtualMachine** view of the counter.  
The HostSystem version lives in `counters/host/` and measures something different.
