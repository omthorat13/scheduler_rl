"""
Evaluates the trained RL scheduler against classic baselines on the SAME
held-out (by-time) test split, and produces a comparison bar chart.

Usage:
    python evaluate.py --trace data/synthetic_trace.csv --model models/dqn_scheduler.zip
"""
import argparse
import copy
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stable_baselines3 import DQN

from data.trace_loader import load_real_trace, train_test_split_by_time
from sim.baselines import ALL_BASELINES
from sim.env import SchedulerEnv


def eval_rl_agent(model, test_procs, historical_job_history=None, K=8):
    env = SchedulerEnv(
        trace_provider=lambda: copy.deepcopy(test_procs),
        K=K,
        initial_job_history=copy.deepcopy(historical_job_history or {}),
    )
    obs, _ = env.reset()
    terminated = False
    while not terminated:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(int(action))
    finished = [p for p in env.processes if p.finish_time is not None]
    n = len(finished)
    avg_wait = sum(p.waiting_time for p in finished) / n
    avg_turnaround = sum(p.turnaround_time for p in finished) / n
    avg_response = sum(p.response_time for p in finished) / n
    makespan = max(p.finish_time for p in finished) - min(p.arrival_time for p in finished)
    return {
        "avg_waiting_time": avg_wait,
        "avg_turnaround_time": avg_turnaround,
        "avg_response_time": avg_response,
        "throughput": n / makespan if makespan > 0 else 0.0,
        "completed": n,
        "makespan": makespan,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", default="data/synthetic_trace.csv")
    ap.add_argument("--model", default="models/dqn_scheduler.zip")
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--out-json", default="results/comparison.json")
    ap.add_argument("--out-plot", default="results/comparison.png")
    args = ap.parse_args()

    processes = load_real_trace(args.trace, has_header=False)
    _, test_procs = train_test_split_by_time(processes, args.train_frac)
    print(f"Evaluating on {len(test_procs)} held-out (later-arriving) processes")

    all_results = {}
    for name, fn in ALL_BASELINES.items():
        procs = copy.deepcopy(test_procs)
        result = fn(procs).metrics()
        all_results[name] = result
        print(f"{name:20s} avg_wait={result['avg_waiting_time']:.2f}  avg_turnaround={result['avg_turnaround_time']:.2f}")

    historical_job_history = {}
    for p in processes[:int(len(processes) * args.train_frac)]:
        historical_job_history.setdefault(p.job_id, []).append(float(p.burst_time))

    model = DQN.load(args.model)
    rl_result = eval_rl_agent(model, test_procs, historical_job_history=historical_job_history, K=args.K)
    all_results["RL (DQN direct policy)"] = rl_result
    print(f"{'RL (DQN direct policy)':20s} avg_wait={rl_result['avg_waiting_time']:.2f}  avg_turnaround={rl_result['avg_turnaround_time']:.2f}")

    with open(args.out_json, "w") as f:
        json.dump(all_results, f, indent=2)

    # ---- plot: avg waiting time comparison ----
    names = list(all_results.keys())
    waits = [all_results[n]["avg_waiting_time"] for n in names]
    colors = ["#4C72B0"] * len(names)
    colors[names.index("RL (DQN direct policy)")] = "#DD8452"
    colors[names.index("SRTF (oracle)")] = "#55A868"

    plt.figure(figsize=(9, 5))
    bars = plt.bar(names, waits, color=colors)
    plt.ylabel("Average Waiting Time")
    plt.title("Scheduler Comparison on Held-Out Trace Segment")
    plt.xticks(rotation=30, ha="right")
    for b, w in zip(bars, waits):
        plt.text(b.get_x() + b.get_width() / 2, w, f"{w:.0f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(args.out_plot, dpi=150)
    print(f"\nSaved results to {args.out_json} and {args.out_plot}")


if __name__ == "__main__":
    main()
