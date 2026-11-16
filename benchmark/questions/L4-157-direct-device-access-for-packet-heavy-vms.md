# Direct device access for four packet-heavy VMs

## Prompt
- VCF 9.1 cluster cl-nfv-02 has 6 ESXi hosts, DRS fully automated. It was upgraded from VCF 5.2 last quarter.
- Each host has two 100 GbE NICs that support SR-IOV, and a DPU configured through NSX Manager.
- VM traffic runs on a distributed switch with Network I/O Control version 3; the virtual machine traffic pool has custom shares.
- Every night the backup tool takes a VM snapshot of each VM. Hosts are patched monthly, one at a time, in maintenance mode.
- Memory is overcommitted: most VMs have no memory reservation.
- An NFV team runs four virtual router VMs, each with a VMXNET3 adapter, virtual hardware version 19, and about 1.4 million packets per second at peak.
- The team asks for one of three changes for the four routers: SR-IOV virtual functions on the 100 GbE NICs, DirectPath I/O of one physical NIC per router, or the DPU in UPTv2 mode.

Which statements are correct?

- A. With SR-IOV, vMotion of the four routers is no longer possible.
- B. With SR-IOV, the nightly snapshot-based backup of the routers keeps working as before.
- C. SR-IOV, like DirectPath I/O, needs a physical NIC of its own for each router.
- D. With DirectPath I/O, the NIC given to one router carries no other VM's traffic.
- E. With SR-IOV, the switch's Network I/O Control shares still divide bandwidth for the routers.
- F. With the DPU in UPTv2 mode, vMotion of the routers stays possible.
- G. UPTv2 runs the routers without a memory reservation, since the DPU does the packet work.
- H. UPTv2 needs the routers on virtual hardware 20 or later, with a VMXNET3 driver that supports it.
- I. After the upgrade to VCF 9.1, Enhanced Data Path is already active on these hosts.
- J. Direct device access would also suit the cluster's ordinary application VMs, so offer it to them.
- K. At 1.4 million packets per second, direct device access brings the routers nothing over VMXNET3.
- L. With SR-IOV, the routers can keep taking part in the cluster's memory overcommit.

## Likely wrong answer
"SR-IOV is just DirectPath I/O again, one NIC per VM" (C). "The DPU does the work, so no reservation is needed" (G). "We are on VCF 9.1 now, so Enhanced Data Path is on" (I). Or the passthrough enthusiasm of J: if it helps the routers, it helps every VM.

## Expected key points
- Answer: A, D, F, H.
- A is correct: SR-IOV has the same incompatible list as DirectPath I/O, vMotion included.
- B is wrong: snapshots are on the incompatible list of SR-IOV and DirectPath I/O, so the snapshot-based backup cannot cover the routers.
- C is wrong: the misconception. The incompatible lists are the same, but SR-IOV lets one physical device be shared by several guests; DirectPath I/O does not.
- D is correct: physical NIC sharing is on the incompatible list of DirectPath I/O; the device belongs to one VM.
- E is wrong: Network I/O Control is on the incompatible list, and SR-IOV is not available with Network I/O Control version 3.
- F is correct: a DPU gives many of the advantages of DirectPath I/O and SR-IOV and still allows the vSphere migration and high-availability features.
- G is wrong: the misconception. UPTv2 requires a full memory reservation and pinning of guest memory.
- H is correct: UPTv2 requires virtual hardware version 20 or later and a VMXNET3 guest driver version that supports the feature. The routers are on version 19 today.
- I is wrong: the misconception. Enhanced Data Path is active by default only on new VCF 9.1 installations; an upgrade keeps the earlier setting.
- J is wrong: Performance Best Practices for vSphere 9.1 says typical VMs do not require DirectPath I/O; the gain is limited, and the VMs would lose vMotion, snapshots, Fault Tolerance and Network I/O Control.
- K is wrong: the over-correction. Very network-intensive workloads with high packet rates are the candidates; the gain is some throughput and a lower CPU cost for networking.
- L is wrong: memory overcommit is on the incompatible list of SR-IOV.

## Notes
- Every fact is in the knowledge base (passthrough-and-offload, from Performance Best Practices for vSphere 9.1, pp. 46-49; resource-controls for SR-IOV with Network I/O Control version 3).

## Metadata
```yaml
id: "0457"
title: "Direct device access for four packet-heavy VMs"
product: [vsphere, nsx]
technology: [network]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi, cluster]
tool: [none]
knowledge:
  - vsphere/technology/network/concepts/passthrough-and-offload
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/network/concepts/passthrough-and-offload
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/network/concepts/passthrough-and-offload"
answer: [A, D, F, H]
misconception: [C, G, I]
misconception_type: []
status: draft
```
