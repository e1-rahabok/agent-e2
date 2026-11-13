# Host-local swap files and vMotion

## Prompt
- A DRS cluster of 8 ESX 9.1 hosts, fully automated. DRS migrates VMs with vMotion several hundred times a day. The VM swap files are in the VM directories on shared SAN datastores today (swap file location Default, cluster setting Virtual machine directory).
- The cluster runs 210 VMs. Their configured memory adds up to 24 TB and their memory reservations to 10 TB. All VMs are powered on.
- Each host has one local NVMe datastore of 1.92 TB. The storage team wants the SAN space back and asks you to set the cluster swap file location to "Datastore specified by host". They have already set the local NVMe datastore as the swap location on hosts 1 to 6. Hosts 7 and 8 were not configured yet.
- In the last 12 months host memory was not overcommitted: no VM showed Swapped, and ballooning was rare.
- The storage team's argument: "Swap files are empty when memory is not overcommitted, and local NVMe has lower latency than the SAN, so the change costs nothing and speeds things up."

Evaluate this change. What are the effects on vMotion, on the SAN space and on the local datastores, and what do you check before you approve it?

## Likely wrong answer
"Local NVMe is faster than the SAN, so swap and vMotion both get faster." Or: "The swap file is empty when memory is not overcommitted, so the location has no effect." Or: the capacity of the local datastores is not compared with the swap space that the VMs need.

## Expected key points
- vMotion: with the swap files on one shared location, the source and destination hosts used the same location and the swap file did not move. With a different local datastore on each host, the locations differ, and the vSphere 9.1 documentation says that during vMotion the swap file is copied to the new location, which can result in slower migrations. The documentation also says that host-local swap can degrade vMotion performance because pages swapped to the local swap file on the source host must be transferred to the destination host. The argument "the swap file is empty" does not remove the first effect, and it holds only for the second one while no pages are swapped.
- Space on the local datastores: the swap file is created at power-on on the local datastore with the size of the configured memory minus the reservation, whether or not the host swaps. Needed: 24 - 10 = 14 TB. Available: 8 x 1.92 TB = 15.36 TB, with about 1.36 TB (9%) to spare in total. The need is per host, not in total: the average is 1.75 TB per host against 1.92 TB, so a host that runs a larger share of the VMs can run out. With one host in maintenance or failed, 7 x 1.92 TB = 13.44 TB, below 14 TB: the swap files of the VMs cannot all be created, and the vendor says a VM whose swap file cannot be created does not power on (a failed host's VMs restarted by HA are affected).
- Hosts 7 and 8 have no datastore specified, so their VMs keep the swap file with the VM on the SAN. A VM that moves between hosts 1 to 6 and hosts 7 or 8 has different locations at both ends, so its swap file is copied too, and the SAN space is not fully released.
- The SAN space returns only gradually: the swap file is created at power-on, and a running VM's existing file leaves the SAN when it is copied by a vMotion to a host with a different location, or at the next power cycle. It does not return when the setting is saved.
- The speed argument matters only when the host swaps. NVMe latency helps host-level swapping; it does nothing for vMotion. Swap files should not be on thin-provisioned storage.
- Alternatives to check: use a shared datastore on cheaper storage as the common swap location of all hosts (the location is the same at both ends, so no copy), or raise memory reservations to shrink the swap files (a reservation equal to the configured memory gives a zero-byte swap file, at the cost of host memory). vSAN and vVols datastores cannot be used for host-local swap.

## Notes
- Public source: VMware vSphere 9.1 PDF (build of 2026-11-02): vCenter Server and Host Management, "Virtual Machines Swap File Location and vSphere vMotion Compatibility" ("if the swap file location on the destination host differs from the swap file location on the source host, the swap file is copied to the new location. This activity can result in slower migrations with vMotion. If the destination host cannot access the specified swap file location, it stores the swap file with the virtual machine configuration file"); Resource Management, "Swap File Location" (swap file created at power-on; if it cannot be created the VM cannot power on; host-local swap "can lead to a slight degradation in performance for vSphere vMotion because pages swapped to a local swap file on the source host must be transferred across the network to the destination host"; vSAN and vVols cannot be specified for host-local swap), "Edit swap file location" table (Datastore specified by host; otherwise the swap file is stored with the VM). Performance Best Practices for VMware vSphere 9.1, revision 20260624, pp. 35-36 (swap file size; local swap and vMotion; no thin-provisioned storage).
- Why one answer: the effects follow from documented statements and the arithmetic (24 - 10 = 14 TB against 15.36 TB and 13.44 TB). The question asks for effects and checks, not for a verdict.
- Debatable risk: the documentation does not say how large the cost of copying the swap file is, and the two vendor descriptions of the vMotion effect differ (copy of the file; swapped-in pages), so the key states both and gives no number. The statement that a running VM's existing swap file moves only on a vMotion copy or a power cycle is an inference from "created at power-on" and "copied when locations differ". Whether a vMotion to a host with a full local datastore fails is not documented, so the key does not claim it.
- Rewritten 2026-11-13 to raise difficulty: capacity arithmetic with a host failure, a half-configured cluster (hosts 7 and 8), the point that swap files are copied when locations differ even without swapping, gradual SAN release, and the shared-datastore alternative.

## Metadata
```yaml
id: "0297"
title: Host-local swap files and vMotion
product: [vsphere]
technology: [memory, storage]
task: judge-setting
level: 400
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
