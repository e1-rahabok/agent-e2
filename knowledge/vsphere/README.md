# vSphere Knowledge

This knowledge base prioritizes **depth of understanding** over quick lookup.

## Structure

### 1. Foundations (cross-cutting)
Deep mental models that apply across all resource areas:

- `metrics-philosophy/` — Nature of metrics, naming complexity, industry-wide nuances
- `vm-vs-guest-os/` — Virtual motherboard vs Guest OS
- `overhead-and-buffers/` — What is real overhead, types of buffers
- `observability-principles/`

### 2. Resource Areas
Each major resource follows the same pattern:

```text
cpu/
├── architecture/           # How it actually works
├── resource-management/  # Mechanisms and rules
├── counters/
│   ├── host/             # HostSystem perspective
│   └── vm/               # VirtualMachine perspective
└── interpretation/       # How to use the knowledge in practice
```

The same structure applies to `memory/`, `storage/`, and `network/`.

## Key Principle

**Never mix Host and VM perspectives** in the same counter file.
