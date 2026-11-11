# Placement: where a knowledge file goes

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

## Slices
The author's books describe metrics from three perspectives: technology, object, and operations management (pillar). A folder tree holds one; tags and links hold the others.
- Example: VM CPU Ready.
  - Technology: `vsphere/technology/cpu/metrics/virtual-motherboard/ready` (folder), `technology: cpu` (tag).
  - Object: `object: VirtualMachine` (tag), listed in `vsphere/object-types/vm/health-check/vm-health-check` (link), part of the VM Performance KPI.
  - Operations management: `pillar: performance` (tag), used by `sp5-framework/performance/performance-kpi-design` and the cluster KPI (links).
- Retrieval filters on any tag. The model follows any link. A website can show any slice without moving a file.

## The knowledge base folder

```text
knowledge/                           # the domain knowledge Agent E2 uses (see KNOWLEDGE-ENGINEERING.md, section 2)
├── catalog/                         # structured data read by harness tools, not chunked as prose:
│                                    # vCenter counters, esxtop fields, thresholds, object model, user terms (YAML)
├── glossary.md                      # the agent's vocabulary: one entry per term, other names, confusable term (all products)
├── misconceptions.md                # Level 300 wrong beliefs and their corrections; given up front, not indexed
├── sp5-framework/                   # the method: how to operate VCF (the SP5 Framework), with VCF terms and examples
│   ├── concepts/                    # the framework across pillars: overview, why not ITIL, health check, SLAs,
│   │                                # class of service, modelling, monitoring vs troubleshooting
│   ├── observability/               # how to read telemetry: input types, interval, aggregation, units, naming,
│   │                                # accounting, thresholds, Triple See Method
│   ├── outputs/                     # how insight reaches people: alerts, dashboards, reports, NOC live screen
│   ├── performance/                 # performance-management (main file: boundary, processes, KPI map, question map),
│   │                                # KPI design, KPI vs SLA, noisy neighbour; troubleshooting/ for flows across technologies
│   └── capacity/                    # capacity-management (main file: boundary, stages, question map), supply, demand,
│                                    # overcommit, forecasting, planning, sizing, reclamation; decision-tree/ across technologies
├── vsphere/
│   ├── architecture/                # vSphere-wide design that every metric depends on: provider/consumer,
│   │                                # VM vs Guest OS, kernel worlds, overhead, resource controls, metric sources
│   ├── technology/                  # raw metrics, by technology (book route: contention first, then consumption)
│   │   └── cpu/ gpu/ memory/ storage/ network/
│   │       ├── concepts/            # how it works
│   │       ├── metrics/<object>/    # one metric, one object type per file: virtual-motherboard/, host/,
│   │       │                        # cluster/, datastore/; comparisons/ for side-by-side groups
│   │       ├── configuration/       # what to set
│   │       ├── decision-tree/       # operational questions within this technology (headroom, downsizing)
│   │       ├── troubleshooting/     # why flows within this technology
│   │       └── images/
│   ├── object-types/                # multi-technology content, by object (book route)
│   │   └── vm/ esxi/ cluster/ ...   # concepts/, metrics/, configuration/, health-check/, troubleshooting/,
│   │                                # decision-tree/, images/
│   └── tools/                       # how each tool shows the counters
│       ├── esxtop/                  # panels, fields, units vs the vSphere Client
│       └── vsphere-client/          # vCenter statistics (levels, rollups, intervals), documentation guidance;
│                                    # screens/ for the screen library (release 1.1)
├── vcf-operations/                  # the product VCF Operations: what it is, ships and does
│   ├── concepts/                    # what the product is for: its role
│   ├── features/                    # features as implemented (real-time metrics, 20-second peaks)
│   ├── dashboards/                  # dashboards as shipped or as built in the product (VM Performance, business applications)
│   ├── reports/                     # the report suite as built in the product
│   ├── alerts/                      # alert definitions, bottom up: symptoms, conditions, cycles, recommendations
│   └── troubleshooting/             # later: VCF Operations' own health and troubleshooting
└── guest-os/                        # Windows, Linux: a separate layer, not Broadcom products, not part of the VM
    └── <technology>/                # concepts/, metrics/, images/ (scope: guest-os, layer: guest-os)
```

- The author's book sees metrics from 3 perspectives: technology, pillar of operations, product. A folder tree holds one hierarchy; tags (`technology`, `pillar`, `product`, `object`) hold the others, and retrieval and the website browse by any of them.
- Two bodies of knowledge, as an expert consultant carries them (2026-11-11):
  - the method, the SP5 Framework: how to operate VCF. Decide, design, read, present: `sp5-framework/`. Written for VMware administrators, in VCF terms with VCF examples and diagrams. Not a general IT framework.
  - the product, VCF 9.x: what each component is, counts, shows and does: `vsphere/`, `vcf-operations/`; the Guest OS above the VM: `guest-os/`.
  - The test for a file: does it say how to operate (method), or how a component behaves (product)? A file that does both is split, and the two files are linked: the product file lists the method file in `internal_derive`, the method file lists the product file in `related`.
- Inside the product, the folders follow the book's blend:
  - raw metrics follow the technology route: `vsphere/technology/<tech>/`;
  - multi-technology content follows the object route: `vsphere/object-types/<object>/`;
  - what VCF Operations is and ships: `vcf-operations/`.
- Inside the method, one folder per part of the framework: `concepts/` across pillars, `observability/`, `outputs/`, and one folder per pillar (`performance/`, `capacity/`).
- Placement rules, so a fact lives in one place:
  - A raw metric about one technology goes in `technology/`, even when it belongs to one object. VM CPU Ready: `vsphere/technology/cpu/metrics/virtual-motherboard/`.
  - `object-types/` holds what combines technologies for one object: vMotion, DRS, admission control, cluster operations. Each object type gets a health check, and only object types do (`health-check/<object>-health-check`): numbered steps in the order availability, performance, security, capacity, with configuration as the drill-down ([flows.md](flows.md)), starting from the object's KPI and models, each step linking the troubleshooting flow to open when it fails.
  - VCF Operations is an observability tool, not a peer of vSphere, vSAN, NSX or the Guest OS: it has nothing to say without a system to manage. Content about a managed object lives with that object, even when VCF Operations computes it:
    - a derived metric of one technology: `vsphere/technology/<tech>/metrics/<object>/` (VM CPU Contention, VM Disk Space);
    - a KPI or model of one object: `vsphere/object-types/<object>/kpis/` or `models/` (VM Performance, Cluster Risk, Close for Business);
    - how VCF Operations shows a counter (rollup, 20-second peak): `vcf-operations/features/`. VCF Operations is not a vSphere tool: it also monitors vSAN, NSX and the Guest OS. `vsphere/tools/` holds the vSphere tools only: esxtop and the vSphere Client.
  - `vcf-operations/` holds only VCF Operations itself: its role, features (real-time metrics), the dashboards and reports as built in it, alert definitions, and later its own sizing, health and performance troubleshooting. See `vcf-operations/concepts/vcf-operations-role`. How to design a dashboard, report or alert is method: `sp5-framework/outputs/`.
  - A concept is a general idea; a file that documents an actual implementation is not a concept. In `vcf-operations/`, `concepts/` holds only what the product is for; implementations go to `features/`, `dashboards/`, `reports/` or `alerts/`. A topic that is both gets two files: the idea in `sp5-framework/`, the implementation in `vcf-operations/` (example: `sp5-framework/observability/real-time-metrics` and `vcf-operations/features/real-time-metrics`).
  - Alerts have two parts. Top down, the alert architecture (taxonomy, routing, deduplication, escalation, design of the set): `sp5-framework/outputs/`. Bottom up, how one alert definition is built in VCF Operations (symptoms, conditions, wait and cancel cycles, meta tags, recommendations, management packs): `vcf-operations/alerts/`.
  - The `product` tag still names `vcf-operations` on a file whose metric VCF Operations computes.
  - How a tool shows the counters (esxtop panels and fields, vCenter statistics levels and rollups, units per tool) goes in `vsphere/tools/<ui>/`. The metric's meaning stays in its metric file.
  - A KPI, model or health check of one object is the method applied to that object: it stays with the object (`vsphere/object-types/<object>/`) and links to the method file.
  - Flows: one technology → `technology/<tech>/<kind>/`; one object, several technologies → `object-types/<object>/<kind>/`; across products (VM slow) → `sp5-framework/<pillar>/<kind>/`. `<kind>` is `troubleshooting` (the why: down or slow) or `decision-tree` (one operational question). `health-check` lives only with an object type: `object-types/<object>/`, `vcf-operations/` for VCF Operations itself, and later `guest-os/` for the Guest OS as its own object. Never on a technology or a pillar.
- Storage, not disk. Datastores, adapters, paths and vSAN are storage but not disks; a disk is one layer. vCenter keeps separate counter groups per layer (`virtualDisk`, `disk`, `datastore`, `storageAdapter`, `storagePath`), and the same label means a different scope in each. One word for folder, tag and glossary: `storage`.
- vCenter is the administrative tool (create VMs, configure switches). Capacity planning and performance troubleshooting are done in VCF Operations. The knowledge base never uses the two names interchangeably.
- Two levels of general content (names say what the content is, not that it is basic):
  - `knowledge/sp5-framework/`: the method, including how to read telemetry (`observability/`).
  - `knowledge/vsphere/architecture/`: vSphere design that its metrics follow from.
- Scope: VCF only. No competitor products, their behaviour or comparisons with them: out of scope for a machine, and politically sensitive. A VMware offering on a hyperscaler (VMware Cloud on AWS, Azure VMware Solution) is VCF and stays.
- A setting of one object goes to that object: Scalable Shares is in `vsphere/object-types/resource-pool/configuration/`. A pillar problem across technologies goes to its pillar: noisy neighbour is in `sp5-framework/performance/`.
- A top-level folder is never named `metrics`: lint and the harness read `/metrics/` in a path as a metric file.
- `metrics/<object>` folder names: `virtual-motherboard`, `host`, `cluster`, `datastore` under `vsphere/technology/`; the same names wherever a metric of that object lives. The `object` tag holds the vSphere managed object type name.
- A VM is a virtual motherboard, not a complete machine. Its raw metrics live in `metrics/virtual-motherboard/` (`object: VirtualMachine`, `layer: virtual-motherboard`). The folder name is in every file id, so the model reads it with every VM chunk.
- Guest OS knowledge (Windows, Linux) is a separate layer and not a Broadcom product. It lives in `knowledge/guest-os/<technology>/` with `scope: guest-os`, `layer: guest-os` and no VM object, even though VMware Tools stores some counters on the VM object. Boundary files comparing Guest OS and VM stay in `knowledge/vsphere/`. A VCF Operations KPI over Guest OS counters (Guest OS Performance) stays in `guest-os/` by this rule.
- Screen library (release 1.1): one file per screen type, in `vsphere/tools/<ui>/screens/` (vSphere Client, esxtop) or `vcf-operations/<features|dashboards|reports>/screens/` (VCF Operations), with a screenshot, a full text twin, the metrics it shows (`metrics_shown`), UI and version (`ui`, `ui_version`). Template: `project/templates/screen.md`.
- Indexed: every `knowledge/**/*.md` except `knowledge/misconceptions.md` (given up front); the catalog is loaded, not chunked. Writing templates live in `project/templates/`; source documents in `project/sources/` (read-only). How files are ingested: `ARCHITECTURE.md`, section Local LLM use.
- `project/tools/lint.py` enforces the folder and tag rules.
