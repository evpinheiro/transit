from vehicle_scheduling.data.itinerary import Itinerary
from vehicle_scheduling.data.scheduled_trip import ScheduledTrip


def import_trips(file_name):
    f = open(file_name)
    content = f.readlines()
    f.close()
    _itineraries = set()
    _trips = []
    for line in content:
        fields = line.split()
        itinerary = Itinerary(fields[0], fields[1], fields[2], fields[3], fields[4])
        _itineraries.add(itinerary)
        _trips.append(ScheduledTrip(fields[5], fields[6], itinerary))
    return _trips


if __name__ == '__main__':
    trips = import_trips("/home/eder/py-workspace/transit/vehicle_scheduling/trips_companyT_bussiness_day-07-10-2019")
    for trip in trips:
        print(trip)
