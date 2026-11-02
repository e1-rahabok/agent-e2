---
id: vsphere-storage-001
title: "Guest queue invisible to the hypervisor"
scope: vsphere
area: storage
input: text
tests: concept
knowledge:
  - vsphere/foundations/visibility-layers
  - vsphere/storage/metrics/virtual-machine/iops
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Visibility (layers A–D diagram)."
status: draft
---

## Prompt
Oracle on a Windows VM is slow. Windows shows a high Disk Queue Length. In vCenter, the VM's disk IOPS and disk latency look normal. The storage team says storage is fine, so it is not an infrastructure problem. Is that conclusion valid?

## Likely wrong answer
"Yes, vSphere metrics are normal so the storage path is healthy."

## Expected key points
- Queues inside the Guest OS (layer A: disk queue, driver queue, etc.) are **not visible to the hypervisor**. The IO has not yet been sent down.
- So VM-level IOPS can **under-report** real demand.
- Normal vSphere metrics do not prove the IO path is healthy end to end. Look inside the Guest OS too.
- Mental model: Guest OS view Demand = A + B; VM view Demand = B + C + D.

## Notes
- Tests: Visibility layers (principle + diagram).
