# Which counter to size VM CPU

## Prompt
- The context is sizing, not performance troubleshooting.

Which counters from the list are the most accurate?

- A. VM CPU Usage (MHz)
- B. VM CPU Usage (%)
- C. VM CPU Demand (MHz)
- D. VM CPU Demand (%)
- E. VM CPU Run - Overlap. In VCF Operations this is CPU Net Run (%).

## Likely wrong answer
C or D (Demand), because it includes unmet demand; or A/B (Usage).

## Expected key points
- Answer: E.
- A and B are wrong: you size the Guest OS, not the VM's virtual hardware. Frequency-based metrics measure throughput.
- C and D are wrong: Demand is an internal counter the kernel uses for scheduling decisions. It does not apply to the Guest OS.
- More accurate: configured vCPU - Idle + a CPU Run Queue factor. No such counter exists; build it as a super metric.

## Notes
- Author (Q186, 2026-11-12): "VM sizing" in an administrator's words almost always means Guest OS sizing. Agent E2 names that reading (term map row vm-sizing). The hint was removed. Claude Haiku 5.5 picked C (Demand) on this prompt.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "A correctly sized VM balances performance, capacity and cost."
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Choose the most accurate counter from the list."

## Metadata
```yaml
id: "0008"
title: "Which counter to size VM CPU"
product: [vsphere, windows]
technology: [cpu]
input: [text]
task: decide-capacity
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/concepts/guest-os-sizing
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/net-run
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q5 VM CPU Rightsize"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [E]
misconception: [C,D]
misconception_type: [frequency-and-hyper-threading]
pair: "0371"
status: draft
```
