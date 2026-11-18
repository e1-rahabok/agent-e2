"""Question 0427: four Real-time storage exports of one VM and its host.

rpt-app-11: Hard disk 1 scsi0:0 on VMFS ds-vmfs-21 (one LUN, shared with other
VMs), Hard disk 2 scsi0:1 on NFS nfs-arch-02. Virtual disk and Datastore views
cover both disks; the VM Disk view has the LUN only (no NFS); the host Disk view
of the LUN counts every VM on it (1.7-2.3 x the VM).
"""

from .. import export_framework, export_formats

N = 30
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=14, hour=10, minute=0)
DEV = "Fibre Channel Disk (naa.600a0b80003c5d2e00001f4a6b7c8d90)"
RR, RW = "Average read requests per second", "Average write requests per second"
F_VD, F_DS = "vcenter-vm-virtual-disk-realtime.csv", "vcenter-vm-datastore-realtime.csv"
F_VMDISK, F_HOST = "vcenter-vm-disk-realtime.csv", "vcenter-host-disk-lun-realtime.csv"
RRATE, WRATE = "counter.disk.read.label", "counter.disk.write.label"
VD_COLS = [f"{RR} for scsi0:0", f"{RW} for scsi0:0", f"{RR} for scsi0:1", f"{RW} for scsi0:1",
           "Read latency for scsi0:0", "Write latency for scsi0:0", "Read latency for scsi0:1", "Write latency for scsi0:1"]
DS_COLS = [f"{RR} for ds-vmfs-21", f"{RW} for ds-vmfs-21", f"{RR} for nfs-arch-02", f"{RW} for nfs-arch-02",
           "Read latency for ds-vmfs-21", "Write latency for ds-vmfs-21", "Read latency for nfs-arch-02",
           "Write latency for nfs-arch-02"]
VMD_COLS = [f"{RR} for {DEV}", f"{RW} for {DEV}", f"{RRATE} for {DEV}", f"{WRATE} for {DEV}"]
HOST_COLS = [f"{RR} for {DEV}", f"{RW} for {DEV}", f"Read latency for {DEV}", f"Write latency for {DEV}",
             f"{RRATE} for {DEV}", f"{WRATE} for {DEV}"]


@export_framework.register
class Q0427(export_framework.QuestionExport):
    question_id = "0427"
    seed = 427

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "io")
        times = export_framework.time_axis(START, N, STEP_S)
        vd, ds, vm, host = [], [], [], []
        j = lambda x: round(x * rng.uniform(0.97, 1.03))
        for t in times:
            r0, w0 = round(350 * rng.uniform(0.95, 1.05)), round(150 * rng.uniform(0.95, 1.05))
            r1, w1 = round(200 * rng.uniform(0.95, 1.05)), round(100 * rng.uniform(0.95, 1.05))
            l = [rng.randint(2, 4), rng.randint(1, 3), rng.randint(3, 6), rng.randint(2, 5)]
            vd.append((t, [r0, w0, r1, w1] + l))
            dl = [max(0, x + rng.randint(-1, 1)) for x in l]
            ds.append((t, [j(r0), j(w0), j(r1), j(w1), dl[0], dl[1], dl[2], dl[3]]))
            vr, vw = j(r0), j(w0)
            vm.append((t, [vr, vw, round(vr * 16 * rng.uniform(0.98, 1.02)), round(vw * 16 * rng.uniform(0.98, 1.02))]))
            hr, hw = round(vr * rng.uniform(1.7, 2.3)), round(vw * rng.uniform(1.7, 2.3))
            host.append((t, [hr, hw, rng.randint(2, 4), rng.randint(1, 3),
                             round(hr * rng.uniform(14, 20)), round(hw * rng.uniform(14, 20))]))
        return {F_VD: export_formats.vcenter_csv(VD_COLS, vd), F_DS: export_formats.vcenter_csv(DS_COLS, ds),
                F_VMDISK: export_formats.vcenter_csv(VMD_COLS, vm), F_HOST: export_formats.vcenter_csv(HOST_COLS, host)}

    def check(self, files):
        fails = []
        spec = {F_VD: VD_COLS, F_DS: DS_COLS, F_VMDISK: VMD_COLS, F_HOST: HOST_COLS}
        parsed = {}
        for f, cols in spec.items():
            try:
                c, r = export_formats.parse_vcenter_csv(files[f])
            except (KeyError, ValueError) as e:
                return [f"{f}: {e}"]
            if c != cols:
                return [f"{f}: columns differ: {c}"]
            if len(r) != N or any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(r, r[1:])):
                fails.append(f"{f}: {len(r)} rows or step not 20 s")
            parsed[f] = r
        stamps = [t for t, _ in parsed[F_VD]]
        if any([t for t, _ in r] != stamps for r in parsed.values()):
            fails.append("time stamps differ between files")
        got = export_formats.parse_vcenter_csv(files[F_VMDISK])[0]
        if len(got) != 4 or any("scsi0" in c or "nfs-arch" in c or not c.endswith(f" for {DEV}") for c in got):
            fails.append("A true, H false: VM Disk file names a virtual disk or the NFS datastore")
        within = lambda a, b, p=0.10: abs(a - b) <= p * b
        for i in range(N):
            k = f"row {i + 1}"
            vd = parsed[F_VD][i][1]
            ds = parsed[F_DS][i][1]
            vm = parsed[F_VMDISK][i][1]
            ho = parsed[F_HOST][i][1]
            d0, d1 = vd[0] + vd[1], vd[2] + vd[3]
            if d1 < 250:
                fails.append(f"{k}: A, G: scsi0:1 total {d1} below 250")
            if not within(ds[0] + ds[1], d0) or not within(ds[2] + ds[3], d1):    # E, G
                fails.append(f"{k}: E false, G true: datastore totals not within 10% of the virtual disks")
            if not within(vm[0] + vm[1], d0):                                    # B, E
                fails.append(f"{k}: B true: VM Disk total not within 10% of scsi0:0")
            if not within(vm[0] + vm[1], ds[0] + ds[1]):
                fails.append(f"{k}: E false: VM Disk total not within 10% of ds-vmfs-21")
            if ho[0] + ho[1] < 1.5 * (vm[0] + vm[1]) or ho[0] < vm[0] or ho[1] < vm[1]:   # C, D
                fails.append(f"{k}: C true, D false: host total not at least 1.5 x VM Disk")
            for req, rate in ((vm[0], vm[2]), (vm[1], vm[3])):
                if req > 0 and not 15 <= rate / req <= 17:
                    fails.append(f"{k}: VM Disk KB per IO {rate / req:.1f}")
        return fails[:20]
