# Creates DeliveryTruck class

class DeliveryTruck:
    def __init__(self, storage, speed, haul, packages, mileage, location, departure):
        self.storage = storage
        self.speed = speed
        self.haul = haul
        self.packages = packages
        self.mileage = mileage
        self.location = location
        self.departure = departure
        self.time = departure

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.storage, self.speed, self.haul, self.packages,
                                               self.mileage, self.location, self.departure)
