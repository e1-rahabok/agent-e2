# <UI> <screen name> (<version>)

<!-- Screen library file, for screenshot upload (release 1.1). One file per screen type.
Location: knowledge/vsphere/tools/<ui>/screens/<slug>.md for vSphere Client and esxtop;
knowledge/vcf-operations/<features|dashboards|reports>/screens/<slug>.md for VCF Operations. The image goes in the images/ folder next to it. -->

![<what the screen shows>](images/<ui>-<screen>-<version>.png)

## Text twin
- Every label, column and control on the screen, in reading order, so a text-only model loses nothing.

## How to recognize it
- Visual cues that tell this screen apart from similar ones: title, tabs, column headers, chart legend.

## What each element shows
| Element | Metric or property | Source file |
|---|---|---|
| <chart line or column> | <metric name, unit, rollup> | `<knowledge id>` |

## Interval and rollup
- Default time range, data interval and rollup. What peaks this view hides.

## Reading it
- Healthy pattern vs problem pattern, with the knowledge files that explain why.

## Misconceptions
- Misconceptions this screen invites → correct reading.

## Metadata
```yaml
id: vsphere/tools/<ui>/screens/<slug>
retriever_guide: how-it-works
scope: vsphere                     # vcf-operations for VCF Operations screens
technology: [cpu]
pillar: [performance]
product: [vsphere]
object: [VirtualMachine]           # object the screen is about
ui: vsphere-client                 # vsphere-client | esxtop | vcf-operations
ui_version: '9.1'
metrics_shown: []                  # knowledge ids of the metric files for every metric on the screen
internal_derive: []
related: []
images:
  - path: images/<ui>-<screen>-<version>.png
    product: [vsphere]
    object: [VirtualMachine]
    topic: '<screen name>'
    image_type: screenshot
source:
  document: <product and version the screenshot was taken from>
  path: <menu path to the screen>
corrections: []
review_notes: []
status: draft
```
