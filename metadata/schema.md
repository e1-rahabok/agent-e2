# Metadata Schema

Common metadata fields that should be attached to documents and structured knowledge entries.

## Recommended fields

| Field | Description | Example |
|-------|-------------|--------|
| `component` | Main product area | `vsphere`, `nsx`, `vsan` |
| `subcomponent` | More specific area | `esxi`, `vcenter`, `ha`, `drs` |
| `type` | Knowledge type | `troubleshooting`, `error`, `config`, `metric`, `glossary` |
| `versions` | Applicable versions | `["8.0", "9.0", "VCF-9.1"]` |
| `severity` | For errors | `error`, `warning` |
| `source` | Origin of the knowledge | `official-doc`, `lab-verified`, `tribal` |
| `last_updated` | ISO date | `2026-11-01` |

This schema will be used both in structured files and when indexing for RAG.
