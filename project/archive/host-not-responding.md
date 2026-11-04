# Troubleshooting Flow: Host Not Responding in vCenter

**Title**: Host shows as Not Responding / Disconnected in vCenter  
**Applies to**: vSphere 7.x / 8.x / VCF 9.x  
**Last Updated**: 2026-11-01  
**Author / Source**: Common field experience + official guidance  

## Symptoms
- Host appears as **Not Responding** or **Disconnected** in vCenter Inventory
- VMs on the host may show as disconnected or have issues
- vCenter cannot communicate properly with the host

## Quick Checks (before deep troubleshooting)
- [ ] Can you ping the host management IP from vCenter or another machine?
- [ ] Is the host showing in DCUI / Direct Console?
- [ ] Are there any recent changes (network, firewall, certificates, patches)?
- [ ] Check if other hosts in the same cluster are healthy

## Decision Flow

```text
Start: Host Not Responding
├─ Can you ping the host management IP?
│  ├─ No  → Network / Physical connectivity problem → Check physical network, upstream switches, host vmknic
│  └─ Yes → Go to next check
├─ Can you open DCUI or SSH to the host?
│  ├─ No  → Host may be crashed / PSOD / management agents down → Check DCUI, logs via alternate methods, consider reboot
│  └─ Yes → Go to next check
├─ Are management agents (hostd / vpxa) running?
│  ├─ No  → Restart management agents
│  └─ Yes → Check vpxa / hostd logs for connection errors with vCenter
├─ Certificate or SSL issue?
│  ├─ Yes → Certificate problem → Check and renew certificates
│  └─ No  → Continue with log analysis and deeper checks
```

## Detailed Steps

### 1. Verify basic connectivity
- Ping the host management VMkernel interface from vCenter Server.
- From the host, ping the vCenter Server IP.
- Expected: Successful ping both ways.

### 2. Check management agents
On the host (SSH or DCUI):
```bash
/etc/init.d/hostd status
/etc/init.d/vpxa status
```
If not running, restart them:
```bash
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
```

### 3. Review key logs
- `/var/log/hostd.log`
- `/var/log/vpxa.log`
- Look for connection resets, SSL errors, authentication failures, or resource exhaustion.

### 4. Certificate check
- Verify the host certificate is valid and trusted by vCenter.
- Common fix: Renew/refresh host certificate from vCenter or using `vpxd` tools.

## Common Root Causes
| Root Cause                    | How to Confirm                          | Resolution                              |
|-------------------------------|-----------------------------------------|-----------------------------------------|
| Management network issue      | Ping fails                              | Fix network / vmknic / upstream         |
| hostd or vpxa crashed         | Agents not running or frequent restarts | Restart agents, check for core dumps    |
| SSL / Certificate problem     | SSL errors in vpxa/hostd logs           | Refresh certificates                    |
| Host overloaded / PSOD        | DCUI inaccessible or purple screen      | Collect logs, reboot if necessary       |
| Firewall blocking             | Connectivity intermittent               | Check esxcli network firewall rules     |

## Related Faults / Log Signatures
- vpxa connection errors
- hostd agent connection failures
- SSL handshake failures

## Related Performance Counters / Properties
- `runtime.connectionState`
- Host CPU / Memory pressure counters (if host is alive but unresponsive)

## Notes & Gotchas
- A host can be pingable but still show as Not Responding if the management agents are hung.
- Always check both hostd and vpxa.
- After fixing, it can take a minute or two for vCenter to update the host status.
- In VCF environments also check SDDC Manager health if the host is part of a workload domain.

## Metadata
```yaml
id: vsphere/system/diagnosis/host-not-responding
retriever_guide: what-to-check
scope: vsphere
technology:
- system
pillar:
- availability
product:
- vsphere
object:
- HostSystem
internal_derive: []
related: []
source:
  document: Not from the book. Generic content from an earlier repository version.
  path: n/a
corrections: []
review_notes:
- Not from the book or an official source. Level 200 content. Author to decide whether to keep, rewrite, or remove.
status: draft
```
