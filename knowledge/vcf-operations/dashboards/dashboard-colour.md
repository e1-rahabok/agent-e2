# Colour and thresholds in dashboards

## Colour carries meaning
- Colour is read faster than numbers when it has a meaning. Operations often only need good or bad before the raw value, and colour scales across hundreds of numbers in a large table.
- Colour sets in the recommended dashboards:
  - Green, yellow, orange, red: green is good and gets worse towards red. Performance and compliance.
  - Dark grey, then green to red: capacity. Dark grey is wastage (unused), which is a bigger issue than over-utilization and can also hurt performance. In a performance dashboard, consider red for oversized, since oversizing hurts performance.
  - Blue: neutral, where the value has no good or bad.
  - Grey: system error, the data is missing because collection failed. Mostly in heat maps; grey, not white, because white is hard to read.
- Provide another cue for users who cannot tell all colours apart, so they keep the function.
- If a whole dashboard is green, there is no need to read the numbers. Example: a compliance dashboard.

## Where colours change
- Use one consistent scale so it is easy to remember:
  - yellow = 2x green;
  - orange = 2x yellow;
  - red = 2x orange, so red is 8x green.
- The scale fails when the range is small. Example: a Horizon user has 1-4 desktops and rarely more, so the bounds are yellow 2, orange 3, red 4.
- Colour thresholds per channel can differ; see `vcf-operations/concepts/system-engagement`. KPI bands: `knowledge/catalog/thresholds-performance.yaml`.

## Gradient
- A gradient suits widgets where the relative comparison among many objects matters.
- Example: a heat map of vSAN disk group utilization, to judge imbalance. With a plain gradient, small differences show as different colours and suggest rebalancing, which can move terabytes.
- Two fixes:
  - minor imbalance is expected; identical values would be strange. Colour only a significant imbalance;
  - utilization turns red only at 75%.
- After both fixes the heat map shows only what matters.

## Traps
- "Different colours mean imbalance" → a gradient colours any difference; minor imbalance is normal. Set the scale so only significant gaps show.
- "Low utilization is green" → in capacity, low utilization is wastage (dark grey), and can point to a bottleneck elsewhere.
- "White for missing data" → white is hard to read; grey means collection error.
- "Use the 2x scale everywhere" → small ranges, such as desktops per user, need explicit bounds.
- "Colour alone is enough" → give colour-blind users another cue.

## Metadata
```yaml
id: vcf-operations/dashboards/dashboard-colour
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- performance
- capacity
- compliance
product:
- vcf-operations
- vsan
internal_derive:
- vcf-operations/dashboards/dashboard-design
related:
- observability/thresholds
- sp5-framework/capacity/capacity-model
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Overall Design Approach > Design Consideration > Color as Meaning (Threshold, Gradient, Example Implementation) (pp. 31-33)'
corrections: []
review_notes:
- 'Section ''Where colours change'': the Horizon bounds (yellow 2, orange 3, red 4) are read from the source screenshot of the widget colour settings (coloring: above).'
- 'Section ''Gradient'': vSAN disk groups exist in the vSAN Original Storage Architecture; vSAN ESA uses a storage pool per host (Claude''s knowledge). The point about gradients holds either way.'
- 'Section ''Where colours change'': the 2x per colour scale differs from the alert scale in sp5-framework/alerts/alert-design (red worse than orange by threshold, population or time). Q140.'
- 'Not copied: the gradient heat maps and the compliance dashboard screenshot.'
status: draft
```
