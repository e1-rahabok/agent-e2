# Host-local swap files and vMotion

## Prompt
- A DRS cluster of 8 ESX hosts. Each host has a local NVMe datastore. The VM swap files are on the shared SAN datastores today.
- The storage team wants the SAN space back and asks to set the cluster swap file location to "Datastore specified by host", with each host's local NVMe datastore.
- Host memory is not overcommitted most of the time. DRS migrates VMs with vMotion several times a day.

What are the effects of this change on vMotion and on the space? Under which condition do they matter?

## Likely wrong answer
"Local NVMe is faster than the SAN, so swap and vMotion both get faster." Or: "The swap file is empty when memory is not overcommitted, so the location has no effect at all."

## Expected key points
- The swap file stays tied to the host the VM runs on. Pages of a VM that are swapped to a local swap file on the source host must be brought back or transferred across the network to the destination host during vMotion, so vMotion can be slower.
- The vendor describes the degradation as slight. It depends on how many pages of the VM are in the swap file, so it matters mainly when the host has swapped (memory overcommitted past ballooning and compression).
- The swap file is still created at power-on on the local datastore, with the size of configured memory minus reservation, so each local datastore needs that space for the VMs that run there. A VM that moves to another host gets a swap file there.
- Gain: SAN space is saved, and the local device has low latency if swapping does occur.
- Swap files should not be on thin-provisioned storage.

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Swap File Location" (host-local swap "can lead to a slight degradation in performance for vSphere vMotion because pages swapped to a local swap file on the source host must be transferred across the network to the destination host"). Performance Best Practices for VMware vSphere 9.1, revision 20260624, page 36 (local swap files "could potentially reduce vMotion performance"; no thin-provisioned storage).
- Why one answer: both documents state the vMotion effect and its cause. The condition (pages must be in the swap file) follows from the mechanism.
- Debatable risk: whether to accept the change is a design choice, so the question asks for effects and the condition, not for a decision. The key points do not state a verdict.

## Metadata
```yaml
id: "0297"
title: Host-local swap files and vMotion
product: [vsphere]
technology: [memory, storage]
task: judge-setting
level: 300
answer_type: judged
input: [text]
object: [cluster, esxi, datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/configuration/host-level-swapping
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/technology/memory/configuration/host-level-swapping
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention]
status: draft
```
