# <short title>

## Prompt
- <Context fact, one per bullet. Exact text sent to the candidate. Must not hint at the answer.>
- <Another fact.>

<The question or instruction, as its own paragraph.>

- A. <Option, one per bullet (multiple choice only).>
- B. <Option.>

## Attachments
<!-- one image link per attachment, with alt text, so a reviewer sees it on GitHub. Delete the section when there are none. Never sent to the model: the runner sends the files themselves. -->

## Likely wrong answer
<The trap a generic AI falls into.>

## Expected key points
- <One point per bullet. Scoring checks these.>

## Reasoning path
<Optional. Order of diagnosis the answer should follow.>

## Notes
- <Optional.>

## Metadata
```yaml
id: question-<nnnn>                    # e.g. question-0031. Never reuse an id.
title: <short title>
scope: vsphere                    # vendor-neutral | vsphere | nsx | vsan
product: [vsphere]                # every product touched: vsphere | vsan | nsx | vcf-operations | windows | linux | kubernetes
technology: [cpu]                 # every area touched: cpu | memory | storage | network | system
pillar: [performance]             # optional: performance | capacity | availability | security | value
area: cpu                         # main area for the report: cpu | memory | storage | network | system | operations-management
input: text                       # text | screenshot | diagram | log | mixed
tests: distinction                # concept | distinction | judgment | troubleshooting
knowledge:                        # knowledge ids the answer should draw on (retrieval check)
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []                   # paths relative to benchmark/questions/, e.g. <id>/<file>.png
origin: book                      # book | quiz | live-lab | real-ticket | synthetic
source_path: "<heading path in the source document>"
format: multiple-choice           # multiple-choice | free-text | compound
level: l400                       # recall | l400 | multi-hop | screenshot (multiple-choice only)
answer: [B]                       # correct letters (multiple-choice only)
trap: [A]                         # trap letters (multiple-choice only)
status: draft                     # draft | reviewed | retired
```
