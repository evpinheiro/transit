from vehicle_scheduling.data_model.transport_network import Deadhead
from deal_with_time import hour_minute

class ScheduledEvent:

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self) -> str:
        return str(hour_minute(self.start_time)) + "-" + str(hour_minute(self.end_time))


class ScheduledTrip(ScheduledEvent):

    def __init__(self, start_time, end_time, itinerary):
        super().__init__(start_time, end_time)
        self.itinerary = itinerary

    def __str__(self) -> str:
        return super().__str__() + "/" + str(self.itinerary)


class ScheduledDeadheadTrip(ScheduledEvent):

    def __init__(self, deadhead: Deadhead, start_time: int, end_time: int):
        super().__init__(start_time, end_time)
        self.deadhead = deadhead

    def __str__(self) -> str:
        return super().__str__() + "/" + str(self.deadhead)


class ScheduledIdleTime(ScheduledEvent):

    def __init__(self, start_time: int, end_time: int):
        super().__init__(start_time, end_time)
