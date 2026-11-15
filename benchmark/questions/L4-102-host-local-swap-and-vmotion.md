# Host-local swap files and vMotion

## Prompt
- A DRS cluster of 8 ESX 9.1 hosts, fully automated. DRS migrates VMs with vMotion several hundred times a day. The VM swap files are in the VM directories on shared SAN datastores today (swap file location Default, cluster setting Virtual machine directory).
- The cluster runs 210 VMs. Their configured memory adds up to 24 TB and their memory reservations to 10 TB. All VMs are powered on.
- Each host has one local NVMe datastore of 1.92 TB. The storage team wants the SAN space back and asks you to set the cluster swap file location to "Datastore specified by host" and each host's swap datastore to its local NVMe datastore. Their change plan names the swap datastore for hosts 1 to 6 only; hosts 7 and 8 were left out.
- In the last 12 months host memory was not overcommitted: no VM showed Swapped, and ballooning was rare.
- The storage team's argument: "Swap files are empty when memory is not overcommitted, and local NVMe has lower latency than the SAN, so the change costs nothing and speeds things up."

Which statements are correct?

- A. The 210 VMs need about 14 TB of swap space: configured memory minus memory reservations.
- B. The 15.36 TB of local NVMe across the eight hosts covers the 14 TB of swap files, so space is not a concern.
- C. A shared datastore on cheaper storage, used as every host's swap location, frees the VM datastores with no copy at vMotion.
- D. A vSAN datastore can be named as the host-local swap location of each host in place of the NVMe datastore.
- E. Higher memory reservations shrink the swap files; a full reservation leaves a zero-byte file but locks host memory.
- F. Swap files are empty while memory is not overcommitted, so moving them to local datastores has no effect on vMotion.
- G. Once all eight hosts swap locally, one host out leaves 13.44 TB of local datastores, below the 14 TB of swap files.
- H. Local NVMe has lower latency than the SAN, so moving the swap files there makes vMotion migrations faster.
- I. vMotion between hosts with different swap locations copies the swap file to the destination, even if no page was swapped.
- J. Host-local swap space is a per-host limit: a host running a larger share of the VMs can run out while the total fits.
- K. After the change, VMs on hosts 7 and 8 keep their swap files with the VM on the SAN: those hosts name no swap datastore.
- L. Each VM's swap file is the size of its configured memory, so the 210 VMs need 24 TB of swap space in total.
- M. SAN space returns gradually: a running VM's swap file stays put until its next power-on or a vMotion copies it.
- N. Pages already swapped to the source host's local swap file must be sent across the network during vMotion.
- O. Thin-provisioned storage suits swap files well, because they stay mostly empty while memory is not overcommitted.

## Likely wrong answer
- B: "15.36 TB of local space is more than the 14 TB of swap files, so it fits."
- F: "The swap file is empty when memory is not overcommitted, so the location has no effect."
- H: "Local NVMe is faster than the SAN, so swap and vMotion both get faster."

## Expected key points
- Answer: A, C, E, G, I, J, K, M, N.
- A is true: the swap file is configured memory minus reservation: 24 - 10 = 14 TB, created at power-on whether or not the host swaps.
- B is false: the misconception; the limit is per host (average 1.75 TB per host against 1.92 TB, about 9% to spare in total), and with one host out the total no longer fits.
- C is true: with one common location both ends of a vMotion use the same location, so the file is not copied.
- D is false: vSAN and vVols datastores cannot be specified for host-local swap.
- E is true: a reservation equal to configured memory gives a zero-byte swap file; the reserved host memory cannot serve other VMs.
- F is false: the misconception; the file takes its full size from power-on, and vMotion copies it whenever the locations differ. "Empty" only removes the second effect (swapped pages), not the copy.
- G is true: with all eight hosts configured, 7 x 1.92 TB = 13.44 TB, below 14 TB, so the swap files of all VMs do not fit on the local datastores after a host failure or during maintenance.
- H is false: the misconception; NVMe latency helps only host-level swapping, which does not happen here; vMotion gets slower (file copy, swapped pages over the network).
- I is true: vSphere 9.1 documentation: if the swap file location on the destination differs from the source, the swap file is copied to the new location, which can slow vMotion. The copy happens because the locations differ, whether or not pages were swapped.
- J is true: with host-local swap, size each local swap datastore for the largest set of VMs the host can run, including DRS moves, maintenance mode and HA restarts.
- K is true: a host with no swap datastore specified stores the swap file with the VM configuration file, so a half-configured cluster keeps some swap files on the SAN; a vMotion between hosts 1-6 and hosts 7 or 8 copies the file too.
- L is false: the swap file is configured memory minus the memory reservation, not configured memory.
- M is true: changing the setting does not move a running VM's swap file; it moves at the next power-on or with a vMotion copy, so the SAN frees space gradually.
- N is true: the documentation: host-local swap can degrade vMotion because pages swapped to the local swap file on the source host must be transferred to the destination host.
- O is false: swap files should not be on thin-provisioned storage (performance and the risk of running out of space); the empty-file argument fails because the file takes its full size.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Stem changed in review (2026-11-14): the plan names the host swap datastores, instead of saying they were already set on hosts 1 to 6. The vSphere 9.1 documentation (Configure Virtual Machine Swapfile Properties for the Host, PDF p. 1875) says the host swap file location cannot be edited while the cluster setting is Virtual machine directory, so the old stem described a state the vSphere Client does not allow.
- Left out of the options: whether a VM whose swap file does not fit on the host's local datastore fails to power on. vSphere 9.1 says a VM whose swap file cannot be created cannot power on (Resource Management, Swap File Location, PDF p. 1873), and also that with Datastore specified by host a swap file that cannot be stored on the host's datastore is stored in the VM folder (Configure Virtual Machine Swapfile Properties for the Host, PDF p. 1875, and Configure a Virtual Machine Swap File Location for a Cluster, PDF p. 1876). The two statements leave open whether a full local datastore causes a power-on failure or a fallback to the SAN. Every option holds either way: G is arithmetic, J says only that a host's local datastore can run out, and B is false in both cases (a power-on failure or swap files spilling back to the SAN).
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
answer_type: deterministic
answer: [A, C, E, G, I, J, K, M, N]
misconception: [H, F, B]
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
