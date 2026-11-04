# <short title>

## Prompt
<Exact text sent to the AI. Scenario first, question last. Must not hint at the answer.>

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
id: <scope>-<area>-<nnn>          # e.g. vsphere-cpu-004. Never reuse an id.
title: <short title>
scope: vsphere                    # vendor-neutral | vsphere | nsx | vsan
area: cpu                         # foundations | cpu | memory | storage | network | general
input: text                       # text | screenshot | diagram | log | mixed
tests: distinction                # concept | distinction | judgment | troubleshooting
knowledge:                        # knowledge ids the answer should draw on (retrieval check)
  - vsphere/cpu/metrics/virtual-motherboard/ready
attachments: []                   # paths under benchmark/attachments/<id>/
origin: book                      # book | quiz | live-lab | real-ticket | synthetic
source_path: "<heading path in the source document>"
format: multiple-choice           # multiple-choice | free-text | compound
level: l400                       # recall | l400 | multi-hop | screenshot (multiple-choice only)
answer: [B]                       # correct letters (multiple-choice only)
trap: [A]                         # trap letters (multiple-choice only)
status: draft                     # draft | reviewed
```
