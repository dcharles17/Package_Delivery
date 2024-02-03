import datetime


# Class definition for a Package
class Package:
    # Constructor method to initialize a Package object
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status, notes):
        self.id = id                     # Unique identifier for the package
        self.address = address           # Delivery address of the package
        self.city = city                 # City of the delivery address
        self.state = state               # State of the delivery address
        self.zipcode = zipcode           # ZIP code of the delivery address
        self.deadline = deadline         # Delivery deadline for the package
        self.weight = weight             # Weight of the package
        self.status = status             # Current status of the package
        self.notes = notes               # Additional notes for the package
        self.depart_time = None          # Departure time of the package from the hub
        self.delivered_time = None       # Delivery time of the package

    # String representation of the Package object
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state, self.zipcode, self.deadline, self.weight, self.status, self.notes, self.depart_time, self.delivered_time)

    # Method to update the status of the package based on the current time
    def status_update(self, current_time):
        if self.delivered_time < current_time:
            self.status = "Delivered"
        elif self.depart_time < current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"




        