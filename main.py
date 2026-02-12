import simpy
import random
from src.simulation import CheckoutSystem

RANDOM_SEED = 42
NEW_CUSTOMERS = 60
INTERVAL_CUSTOMERS = 10.0

random.seed(RANDOM_SEED)

env = simpy.Environment()
checkout = CheckoutSystem(env)
env.process(checkout.generate_arrivals(NEW_CUSTOMERS))
env.run()

print(f"Customers served: {len(checkout.customers)}")
for customer in checkout.customers:
    print(f"Customer {customer.id}: Waited {customer.waiting_time:.2f} min, Total time {customer.time_in_system:.2f} min")


metrics = checkout.calculate_metrics()
print("\nMetrics:", metrics)