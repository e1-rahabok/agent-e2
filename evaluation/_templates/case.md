---
id: <scope>-<area>-<nnn>          # e.g. vsphere-cpu-004. Never reuse an id.
title: <short title>
scope: vsphere                    # vendor-neutral | vsphere | nsx | vsan
area: cpu                         # foundations | cpu | memory | storage | network | general
input: text                       # text | screenshot | diagram | log | mixed
tests: distinction                # concept | distinction | judgment | troubleshooting
knowledge:                        # knowledge ids the answer should draw on (retrieval check)
  - vsphere/cpu/metrics/virtual-machine/ready
attachments: []                   # paths under evaluation/attachments/<id>/
origin: book                      # book | live-lab | real-ticket | synthetic
source_path: "<heading path in the source document>"
status: draft                     # draft | reviewed
---

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
