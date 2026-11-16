"""Tests for the export generator. Run from the repo root:
    python3 -m unittest project/tools/test_exportgen.py
"""

import datetime as dt
import tempfile
import unittest
from pathlib import Path

from project.tools.exportgen import core, formats, relations as rel
from project.tools.exportgen.__main__ import main

TEMPLATES = core.REPO_ROOT / "project" / "sources" / "export-templates"
T0 = dt.datetime(2026, 11, 15, 9, 5, 40, tzinfo=dt.timezone.utc)


def template(rel_path):
    with open(TEMPLATES / rel_path, encoding="utf-8", newline="") as f:
        return f.read()


class Determinism(unittest.TestCase):
    def test_same_seed_same_bytes(self):
        for cid, case in core.load_cases().items():
            a, b = case.generate(case.seed), case.generate(case.seed)
            self.assertEqual(a, b, cid)

    def test_other_seed_differs(self):
        case = core.load_cases()["example-1"]
        self.assertNotEqual(case.generate(1), case.generate(2))


class VcenterFormat(unittest.TestCase):
    def test_matches_template_header_style(self):
        sample = template("vcenter-chart-export/vm-cpu-usage-readiness-realtime-sample.csv")
        cols, rows = formats.parse_vcenter_csv(sample)
        out = formats.vcenter_csv(cols, rows)
        self.assertEqual(out, sample)

    def test_template_samples_round_trip(self):
        for p in (TEMPLATES / "vcenter-chart-export").glob("*.csv"):
            text = p.read_text(encoding="utf-8", newline="")
            cols, rows = formats.parse_vcenter_csv(text)
            self.assertEqual(formats.vcenter_csv(cols, rows), text, p.name)

    def test_bom_quoting_time(self):
        out = formats.vcenter_csv(["Usage for vm-a"], [(T0, [1.5])])
        self.assertTrue(out.startswith('\ufeff"Time","Usage for vm-a"\n'))
        self.assertIn('"2026-11-15T09:05:40.000Z",1.5\n', out)

    def test_parser_rejects_missing_bom(self):
        with self.assertRaises(ValueError):
            formats.parse_vcenter_csv('"Time","x"\n')

    def test_intervals(self):
        self.assertEqual(core.INTERVAL_S, {"realtime": 20, "day": 300, "week": 1800, "month": 7200})
        t = core.time_axis(T0, 3, core.INTERVAL_S["day"])
        self.assertEqual((t[1] - t[0]).total_seconds(), 300)


class OtherFormats(unittest.TestCase):
    def test_vcf_chart_matches_sample(self):
        sample = template("vcf-operations/chart-export-sample.csv")
        # the sample lines are 1, 3-6; rebuild with the same title and rows
        title, rows = formats.parse_vcf_chart_csv(sample)
        self.assertEqual(formats.vcf_chart_csv(title, rows), sample)

    def test_vcf_time(self):
        t = dt.datetime(2026, 11, 15, 12, 28, 38, tzinfo=dt.timezone.utc)
        self.assertEqual(formats.vcf_time(t), "November 15, 2026, 8:28:38\u202fPM GMT+08:00")

    def test_vcf_list_round_trip(self):
        cols = ["CPU|Ready (%)", "CPU|Ready (%) (Max)"]
        text = formats.vcf_list_csv(cols, [("vm-a", [0.5, 3.25]), ("vm-b", [None, 1.0])])
        c, rows = formats.parse_vcf_list_csv(text)
        self.assertEqual(c, cols)
        self.assertEqual(rows[1], ("vm-b", [None, 1.0]))

    def test_typeperf_style(self):
        sample = template("windows-typeperf/typeperf-10x1s.csv").split("\n")
        self.assertTrue(sample[0].startswith('"(PDH-CSV 4.0) ('))
        names = [formats.typeperf_name("HOST", "Processor", 0, "% Processor Time")]
        out = formats.typeperf_csv(names, [(T0, [12.5]), (T0 + dt.timedelta(seconds=1), [None])])
        lines = out.split("\n")
        self.assertEqual(lines[0], '"(PDH-CSV 4.0) (UTC)(0)","\\\\HOST\\Processor(0)\\% Processor Time"')
        self.assertEqual(lines[1], '"11/15/2026 09:05:40.000","12.5"')
        self.assertEqual(lines[2], '"11/15/2026 09:05:41.000"," "')
        cols, rows = formats.parse_typeperf_csv(out)
        self.assertEqual(rows[1][1], [None])
        # the sample's time stamp has the same shape
        self.assertRegex(sample[1].split('","')[0], r'^"\d\d/\d\d/\d{4} \d\d:\d\d:\d\d\.\d{3}$')

    def test_typeperf_unquoted_rejected(self):
        with self.assertRaises(ValueError):
            formats.parse_typeperf_csv('"(PDH-CSV 4.0) (UTC)(0)","a"\n"11/15/2026 09:05:40.000",1\n')

    def test_esxtop_batch(self):
        head = template("esxtop/batch-header.txt")
        self.assertTrue(head.startswith('"(PDH-CSV 4.0) (UTC)(0)","\\\\'))
        cols = [formats.esxtop_name("h1", "Group Cpu(7:vm)", "% Ready"), formats.esxtop_name("h1", "Memory", "Free MBytes")]
        out = formats.esxtop_batch_csv(cols, [(T0, [1.234, 5.0])])
        self.assertEqual(out.split("\n")[1], '"11/15/2026 09:05:40","1.23","5.00"')
        self.assertEqual(formats.parse_esxtop_batch(out)[0], cols)
        with self.assertRaises(ValueError):
            formats.esxtop_batch_csv(cols, [(T0, [1.0])])

    def test_panel_headers_match_samples(self):
        for kind, fname, first in (("c", "panel-c.txt", "ID"), ("m", "panel-m.txt", "GID"),
                                   ("u", "panel-u.txt", "DEVICE"), ("d", "panel-d.txt", "ADAPTR"),
                                   ("v", "panel-v.txt", "GID"), ("n", "panel-n.txt", "PORT-ID")):
            sample = template("esxtop/" + fname).replace("\r", "")
            ours = formats.esxtop_panel(kind, "status", []).split("\n")[1]
            want = [ln for ln in sample.split("\n") if ln.split()[:1] == [first]][-1]
            self.assertEqual(ours.split(), want.split(), kind)
            if kind in ("c", "d", "v", "n", "u", "m"):
                self.assertEqual(ours, want, kind)

    def test_cpu_row_layout(self):
        row = (35068, 35068, "sun05-webmin01", 11, 0.0, 0.0, 0.0, 0.26, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0)
        got = formats.esxtop_panel("c", "s", [row]).split("\n")[2]
        sample = template("esxtop/panel-c.txt").replace("\r", "").split("\n")
        want = [ln for ln in sample if ln.startswith("      35068       35068 sun05-webmin01")][-1]
        self.assertEqual(got.replace("-", "0"), want.replace("-", "0"))

    def test_linux_templates(self):
        free = template("linux-photon/free-m.txt")
        m = formats.parse_free_m(free)["Mem"]
        out = formats.free_m((m["total"], m["used"], m["free"], m["shared"], m["buff/cache"], m["available"]),
                             tuple(formats.parse_free_m(free)["Swap"].values()))
        self.assertEqual(out, free)
        sar = template("linux-photon/sar-u-1-5.txt")
        rows = [(ln[:11], [float(x) for x in ln.split()[3:]]) for ln in sar.splitlines()[3:8]]
        avg = [float(x) for x in sar.splitlines()[8].split()[2:]]
        self.assertEqual(formats.sar_u("6.1.176-4.ph5", "vcf-m02-ops01.acepod.com", "11/15/2026", 8,
                                       "11:29:45 AM", rows, avg), sar)
        io = template("linux-photon/iostat-xd-1-3.txt")
        blocks = formats.parse_iostat_blocks(io)
        again = formats.iostat_xd("6.1.176-4.ph5", "vcf-m02-ops01.acepod.com", "11/15/2026", 8,
                                  [list(b.items()) for b in blocks])
        self.assertEqual(again, io)
        ip = template("linux-photon/ip-s-link.txt")
        parsed = formats.parse_ip_s_link(ip)
        self.assertEqual(parsed["eth0"]["RX"]["dropped"], 1661)

    def test_ip_s_link_round_trip(self):
        i = dict(index=2, name="eth0", flags="BROADCAST,MULTICAST,UP,LOWER_UP", mtu=1500, qdisc="mq",
                 state="UP", kind="ether", rx=(25423420915, 84667764, 0, 1661, 0, 49684),
                 tx=(45903921460, 57281361, 0, 0, 0, 0))
        text = formats.ip_s_link([i])
        want = template("linux-photon/ip-s-link.txt").split("2: eth0")[1].split("    altname")[0]
        self.assertEqual(text, "2: eth0" + want)

    def test_text_tools_parse(self):
        p = formats.proc_pressure_memory((1.5, 0.8, 0.2, 12345), (0.5, 0.3, 0.1, 5000))
        self.assertTrue(p.startswith("some avg10=1.50 avg60=0.80 avg300=0.20 total=12345\nfull "))
        self.assertEqual(formats.parse_pressure(p)["full"]["total"], 5000)
        mp = formats.mpstat_all("6.1.0", "h", "11/15/2026", 2, "11:00:00 AM",
                                [[5, 0, 5, 0, 0, 0, 0, 0, 0, 90], [10, 0, 0, 0, 0, 0, 0, 0, 0, 90],
                                 [0, 0, 10, 0, 0, 0, 0, 0, 0, 90]])
        self.assertEqual(formats.parse_mpstat(mp)["0"]["%usr"], 10.0)
        v = formats.vmstat([(1, 0, 0, 100, 10, 200, 0, 0, 1, 2, 30, 40, 5, 1, 94, 0, 0)])
        self.assertIn("us sy id wa st", v)
        t = formats.top_summary("11:00:00", "1 day,  2:00", 1, (0.1, 0.2, 0.3), (100, 1, 99, 0, 0),
                                dict(us=1, sy=1, ni=0, id=96, wa=0, hi=0, si=0, st=2),
                                (1000, 100, 400, 500), (100, 100, 0, 500))
        self.assertIn("2.0 st", t)

    def test_windows_text(self):
        s = formats.systeminfo_virtual_memory(9431, 5012, 4419, ["C:\\pagefile.sys"])
        self.assertIn("Virtual Memory: In Use:    4,419 MB", s)
        self.assertIn("Page File Location(s):     C:\\pagefile.sys", s)
        pf = formats.win32_pagefileusage([dict(Name="C:\\pagefile.sys", AllocatedBaseSize=4096, CurrentUsage=10, PeakUsage=20)])
        self.assertIn("AllocatedBaseSize : 4096", pf)
        cpu = formats.win32_processor([dict(SocketDesignation="CPU 0", Name="x", NumberOfCores=2, NumberOfLogicalProcessors=2)])
        self.assertIn("NumberOfLogicalProcessors : 2", cpu)


class Relations(unittest.TestCase):
    def test_state_sum(self):
        self.assertEqual(rel.vcpu_state_total_ms(4), 80000)
        self.assertEqual(rel.vcpu_state_total_ms(4, 300), 1_200_000)
        w = rel.wait_from_states(4, 10000, 2000, 100)
        self.assertEqual(rel.state_sum_ms(10000, 2000, 100, w), 80000)

    def test_readiness(self):
        self.assertAlmostEqual(rel.readiness_pct(8000, 4), 10.0)
        self.assertAlmostEqual(rel.ready_ms_from_readiness(10, 4), 8000)
        self.assertAlmostEqual(rel.ms_to_pct(2000), 10.0)
        self.assertAlmostEqual(rel.pct_to_ms(10), 2000)

    def test_rollup(self):
        v = list(range(30))
        self.assertEqual(rel.rollup_means(v, 15), [7.0, 22.0])
        self.assertEqual(rel.rollup_sums(v, 15), [105, 330])
        self.assertEqual(rel.samples_per_rollup(300), 15)
        self.assertEqual(rel.rollup_windows([1, 2, 3], 2), [[1, 2]])

    def test_latency_and_little(self):
        self.assertAlmostEqual(rel.weighted_latency(1.0, 900, 11.0, 100), 2.0)
        self.assertAlmostEqual(rel.outstanding_io(2000, 5), 10.0)
        self.assertAlmostEqual(rel.iops_for_outstanding(10, 5), 2000)
        self.assertAlmostEqual(rel.iops_weighted_mean([1, 100], [990, 10]), 1.99, places=2)

    def test_esxtop(self):
        self.assertEqual(rel.gavg(2.0, 0.5), 2.5)
        self.assertTrue(rel.qavg_within_kavg(0.2, 0.5))
        self.assertFalse(rel.qavg_within_kavg(0.6, 0.5))
        self.assertEqual(rel.group_sum([[1, 2], [3, 4]]), [4, 6])
        self.assertAlmostEqual(rel.esxtop_wait(1.0, 70.0), 71.0)
        self.assertAlmostEqual(rel.cluster_mean([10, 20, 90]), 40.0)

    def test_network_and_units(self):
        self.assertEqual(rel.vmnic_usage(100, 50), 150)
        self.assertAlmostEqual(rel.bytes_per_packet(100, 1024), 100.0)
        self.assertAlmostEqual(rel.kbytes_per_s_for_packets(1024, 100), 100.0)
        self.assertAlmostEqual(rel.kbps_to_mbps(1000), 8.192)
        self.assertAlmostEqual(rel.mbps_to_kbps(rel.kbps_to_mbps(1000)), 1000)
        self.assertEqual(rel.kb_to_bytes(2), 2048)
        self.assertEqual(rel.kbit_to_bits(2), 2000)
        self.assertAlmostEqual(rel.mbytes_per_s_to_mbit_per_s(1), 8.388608)
        self.assertAlmostEqual(rel.kb_to_mb(2048), 2.0)


class Cases(unittest.TestCase):
    def test_examples_pass_check(self):
        for cid in ("example-1", "example-2"):
            case = core.load_cases()[cid]
            self.assertEqual(case.check(case.generate(case.seed)), [], cid)

    def test_example_values(self):
        files = core.load_cases()["example-1"].generate()
        cols, rows = formats.parse_vcenter_csv(files["vm-cpu-realtime.csv"])
        self.assertEqual(len(rows), 180)
        self.assertEqual(len(cols), 6)

    def test_corrupted_files_fail(self):
        c1 = core.load_cases()["example-1"]
        f = c1.generate()
        lines = f["vm-cpu-realtime.csv"].split("\n")
        parts = lines[5].split(",")
        parts[4] = str(int(parts[4]) + 500)  # Run changes, state sum breaks
        lines[5] = ",".join(parts)
        self.assertTrue(c1.check({"vm-cpu-realtime.csv": "\n".join(lines)}))
        c2 = core.load_cases()["example-2"]
        t = c2.generate()["esxtop-cpu.txt"]
        bad = t.replace("web-demo-01         6   88.96", "web-demo-01         6   95.96")
        self.assertNotEqual(bad, t)
        self.assertTrue(c2.check({"esxtop-cpu.txt": bad}))

    def test_cap_enforced(self):
        self.assertEqual(core.check_size_cap({"a.csv": "x" * 24000}), [])
        self.assertTrue(core.check_size_cap({"a.csv": "x" * 24001}))
        self.assertEqual(core.check_size_cap({"a.txt": "x" * 30000}), [])

    def test_cli_generate_check_and_failure(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(main(["generate", "all", "--out", d]), 0)
            self.assertEqual(main(["check", "all", "--out", d]), 0)
            p = Path(d) / "example-1" / "vm-cpu-realtime.csv"
            p.write_text(p.read_text(encoding="utf-8").replace("\n", "\n\n", 1), encoding="utf-8")
            self.assertNotEqual(main(["check", "example-1", "--out", d]), 0)
            p.unlink()
            self.assertNotEqual(main(["check", "example-1", "--out", d]), 0)

    def test_noise_helpers(self):
        rng = core.make_rng(5)
        w = core.bounded_walk(rng, 100, 0.5, 0.3, 0.0, 1.0)
        self.assertTrue(all(0 <= x <= 1 for x in w))
        b = core.burst_profile(10, 4, 2, ramp=1)
        self.assertEqual(b[4:6], [1.0, 1.0])
        self.assertEqual(b[0], 0.0)
        self.assertEqual(core.clamp(5, 0, 1), 1)


class NetworkCases(unittest.TestCase):
    """Cases 0420, 0413, 0415: generate + check pass, determinism, a broken row fails."""

    def _blocks(self, cid):
        qp = core.question_path(cid)
        self.assertIsNotNone(qp)
        return core.read_inline_blocks(qp.read_text(encoding="utf-8", newline=""))

    def test_generate_check_determinism(self):
        for cid in ("0420", "0413", "0415"):
            case = core.load_cases()[cid]
            files = case.generate(case.seed)
            self.assertEqual(files, case.generate(case.seed), cid)
            self.assertEqual(case.generate_inline(case.seed), case.generate_inline(case.seed), cid)
            self.assertEqual(case.check(files), [], cid)
            self.assertEqual(core.check_size_cap(files), [], cid)
            blocks = dict(self._blocks(cid))
            blocks.update({n: t.rstrip("\n") for n, t in case.generate_inline(case.seed).items()})
            self.assertEqual(case.check_inline(blocks, files), [], cid)

    def test_broken_rows_fail(self):
        c = core.load_cases()["0413"]
        name, text = next(iter(c.generate().items()))
        lines = text.split("\n")
        parts = lines[3].split(",")
        parts[-1] = str(int(parts[-1]) + 1)
        lines[3] = ",".join(parts)
        self.assertTrue(c.check({name: "\n".join(lines)}))
        c = core.load_cases()["0415"]
        name, text = next(iter(c.generate().items()))
        self.assertTrue(c.check({name: text.replace(',0,', ',7,', 1)}))
        c = core.load_cases()["0420"]
        self.assertTrue(c.check_inline({1: "bad", 2: "bad"}, {}))

    def test_inline_blocks_round_trip(self):
        md = "# T\n\n## Prompt\n- a\n\n```text\nx\n```\n\n```text\ny\n```\n\n## Notes\n```text\nz\n```\n"
        self.assertEqual(core.read_inline_blocks(md), {1: "x", 2: "y"})
        out = core.write_inline_blocks(md, {2: "Y1\nY2\n"})
        self.assertEqual(core.read_inline_blocks(out), {1: "x", 2: "Y1\nY2"})
        self.assertIn("```text\nz\n```", out)
        with self.assertRaises(ValueError):
            core.write_inline_blocks(md, {3: "q"})


class ClusterCapacityCases(unittest.TestCase):
    IDS = ("0401", "0431", "0438", "0440", "0386", "0385", "0391", "0393", "0387", "0434")

    def test_generate_check_deterministic(self):
        cases = core.load_cases()
        for cid in self.IDS:
            case = cases[cid]
            files = case.generate(case.seed)
            self.assertEqual(files, case.generate(case.seed), cid)
            self.assertEqual(case.check(files), [], cid)
            self.assertEqual(core.check_size_cap(files), [], cid)

    def test_corrupted_rows_fail(self):
        case = core.load_cases()["0438"]
        name = "vcf-operations-cluster-hosts-cpu-usage-7-days.csv"
        files = case.generate()
        lines = files[name].split("\n")
        parts = lines[40].split(",")
        parts[-1] = str(float(parts[-1]) + 20)
        lines[40] = ",".join(parts)
        self.assertTrue(case.check({name: "\n".join(lines)}))


class CpuCoStopCases(unittest.TestCase):
    IDS = ("0369", "0370", "0371", "0372", "0373", "0375")

    def test_generate_check_deterministic(self):
        cases = core.load_cases()
        for cid in self.IDS:
            case = cases[cid]
            files = case.generate(case.seed)
            self.assertEqual(files, case.generate(case.seed), cid)
            self.assertEqual(case.generate_inline(case.seed), case.generate_inline(case.seed), cid)
            self.assertEqual(case.check(files), [], cid)
            self.assertEqual(core.check_size_cap(files), [], cid)
            inline = case.generate_inline(case.seed)
            self.assertEqual(case.check_inline(inline, files), [], cid)

    def test_corrupted_cpu_files_fail(self):
        cases = core.load_cases()
        c = cases["0372"]
        name, text = next(iter(c.generate().items()))
        lines = text.split("\n")
        parts = lines[5].split(",")
        parts[5] = str(int(parts[5]) + 7)
        lines[5] = ",".join(parts)
        self.assertTrue(c.check({name: "\n".join(lines)}))
        c = cases["0375"]
        block = c.generate_inline()[1]
        self.assertTrue(c.check_inline({1: block.replace("   0.00    0.00 \n", "   0.30    0.00 \n", 1)}, {}))
        c = cases["0373"]
        files = c.generate()
        bad = c.generate_inline()[1].replace("Average:", "Averagx:", 1)
        self.assertTrue(c.check_inline({1: bad}, files))


class CpuClusterCases(unittest.TestCase):
    """Cases 0368, 0381, 0436, 0374, 0376, 0379, 0433: generate + check, determinism, broken input fails."""
    IDS = ("0368", "0381", "0436", "0374", "0376", "0379", "0433")

    def test_generate_check_deterministic(self):
        cases = core.load_cases()
        for cid in self.IDS:
            case = cases[cid]
            files = case.generate(case.seed)
            self.assertEqual(files, case.generate(case.seed), cid)
            self.assertEqual(case.generate_inline(case.seed), case.generate_inline(case.seed), cid)
            self.assertEqual(case.check(files), [], cid)
            self.assertEqual(core.check_size_cap(files), [], cid)
            blocks = {}
            qp = core.question_path(cid)
            if qp is not None:
                blocks = core.read_inline_blocks(qp.read_text(encoding="utf-8", newline=""))
            blocks.update({n: t.rstrip("\n") for n, t in case.generate_inline(case.seed).items()})
            self.assertEqual(case.check_inline(blocks, files), [], cid)

    def test_broken_input_fails(self):
        cases = core.load_cases()
        c = cases["0368"]
        files = c.generate()
        name = "vcenter-vm-cpu-realtime.csv"
        lines = files[name].split("\n")
        parts = lines[2].split(",")
        parts[3] = str(int(parts[3]) + 500)           # Ready: state sum and Readiness break
        lines[2] = ",".join(parts)
        self.assertTrue(c.check({**files, name: "\n".join(lines)}))
        c = cases["0436"]
        block = c.generate_inline()[2].replace("      0.00 ", "   1000.00 ", 1)
        self.assertTrue(c.check_inline({1: "bad", 2: block}, {}))
        c = cases["0376"]
        block = c.generate_inline()[1]
        self.assertTrue(c.check_inline({1: block.replace("vmx-vcpu-2", "vmx-vcpu-9")}, {}))
        c = cases["0379"]
        self.assertTrue(c.check_inline({1: "Name : other"}, {}))

    def test_numa_panel_and_grid_formats(self):
        text = formats.esxtop_panel("m-numa", "status", [(1, "vm-a", 1.0, 1.0, 1.0, "0", 0, 0.0, 1.0, 100, 1.0, 0.5, 0.0, 0.0),
                                                           (2, "hostd.1", 60.0, 60.0, 59.0, None, None, None, None, None, None, None, None, None)])
        head, rows = formats.parse_esxtop_panel(text, "m-numa")
        self.assertEqual(head[-3:], ["OVD_ND0", "GST_ND1", "OVD_ND1"])
        self.assertEqual(rows[1][5:], ["-"] * 9)
        grid = formats.vsphere_grid_csv(["Name", "DRS Score"], [["a", "41%"]])
        self.assertEqual(formats.parse_vsphere_grid_csv(grid), (["Name", "DRS Score"], [["a", "41%"]]))
        with self.assertRaises(ValueError):
            formats.parse_vsphere_grid_csv("Name,Score\na,1\n")


if __name__ == "__main__":
    unittest.main()


class MemoryExportCases(unittest.TestCase):
    """Cases 0388, 0390, 0392, 0395, 0397, 0403: generate + check pass, determinism, a broken file fails."""
    IDS = ("0388", "0390", "0392", "0395", "0397", "0403")

    def test_generate_check_deterministic(self):
        cases = core.load_cases()
        for cid in self.IDS:
            case = cases[cid]
            files = case.generate(case.seed)
            self.assertEqual(files, case.generate(case.seed), cid)
            self.assertEqual(case.check(files), [], cid)
            self.assertEqual(core.check_size_cap(files), [], cid)

    def test_broken_files_fail(self):
        cases = core.load_cases()
        files = cases["0403"].generate()
        name = "vcenter-vm-memory-12h.csv"
        broken = dict(files)
        broken[name] = files[name].replace(",0\n", ",3\n", 1)
        self.assertTrue(cases["0403"].check(broken))
        files = cases["0397"].generate()
        name = "vcf-operations-guest-needed-memory.csv"
        broken = dict(files)
        broken[name] = files[name].replace("-,-,-,\n", "-,-,-,\n", 1).replace(",,-,-,-,", ",1,-,-,-,", 1)
        self.assertTrue(cases["0397"].check(broken))
