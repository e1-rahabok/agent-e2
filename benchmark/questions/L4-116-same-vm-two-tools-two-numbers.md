# The same VM in two tools, two numbers

## Prompt
- app-07, 8 vCPUs, yesterday between 14:00 and 14:30. The owner reported slowness around 14:15.
- vSphere Client, 1 Week chart, CPU Usage, the 30-minute point at 14:00: 58%.
- VCF Operations, CPU Usage (%) for the same VM, the six 5-minute points from 14:00 to 14:25: 40, 38, 42, 96, 92, 40.
- At the 14:15 cycle (the 96% point), VCF Operations shows CPU Contention (%) of 9.8% and CPU Ready (%) of 2.9%.
- The 14:15 cycle in VCF Operations also shows these 5-minute values: Co-stop 6.4%, Overlap 0.2%, Other Wait 0.3%.
- The platform engineer says: "The two tools disagree, so one of them collects wrongly. Open a support case against VCF Operations."

Which statements about the two pairs of numbers and the next step are correct?

- A. Co-stop at 14:15 is runtime the guest demanded, so it counts in the guest's CPU sizing.
- B. VCF Operations collected app-07's CPU Usage wrongly or late in that half hour.
- C. Inside the guest, the Co-stop at 14:15 was a freeze, as Ready is, and the guest cannot tell them apart.
- D. The 1 Week chart keeps the highest value of each 30-minute window, so 58% was the peak at 14:00.
- E. The vSphere Client offers no counter named Contention for the VM.
- F. CPU Contention is the vSphere Ready counter under another name, so 9.8% against 2.9% points to a collection error.
- G. The 9.8% is Overlap plus Co-stop plus Ready plus Other Wait for the 14:15 cycle.
- H. CPU Contention in VCF Operations 9.1 is the vSphere CPU Latency counter, passed through.
- I. Most of the 9.8% at 14:15 is Co-stop, while Ready is the smaller part.
- J. The co-stopped vCPUs of app-07 were held back because no physical thread was free for them.
- K. The Ready of 2.9% is the full CPU wait of app-07 in the 14:15 cycle.
- L. For the 14:15 slowness, the 5-minute VCF Operations values are sharper evidence than the 1 Week point.
- M. A snapshot on app-07 is one cause of its Co-stop at 14:15 to rule out.
- N. History and analysis of contention are read in VCF Operations; vCenter keeps a short, averaged history.
- O. A CPU Contention of 9.8% at 14:15 calls for another host in the cluster of app-07.

## Likely wrong answer
- B: "The tools disagree on Usage, so the VCF Operations data is wrong or delayed."
- F: "Contention is the vSphere Ready counter under another name, so 9.8% against 2.9% shows an error."

## Expected key points
- Answer: A, C, E, G, I, L, M, N.
- A is correct: a co-stopped vCPU is paused while the guest wants to run it; that is runtime the guest demanded, so Co-stop counts in Guest OS CPU sizing.
- B is wrong: (40 + 38 + 42 + 96 + 92 + 40) / 6 = 58%, exactly the 30-minute point. The difference is the interval and the rollup (average), not collection.
- C is correct: the effect of Co-stop on the Guest OS is the same as Ready, a freeze; the guest cannot tell which of the two held it.
- D is wrong: the 1 Week chart shows 30-minute averages; peaks are rolled away.
- E is correct: CPU Contention is computed by VCF Operations; vSphere has no counter of that name (its nearest counter is CPU Latency).
- F is wrong: Contention sums the time a vCPU does not get CPU (Overlap, Co-stop, Ready and Other Wait below 1%), so it cannot match Ready alone.
- G is correct: 0.2 + 6.4 + 2.9 + 0.3 = 9.8% (Other Wait is added while below 1%).
- H is wrong: Contention has its own formula (Broadcom KB 394770: the sum of overlap, ready, co-stop and other wait). CPU Latency also reflects Hyper-Threading and frequency, which Contention does not.
- I is correct: Co-stop is 6.4 of the 9.8 points. For an 8-vCPU VM the siblings are held back when one vCPU waits: multi-vCPU scheduling loss, not a shortage of host CPU alone.
- J is wrong: co-stopped vCPUs are held back to stay in step with a sibling, even when physical threads are free for them.
- K is wrong: Co-stop (6.4%), Overlap and Other Wait add to the wait; Ready alone understates it. Quote Contention with its parts, or Ready and Co-stop, read against Run.
- L is correct: the 5-minute points show the 96% and 92% plateau that the 30-minute average hides.
- M is correct: snapshots are a known cause of Co-stop (Broadcom KB 2000058), next to Ready on a sibling vCPU and the VM's size against the NUMA node; they belong to the VM, not to the host, and are checked on the VM.
- N is correct: vCenter is the administrative tool, with a short history that rolls peaks away; capacity and performance analysis are done in VCF Operations.
- O is wrong: Contention says that the VM waited, not why. Before capacity, the flow reads the VM's width against its work, the siblings' Ready, limits and shares, and the host's load in the same cycles; most of this 9.8% is Co-stop, which the VM's width and its siblings' Ready drive.

## Notes
- Public source: Broadcom KB 394770, How is CPU Contention (%) calculated (Aria/VCF Operations 8.x; no updated date shown): "Value is the sum of CPU overlap, ready, co-stop and other wait", from the 15 20-second points of each 5-minute cycle. vSphere 9.1 Monitoring and Performance: Data Collection Intervals (1 Week: 30-minute points; 6 points of 1 Day); Usage rollup is an average. The knowledge file states that Other Wait is added only when below 1% and that from VCF Operations 8.18 the formula includes limit time; the KB does not say so, and neither fact is used in the key (Other Wait is 0.3% and the VM has no limit in the scenario).
- Why the key holds: both differences are arithmetic on the numbers given plus documented definitions.
- Debatable risk: low. The knowledge file's July 2024 (8.18) change of the formula is not checked against a vendor page; the question does not rely on it.
- Rests on: the role file's principle that a passed-through metric means what its source means and only computed metrics have their own definition; the vendor sources above.
- Option H rests on Broadcom KB 394770 (the formula) and the knowledge file's comparison of Contention and Latency, not on the 8.18 date.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the stem no longer says the vSphere Client has no Contention counter (that is now option E); A and B one fact each and no longer negations of each other; E no longer negates H; O (the wrong action) added. An over-correction option (VCF Operations CPU Usage has its own formula) was tried and dropped on review 2026-11-15: no knowledge file states that VM CPU Usage is passed through. Key unchanged.
- Paired with 0370 (theory and practical, design.md 3.9).
- Changed in the 2026-11-15 audit: CPU Ready moved from the vSphere Client 1 Day chart to VCF Operations (at level 1 the 1 Day chart keeps one summed value in ms for the VM, not a per-vCPU percentage). Over-cap facts replaced in place, same truth: A (two readings differ in interval and rollup) and C (the 58% is the mean of the six points), held by 0047 and 0432, are now Co-stop in Guest OS sizing (A) and Co-stop felt as a freeze (C); M (Co-stop grows with the vCPU count), held by 0107 and 0373, is now the snapshot cause (M). O key point no longer says Co-stop comes from the VM's size alone.
- Changed 2026-11-16: M lost "before looking at the host", an order of checks the knowledge base does not state; it now says only that a snapshot is one cause to rule out.

## Metadata
```yaml
id: "0357"
title: "The same VM in two tools, two numbers"
product: [vsphere, vcf-operations]
technology: [cpu, system]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,C,E,G,I,L,M,N]
misconception: [B,F]
input: [text]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vcf-operations/vcf-operations-role
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
knowledge_main: vcf-operations/vcf-operations-role
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [tool-confusion, rollup-and-interval]
pair: "0370"
status: draft
```
