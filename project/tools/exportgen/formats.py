"""Writers (and parsers for the checks) for every export format.

Formats come from project/sources/export-templates. Captured formats:
vCenter chart CSV, VCF Operations chart CSV, Windows typeperf CSV, esxtop
batch CSV and panels, Linux top/sar/iostat/free/ip. Names and formats only;
no lab values.

Assumed formats (no template exists; marked here and in the README):
- VCF Operations LIST VIEW CSV: designed from picker-labels.md. One row per
  object, a "Name" column, one column per metric labelled as the picker
  labels it (for example "CPU|Ready (%)"), and "<Label> (Max)", "(Min)",
  "(First)", "(Last)" columns where a question needs them. Real list
  exports may differ (header names, quoting, extra columns).
- /proc/pressure/memory: the standard Linux PSI text.
- mpstat -P ALL, vmstat, top summary (standard procps; the template's top
  ran in a graph display mode that shows no %st), sar -u ALL columns.
- esxtop batch: the template header (12,608 fields) and data row (12,708)
  differ; writers here keep header and rows at the same field count.
- systeminfo: only the Virtual Memory and Page File lines.
"""

import csv
import datetime as dt
import io
from dataclasses import dataclass

BOM = "\ufeff"


# ---- numbers and time -------------------------------------------------------

def fmt_value(v, nd=2):
    """Number as an export prints it: int as is, float with at most nd
    decimals and no trailing zeros (0.05, 2.9, 12), None as empty."""
    if v is None:
        return ""
    if isinstance(v, bool):
        raise TypeError("bool is not a value")
    if isinstance(v, int):
        return str(v)
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def iso_ms(t):
    """vCenter time stamp: 2026-11-15T09:05:40.000Z (UTC, milliseconds)."""
    t = t.astimezone(dt.timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def parse_iso_ms(s):
    """Inverse of iso_ms()."""
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=dt.timezone.utc)


def _csv_line(fields):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="").writerow(fields)
    return buf.getvalue()


# ---- vCenter chart export ---------------------------------------------------

def vcenter_csv(columns, rows):
    """vCenter Monitor > Performance > Advanced > Export to CSV.

    columns: full column names after Time, e.g. "Usage for web-01".
    rows: (datetime, [values]) pairs; values numbers or None.
    UTF-8 BOM, header and time quoted, values unquoted, LF line ends.
    Real-time is 20 s, Past day 5 min, Past week 30 min, Past month 2 h;
    the writer does not care, the caller builds the time axis.
    """
    out = [BOM + ",".join(['"Time"'] + [f'"{c}"' for c in columns])]
    for t, vals in rows:
        if len(vals) != len(columns):
            raise ValueError("row length differs from header")
        out.append(",".join([f'"{iso_ms(t)}"'] + [fmt_value(v) for v in vals]))
    return "\n".join(out) + "\n"


def parse_vcenter_csv(text):
    """Return (columns, rows): columns without Time, rows [(datetime, [float|None])].
    Raises ValueError when the BOM, the quoting or the Time column is off."""
    if not text.startswith(BOM):
        raise ValueError("no UTF-8 byte-order mark")
    lines = text[1:].splitlines()
    head = next(csv.reader([lines[0]]))
    if head[0] != "Time" or not lines[0].startswith('"Time"'):
        raise ValueError("first column is not quoted Time")
    rows = []
    for ln in lines[1:]:
        if not ln.startswith('"'):
            raise ValueError("time stamp not quoted")
        f = next(csv.reader([ln]))
        rows.append((parse_iso_ms(f[0]), [float(x) if x != "" else None for x in f[1:]]))
    return head[1:], rows


def column(columns, rows, name):
    """Values of one parsed column."""
    i = columns.index(name)
    return [r[1][i] for r in rows]


# ---- VCF Operations ---------------------------------------------------------

_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


def vcf_time(t, tz_hours=8):
    """'November 15, 2026, 8:28:38\u202fPM GMT+08:00' in the given zone.
    The sample has a narrow no-break space (U+202F) before AM/PM."""
    z = dt.timezone(dt.timedelta(hours=tz_hours))
    t = t.astimezone(z)
    h12 = t.hour % 12 or 12
    ampm = "AM" if t.hour < 12 else "PM"
    sign = "+" if tz_hours >= 0 else "-"
    return (f"{_MONTHS[t.month - 1]} {t.day}, {t.year}, {h12}:{t.minute:02d}:{t.second:02d}"
            f"\u202f{ampm} GMT{sign}{abs(tz_hours):02d}:00")


def parse_vcf_time(s):
    """Inverse of vcf_time(); returns an aware datetime."""
    body, tz = s.rsplit(" GMT", 1)
    sign = -1 if tz[0] == "-" else 1
    hh, mm = tz[1:].split(":")
    z = dt.timezone(sign * dt.timedelta(hours=int(hh), minutes=int(mm)))
    month, rest = body.split(" ", 1)
    day, year, clock, ampm = rest.replace(",", "").split()
    h, m, s2 = (int(x) for x in clock.split(":"))
    h = h % 12 + (12 if ampm == "PM" else 0)
    return dt.datetime(int(year), _MONTHS.index(month) + 1, int(day), h, m, s2, tzinfo=z)


def vcf_chart_csv(title, rows, tz_hours=8):
    """VCF Operations chart > More Actions > Download comma separated data.

    Line 1 '<object> - <metric label>', blank line, header
    'Date & Time,Value,Low DT,High DT,Smooth,' then
    '"<time>",<value>,-,-,-,'. Values unquoted at full precision (repr).
    rows: (datetime, value).
    """
    out = [title, "", "Date & Time,Value,Low DT,High DT,Smooth,"]
    for t, v in rows:
        val = "" if v is None else (str(v) if isinstance(v, int) else repr(float(v)))
        out.append(f'"{vcf_time(t, tz_hours)}",{val},-,-,-,')
    return "\n".join(out) + "\n"


def parse_vcf_chart_csv(text):
    """Return (title, [(datetime, float|None)])."""
    lines = text.split("\n")
    if lines[1] != "" or lines[2] != "Date & Time,Value,Low DT,High DT,Smooth,":
        raise ValueError("VCF chart header differs")
    rows = []
    for ln in lines[3:]:
        if not ln:
            continue
        f = next(csv.reader([ln]))
        if f[2:5] != ["-", "-", "-"] or f[5:] != [""]:
            raise ValueError("VCF chart row tail differs")
        rows.append((parse_vcf_time(f[0]), float(f[1]) if f[1] != "" else None))
    return lines[0], rows


def vcf_list_csv(metric_columns, rows, name_header="Name"):
    """VCF Operations List view CSV (ASSUMED format, not captured).

    metric_columns: full column names, e.g. "CPU|Ready (%)",
    "Memory|Balloon (%) (Max)". rows: (object name, [values]).
    Standard CSV quoting: a field is quoted only when it holds a comma,
    a quote or a line break. Blank cell = no data.
    """
    out = [_csv_line([name_header] + list(metric_columns))]
    for name, vals in rows:
        if len(vals) != len(metric_columns):
            raise ValueError("row length differs from header")
        out.append(_csv_line([name] + [fmt_value(v, 4) for v in vals]))
    return "\n".join(out) + "\n"


def parse_vcf_list_csv(text):
    """Return (metric_columns, [(name, [float|None])])."""
    rdr = list(csv.reader(io.StringIO(text)))
    return rdr[0][1:], [(r[0], [float(x) if x != "" else None for x in r[1:]]) for r in rdr[1:]]


def vsphere_grid_csv(columns, rows):
    """vSphere Client data grid > Export CSV (ASSUMED format, not captured).
    Header and every cell quoted, cells as the grid prints them (strings).
    columns: names; rows: lists of strings. LF line ends."""
    def q(s):
        return '"' + str(s).replace('"', '""') + '"'
    out = [",".join(q(c) for c in columns)]
    for r in rows:
        if len(r) != len(columns):
            raise ValueError("row length differs from header")
        out.append(",".join(q(c) for c in r))
    return "\n".join(out) + "\n"


def parse_vsphere_grid_csv(text):
    """Return (columns, [list of str]). Raises ValueError when a field is unquoted."""
    lines = [ln for ln in text.split("\n") if ln]
    for ln in lines:
        if not (ln.startswith('"') and ln.endswith('"')):
            raise ValueError("grid field not quoted")
    rdr = [next(csv.reader([ln])) for ln in lines]
    return rdr[0], rdr[1:]


# ---- Windows typeperf -------------------------------------------------------

def typeperf_name(host, obj, instance, counter):
    r"""\\HOST\object(instance)\counter. instance None gives \\HOST\object\counter."""
    inst = f"({instance})" if instance is not None else ""
    return f"\\\\{host}\\{obj}{inst}\\{counter}"


def typeperf_csv(columns, rows, tz_label="UTC", bias_minutes=0):
    """typeperf -o file.csv: every field quoted, PDH-CSV 4.0 first field,
    time 'MM/DD/YYYY HH:MM:SS.fff' in local time, values as full-precision
    strings. A None value is a single space (as in the first sample row of
    a rate counter). columns: full counter names; rows: (datetime, values).
    """
    def q(s):
        return '"' + s + '"'
    out = [",".join([q(f"(PDH-CSV 4.0) ({tz_label})({bias_minutes})")] + [q(c) for c in columns])]
    for t, vals in rows:
        if len(vals) != len(columns):
            raise ValueError("row length differs from header")
        cells = [q(t.strftime("%m/%d/%Y %H:%M:%S.") + f"{t.microsecond // 1000:03d}")]
        for v in vals:
            cells.append(q(" " if v is None else (str(v) if isinstance(v, int) else repr(float(v)))))
        out.append(",".join(cells))
    return "\n".join(out) + "\n"


def parse_typeperf_csv(text):
    """Return (columns, [(datetime, [float|None])]). Fails when a field is unquoted."""
    lines = [ln for ln in text.split("\n") if ln]
    for ln in lines:
        if not (ln.startswith('"') and ln.endswith('"')):
            raise ValueError("typeperf field not quoted")
    head = next(csv.reader([lines[0]]))
    if not head[0].startswith("(PDH-CSV 4.0) ("):
        raise ValueError("first field is not PDH-CSV 4.0")
    rows = []
    for ln in lines[1:]:
        f = next(csv.reader([ln]))
        t = dt.datetime.strptime(f[0], "%m/%d/%Y %H:%M:%S.%f")
        rows.append((t, [None if x.strip() == "" else float(x) for x in f[1:]]))
    return head[1:], rows


# ---- esxtop batch -----------------------------------------------------------

def esxtop_name(host, group, counter):
    r"""\\host\Group\Counter, e.g. \\h\Group Cpu(1234:vm)\% Ready."""
    return f"\\\\{host}\\{group}\\{counter}"


def esxtop_batch_csv(columns, rows):
    """esxtop -b: every field quoted, first field '(PDH-CSV 4.0) (UTC)(0)',
    time '"MM/DD/YYYY HH:MM:SS"' UTC, values with two decimals.
    Header and data rows have the same field count (the captured template
    differs by 100 fields; unresolved). columns: full names; rows: (datetime, values).
    """
    def q(s):
        return '"' + s + '"'
    out = [",".join([q("(PDH-CSV 4.0) (UTC)(0)")] + [q(c) for c in columns])]
    for t, vals in rows:
        if len(vals) != len(columns):
            raise ValueError("row length differs from header")
        out.append(",".join([q(t.strftime("%m/%d/%Y %H:%M:%S"))] + [q(f"{v:.2f}") for v in vals]))
    return "\n".join(out) + "\n"


def parse_esxtop_batch(text):
    """Return (columns, [(datetime, [float])]); raises when the field counts differ."""
    lines = [ln for ln in text.split("\n") if ln]
    head = next(csv.reader([lines[0]]))
    if head[0] != "(PDH-CSV 4.0) (UTC)(0)":
        raise ValueError("first field differs")
    rows = []
    for ln in lines[1:]:
        f = next(csv.reader([ln]))
        if len(f) != len(head):
            raise ValueError(f"data row has {len(f)} fields, header {len(head)}")
        rows.append((dt.datetime.strptime(f[0], "%m/%d/%Y %H:%M:%S"), [float(x) for x in f[1:]]))
    return head[1:], rows


# ---- esxtop panels ----------------------------------------------------------

@dataclass
class Col:
    """One panel column. width includes the lead; hlead/dlead are leading
    spaces of the header and data cell (left-aligned columns)."""
    header: str
    width: int
    align: str = "r"
    fmt: str = "%.2f"
    hlead: int = 0
    dlead: int = 0


def _cell(text, col, lead):
    s = " " * lead + text
    return s.ljust(col.width) if col.align == "l" else s.rjust(col.width)


def _fmt_cell(v, col, widen=True):
    if v is None:
        return _cell("-", col, col.dlead)
    if isinstance(v, str):
        return _cell(v, col, col.dlead)
    text = col.fmt % v
    if widen and col.align == "r" and len(text) >= col.width:
        text = " " + text      # esxtop widens the cell instead of gluing two numbers together
    return _cell(text, col, col.dlead)


def _g9(*names, fmt="%.2f"):
    return [Col(n, 9, fmt=fmt) for n in names]


PANEL_COLUMNS = {
    "c": [Col("ID", 11, fmt="%d"), Col("GID", 12, fmt="%d"), Col("NAME", 18, "l", "%s", 1, 1), Col("NWLD", 4, fmt="%d")]
         + [Col(n, 8) for n in ["%USED", "%RUN", "%SYS", "%WAIT", "%VMWAIT", "%RDY",
                                "%IDLE", "%OVRLP", "%CSTP", "%MLMTD", "%SWPWT"]],
    "m": [Col("GID", 11, fmt="%d"), Col("NAME", 18, "l", "%s", 1, 1), Col("MEMSZ", 7)]
         + _g9("GRANT", "CNSM", "SZTGT", "TCHD", "TCHD_W", "SWCUR", "SWTGT")
         + [Col("SWR/s", 8), Col("SWW/s", 8)]
         + _g9("LLSWR/s", "LLSWW/s", "OVHDUW", "OVHD", "OVHDMAX"),
    # memory panel after `f` toggled off every group except ID/name, MEMSZ, GRANT, CNSM and NUMA STATS
    "m-numa": [Col("GID", 11, fmt="%d"), Col("NAME", 18, "l", "%s", 1, 1), Col("MEMSZ", 10),
               Col("GRANT", 10), Col("CNSM", 10), Col("NHN", 5, fmt="%s"), Col("NMIG", 5, fmt="%d"),
               Col("NRMEM", 10), Col("NLMEM", 10), Col("N%L", 5, fmt="%d"), Col("GST_ND0", 10),
               Col("OVD_ND0", 9), Col("GST_ND1", 10), Col("OVD_ND1", 9)],
    "u": [Col("DEVICE", 37, "l", "%s"), Col("PATH/WORLD/PARTITION", 21, "l", "%s", 1, 10),
          Col("DQLEN", 6, fmt="%d"), Col("WQLEN", 6, fmt="%d"), Col("ACTV", 5, fmt="%d"),
          Col("QUED", 5, fmt="%d"), Col("%USD", 5, fmt="%d"), Col("LOAD", 6)]
         + _g9("CMDS/s", "READS/s", "WRITES/s", "MBREAD/s", "MBWRTN/s", "DAVG/cmd",
               "KAVG/cmd", "GAVG/cmd", "QAVG/cmd"),
    "d": [Col("ADAPTR", 7, "l", "%s", 1, 1), Col("PATH", 22, "l", "%s", 1, 1),
          Col("NPTH", 4, fmt="%d")]
         + _g9("CMDS/s", "READS/s", "WRITES/s", "MBREAD/s", "MBWRTN/s", "DAVG/cmd",
               "KAVG/cmd", "GAVG/cmd", "QAVG/cmd"),
    "v": [Col("GID", 11, fmt="%d"), Col("VMNAME", 18, "l", "%s", 1, 1), Col("VDEVNAME", 8),
          Col("NVDISK", 7, fmt="%d")]
         + _g9("CMDS/s", "READS/s", "WRITES/s", "MBREAD/s", "MBWRTN/s")
         + [Col("LAT/rd", 7, fmt="%.3f"), Col("LAT/wr", 7, fmt="%.3f")],
    "n": [Col("PORT-ID", 10, fmt="%d"), Col("USED-BY", 33, "l", "%s", 1, 1),
          Col("TEAM-PNIC", 9), Col("DNAME", 19, "l", "%s", 1, 1), Col("PKTTX/s", 8),
          Col("MbTX/s", 8), Col("PSZTX", 8), Col("PKTRX/s", 11), Col("MbRX/s", 8),
          Col("PSZRX", 8), Col("%DRPTX", 7), Col("%DRPRX", 7)],
}


def esxtop_status_line(clock, uptime, worlds, vms, vcpus, tail):
    """First panel line, e.g.
    '11:28:55am up 218 days 21:52, 849 worlds, 3 VMs, 7 vCPUs; CPU load average: 0.04, 0.04, 0.04'.
    tail: 'CPU load average: a, b, c' or 'MEM overcommit avg: a, b, c'."""
    return f"{clock} up {uptime}, {worlds} worlds, {vms} VMs, {vcpus} vCPUs; {tail}"


def esxtop_cpu_tail(load):
    """CPU load average tail for the status line."""
    return "CPU load average: " + ", ".join(f"{x:.2f}" for x in load)


def esxtop_cpu_summary(pcpu_used, pcpu_util, core_util, numa_used, numa_util, numa_core):
    """The three summary lines above the CPU table (PCPU USED, PCPU UTIL, CORE UTIL)."""
    def f(x):
        return f"{x:4.1f}" if x < 100 else f"{x:4.0f}"
    return [
        "PCPU USED(%): " + " ".join(f(x) for x in pcpu_used) + f" NUMA: {f(numa_used)} AVG: {f(numa_used)}",
        "PCPU UTIL(%): " + " ".join(f(x) for x in pcpu_util) + f" NUMA: {f(numa_util)} AVG: {f(numa_util)}",
        "CORE UTIL(%): " + "     ".join(f(x) for x in core_util) + f"     NUMA: {f(numa_core)} AVG: {f(numa_core)}",
    ]


def esxtop_mem_summary(total, vmk, other, free, managed, minfree, rsvd, ursvd, state):
    """PMEM and VMKMEM lines of the memory panel (the other header lines are
    omitted unless the caller adds them)."""
    return [
        f"PMEM  /MB: {total:6d}   total: {vmk:5d}     vmk,{other:5d} other, {free:6d} free",
        f"VMKMEM/MB: {managed:6d} managed: {minfree:5d} minfree, {rsvd:5d} rsvd, {ursvd:6d} ursvd,  {state} state",
    ]


def esxtop_panel(kind, status_line, rows, summary_lines=()):
    """Interactive esxtop panel as plain text (escape codes removed).
    kind: 'c','m','u','d','v','n'. rows: tuples matching PANEL_COLUMNS[kind];
    None prints '-'. Header line and rows end with a space, as in the samples."""
    cols = PANEL_COLUMNS[kind]
    lines = [status_line, *summary_lines,
             "".join(_cell(c.header, c, c.hlead) for c in cols) + " "]
    for r in rows:
        if len(r) != len(cols):
            raise ValueError("row length differs from panel columns")
        lines.append("".join(_fmt_cell(v, c, i > 0) for i, (v, c) in enumerate(zip(r, cols))) + " ")
    return "\n".join(lines) + "\n"


def parse_esxtop_panel(text, kind):
    """Rows of a panel as lists of strings (split on whitespace), keyed by
    the panel's header names: returns (header_names, [list of str]).
    Names must not contain spaces (the generated ones do not)."""
    lines = text.split("\n")
    first = PANEL_COLUMNS[kind][0].header
    for i, ln in enumerate(lines):
        if ln.split()[:1] == [first]:
            head = ln.split()
            rows = [l.split() for l in lines[i + 1:] if l.strip()]
            for r in rows:
                if len(r) != len(head):
                    raise ValueError(f"row has {len(r)} fields, header {len(head)}: {r}")
            return head, rows
    raise ValueError("panel header not found")


# ---- Linux text -------------------------------------------------------------

def linux_banner(kernel, host, date, ncpu):
    """sysstat banner: 'Linux <kernel> (<host>) <TAB>MM/DD/YYYY <TAB>_x86_64_<TAB>(N CPU)'."""
    return f"Linux {kernel} ({host}) \t{date} \t_x86_64_\t({ncpu} CPU)\n"


def top_summary(clock, uptime, users, load, tasks, cpu, mem_mib, swap_mib, procs=()):
    """top -b -n1: summary and process table (standard procps summary).
    tasks: (total, running, sleeping, stopped, zombie).
    cpu: dict us, sy, ni, id, wa, hi, si, st (percent, sum 100).
    mem_mib: (total, free, used, buff_cache); swap_mib: (total, free, used, avail_mem).
    procs: (pid, user, pr, ni, virt_kb, res_kb, shr_kb, state, cpu, mem, time, command).
    """
    l = [f"top - {clock} up {uptime},  {users} user,  load average: " + ", ".join(f"{x:.2f}" for x in load),
         "Tasks: %d total, %d running, %d sleeping, %d stopped, %d zombie" % tuple(tasks),
         "%%Cpu(s): %4.1f us, %4.1f sy, %4.1f ni, %4.1f id, %4.1f wa, %4.1f hi, %4.1f si, %4.1f st"
         % tuple(cpu[k] for k in ("us", "sy", "ni", "id", "wa", "hi", "si", "st")),
         "MiB Mem : %8.1f total, %8.1f free, %8.1f used, %8.1f buff/cache" % tuple(mem_mib),
         "MiB Swap: %8.1f total, %8.1f free, %8.1f used. %8.1f avail Mem " % tuple(swap_mib),
         "",
         "    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND"]
    for p in procs:
        l.append("%7d %-9s %3s %3d %7d %6d %6d %s %5.1f %5.1f %9s %s" % tuple(p))
    return "\n".join(l) + "\n"


def sar_u(kernel, host, date, ncpu, start_clock, rows, average,
          cols=("%user", "%nice", "%system", "%iowait", "%steal", "%idle")):
    """sar -u. start_clock: the time on the header row ('11:29:45 AM');
    rows: (clock, [values]); average: [values]. Layout as in the template."""
    out = [linux_banner(kernel, host, date, ncpu).rstrip("\n"), "",
           f"{start_clock:<11} {'CPU':>7}" + "".join(f"{c:>10}" for c in cols)]
    for clock, vals in rows:
        out.append(f"{clock:<11} {'all':>7}" + "".join(f"{v:>10.2f}" for v in vals))
    out.append(f"{'Average:':<11} {'all':>7}" + "".join(f"{v:>10.2f}" for v in average))
    return "\n".join(out) + "\n"


_IOSTAT_COLS = [("r/s", 8), ("rkB/s", 10), ("rrqm/s", 9), ("%rrqm", 7), ("r_await", 8),
                ("rareq-sz", 9), ("w/s", 8), ("wkB/s", 10), ("wrqm/s", 9), ("%wrqm", 7),
                ("w_await", 8), ("wareq-sz", 9), ("d/s", 8), ("dkB/s", 10), ("drqm/s", 9),
                ("%drqm", 7), ("d_await", 8), ("dareq-sz", 9), ("f/s", 8), ("f_await", 8),
                ("aqu-sz", 8), ("%util", 7)]
IOSTAT_COLUMNS = [n for n, _ in _IOSTAT_COLS]


def iostat_xd(kernel, host, date, ncpu, samples):
    """iostat -xd: samples is a list of blocks; a block is a list of
    (device, {column: value}); missing columns print 0.00. Blocks are
    separated by two blank lines, as in the template."""
    out = [linux_banner(kernel, host, date, ncpu).rstrip("\n"), ""]
    head = f"{'Device':<13}" + "".join(f"{n:>{w}}" for n, w in _IOSTAT_COLS)
    for block in samples:
        out.append(head)
        for dev, vals in block:
            out.append(f"{dev:<13}" + "".join(f"{vals.get(n, 0.0):>{w}.2f}" for n, w in _IOSTAT_COLS))
        out.extend(["", ""])
    return "\n".join(out) + "\n"


def parse_iostat_blocks(text):
    """Return a list of blocks, each {device: {column: float}}."""
    blocks, cur, cols = [], None, None
    for ln in text.split("\n"):
        if ln.startswith("Device"):
            cols = ln.split()[1:]
            cur = {}
            blocks.append(cur)
        elif cur is not None and ln.strip():
            f = ln.split()
            cur[f[0]] = dict(zip(cols, (float(x) for x in f[1:])))
    return blocks


def free_m(mem, swap):
    """free -m. mem: (total, used, free, shared, buff_cache, available); swap: (total, used, free)."""
    head = " " * 8 + "".join(f"{n:>12}" for n in ["total", "used", "free", "shared", "buff/cache", "available"])
    return "\n".join([head,
                      f"{'Mem:':<8}" + "".join(f"{v:>12d}" for v in mem),
                      f"{'Swap:':<8}" + "".join(f"{v:>12d}" for v in swap)]) + "\n"


def parse_free_m(text):
    """Return {'Mem': {col: int}, 'Swap': {col: int}}."""
    lines = text.splitlines()
    cols = lines[0].split()
    out = {}
    for ln in lines[1:]:
        f = ln.split()
        out[f[0].rstrip(":")] = dict(zip(cols, (int(x) for x in f[1:])))
    return out


def ip_s_link(ifaces):
    """ip -s link. Each iface: dict index, name, flags, mtu, qdisc, state, kind
    ('loopback' or 'ether'), rx=(bytes, packets, errors, dropped, missed, mcast),
    tx=(bytes, packets, errors, dropped, carrier, collsns). MACs print as xx:xx:...
    as in the template."""
    out = []
    for i in ifaces:
        mac = "xx:xx:xx:xx:xx:xx"
        out.append(f"{i['index']}: {i['name']}: <{i['flags']}> mtu {i['mtu']} qdisc {i['qdisc']} "
                   f"state {i['state']} mode DEFAULT group default qlen 1000")
        out.append(f"    link/{i['kind']} {mac} brd {mac}")
        w0 = max(len(str(i["rx"][0])), len(str(i["tx"][0])), 8)
        w1 = max(len(str(i["rx"][1])), len(str(i["tx"][1])), 7)
        for tag, names, vals in (("RX:", ["errors", "dropped", "missed", "mcast"], i["rx"]),
                                 ("TX:", ["errors", "dropped", "carrier", "collsns"], i["tx"])):
            if tag == "RX:":
                h = ["bytes", "packets", "errors", "dropped", "missed", "mcast"]
            else:
                h = ["bytes", "packets", "errors", "dropped", "carrier", "collsns"]
            widths = [w0, w1, 6, 7, 7, 7]
            out.append("    " + tag + h[0].rjust(widths[0] - 3) + "".join(" " + n.rjust(w) for n, w in zip(h[1:], widths[1:])) + " " * 11)
            out.append("    " + str(vals[0]).rjust(widths[0]) + "".join(" " + str(v).rjust(w) for v, w in zip(vals[1:], widths[1:])) + " ")
    return "\n".join(out) + "\n"


def parse_ip_s_link(text):
    """Return {iface: {'RX': {col: int}, 'TX': {col: int}}}."""
    res, cur, tag, cols = {}, None, None, None
    for ln in text.splitlines():
        if ln and not ln.startswith(" "):
            cur = ln.split(":")[1].strip()
            res[cur] = {}
        elif ln.strip().startswith(("RX:", "TX:")):
            tag = ln.strip()[:2]
            cols = ln.strip()[3:].split()
        elif cur and tag and ln.strip() and ln.strip()[0].isdigit() and cols and "/" not in ln:
            res[cur][tag] = dict(zip(cols, (int(x) for x in ln.split())))
            tag = None
    return res


def vmstat(rows):
    """vmstat (one line header). rows: (r, b, swpd, free, buff, cache, si, so, bi, bo, in, cs, us, sy, id, wa, st)."""
    out = ["procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----",
           " r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st"]
    for r in rows:
        out.append("%2d %2d %6d %6d %6d %6d %4d %4d %5d %5d %4d %4d %2d %2d %2d %2d %2d" % tuple(r))
    return "\n".join(out) + "\n"


def vmstat_swap_counters(pswpin, pswpout):
    """grep -E '^(pswpin|pswpout) ' /proc/vmstat (pages since boot)."""
    return f"pswpin {pswpin}\npswpout {pswpout}\n"


def mpstat_all(kernel, host, date, ncpu, clock, per_cpu, average_per_cpu=None):
    """mpstat -P ALL (standard sysstat layout, no template). per_cpu: list of
    [usr, nice, sys, iowait, irq, soft, steal, guest, gnice, idle], index 0 = 'all',
    then CPU 0..N-1. average_per_cpu: same shape, adds an 'Average:' block."""
    cols = ["%usr", "%nice", "%sys", "%iowait", "%irq", "%soft", "%steal", "%guest", "%gnice", "%idle"]

    def block(label, data):
        res = [f"{label:<11}  {'CPU':>3}" + "".join(f"{c:>8}" for c in cols)]
        for i, v in enumerate(data):
            name = "all" if i == 0 else str(i - 1)
            res.append(f"{label:<11}  {name:>3}" + "".join(f"{x:>8.2f}" for x in v))
        return res

    out = [linux_banner(kernel, host, date, ncpu).rstrip("\n"), ""]
    out += block(clock, per_cpu)
    if average_per_cpu is not None:
        out.append("")
        out += block("Average:", average_per_cpu)
    return "\n".join(out) + "\n"


def parse_mpstat(text):
    """Return {cpu_name: {column: float}} for the first block."""
    res, cols = {}, None
    for ln in text.splitlines()[2:]:
        if not ln.strip():
            break
        f = ln.split()
        if "CPU" in f:
            cols = f[f.index("CPU") + 1:]
        else:
            idx = 2 if f[1] in ("AM", "PM") else 1
            res[f[idx]] = dict(zip(cols, (float(x) for x in f[idx + 1:])))
    return res


def proc_pressure_memory(some, full):
    """/proc/pressure/memory (standard PSI text; ASSUMED, no template).
    some, full: (avg10, avg60, avg300, total_us)."""
    def line(tag, v):
        return f"{tag} avg10={v[0]:.2f} avg60={v[1]:.2f} avg300={v[2]:.2f} total={int(v[3])}"
    return line("some", some) + "\n" + line("full", full) + "\n"


def parse_pressure(text):
    """Return {'some': {avg10..total}, 'full': {...}}."""
    res = {}
    for ln in text.splitlines():
        tag, *kv = ln.split()
        res[tag] = {k: float(v) for k, v in (x.split("=") for x in kv)}
    return res


# ---- Windows text -----------------------------------------------------------

def systeminfo_virtual_memory(max_mb, available_mb, in_use_mb, page_files):
    """The systeminfo lines about virtual memory (MB with thousands separator)."""
    lines = [f"Virtual Memory: Max Size:  {max_mb:,} MB",
             f"Virtual Memory: Available: {available_mb:,} MB",
             f"Virtual Memory: In Use:    {in_use_mb:,} MB"]
    first = True
    for p in page_files:
        lines.append(("Page File Location(s):     " if first else " " * 27) + p)
        first = False
    return "\n".join(lines) + "\n"


def powershell_list(records, order):
    """Format-List output of Get-CimInstance: 'Name : value' lines, names padded
    to the longest, one blank line after each record. records: list of dicts."""
    w = max(len(k) for k in order)
    out = []
    for r in records:
        out += [f"{k:<{w}} : {r[k]}" for k in order]
        out.append("")
    return "\n".join(out) + "\n"


def win32_pagefileusage(records):
    """Get-CimInstance Win32_PageFileUsage | Format-List Name, AllocatedBaseSize, CurrentUsage, PeakUsage."""
    return powershell_list(records, ["Name", "AllocatedBaseSize", "CurrentUsage", "PeakUsage"])


def win32_processor(records):
    """Get-CimInstance Win32_Processor | Format-List with the fields
    SocketDesignation, Name, NumberOfCores, NumberOfLogicalProcessors."""
    return powershell_list(records, ["SocketDesignation", "Name", "NumberOfCores", "NumberOfLogicalProcessors"])
