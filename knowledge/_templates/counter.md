---
id: vsphere/<resource>/counters/<object>/<slug>   # one object per file
type: counter
scope: vsphere
resources: [cpu]
object: vm                        # exactly one: guest-os | vcpu | vm | esxi | cluster | datastore | ...
data_source: esxi                 # esxi | vcenter | vcf-operations | guest-os
names:
  book: <name used in the book>
  vcenter_ui: <label in vSphere Client>
  vcenter_api: <group.counter.rollup>
  esxtop: <column>
  vcf_operations: <metric key>
unit: <ms | % | MHz | KB | ...>
rollup: <average | summation | latest | maximum | minimum>
kind: consumer                    # consumer | provider | sum-of-consumers
derived_from: []                  # concept ids this counter follows from
same_name_as: []                  # ids of the same counter on other objects
related: []
source:
  document: PART 3 - Counters.docx
  path: <heading path>
corrections: []
review_notes: []
status: draft
---

# <Object> <Counter name>

## Definition
- What it measures, from this object's vantage point.

## Formula
```text
<plain-text formula>
```

## Includes / excludes
- includes:
- excludes:

## Mechanism
- Why the value behaves this way.

## Differs from same name on other objects
- <object>: <difference> — see <id>.

## Interpretation
- What a high or low value means. Conditions. No universal thresholds unless the source gives one.

## Traps
- Wrong conclusion → correct conclusion.
