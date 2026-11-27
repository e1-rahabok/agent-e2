# Requirements: the knowledge export for isvara.io

What Agent E2 publishes for isvara.io to build its articles from, and how it is tested. The export is contract C4, knowledge content for isvara.io; its shape and its check are in the workspace's [knowledge-export.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/requirements/knowledge-export.md). Every requirement here belongs to milestone M4 in the workspace's [ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md). IDs are explained in the [glossary](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/glossary.md).

### R-E2-027 The export holds every knowledge file, with what an article needs

Source: Q-WS-41 (the recommendation of one record per published file; the author asked to review the change first, in the [before and after](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/design/isvara-before-and-after.md)); [WD-005](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/DECISIONS.md); [WD-027](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/DECISIONS.md).

- Given agent-e2 at one commit
- When the export tool runs
- Then it writes one record per knowledge file under `knowledge/`: its ID, title, sections with their text, misconceptions, the tags `retriever_guide`, `technology`, `pillar`, `product`, `object`, `layer` and `metric_class`, its `related` and `internal_derive` files, its images with their tags, its `source.path`, the catalog rows it cites, a fingerprint of its text and the date it last changed
- And it writes the catalog, the glossary and the `user-terms` rows
- And it records the commit it was written from

Test scenarios:
- T-E2-027a (anywhere, automated by a unit test of the export tool, to write): every Markdown file under `knowledge/` has one record with every field; a fixture file changed by one word gets a new fingerprint.
- T-E2-027b (anywhere, the same test): every `related`, `internal_derive` and image path of every record resolves to a record or an image file of the export.

### R-E2-028 KNOWLEDGE-ENGINEERING.md holds the knowledge model

Source: [WD-035](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/DECISIONS.md) (adding the knowledge model to agent-e2's KNOWLEDGE-ENGINEERING.md stays in release 1.0); [WD-027](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/DECISIONS.md).

- Given the workspace's [knowledge model](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/knowledge-model.md)
- When a session reads agent-e2's [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md)
- Then it finds the three learning paths and the tags each comes from, the four lenses as a completeness check with the form that serves each lens, and the Day 2 boundary
- And the forms deferred by WD-035 (workload footprints, investigations over several steps, "At large scale" notes) are named as after release 1.0

Test scenarios:
- T-E2-028a (anywhere, automated by agent-e2's rules check, extended): KNOWLEDGE-ENGINEERING.md names each value of `retriever_guide` under one lens, and each path's tag; a form under no lens fails.
