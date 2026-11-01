# Performance Counter: cpu.usage.average

**Counter**: `cpu.usage.average`  
**Group**: cpu  
**Rollup**: average  
**Unit**: percent  
**Applies to**: HostSystem, VirtualMachine, ResourcePool, ClusterComputeResource  
**Last Updated**: 2026-11-01  

## Description
CPU usage as a percentage during the interval.  
This is one of the most commonly monitored counters for both hosts and virtual machines.

- On a **Host**: Average CPU utilization across all physical cores.
- On a **VM**: CPU usage of that virtual machine in relation to its entitled resources.

## How to Interpret
- **Host**:  
  - Sustained values above 80-85% often indicate the host is under significant CPU pressure.  
  - Values consistently near 100% usually mean the host is CPU constrained.

- **Virtual Machine**:  
  - High values can mean the VM needs more CPU resources or is ready-time constrained.  
  - Always look at this together with `cpu.ready.summation`.

## Useful Thresholds (practical)
| Level     | Host                          | Virtual Machine                  |
|-----------|-------------------------------|----------------------------------|
| Healthy   | < 70%                         | Depends on workload              |
| Warning   | 80–90% sustained              | High + rising ready time         |
| Critical  | > 90–95% sustained            | High usage + high ready time     |

## Related Counters
- `cpu.ready.summation` (very important)
- `cpu.usage.maximum`
- `cpu.usagemhz.average`
- `cpu.coreUtilization.average`
- `cpu.utilization.average`

## Related Properties
- `summary.quickStats.overallCpuUsage`
- `runtime.maxCpuUsage`
- `config.hardware.numCPU`

## Related Alarms
- Host CPU Usage alarms
- Virtual Machine CPU Usage alarms

## Notes
- `cpu.usage.average` alone is not enough. Always correlate with **CPU Ready** time when troubleshooting VM performance.
- In hyper-threaded environments the interpretation can be slightly different — still treat sustained high values as a signal to investigate further.
- This counter is available in real-time and historical performance charts in vCenter.
