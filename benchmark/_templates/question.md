# <short title>

## Prompt
- <Context fact, one per bullet. Exact text sent to the candidate. Must not hint at the answer. Public vocabulary only (benchmark/design.md, section 6.1).>
- <A reference to an attachment links to it: [the attached chart export](<id>/<file>.csv). The model reads only the words.>

<The question or instruction, as its own paragraph.>

- A. <Option, one per bullet (multiple choice only).>
- B. <Option.>

## Likely wrong answer
<The Level 300 misconception a generic AI holds.>

## Expected key points
- <One point per bullet. Scoring checks these.>

## Reasoning path
<Optional. Order of checks the answer should follow.>

## Notes
- <Optional.>

## Metadata
```yaml
id: "<nnnn>"                     # never reused; tag meanings and values: benchmark/README.md, section Question fields
title: <short title>
product: [vsphere]                # vsphere | vsan | nsx | vcf-operations | windows | linux | kubernetes
technology: [cpu]                 # cpu | memory | storage | network | system
task: read-metric                 # read-metric | troubleshoot | decide-capacity | explain-mechanism | judge-setting
level: 400                        # 100 | 200 | 300 | 400
answer_type: deterministic        # every question is multiple choice (Q199)
input: [text]                     # text | table | screenshot; from the attachments
object: [vm]                      # vm | esxi | cluster | resource-pool | datastore | network | guest-os
tool: [vcenter]                   # vcenter | vcf-operations | esxtop | guest-os-tools | none
knowledge:                        # knowledge ids the answer depends on
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready   # the file that holds the answer or the misconception; also in knowledge
attachments: []                   # paths relative to benchmark/questions/, e.g. <id>/<file>.png
origin: book                      # book | quiz | real-ticket | synthetic
source_path: "<heading path in the source document>"
answer: [B]                       # deterministic only
misconception: [A]                # deterministic only
misconception_type: [layer-confusion]   # project/tools/tags.yaml, misconception_type
pair: "<nnnn>"                    # optional: the paired question (benchmark/design.md, section 3.9); delete if none
status: draft                     # draft | awaiting-input | reviewed | deferred | retired
```
