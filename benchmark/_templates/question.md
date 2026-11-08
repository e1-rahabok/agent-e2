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
<Optional. Order of checks the answer should follow.>

## Notes
- <Optional.>

## Metadata
```yaml
id: question-<nnnn>               # never reused; tag meanings and values: benchmark/README.md, section Question fields
title: <short title>
product: [vsphere]                # vsphere | vsan | nsx | vcf-operations | windows | linux | kubernetes
technology: [cpu]                 # cpu | memory | storage | network | system
task: read-metric                 # read-metric | troubleshoot | decide-capacity | explain-mechanism | judge-setting
level: 400                        # 100 | 200 | 300 | 400
answer_type: deterministic        # deterministic | judged
input: [text]                     # text | table | screenshot; from the attachments
knowledge:                        # knowledge ids the answer depends on
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []                   # paths relative to benchmark/questions/, e.g. <id>/<file>.png
origin: book                      # book | quiz | real-ticket | synthetic
source_path: "<heading path in the source document>"
answer: [B]                       # deterministic only
trap: [A]                         # deterministic only
status: draft                     # draft | reviewed | retired
```
