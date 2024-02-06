# Studen Id: 000733464
import csv
from datetime import timedelta
import datetime
from Package import Package
from ChainingHashTable import ChainingHashTable
from Truck import Truck

# File path to the CSV containing package data
package_csv = 'CSV_Data/Packages.csv'

# List to store Package objects
packages = []

# Create an instance of ChainingHashTable
chaining_hash_table = ChainingHashTable()

# Read and store addresses from the Addresses.csv file
with open("CSV_Data/Addresses.csv") as address_csv:
    addresses = csv.reader(address_csv)
    addresses = list(addresses)

# Function to get the ID of an address
def get_address_id(address):
    # Check if the address is the hub address
    if address == hub_address:
        return 0

    # Iterate through the list of addresses to find the matching address
    for index, row in enumerate(addresses):
        if address in row[0]:
            return index
    
    # Print a message if the address is not found
    print(f"Address not found: {address}")

# Read and store distances from the Distances.csv file
with open("CSV_Data/Distances.csv") as distance_csv:
    distances = csv.reader(distance_csv)
    distances = list(distances)

# Function to find the distance between two points
def find_distance(pointA, pointB):
    # Retrieve the distance from the distances matrix
    total_distance = distances[int(pointA)][int(pointB)]

    # If the distance is not available, try the reverse order
    if total_distance == '':
        total_distance = distances[int(pointB)][int(pointA)]
    
    return float(total_distance)

# Take HH:MM and convert to timedelta
def convert_time_str_to_timedelta(time_str):
    try:
        # Try parsing with '%H:%M' format
        hours, minutes = map(int, time_str.split(':'))
        delta = timedelta(hours=hours, minutes=minutes)
    except ValueError:
        # Handle invalid input (you can customize this part based on your requirements)
        print("Invalid time format. Please use HH:MM.")
        delta = timedelta()

    return delta

# Read data from the CSV file and populate the packages list and chaining hash table
with open(package_csv, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        # Create a Package object for each row in the CSV
        package = Package(
            id = int(''.join(char for char in row[0] if char.isdigit())),
            address=row[1],
            city=row[2],
            state=row[3],
            zipcode=row[4],
            deadline=row[5],
            weight=row[6],
            status="At Hub",
            notes=row[7]
        )

        # Append the Package object to the packages list
        packages.append(package)

        # Insert the Package into the chaining hash table using its id as the key
        chaining_hash_table.insert(package.id, package)

# Nearest Neighbor method
def greedy_algorithm(truck):

    while truck.packages:
        min_distance = 20
        nearest_location = None

        # Find the nearest location from the current truck location
        for package in truck.packages:
            distance = find_distance(get_address_id(truck.location), get_address_id(package.address))

            # Update the nearest location if the current distance is smaller
            if distance <= min_distance:
                min_distance = distance

                # Package is the nearest location
                nearest_location = package

        # Add the nearest location to the route
        truck.route.append(nearest_location.id)

        # Remove assigned packge from the unvisted set
        truck.packages.remove(nearest_location)

        # Add miles traveled
        truck.milesTraveled += min_distance

        # Add time it took for delivery
        truck.current_time += datetime.timedelta(hours=min_distance / 18)

        # Update truck location
        truck.location = nearest_location.address

        # Assign the departed time to the package
        nearest_location.depart_time = truck.depart_time

        # Assign the delivered time to the package
        nearest_location.delivered_time = truck.current_time

    return truck.route


# Function to load trucks
def load_trucks(trucks, packages):
    # Create new lists for packages with the earliest deadline, notes, and remaining packages
    packages_with_deadline = []
    packages_with_notes = []
    remaining_packages = []

    # Manually add some special case packages to lists
    package2 = chaining_hash_table.search(2)
    package4 = chaining_hash_table.search(4)
    package8 = chaining_hash_table.search(8)
    package9 = chaining_hash_table.search(9)
    package13 = chaining_hash_table.search(13)
    package15 = chaining_hash_table.search(15)
    package19 = chaining_hash_table.search(19)
    package20 = chaining_hash_table.search(20)
    package21 = chaining_hash_table.search(21)
    package24 = chaining_hash_table.search(24)

    # Add some packages to lists for different trucks
    packages_with_notes.append(package2)
    packages_with_notes.append(package4)
    packages_with_notes.append(package8)
    packages_with_notes.append(package21)
    packages_with_notes.append(package24)
    remaining_packages.append(package9)
    packages_with_deadline.append(package13)
    packages_with_deadline.append(package15)
    packages_with_deadline.append(package19)
    packages_with_deadline.append(package20)

    # Remove assigned packages from original list
    packages.remove(package2)
    packages.remove(package4)
    packages.remove(package8)
    packages.remove(package9)
    packages.remove(package13)
    packages.remove(package15)
    packages.remove(package19)
    packages.remove(package20)
    packages.remove(package21)
    packages.remove(package24)

    # Separate packages with the earliest deadline and notes
    for package in packages:
        if package.notes:
            packages_with_notes.append(package)
        else:
            packages_with_deadline.append(package)

    # Sort packages based on their deadline (earliest first) and take the top 16
    packages_with_deadline = sorted(packages_with_deadline, key=lambda x: x.deadline)[:14]

    # Find ids from lists
    packages_ids = set(package.id for package in packages)
    packages_with_notes_ids = set(package.id for package in packages_with_notes)
    packages_with_deadline_ids = set(package.id for package in packages_with_deadline)
    
    # Combine the sets
    combined_ids = packages_with_notes_ids.union(packages_with_deadline_ids)

    # Find remaining ids
    difference = packages_ids - combined_ids

    # Convert the result back to a list
    difference_list = list(difference)

    # Search hash table for each ID in difference_list
    for package_id in difference_list:
        package = chaining_hash_table.search(package_id)
        if package:
            remaining_packages.append(package)

    # Load the first truck with packages with the earliest deadline
    for package in packages_with_deadline:
        trucks[0].load_package(package)

    # Load the second truck with packages with non-null notes
    for package in packages_with_notes:
        trucks[1].load_package(package)

    # Load the third truck with all remaining packages
    for package in remaining_packages:
        trucks[2].load_package(package)

    # Assign routes using the greedy algorithm for each truck
    for truck in trucks:
        truck.route = greedy_algorithm(truck)
        

# Variable to hold WGU hub address(starting location)
hub_address = "4001 S 700 E"

# Intances of Truck
truck1 = Truck(16, 18, hub_address, datetime.timedelta(hours=8))
truck2 = Truck(16, 18, hub_address, datetime.timedelta(hours=9, minutes =5))
truck3 = Truck(16, 18, hub_address, datetime.timedelta(hours=10, minutes=20))

# Load the trucks with the Greedy Algorithm
load_trucks([truck1, truck2, truck3], packages)



class Main:
    # Display route and total mileage for each truck
    for i, truck in enumerate([truck1, truck2, truck3], start=1):
        print(f"Truck {i} Route:", truck.route)
        print(f"Total mileage for Truck {i}: {truck.milesTraveled} miles\n")

    # Calculate and display the total mileage for all trucks
    total_mileage = sum(truck.milesTraveled for truck in [truck1, truck2, truck3])
    print(f"Total mileage for all 3 trucks: {total_mileage} miles\n")

    # Main program loop
    while True:
        print("1. List All Packages")
        print("2. Get A Package Status At A Specific Time")
        print("3. Get All Package Statuses At A Specific Time")
        print("0. Exit Program")
        
        # User input for menu option
        user_text = input("Please type the number of the option you choose:  ")
        
        if user_text == "1":
            # Option to list all packages
            for i in range(1, 41):
                print(chaining_hash_table.search(i))
                print(str(package))

        elif user_text == "2":
            # Option to get the status of a specific package at a specific time
            user_package = input("Please Enter The Package ID:  ")
            package = chaining_hash_table.search(int(user_package))
            user_time = input("Please Specify a Time (Format HH:MM):  ")
            package_time = convert_time_str_to_timedelta(user_time)
            package.status_update(package_time) 

            print("Status of Package ID: ", package.id, " at ", user_time, " is: ", package.status, ", Delivered Time is: ", package.delivered_time)

        elif user_text == "3":
            # Option to get the status of all packages at a specific time
            user_time = input("Please Specify a Time (Format HH:MM):  ")
            package_time = convert_time_str_to_timedelta(user_time)
            for packageId in range(1, 41):
                package = chaining_hash_table.search(packageId)
                package.status_update(package_time)

                print("Status of Package ID: ", package.id, " at ", user_time, " is: ", package.status, ", Delivered Time is: ", package.delivered_time)

        elif user_text == "0":
            # Exit the program
            break

                