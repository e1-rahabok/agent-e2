# IP storage: storage counters vs network counters

## Principle
- With IP storage (iSCSI, NFS, NVMe/TCP), every storage IO is also network traffic.
- Storage read and write do not map 1:1 to network Receive and Transmit.
- The mapping depends on the storage block size (normally 4 KB or 8 KB), the network packet size (MTU; ideally 9,000 bytes) and the TCP handshake packets.
- Storage counters measure the logical payload. Network counters measure whole frames: headers, encapsulation and acknowledgements in both directions.

## Header overhead per frame (iSCSI over IPv4 and TCP)
| Layer | Bytes |
|---|---|
| Ethernet II header | 14 |
| IPv4 header (no options) | 20 |
| TCP header (no options) | 20 |
| iSCSI Basic Header Segment (holds the 16-byte SCSI command) | 48 |
| Ethernet frame check sequence | 4 |

```text
Control frame with no payload = 14 + 20 + 20 + 48 + 4 = 106 bytes
```

## Example: one 8 KB iSCSI read
1. The host sends the read command: 1 Transmit packet, 106 bytes.
2. The array acknowledges it with a TCP ACK: 1 Receive packet, 64 bytes (minimum Ethernet frame with padding).
3. The array returns the data. MTU 9,000 allows a TCP segment of up to 8,960 bytes, so 8 KB fits in one frame: 1 Receive packet, 14 + 20 + 20 + 48 + 8,192 + 4 = 8,298 bytes.
4. The host acknowledges the data: 1 Transmit packet, 64 bytes.

| Counter on the host | Increase | From |
|---|---|---|
| Network Transmit packets | 2 | read command + ACK of the data |
| Network Transmit bytes | 170 | 106 + 64 |
| Network Receive packets | 2 | ACK of the command + data frame |
| Network Receive bytes | 8,362 | 64 + 8,298 |
| Storage read operations | 1 | one IO |
| Storage read bytes | 8,192 | logical payload |

- A read is mostly Receive. Transmit carries only the command and the acknowledgement.
- A write reverses the pattern: the data goes out as Transmit.

## Consequences
- Network bytes are not storage throughput. Subtract the headers and count the acknowledgements in both directions before comparing them.
- A 9,000-byte MTU keeps a 4 KB or 8 KB block in one frame: no IP fragmentation, so the overhead stays a fixed set of headers per IO.
- With a 1,500-byte MTU the same 8 KB block needs several frames, each with its own headers: more packets per IO and more overhead.

## Misconceptions
- "Storage reads appear as network Transmit because the host issues the command" → only the command is Transmit; the data returns as Receive.
- "Network Receive throughput equals storage read throughput" → network bytes include headers and acknowledgements.

## Metadata
```yaml
id: vsphere/technology/storage/concepts/ip-storage-network-accounting
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
- network
pillar:
- performance
product:
- vsphere
object:
- HostSystem
internal_derive:
- vsphere/technology/storage/concepts/storage-layers
related:
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/network/metrics/host/throughput
- vsphere/tools/esxtop/units-vs-vsphere-client
source:
  document: 'Technical note: Storage and Network Accounting for iSCSI over 10 GbE (Google Doc, read 2026-11-04)'
  path: https:/docs.google.com/document/d/1E7Or6rsJZ_P1MUZZfL1X3RSXPxhR2lW2fSp3wcaqnGo/edit
corrections: []
review_notes:
- 'Whole file: from the technical note linked in source.path. Replaces the book statement that read and write both map to network Transmit.'
- 'To check: Section ''Principle'': NFS and NVMe/TCP named as IP storage; the note covers iSCSI only.'
- 'To check: Sections ''Worked example'' (write reverses the pattern) and ''Consequences'' (1,500-byte MTU needs several frames): inferred from the note.'
status: draft
```
