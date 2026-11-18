"""Counter relations a generated export must keep (exports document, section 7.4).

Pure functions, no state. A case computes every derived value with these on
every row, and its check recomputes them from the re-parsed text. Units are
in the name: *_ms are milliseconds per sample, *_pct are percent.

Conventions (vCenter): KB = 1024 bytes, KBps = 1024 bytes per second,
Mbps = 1,000,000 bits per second. esxtop: MBytes = 1024 * 1024 bytes,
Mbits = 1,000,000 bits.
"""

REALTIME_INTERVAL_S = 20
MS_PER_SAMPLE = REALTIME_INTERVAL_S * 1000


# ---- CPU state time ---------------------------------------------------------

def vcpu_state_total_ms(vcpus, interval_s=REALTIME_INTERVAL_S):
    """Milliseconds all vCPUs of a VM have in one sample: vcpus x interval.

    One real-time sample is 20 s = 20,000 ms per vCPU. For a rollup the
    summation counters (Run, Ready, Co-stop, Wait) are the sum of the
    interval's samples, so pass the rollup interval (300 s for Past day,
    1800 s for Past week, 7200 s for Past month).
    """
    return vcpus * interval_s * 1000


def state_sum_ms(run_ms, ready_ms, costop_ms, wait_ms):
    """Run + Ready + Co-stop + Wait. Must equal vcpu_state_total_ms()."""
    return run_ms + ready_ms + costop_ms + wait_ms


def wait_from_states(vcpus, run_ms, ready_ms, costop_ms, interval_s=REALTIME_INTERVAL_S):
    """The Wait that closes the state sum: total - Run - Ready - Co-stop.

    Wait includes Idle and Swap wait, so a quiet VM has a large Wait.
    """
    return vcpu_state_total_ms(vcpus, interval_s) - run_ms - ready_ms - costop_ms


def readiness_pct(ready_ms, vcpus, interval_s=REALTIME_INTERVAL_S):
    """Readiness % = Ready ms / (vCPUs x interval ms) x 100.

    This is the average over the vCPUs, not the sum. A VM at 10% Readiness
    with 4 vCPUs has 8,000 ms Ready per 20 s sample.
    """
    return 100.0 * ready_ms / vcpu_state_total_ms(vcpus, interval_s)


def ready_ms_from_readiness(readiness, vcpus, interval_s=REALTIME_INTERVAL_S):
    """Inverse of readiness_pct(): Ready ms for a Readiness %."""
    return readiness * vcpu_state_total_ms(vcpus, interval_s) / 100.0


def ms_to_pct(ms, interval_s=REALTIME_INTERVAL_S):
    """A per-vCPU millisecond counter as a percent of one interval."""
    return 100.0 * ms / (interval_s * 1000)


def pct_to_ms(pct, interval_s=REALTIME_INTERVAL_S):
    """Percent of one interval as milliseconds (per vCPU)."""
    return pct * interval_s * 1000 / 100.0


# ---- Rollups ----------------------------------------------------------------

def rollup_mean(samples):
    """Rollup point of an average counter (Usage, Readiness, latency): the
    mean of the samples in the interval. 15 real-time samples make one
    5-minute point; 90 make a 30-minute point; 360 make a 2-hour point."""
    samples = list(samples)
    return sum(samples) / len(samples)


def rollup_sum(samples):
    """Rollup point of a summation counter (Ready ms, Run ms, ...): the
    sum of the samples in the interval, not the mean."""
    return sum(samples)


def rollup_windows(values, per_window):
    """Split values into consecutive windows of per_window samples.
    A trailing partial window is dropped."""
    n = len(values) // per_window
    return [values[i * per_window:(i + 1) * per_window] for i in range(n)]


def rollup_means(values, per_window):
    """Mean of each consecutive window."""
    return [rollup_mean(w) for w in rollup_windows(values, per_window)]


def rollup_sums(values, per_window):
    """Sum of each consecutive window."""
    return [rollup_sum(w) for w in rollup_windows(values, per_window)]


def samples_per_rollup(interval_s, base_s=REALTIME_INTERVAL_S):
    """How many base samples one rollup point holds."""
    return interval_s // base_s


# ---- Storage ----------------------------------------------------------------

def weighted_latency(read_ms, reads, write_ms, writes):
    """Command latency: read and write latency weighted by their request
    counts. A few slow writes hide behind many fast reads."""
    total = reads + writes
    if total == 0:
        return 0.0
    return (read_ms * reads + write_ms * writes) / total


def outstanding_io(iops, latency_ms):
    """Little's law: outstanding = IOPS x latency (seconds)."""
    return iops * latency_ms / 1000.0


def iops_for_outstanding(outstanding, latency_ms):
    """Little's law solved for IOPS."""
    return outstanding * 1000.0 / latency_ms


def gavg(davg_ms, kavg_ms):
    """esxtop GAVG/cmd = DAVG/cmd + KAVG/cmd."""
    return davg_ms + kavg_ms


def qavg_within_kavg(qavg_ms, kavg_ms, tol=0.0):
    """QAVG is part of KAVG, so QAVG <= KAVG."""
    return qavg_ms <= kavg_ms + tol


def iops_weighted_mean(values, iops):
    """Aggregate latency over several disks: mean weighted by each disk's IOPS."""
    total = sum(iops)
    if total == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, iops)) / total


# ---- Network ----------------------------------------------------------------

def vmnic_usage(receive, transmit):
    """vCenter vmnic Usage = receive rate + transmit rate (same unit, KBps)."""
    return receive + transmit


def bytes_per_packet(kbytes_per_s, packets_per_s):
    """Average packet size in bytes from a KBps rate (1 KB = 1024 bytes)."""
    if packets_per_s == 0:
        return 0.0
    return kbytes_per_s * 1024.0 / packets_per_s


def kbytes_per_s_for_packets(packets_per_s, bytes_per_pkt):
    """KBps that a packet rate and size produce."""
    return packets_per_s * bytes_per_pkt / 1024.0


# ---- esxtop and aggregation -------------------------------------------------

def esxtop_wait(vmwait_pct, idle_pct):
    """esxtop %WAIT of a vCPU world = %VMWAIT + %IDLE."""
    return vmwait_pct + idle_pct


def group_sum(worlds):
    """esxtop group row = sum of its worlds, column by column.
    worlds: list of equal-length lists of numbers; returns the sum list."""
    return [sum(col) for col in zip(*worlds)]


def cluster_mean(host_values):
    """Cluster value of a percent metric over identical hosts = mean of hosts."""
    host_values = list(host_values)
    return sum(host_values) / len(host_values)


def load_ratio(load_average, vcpus):
    """Load average per vCPU."""
    return load_average / vcpus


# ---- Units ------------------------------------------------------------------

def kb_to_bytes(kb):
    """KB (vCenter, 1024 bytes) to bytes."""
    return kb * 1024


def kbit_to_bits(kbit):
    """kb (kilobit, 1000 bits) to bits. KB and kb differ by 8192/1000."""
    return kbit * 1000


def kbps_to_mbps(kbytes_per_s):
    """vCenter KBps (1024 bytes/s) to Mbps (1,000,000 bit/s)."""
    return kbytes_per_s * 1024 * 8 / 1_000_000


def mbps_to_kbps(mbit_per_s):
    """Mbps to vCenter KBps."""
    return mbit_per_s * 1_000_000 / 8 / 1024


def mbytes_per_s_to_mbit_per_s(mbytes_per_s):
    """esxtop MBREAD/s (MB/s) to Mbit/s: x 8 x 1.048576."""
    return mbytes_per_s * 1024 * 1024 * 8 / 1_000_000


def kb_to_mb(kb):
    """KB to MB (1024)."""
    return kb / 1024.0
