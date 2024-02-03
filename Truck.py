from ChainingHashTable import ChainingHashTable


# Class definition for a Truck
class Truck:
    # Constructor method to initialize a Truck object
    def __init__(self, capacity, speed, location, depart_time):
        self.capacity = capacity  # Maximum number of packages the truck can carry
        self.packages = []        # List to store packages loaded onto the truck
        self.milesTraveled = 0    # Total mileage traveled by the truck
        self.speed = speed         # Speed of the truck in miles per hour
        self.location = location   # Current location of the truck
        self.depart_time = depart_time  # Departure time of the truck
        self.current_time = depart_time  # Current time of the truck (initialized as the departure time)
        self.route = []            # List to store the route of the truck

    # String representation of the Truck object
    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.capacity, self.packages, self.milesTraveled, self.speed, self.location)

    # Method to load a package onto the truck
    def load_package(self, package):
        # Check if the truck has capacity for the package
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    # Method to calculate the total mileage traveled by the truck
    def calculate_total_mileage(self):
        return self.milesTraveled
