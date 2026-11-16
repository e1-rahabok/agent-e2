# Which counter to size VM CPU

## Prompt
- The owner of a VM asks for more vCPUs. You size the vCPU count the guest needs, not the VM's cost on the host.

Which of these counters are better inputs for the vCPU count the guest needs than the others listed?

- A. VM CPU Usage (MHz), from vCenter
- B. VM CPU Used (ms), from vCenter
- C. VM CPU Demand (MHz), from vCenter
- D. VM CPU Demand (%), from VCF Operations
- E. CPU Net Run (%), from VCF Operations

## Likely wrong answer
C or D: Demand read as the CPU the guest asks for, unmet demand included. Or A: Usage read as the work the guest needs.

## Expected key points
- Answer: E.
- A is wrong: Usage counts cycles. Turbo, power saving and Hyper-Threading move it, and it carries load charged at VM level; the guest sees none of these.
- B is wrong: VM Used includes System and the VMX, MKS and helper worlds, hypervisor overhead that is not guest demand, and it is scaled by frequency and Hyper-Threading.
- C is wrong: Demand is an internal counter of the kernel scheduler, and like Usage it moves with frequency and Hyper-Threading.
- D is wrong: the same counter as C, in %.
- E is correct: the best of the list. Net Run is Run minus Overlap: run time, blind to frequency and Hyper-Threading. It still leaves out Ready, Co-stop and the non-idle waits the guest demanded; the fuller Guest OS formula is configured vCPU - Idle + a run queue factor (no single counter; build it as a super metric).

## Notes
- Author (Q186, 2026-11-12): "VM sizing" in an administrator's words almost always means Guest OS sizing. Agent E2 names that reading (term map row vm-sizing).
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "A correctly sized VM balances performance, capacity and cost."
- Changed in the 2026-11-15 audit: the stem names the job (the owner asks for more vCPUs: Guest OS sizing, not VM footprint, where Usage or Demand can be right) and asks for a comparison with the others listed (no singular superlative, no absolute "suit": Net Run leaves out Ready and Co-stop). B (VM CPU Usage (%), the same truth as A) replaced by VM CPU Used (ms) (guest-os-sizing, CPU: exclude, Hypervisor overhead); E no longer carries an explanation sentence. Kept as text: the evidence form is the practical partner 0371.
- Open in the knowledge base: net-run and run remove Overlap from the sizing input, overlap and guest-os-sizing keep it inside Run. E stays the best of the list either way (Run is not an option).

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
  - guest-os/system/guest-os-sizing
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
