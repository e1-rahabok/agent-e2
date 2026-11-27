# CLAUDE.md

Rules for Claude in spec-driven development, for any project. The project's own rules, tools and paths are in [CLAUDE-PROJECT.md](CLAUDE-PROJECT.md), loaded with this file:

@CLAUDE-PROJECT.md

## Order of work

- Work only on the earliest milestone in ROADMAP.md that is not done. The project's hook prints it at every prompt.
- When a request belongs to a later milestone: list it as parked, in one line, and act on nothing in it.
- When the author makes a suggestion: reply with strengths, weaknesses, gaps and a recommendation. Write to a repository only after the author agrees, or says "do it" or "decide".
- Write `: done` on a milestone's heading only after the author approves it, from its review page when it has one.

## Before acting

- Read ROADMAP.md, the files the request touches, and the CLAUDE.md of each repository it touches.
- Before asking the author: search DECISIONS.md, the glossary and the interview records, and quote what they say.
- Decide what the code, the documents or knowledge of the field settle, and state the decision. Ask the author only about judgement, experience, scope and taste.
- Verify a claim from an audit, a review or another session against the files. Report a contradiction with both sources.

## Replies to the author

- Bullet points and short sentences. Each name in full on first use.
- Separate what you know, what you believe and what you have not checked. Disagree when there is a reason.
- Describe how two parts relate by mechanism: code, network, data, dependency or contract.

## Stop and ask

Stop the line of work, add a question with a recommendation and an empty `Answer:` line to OPEN-QUESTIONS.md, and tell the author, when:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract's shape or reverse a decision;
- a test needs a system that cannot be reached. Report the test as not run.

## Requirements

- Every requirement cites the question or decision it comes from.
- Every requirement has at least one test scenario, and every test scenario names its requirement.
- Before writing a requirement on existing behaviour: read the code that implements it.

## Tests and checks

- Never weaken, skip, delete or loosen a test or a check. A failure is a bug to fix or a question for the author.
- Change a contract between two parts in three steps: add the new shape, move each consumer, remove the old shape.
- Give every new contract a check, or a ROADMAP line that adds one. Add a gap to a check's baseline only with a question in OPEN-QUESTIONS.md.
- Before each commit: run and pass the checks listed in CLAUDE-PROJECT.md.

## Writing

- Machine documents: CLAUDE.md, CLAUDE-PROJECT.md and the requirement files. One rule or fact per bullet, trigger before action, exact names, no history.
- All other documents, commit messages and pull request text are for people. Follow the writing rules named in CLAUDE-PROJECT.md. Reread each changed line for slogans and "X, not Y".
- Every file reference a link. Every ID with its meaning or a glossary link on first use. Each paragraph on one source line.
- A new ID prefix, term or heading must be guessable from itself and overlap no existing one. When a name stops being true: rename it in every file.

## Decisions, questions and Git

- Record each decision in DECISIONS.md, one block per decision, with its date and reason.
- One branch and one pull request per change. Mark finished ROADMAP lines with their pull request. Never push to a default branch.
- Never merge while checks are pending or failing.
- Put a warning at the top of the pull request and the report when a contract's shape changes, a decision changes, or files are deleted.
- Wait for the author before deleting data. Never print, log or commit a credential.

## Session end

- When work remains: give the author a prompt for the next session: files to read, settled scope, tasks, how to report.
