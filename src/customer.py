class Customer:

    def __init__(self, customer_id, arrival_time, interarrival_time):
        self.id = customer_id
        self.arrival_time = arrival_time
        self.interarrival_time = interarrival_time
        self.service_start_time = None
        self.service_time = None
        self.completion_time = None

    @property
    def waiting_time(self):
        return self.service_start_time - self.arrival_time

    @property
    def time_in_system(self):
        return self.completion_time - self.arrival_time
