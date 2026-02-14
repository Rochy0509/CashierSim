import simpy
from src.customer import Customer
from src.utils import generate_service_time, generate_interarrival_time

OPERATING_MINUTES = 540

class CheckoutSystem:

    def __init__(self, env):
        self.env = env
        self.cashier = simpy.Resource(env, capacity=1)
        self.customers = []

    def customer_process(self, customer):
        with self.cashier.request() as request:
            yield request

            customer.service_start_time = self.env.now
            customer.service_time = generate_service_time()

            yield self.env.timeout(customer.service_time)

            customer.completion_time = self.env.now

        self.customers.append(customer)

    def generate_arrivals(self, num_customers):
        for i in range(num_customers):
            interarrival = generate_interarrival_time()
            yield self.env.timeout(interarrival)
            if self.env.now > OPERATING_MINUTES:
                break
            customer = Customer(i + 1, self.env.now, interarrival)
            self.env.process(self.customer_process(customer))

    def calculate_metrics(self):
        if len(self.customers) == 0:
            return {
                'avg_waiting_time': 0,
                'avg_time_in_system': 0,
                'probability_of_waiting': 0,
                'cashier_utilization': 0,
                'idle_time_percentage': 100,
                'total_customers': 0,
                'total_service_time': 0
            }

        total_waiting_time = sum(c.waiting_time for c in self.customers)
        avg_waiting_time = total_waiting_time / len(self.customers)

        total_time_in_system = sum(c.time_in_system for c in self.customers)
        avg_time_in_system = total_time_in_system / len(self.customers)

        customers_who_waited = sum(1 for c in self.customers if c.waiting_time > 0)
        probability_of_waiting = customers_who_waited / len(self.customers)

        total_service_time = sum(c.service_time for c in self.customers)

        last_completion = max(c.completion_time for c in self.customers)
        total_time = max(last_completion, OPERATING_MINUTES)
        cashier_utilization = (total_service_time / total_time) * 100

        idle_time_percentage = 100 - cashier_utilization

        return {
            'avg_waiting_time': avg_waiting_time,
            'avg_time_in_system': avg_time_in_system,
            'probability_of_waiting': probability_of_waiting,
            'cashier_utilization': cashier_utilization,
            'idle_time_percentage': idle_time_percentage,
            'total_customers': len(self.customers),
            'total_service_time': total_service_time
        }