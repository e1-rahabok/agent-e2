# cpu.usage.average (Host perspective)

**Counter**: `cpu.usage.average`  
**Object Type**: HostSystem  
**Unit**: percent  
**Rollup**: average  
**Last Updated**: 2026-11-02

## Description
Average CPU utilization across all physical cores on the host during the interval.

This counter reflects how busy the physical CPUs of the ESXi host are.

## Interpretation Notes
- Sustained values above ~80-85% indicate the host is under significant CPU pressure.
- Near 100% sustained usually means the host is CPU constrained.
- Always correlate with CPU Ready time of the VMs running on the host and with `cpu.coreUtilization.average`.

## Related Counters (Host)
- `cpu.coreUtilization.average`
- `cpu.utilization.average`
- `cpu.usagemhz.average`
- `cpu.ready.summation` (look at the VMs)

## Notes
This is the **Host** view of the counter.  
The VirtualMachine version of `cpu.usage.average` has a different meaning and lives in `counters/vm/`.
