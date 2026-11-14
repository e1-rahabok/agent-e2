# Placement: where a knowledge file goes

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

## Slices
The author's books describe metrics from three perspectives: technology, object, and operations management (pillar). A folder tree holds one; tags and links hold the others.
- Example: VM CPU Ready.
  - Technology: [`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md) (folder), `technology: cpu` (tag).
  - Object: `object: VirtualMachine` (tag), listed in [`vsphere/object-types/vm/vm-health-check`](../../knowledge/vsphere/object-types/vm/vm-health-check.md) (link), part of the VM Performance KPI.
  - Operations management: `pillar: performance` (tag), used by [`sp5-framework/performance/performance-kpi-design`](../../knowledge/sp5-framework/performance/performance-kpi-design.md) and the cluster KPI (links).
- Retrieval filters on any tag. The model follows any link. A website can show any slice without moving a file.

## The knowledge base folder

```text
knowledge/                           # the domain knowledge Agent E2 uses (see KNOWLEDGE-ENGINEERING.md, section 2)
├── catalog/                         # structured data read by harness tools, not chunked as prose:
│                                    # vCenter counters, esxtop fields, thresholds, object model, user terms (YAML)
├── glossary.md                      # the agent's vocabulary: one entry per term, other names, confusable term (all products)
├── sp5-framework/                   # the method: how to operate VCF (the SP5 Framework), with VCF terms and examples
│   ├── concepts/                    # the framework across pillars: overview, why not ITIL, health check, SLAs,
│   │                                # class of service, modelling, monitoring vs troubleshooting
│   ├── observability/               # how to read telemetry: input types, interval, aggregation, units, naming,
│   │                                # accounting, thresholds, Triple See Method
│   ├── outputs/                     # how insight reaches people: alerts, dashboards, reports, NOC live screen
│   ├── performance/                 # performance-management (main file: boundary, processes, KPI map, question map),
│   │                                # KPI design, KPI vs SLA, noisy neighbour, vm-slow (the flow across technologies)
│   └── capacity/                    # capacity-management (main file: boundary, stages, question map), supply, demand,
│                                    # overcommit, forecasting, planning, sizing, reclamation; decision-tree/ across technologies
├── vsphere/
│   ├── architecture/                # vSphere-wide design that every metric depends on: provider/consumer,
│   │                                # VM vs Guest OS, kernel worlds, overhead, resource controls, metric sources
│   ├── technology/                  # raw metrics, by technology (book route: contention first, then consumption)
│   │   └── cpu/ gpu/ memory/ storage/ network/   # the kind folders below exist from 2 files; one file sits here
│   │       ├── concepts/            # how it works
│   │       ├── metrics/<object>/    # one metric, one object type per file: virtual-motherboard/, host/,
│   │       │                        # cluster/, datastore/; comparisons/ for side-by-side groups
│   │       ├── configuration/       # what to set
│   │       ├── decision-tree/       # operational questions within this technology (headroom, downsizing)
│   │       ├── troubleshooting/     # why flows within this technology
│   │       └── images/
│   ├── object-types/                # multi-technology content, by object (book route); one folder per object type
│   │   └── vm/ esxi/ cluster/ ...   # <object>-alerts, <object>-health-check, <object>-performance (KPI) directly in
│   │                                # the object folder; concepts/, metrics/, configuration/, models/, troubleshooting/,
│   │                                # decision-tree/ once they hold 2 or more files; images/
│   └── tools/                       # how each tool shows the counters
│       ├── esxtop/                  # panels, fields, units vs the vSphere Client
│       └── vsphere-client/          # vCenter statistics (levels, rollups, intervals), documentation guidance;
│                                    # screens/ for the screen library (release 1.1)
├── vcf-operations/                  # the product VCF Operations: what it is, ships and does
│   ├── vcf-operations-role          # what the product is for
│   ├── alert-definitions            # how VCF Operations builds an alert definition: symptoms, conditions, cycles
│   ├── report-suite                 # the report suite as built in the product
│   ├── features/                    # features as implemented (real-time metrics, 20-second peaks)
│   └── dashboards/                  # dashboards as shipped or as built in the product (VM Performance, business applications)
└── guest-os/                        # Windows, Linux: a separate layer, not Broadcom products, not part of the VM
    ├── guest-os-alerts              # the Guest OS alert set: the Guest OS is the object
    └── <technology>/                # cpu/ memory/ storage/ system/ (scope: guest-os, layer: guest-os); kind folders
                                     # from 2 files, images/
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
- Folders group files. Two kinds of folder (2026-11-12):
  - slice folders name a part of the knowledge the id must carry: an area (`sp5-framework`, `vsphere`, `vcf-operations`, `guest-os`), a pillar or part of the method, a technology, an object type, and `metrics/<object>/` (`virtual-motherboard`, `host`, `cluster`, `datastore`, `distributed-switch`). They stay even with one file: `vsphere/object-types/datastore/` holds only datastore-alerts today;
  - kind folders name a kind of file (`concepts`, `metrics`, `configuration`, `health-check`, `troubleshooting`, `decision-tree`, `kpis`, `models`, `comparisons`, `alerts`, `features`, `dashboards`, `reports`, `screens`). A kind folder exists only with 2 or more files; one file sits in the parent folder. When a second file of the kind arrives, both move into the new folder and moved.yaml records it. Lint checks it.
  - The kind of a file is its `retriever_guide`, not its folder. The harness (reading plan, flow executor, catalog, search filters) and lint read the metadata; the file name carries the kind for a reader (`vm-health-check`, `vm-alerts`, `vm-performance`).
- Inside the method, one folder per part of the framework: `concepts/` across pillars, `observability/`, `outputs/`, and one folder per pillar (`performance/`, `capacity/`).
- Placement rules, so a fact lives in one place:
  - A raw metric about one technology goes in `technology/`, even when it belongs to one object. VM CPU Ready: `vsphere/technology/cpu/metrics/virtual-motherboard/`.
  - `object-types/` holds what combines technologies for one object: vMotion, DRS, admission control, cluster operations. Each object type gets a health check, and only object types do (`<object>-health-check`, `retriever_guide: health-check`): numbered steps in the order availability, performance, security, capacity, with configuration as the drill-down ([flows.md](flows.md)), starting from the object's KPI and models, each step linking the troubleshooting flow to open when it fails.
  - VCF Operations is an observability tool, not a peer of vSphere, vSAN, NSX or the Guest OS: it has nothing to say without a system to manage. Content about a managed object lives with that object, even when VCF Operations computes it:
    - a derived metric of one technology: `vsphere/technology/<tech>/metrics/<object>/` (VM CPU Contention, VM Disk Space);
    - a KPI or model of one object: `vsphere/object-types/<object>/` (VM Performance as `vm/vm-performance`; Cluster Risk and Close for Business in `cluster/models/`);
    - how VCF Operations shows a counter (rollup, 20-second peak): `vcf-operations/features/`. VCF Operations is not a vSphere tool: it also monitors vSAN, NSX and the Guest OS. `vsphere/tools/` holds the vSphere tools only: esxtop and the vSphere Client.
  - `vcf-operations/` holds only VCF Operations itself: its role, features (real-time metrics), the dashboards and reports as built in it, how an alert definition works, and later its own sizing, health and performance troubleshooting. See [`vcf-operations/vcf-operations-role`](../../knowledge/vcf-operations/vcf-operations-role.md). How to design a dashboard, report or alert is method: `sp5-framework/outputs/`.
  - A concept is a general idea; a file that documents an actual implementation is not a concept. In `vcf-operations/`, only the role file says what the product is for; implementations are features, dashboards, reports and alert definitions. A topic that is both gets two files: the idea in `sp5-framework/`, the implementation in `vcf-operations/` (example: [`sp5-framework/observability/real-time-metrics`](../../knowledge/sp5-framework/observability/real-time-metrics.md) and [`vcf-operations/features/real-time-metrics`](../../knowledge/vcf-operations/features/real-time-metrics.md)).
  - Alerts have three parts, and each fact lives in one (2026-11-12):
    - the method, top down: what an alert is, how to design the set, personas, threshold design (`sp5-framework/outputs/`);
    - the recommended set, one file per object type in VCF Operations, because an alert fires on one object type, not on a technology: `vsphere/object-types/<object>/<object>-alerts`, and [`guest-os/guest-os-alerts`](../../knowledge/guest-os/guest-os-alerts.md) for the Guest OS. Each alert is a `##` section under its catalog name: what it detects, why each symptom is in it, who receives it, which flow to open. A section per resource left out says why. No values: thresholds, populations and waits live only in `catalog/thresholds-alerts.yaml`, whose rows point to the file (`kb`) and come with it into the context. An object type with no alert in the set still gets its file, which says why (datastore cluster, distributed switch);
    - the product, bottom up: how VCF Operations builds and evaluates an alert definition (symptoms, conditions, wait and cancel cycles, meta tags, recommendations, management packs), and after 1.0 the alerts it ships: `vcf-operations/`.
    - Never a `*-alerts` file under `technology/`: lint rejects it. The technology view (which alerts test VM CPU Ready) is a catalog query: each symptom's `kb` is its metric file.
  - The `product` tag still names `vcf-operations` on a file whose metric VCF Operations computes.
  - How a tool shows the counters (esxtop panels and fields, vCenter statistics levels and rollups, units per tool) goes in `vsphere/tools/<ui>/`. The metric's meaning stays in its metric file.
  - A KPI, model, alert set or health check of one object is the method applied to that object: it stays with the object (`vsphere/object-types/<object>/`) and links to the method file. This is not object-first folders (declined 2026-11-04 and 2026-11-06): metrics stay by technology.
  - Flows: one technology → `technology/<tech>/`; one object, several technologies → `object-types/<object>/`; across products (VM slow) → `sp5-framework/<pillar>/`; each in a `troubleshooting/` or `decision-tree/` folder once there are 2. The kind is `retriever_guide`: `troubleshooting` (the why: down or slow) or `decision-tree` (one operational question). A health check lives only with an object type: `object-types/<object>/<object>-health-check`, `vcf-operations/` for VCF Operations itself, and later `guest-os/` for the Guest OS as its own object. Never on a technology or a pillar.
- Storage, not disk. Datastores, adapters, paths and vSAN are storage but not disks; a disk is one layer. vCenter keeps separate counter groups per layer (`virtualDisk`, `disk`, `datastore`, `storageAdapter`, `storagePath`), and the same label means a different scope in each. One word for folder, tag and glossary: `storage`.
- vCenter is the administrative tool (create VMs, configure switches). Capacity planning and performance troubleshooting are done in VCF Operations. The knowledge base never uses the two names interchangeably.
- Two levels of general content (names say what the content is, not that it is basic):
  - [`knowledge/sp5-framework/`](../../knowledge/sp5-framework): the method, including how to read telemetry (`observability/`).
  - [`knowledge/vsphere/architecture/`](../../knowledge/vsphere/architecture): vSphere design that its metrics follow from.
- Scope: VCF only. No competitor products, their behaviour or comparisons with them: out of scope for a machine, and politically sensitive. A VMware offering on a hyperscaler (VMware Cloud on AWS, Azure VMware Solution) is VCF and stays.
- A setting of one object goes to that object: Scalable Shares is in [`vsphere/object-types/resource-pool/resource-pool-design`](../../knowledge/vsphere/object-types/resource-pool/resource-pool-design.md). A pillar problem across technologies goes to its pillar: noisy neighbour is in `sp5-framework/performance/`.
- A pillar folder's main file is [`README.md`](../../README.md), so GitHub opens it with the folder. Its `id` keeps a descriptive name (`sp5-framework/capacity/capacity-management`): the id, not the file name, is what the model reads and links use. Lint checks it.
- A top-level folder is never named `metrics`: lint requires `retriever_guide: metric-meaning` of every file under a `metrics/` folder.
- `metrics/<object>` folder names: `virtual-motherboard`, `host`, `cluster`, `datastore` under `vsphere/technology/`; the same names wherever a metric of that object lives. The `object` tag holds the vSphere managed object type name.
- A VM is a virtual motherboard, not a complete machine. Its raw metrics live in `metrics/virtual-motherboard/` (`object: VirtualMachine`, `layer: virtual-motherboard`). The folder name is in every file id, so the model reads it with every VM chunk.
- Guest OS knowledge (Windows, Linux) is a separate layer and not a Broadcom product. It lives in `knowledge/guest-os/<technology>/` with `scope: guest-os`, `layer: guest-os` and no VM object, even though VMware Tools stores some counters on the VM object. Boundary files comparing Guest OS and VM stay in [`knowledge/vsphere/`](../../knowledge/vsphere). A VCF Operations KPI over Guest OS counters (Guest OS Performance) stays in `guest-os/` by this rule.
- Screen library (release 1.1): one file per screen type, in `vsphere/tools/<ui>/screens/` (vSphere Client, esxtop) or `vcf-operations/<features|dashboards|reports>/screens/` (VCF Operations), with a screenshot, a full text twin, the metrics it shows (`metrics_shown`), UI and version (`ui`, `ui_version`). Template: [`project/templates/screen.md`](../templates/screen.md).
- Indexed: every `knowledge/**/*.md`; the catalog is loaded, not chunked. Writing templates live in [`project/templates/`](../templates); source documents in [`project/sources/`](../sources) (read-only). How files are ingested: [`ARCHITECTURE.md`](../../ARCHITECTURE.md), section Local LLM use.
- [`project/tools/lint.py`](../tools/lint.py) enforces the folder and tag rules.
