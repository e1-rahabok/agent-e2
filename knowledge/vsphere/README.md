# vSphere Knowledge

This folder contains structured knowledge for the **vSphere** domain.

The organization follows normal vSphere concepts so that experienced administrators can navigate it easily.

## Folders

| Folder | What belongs here |
|--------|-------------------|
| `object-types/` | Managed Object types (VirtualMachine, HostSystem, ClusterComputeResource, Datastore, etc.) |
| `properties/` | Important properties of managed objects |
| `performance-counters/` | Performance counters (cpu.usage.average, mem.active.average, etc.) |
| `alarms/` | Alarm definitions and what they mean |
| `logs/` | Important log messages and signatures from hostd, vpxa, vpxd, ESXi, etc. |
| `faults/` | Faults, error codes, and common failure signatures |
| `advanced-settings/` | Advanced options / settings |
| `troubleshooting/` | Decision trees and step-by-step troubleshooting flows |
| `glossary/` | Precise definitions of terms |

## Guidelines

- One major topic per file
- Prefer clear, descriptive filenames
- Use the templates in `../_templates/`
- Write for other experienced vSphere admins
