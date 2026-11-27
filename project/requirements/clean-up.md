# Requirements: clean-up of agent-e2

The clean-up of agent-e2 in milestone M2 of the workspace's [ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md): the plan for release 1.0 and the older benchmarks. Question IDs point at the interview ([round 1](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/interview-round-1.md), [round 2](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/interview-round-2.md), [round 3](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/interview-round-3.md), [round 4](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/interview-round-4.md)); other IDs are explained in the [glossary](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/glossary.md).

## Agent E2's repository for release 1.0

### R-REPO-003 Agent E2's plan describes release 1.0

Milestone: M2.

Source: Q-WS-6 (round 1: "Update Agent E2's plan. It's outdated."); Q-WS-58 (round 2: milestones A1 to A6).

- Given Agent E2's [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md)
- When a session reads it at the start of work
- Then its milestones are A1 to A6 as decided in Q-WS-58, with the items of the on-premises deployment (local model, offline bundle, live test with blocked network) listed as parked
- And its fine-tuning row points to the workspace's [design note](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/design/fine-tuning.md)
- And agent-e2's CLAUDE-PROJECT.md sends questions that bind several repositories to this workspace (WD-019)

Test scenarios:
- T-REPO-003a (anywhere, manual review): the plan's milestone table has A1 to A6 and a parked row for the on-premises deployment; agent-e2's rules check passes.

### R-REPO-004 The older benchmarks are removed

Milestone: M2.

Source: Q-WS-12 (round 1: "Remove them permanently."); Q-WS-59 (round 2: what is removed and what stays).

- Given the older benchmark material listed in Q-WS-59
- When the removal is merged
- Then the result folders from before 2026-11-16, the retired questions, the old harness code and its design notes, the old plan decisions and review, and the retrieval results of 2026-11-14 are deleted from main
- And the round of 2026-11-16 and the question-set history files stay
- And the free-text judge's scoring rubric is kept first, in agent-e2's benchmark folder, for the new grader of M3
- And the live documents that quote old numbers (MISSION.md, README.md, harness/README.md, harness/AGENT.md, benchmark/design.md, benchmark/models.md) are rewritten without them
- And git history is not rewritten

Test scenarios:
- T-REPO-004a (anywhere, automated by agent-e2's rules check and its unit tests): both pass after the removal.
- T-REPO-004b (anywhere, automated by a link search to write): no file on main links to a deleted path.
