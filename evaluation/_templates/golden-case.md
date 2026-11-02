# Golden Evaluation Case Template

**ID**: unique-id (e.g. `cpu-host-not-responding-01`)  
**Category**: cpu / memory / storage / network / foundations / general  
**Type**: text | screenshot | diagram | log | mixed  
**Difficulty**: basic | intermediate | advanced  
**Last Updated**: YYYY-MM-DD  
**Source**: live-lab / real-ticket / synthetic / book  

## Input

### User Prompt
The exact (or realistic) text the user would type.

### Attachments (if any)
- `screenshots/hostname-not-responding.png` — Description of what the screenshot shows
- `diagrams/cluster-layout.drawio` — Short description
- `logs/vpxa-excerpt.log` — Relevant portion

## Expected Behavior

### Key Points the Answer Must Cover
- Point 1
- Point 2
- Point 3

### Correct Reasoning Path
High-level description of the diagnostic or explanatory path the AI should follow.

### Relevant Knowledge Areas
Which parts of the knowledge base should be retrieved (e.g. `foundations/metrics-philosophy`, `cpu/resource-management`, specific counters, etc.).

### What a Bad Answer Looks Like
Common failure modes (shallow reply, mixed Host/VM perspective, missing nuance, hallucination, etc.).

## Notes
Any additional context, edge cases, or tribal knowledge related to this case.
