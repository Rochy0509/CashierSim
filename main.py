import simpy
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.simulation import CheckoutSystem

RANDOM_SEED = 42
CASES = [20, 40, 60]

all_metrics = {}

for num in CASES:
    np.random.seed(RANDOM_SEED)
    env = simpy.Environment()
    checkout = CheckoutSystem(env)
    env.process(checkout.generate_arrivals(num))
    env.run()

    metrics = checkout.calculate_metrics()
    all_metrics[num] = metrics

    print(f"\n--- Case: {num} Customers (Served: {len(checkout.customers)}) ---")
    print(f"  Avg Wait: {metrics['avg_waiting_time']:.2f} min | "
          f"Avg System Time: {metrics['avg_time_in_system']:.2f} min")
    print(f"  P(Wait): {metrics['probability_of_waiting']:.2%} | "
          f"Utilization: {metrics['cashier_utilization']:.2f}% | "
          f"Idle: {metrics['idle_time_percentage']:.2f}%")

labels = [f"{c} cust" for c in CASES]
x = np.arange(len(CASES))
w = 0.25

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Checkout System — Comparative Analysis", fontsize=14, fontweight='bold')

axes[0, 0].bar(x, [all_metrics[c]['avg_waiting_time'] for c in CASES], width=w, color='#e74c3c')
axes[0, 0].set_title("Avg Waiting Time (min)")
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(labels)
for i, c in enumerate(CASES):
    axes[0, 0].text(i, all_metrics[c]['avg_waiting_time'] + 0.1,
                    f"{all_metrics[c]['avg_waiting_time']:.2f}", ha='center', fontsize=9)

axes[0, 1].bar(x, [all_metrics[c]['avg_time_in_system'] for c in CASES], width=w, color='#3498db')
axes[0, 1].set_title("Avg Time in System (min)")
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(labels)
for i, c in enumerate(CASES):
    axes[0, 1].text(i, all_metrics[c]['avg_time_in_system'] + 0.1,
                    f"{all_metrics[c]['avg_time_in_system']:.2f}", ha='center', fontsize=9)

util_vals = [all_metrics[c]['cashier_utilization'] for c in CASES]
idle_vals = [all_metrics[c]['idle_time_percentage'] for c in CASES]
axes[1, 0].bar(x - w/2, util_vals, width=w, color='#2ecc71', label='Utilization')
axes[1, 0].bar(x + w/2, idle_vals, width=w, color='#95a5a6', label='Idle')
axes[1, 0].set_title("Cashier Utilization vs Idle (%)")
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(labels)
axes[1, 0].legend()

prob_vals = [all_metrics[c]['probability_of_waiting'] * 100 for c in CASES]
axes[1, 1].bar(x, prob_vals, width=w, color='#f39c12')
axes[1, 1].set_title("Probability of Waiting (%)")
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(labels)
for i, v in enumerate(prob_vals):
    axes[1, 1].text(i, v + 0.5, f"{v:.1f}%", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig("images/comparative_analysis.png", dpi=150)
print("\nChart saved to images/comparative_analysis.png")

util_60 = all_metrics[60]['cashier_utilization']
if util_60 < 80:
    print(f"\nConclusion: Utilization at 60 customers is {util_60:.2f}% (<80%). One cashier is sufficient.")
else:
    print(f"\nConclusion: Utilization at 60 customers is {util_60:.2f}% (>=80%). Consider a second cashier.")