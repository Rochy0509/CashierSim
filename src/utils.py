import numpy as np

SERVICE_TIMES= [1, 2, 3, 4, 5, 6, 7]
SERVICE_PROBABILITIES = [0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05]


def generate_interarrival_time():
    return np.random.uniform(1, 10)

def generate_service_time():
    return np.random.choice(SERVICE_TIMES, p=SERVICE_PROBABILITIES)