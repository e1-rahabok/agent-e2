# <Concept name>

## Definition
- One fact per bullet.

## Mechanism
- How it works. Why metrics behave this way.

## Formula
```text
<plain-text formula, if any>
```

## Traps
- Wrong conclusion → correct conclusion, with the reason.

## Metadata
```yaml
id: vsphere/technology/<technology>/concepts/<slug>     # path without knowledge/ and .md
retriever_guide: how-it-works                # see KNOWLEDGE-ENGINEERING.md, retriever_guide: how-it-works | metric-meaning | term-meaning | what-to-set | health-check | troubleshooting
scope: vsphere                               # vendor-neutral | vsphere
technology: [cpu]                            # cpu | memory | storage | network | system
pillar: [performance]                        # availability | performance | compliance | capacity | value
product: [vsphere]                           # vsphere | vsan | nsx | vcf-operations | windows | linux | kubernetes
object: [VirtualMachine, HostSystem]         # vSphere managed object types; omit if none
internal_derive: []                          # ids of other knowledge-base files this file is derived from (internal links only)
related: []                                  # ids to retrieve together
images:  # one entry per image linked in the body; omit when none
  - path: ../../images/<name>.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['<metric name>']   # and/or topic: '<concept>'
    image_type: timeline         # diagram, table, timeline, distribution, scatter, screenshot
    sample: '<optional: fleet size and period>'
source:
  document: <document name, version, revision>
  path: <heading path and pages>
corrections: []                              # author facts not yet in the uploaded source; name the section
review_notes: []                             # open questions, source URLs, Claude-knowledge facts with section names
status: draft                                # draft | reviewed
```
