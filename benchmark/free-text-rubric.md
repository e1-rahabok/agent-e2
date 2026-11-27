# Free-text answer rubric

The scoring rubric of the judge that scored the benchmark's free-text answers 0-3 until every question became multiple choice (Q-E2-199). Copied word for word from `RUBRIC` and `SYSTEM` in [judge.py](https://github.com/e1-rahabok/agent-e2/blob/ebbc7dc0be3268abc0f4939fe1ea40e400ac9bbb/project/archive/legacy/judge-2026-11-14/judge.py) at commit ebbc7dc; the file itself is deleted and git history keeps it. The automated grader of the release 1.0 answer set ([R-E2-005](../project/requirements/answer-service.md), workspace milestone M3) scores by this rubric. Not indexed.

## Rubric

```text
Score the answer on this scale:
0 = wrong, or falls into the likely wrong answer, or contradicts a key point.
1 = avoids the likely wrong answer, but the reason is missing or wrong.
2 = correct conclusion, with the right reason (the mechanism or vantage point in the key points).
3 = as 2, and it also states what to check next, or covers every key point.

Rules:
- Judge facts, not style or length. Extra correct detail neither adds nor costs points.
- A statement that contradicts a key point caps the score at 0, even when other parts are right.
- An answer that says the question cannot be settled from the information available scores 0 and is marked unsure.
- The key points are the truth for this question, even where general IT practice says otherwise.
- Use only the key points and the question. Do not reward knowledge the key points do not contain.
```

## System prompt and reply format

The judge's system prompt was the first line below, then the rubric above, then the reply format:

```text
You grade answers to VMware vSphere and VCF operations questions against an expert answer key.
Reply with one JSON object and nothing else:
{"score": 0-3, "misconception": true|false, "unsure": true|false, "missed": "<key point missed, or empty>", "reason": "<one sentence>"}
misconception = the answer states the likely wrong answer (the Level 300 misconception).
```

## Input the judge read

- One user message: the question, then `Expected key points (the answer key)`, then `Likely wrong answer` (`(none given)` when the question has none), then `Answer to grade` (`(empty)` for an empty answer). The question's images followed the text.
- Temperature 0. A reply that was not valid JSON got one retry with the message `Reply with the JSON object only.`; a second bad reply failed the grading with its first 200 characters.
