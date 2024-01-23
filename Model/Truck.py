class Truck:
    def __init__(self, capacity):
        self.capacity = capacity
        self.packages = []
        self.mileage = 0

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    def deliver_packages(self, distance):
        self.mileage += distance
        for package in self.packages:
            package['delivery_status'] = 'Delivered'
