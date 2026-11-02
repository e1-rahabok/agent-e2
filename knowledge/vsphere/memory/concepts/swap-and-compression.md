# Swap and compression

## Mechanism
- Compression and swapping work together. A page that cannot be compressed enough is swapped.
- Page size: 4 KB. Two compression levels: 4:1 (1 KB) and 2:1 (2 KB).
- If compression does not get the page below 2 KB, the page is swapped instead: cheaper.
- So Swapped can be 0 while everything was compressed.
- A large page (2 MB) is not compressed directly. It is split into 4 KB pages first.
- Compressed is preferred: unzipping from DRAM is faster than reading from SSD.
- Host cache (if designed on fast SSD) is faster than disk swap.
- Compressed and swapped data stays out until the guest requests it. Bringing it back costs CPU.

## Transition: input, process, output
| Stage | Metric | Meaning |
|---|---|---|
| Input | Swap Target | Pages to be compressed or swapped. Not pages already processed. Read it as compress-swap target. |
| Process | Compression rate, Decompression rate | Rate of compressing and decompressing. |
| Process | Swap out rate, Swap in rate | Rate of moving pages from DIMM to the swap file and back. |
| Output | Swapped, Swap out, Swap in | Swap result. |
| Output | Compressed, Compression saved | Compression result and savings. No compressed-in or compressed-out amounts. |

- The rate tells the shape: 10 MB in 1 second (acute) differs from 10 KB per second over 1,000 seconds (chronic). Same total.
- In and out happen at the same time on different pages. The swap file size can stay constant while its content changes.
- So Swapped is not Swap in - Swap out.

## Swap out vs swap in
- Swap out: ESXi was under memory pressure or the VM hit a limit. Not contention by itself: the page may never be requested.
- Swap in: contention. The guest requested a swapped page. Correlates highly with Memory Latency.
- Swap in does not mean current host pressure. It means pressure in the past, and the guest now requests that data.

## Example
- Swap out rate 6,331.93 + 5,026.4 + 1,882.13 + 615.86 = 13,856 KB/s over 300 s: 13,856 × 300 / 1,024 ≈ 4,059 MB. Swapped was 4,157 MB.
- No swap in during the period.
- Consumed dropped 4,868 MB (7,719 - 2,851). Other factors also contributed.
![Swap out rate summed over 300 seconds matches Swapped](../images/swap-out-rate-example.png)

## Example: limit, swap and compress in opposite directions
- 64 GB VM. Swapped plus compressed peaked at 20 GB over 7 days.
- Consumed was flat for 7 days: a limit. The small gap above the limit is VM overhead.
- Granted hovered above Consumed.
- The guest kept using pages: some were swapped in; others were compressed or swapped to make room. So Swapped and Compressed moved in opposite directions.
![Limit: Consumed flat, swapped and compressed move in opposite directions](../images/limit-swap-compress-opposite.png)

## Traps
- "Swapped = Swap in - Swap out" → in and out run in parallel on different pages.
- "Swap out means contention" → only swap in is contention.
- "Swapped 0 means no reclamation" → pages may all be compressed.

## Metadata
```yaml
id: vsphere/memory/concepts/swap-and-compression
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
internal_derive:
- vsphere/memory/concepts/overcommit-techniques
related:
- vsphere/memory/metrics/virtual-machine/swapped
- vsphere/memory/metrics/virtual-machine/compressed
- vsphere/memory/metrics/virtual-machine/swap-target
- vsphere/memory/metrics/virtual-machine/swap-in-rate
- vsphere/memory/metrics/virtual-machine/latency
- vsphere/memory/concepts/ballooning
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Swap + Compress; Transition; Example; Quiz
corrections: []
review_notes:
- 'Section ''Mechanism'': the book''s sentence on why there is no 3:1 compression is incomplete. Left out.'
status: draft
```
