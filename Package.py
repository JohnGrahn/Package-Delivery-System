# Creates Package class
class Package:
    def __init__(self, pack_id, deliv_address, city, state, deliv_zip, deadline, pack_weight, deliv_status):
        self.pack_id = pack_id
        self.deliv_address = deliv_address
        self.city = city
        self.state = state
        self.deliv_zip = deliv_zip
        self.deadline = deadline
        self.pack_weight = pack_weight
        self.deliv_status = deliv_status
        self.depart_time = None
        self.deliv_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.pack_id, self.deliv_address, self.city, self.state,
                                                       self.deliv_zip, self.deadline, self.pack_weight,
                                                       self.deliv_time, self.deliv_status)

    def pack_update(self, time_convert):
        if self.deliv_time < time_convert:
            self.deliv_status = "Arrived at destination and delivered"
        elif self.depart_time > time_convert:
            self.deliv_status = "On way to destination"
        else:
            self.deliv_status = "Package is at a hub"
