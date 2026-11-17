"""
Live step-by-step demo of the RL scheduler's decision process -- for showing
in a viva/demo, not for generating report numbers (use evaluate.py for that).

For each of the first N scheduling decisions, prints:
  - the current ready queue (up to 8 candidates the agent can see)
  - each candidate's OBSERVABLE features (waiting time, priority, historical
    average burst estimate -- NOT the true burst time, since the agent can't
    see that either)
  - which one the agent picked, and its TRUE burst time (revealed only in
    this printout, for your own sanity-check / narration -- the agent never
    sees this value)
  - for contrast: what FCFS would have picked at the same moment

Usage:
    python demo_trace.py --trace data/synthetic_trace.csv --model models/dqn_scheduler_best.zip --steps 6
"""
import argparse
import copy
from stable_baselines3 import DQN
from data.trace_loader import load_real_trace, train_test_split_by_time
from sim.env import SchedulerEnv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", default="data/synthetic_trace.csv")
    ap.add_argument("--model", default="models/dqn_scheduler_best.zip")
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--steps", type=int, default=6, help="how many decisions to show")
    ap.add_argument("--skip", type=int, default=0, help="advance this many decisions silently first, so the demo starts once the queue is already full/interesting")
    args = ap.parse_args()

    processes = load_real_trace(args.trace, has_header=True)
    train_procs, test_procs = train_test_split_by_time(processes, args.train_frac)
    historical_job_history = {}
    for p in train_procs:
        historical_job_history.setdefault(p.job_id, []).append(float(p.burst_time))

    model = DQN.load(args.model)
    env = SchedulerEnv(
        trace_provider=lambda: copy.deepcopy(test_procs),
        K=args.K,
        initial_job_history=copy.deepcopy(historical_job_history),
    )
    obs, _ = env.reset()

    # silently advance past the early decisions so the demo opens with a
    # fuller, more illustrative queue rather than the 1-2-candidate startup
    for _ in range(args.skip):
        cands = env._candidates()
        action = args.K + 1 if not cands else (model.predict(obs, deterministic=True)[0])
        obs, reward, terminated, truncated, info = env.step(int(action))
        if terminated:
            print("Trace ended during skip phase -- reduce --skip.")
            return

    print("=" * 78)
    print(f"LIVE TRACE: RL scheduler decisions on held-out (unseen) processes")
    print(f"({len(test_procs)} processes total, showing first {args.steps} decisions)")
    print("=" * 78)

    for step in range(args.steps):
        cands = env._candidates()
        if not cands:
            print(f"\n[decision {step+1}] queue empty, fast-forwarding to next arrival...")
            action = args.K + 1  # force the empty-queue path
            obs, reward, terminated, truncated, info = env.step(action)
            continue

        print(f"\n--- Decision {step+1}  (simulated time = {env.now:.1f}) ---")
        print(f"{'slot':<5}{'job_id':<10}{'waited':<10}{'priority':<10}{'hist_avg_burst':<16}{'confidence':<12}")
        for i, p in enumerate(cands):
            waited = env.now - p.last_ready_time
            hist = env.job_history.get(p.job_id, [])
            hist_str = f"{sum(hist)/len(hist):.1f}" if hist else "no history"
            conf = f"{len(hist)} samples" if hist else "none yet"
            print(f"{i:<5}{p.job_id:<10}{waited:<10.1f}{p.priority:<10}{hist_str:<16}{conf:<12}")

        # what FCFS would pick: earliest arrival = slot 0 by construction
        fcfs_choice = 0

        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        if action >= len(cands):
            print(f"  -> RL agent chose slot {action}, but only {len(cands)} candidate(s) exist "
                  f"-> falls back to slot 0 (earliest-arrived), small penalty applied")
            effective_action = 0
        else:
            effective_action = action
        chosen = cands[effective_action]

        print(f"  -> Dispatched: job {chosen.job_id} (slot {effective_action}), "
              f"TRUE burst={chosen.burst_time:.1f}s -- hidden from the agent, shown here for narration")
        if effective_action == fcfs_choice:
            print(f"     (same choice FCFS would make here)")
        else:
            fcfs_pick = cands[fcfs_choice]
            print(f"     (FCFS would have picked slot 0 instead: job {fcfs_pick.job_id}, "
                  f"true burst={fcfs_pick.burst_time:.1f}s)")

        obs, reward, terminated, truncated, info = env.step(action)
        if terminated:
            break

    print("\n" + "=" * 78)
    print("End of trace. Run evaluate.py for full aggregate metrics across all")
    print("150 held-out processes and all baseline schedulers.")
    print("=" * 78)


if __name__ == "__main__":
    main()
