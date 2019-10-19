class ScheduledTrip:

    def __init__(self, start_time, end_time, itinerary):
        self.start_time = start_time
        self.end_time = end_time
        self.itinerary = itinerary

    def __str__(self) -> str:
        return str(self.start_time) + "-" + str(self.end_time) + "-" + str(self.itinerary)
