# vSphere Knowledge

This knowledge base is organized for **depth of understanding**, not just quick lookup.

## Structure by Resource Area

Each major resource area follows the same pattern:

```text
cpu/
├── architecture/           # How it actually works
├── resource-management/  # Mechanisms and rules
├── counters/
│   ├── host/             # HostSystem perspective
│   └── vm/               # VirtualMachine perspective
└── interpretation/       # How to use the knowledge in practice
```

The same structure applies to `memory/`, `storage/`, `network/`, etc.

## Key Principle

**Never mix Host and VM perspectives** in the same counter file.  
Even when the counter name is identical, the meaning changes.

## Other folders

- `troubleshooting/` — Cross-cutting troubleshooting flows
- `glossary/` — Precise definitions of terms
