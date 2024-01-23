class ChainingHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, package_id):
        return hash(package_id) % self.size

    def insert_package(self, package_id, delivery_address, delivery_deadline, delivery_city, delivery_zip, package_weight, delivery_status):
        index = self.hash_function(package_id)

        if self.table[index] is None:
            self.table[index] = []

        # Check if the package_id already exists, if yes, update the data
        for package in self.table[index]:
            if package['package_id'] == package_id:
                package.update({
                    'delivery_address': delivery_address,
                    'delivery_deadline': delivery_deadline,
                    'delivery_city': delivery_city,
                    'delivery_zip': delivery_zip,
                    'package_weight': package_weight,
                    'delivery_status': delivery_status,
                })
                return

        # If package_id doesn't exist, append a new package
        self.table[index].append({
            'package_id': package_id,
            'delivery_address': delivery_address,
            'delivery_deadline': delivery_deadline,
            'delivery_city': delivery_city,
            'delivery_zip': delivery_zip,
            'package_weight': package_weight,
            'delivery_status': delivery_status,
        })

    def lookup_package(self, package_id):
        index = self.hash_function(package_id)

        if self.table[index] is not None:
            for package in self.table[index]:
                if package['package_id'] == package_id:
                    return package

        return None