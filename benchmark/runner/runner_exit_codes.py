"""Exit codes of answer_questions_for_one_model.py and run_all_models_in_one_round.py. One meaning each, so a script (or the LLM that runs a round) can decide what to do next."""
OK = 0              # finished: report written
CRASHED = 1         # unexpected error (Python raises 1): relaunch with --resume
USAGE = 2           # bad flags (argparse)
STOPPED = 3         # stopped at --max-minutes: relaunch with --resume, no change
PREFLIGHT = 4       # preflight failed: nothing was run, or the run was refused (credits, projection)
UNHEALTHY = 5       # the answers were invalid (cut off, unparsable, errors): run stopped, nothing to resume
BUDGET = 6          # the gateway refused for credits or key budget (HTTP 402) or the key (401, 403): top up, then relaunch
PARTIAL = 7         # run_all: some runs finished, others failed (see the printed list)
GATEWAY_DOWN = 8    # the gateway or a provider kept failing (HTTP 5xx, 429, timeouts): not a setting problem. Wait, then relaunch the same folder with --resume (run_all does it)
