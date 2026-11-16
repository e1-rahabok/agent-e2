# Batch VM pages under a memory limit

## Prompt
- fin-batch-03 is a Windows Server VM with 16 GB of memory configured, no reservation and a memory limit of 6,144 MB left from a load test last year. VMware Tools is installed without its balloon driver: the hardening template leaves it out.
- Its host, esx-09, has 512 GB of memory, 61% Consumed and the esxtop memory state high. No other VM on esx-09 shows Ballooned memory, Swapped or Compressed.
- The nightly batch runs 01:00-03:00 and has slowed down for weeks. vCenter, Past day chart, 5-minute averages during the batch:
  - Consumed flat at 5.9 GB; Swapped 7.4 GB; Compressed 0.9 GB; Ballooned memory 0.
  - Swap in rate 7,800 KBps; Swap out rate 7,500 KBps; Latency 9%.
  - Virtual disk write latency of the disk that holds the Windows page file: 26 ms.
  - Datastore holding the VM's swap file: read latency 18 ms.
- Windows Performance Monitor during the batch: Memory\Pages Output/sec 1,900; Memory\Pages Input/sec 2,300; page file volume Avg. Disk sec/Write 0.028.
- The application team plans to restart Windows tonight "to clear the host swap". The storage team is asked to find the fault on the datastore.

Which statements are correct?

- A. A page that ESXi swapped and Windows then pages out is read from the VM swap file and written to the page file.
- B. The 26 ms page-file write latency points to a storage fault as the cause of the slow batch.
- C. A Windows restart tonight clears the VM's swap file and brings the swapped pages back into memory.
- D. Powering the VM off and on deletes its swap file, together with the pages swapped into it.
- E. After a power-off and power-on, the batch will run without host swapping, even with the 6,144 MB limit kept in place.
- F. ESXi compresses and swaps under this limit rather than ballooning, because the VM has no balloon driver.
- G. Turning the balloon driver back on, with the limit unchanged, would stop Windows from paging.
- H. Swap in at about the rate of swap out shows a stable VM whose vCPUs do not wait on memory.
- I. The VM's compression cache is full, which is why ESXi swaps the remaining pages.
- J. Moving the VM swap file to a faster device can shorten each swap-in while the limit stays.

## Answers
A, D, F, J

## Explanation
- A is correct: double paging. If the guest pages out a page ESXi swapped, ESXi first reads it from the host swap file and the guest writes it back to guest swap: one page costs two reads and a write, on both swap devices. That is why the page-file disk and the swap datastore are both busy.
- B is wrong: the slow batch comes from the limit. Host swapping is the result of the limit on a host with free memory; the page-file and swap-file I/O is the load that memory pressure on both layers adds, not a storage fault.
- C is wrong: a restart of the Guest OS keeps the VM running and its swap file; the swapped pages stay there until the guest touches them.
- D is correct: power-off deletes the VM swap file, so the future swap-in waits on those pages go away.
- E is wrong: over-correction of D. The limit stays, so the batch pushes the VM over it again and ESXi compresses and swaps again: a page can be swapped out again later.
- F is correct: under a limit the balloon goes first when the driver runs; with the driver missing, ESXi compresses and swaps, picking pages without asking the guest.
- G is wrong: with the limit unchanged, the balloon makes Windows give up pages, and Windows pages out to fill it: the balloon moves the paging into the guest, it does not stop it.
- H is wrong: swap in is contention: the guest touched swapped pages and the vCPU waited; Latency is 9%. In and out run at the same time on different pages.
- I is wrong: the compression cache is capped at 10% of the VM's memory by default (Mem.MemZipMaxPct): 1.6 GB for 16 GB, and 0.9 GB is below it. Pages that do not compress to 2 KB or smaller are swapped.
- J is correct: putting the VM swap file on faster, lower-latency storage (such as host swap cache) is one of the actions for VM memory latency; it shortens each wait but does not remove the cause.
- Misconception: B: "The disk latency shows a storage problem." C: "Restart Windows to clear the swap."

## Notes
- Sources: the knowledge base, Swap and compression (Cost of a swapped page: double paging; compression cache 10%; swap in vs swap out), VM memory latency high (actions: faster swap storage; power-cycle deletes the swap file, a Guest OS restart keeps it; vSphere 9.1 documentation, Delete Swap Files, p. 1876), Memory limit (enforcement order: balloon, then compression, then swap).
- Not counted here on purpose (each already has its two questions): that a limit caps the VM on a host with free memory, and that host swapping is distinct from guest paging.

## Metadata
```yaml
id: "0455"
title: Batch VM pages under a memory limit
product: [vsphere, windows]
technology: [memory, storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os, datastore]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/vm-memory-latency-high
  - vsphere/technology/memory/concepts/memory-limit
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/concepts/swap-and-compression"
misconception: [B, C]
misconception_type: [layer-confusion]
status: draft
```
