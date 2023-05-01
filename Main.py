# John Grahn
# Student ID #000961901
# C950 Data Structures and Algorithms 2
# Western Governors University Parcel Service Routing Program

import csv
import datetime
import DeliveryTruck
from builtins import ValueError
from NewHashTbl import NewHashTbl
from Package import Package

# Opens WGUPS Addresses File
with open("Data/WGUPS_Addresses.csv") as Addr_CSV:
    WGUPS_Addresses_CSV = csv.reader(Addr_CSV)
    WGUPS_Addresses_CSV = list(WGUPS_Addresses_CSV)

# Opens WGUPS Packages File
with open("Data/WGUPS_Packages.csv") as Pack_CSV:
    WGUPS_Packages_CSV = csv.reader(Pack_CSV)
    WGUPS_Packages_CSV = list(WGUPS_Packages_CSV)

# Opens WGUPS Distances File
with open("Data/WGUPS_Distances.csv") as Dist_CSV:
    WGUPS_Distances_CSV = csv.reader(Dist_CSV)
    WGUPS_Distances_CSV = list(WGUPS_Distances_CSV)


# Method creates Package object and loads data into hash table
def wgups_load_pack_data(file, pack_hash_tbl):
    with open(file) as pack_data:
        pack_cache = csv.reader(pack_data)
        for pack in pack_cache:
            pack_id = int(pack[0])
            pack_address = pack[1]
            pack_city = pack[2]
            pack_state = pack[3]
            pack_zip = pack[4]
            pack_deadline = pack[5]
            pack_weight = pack[6]
            pack_deliv_status = "Hub"

            wgups_pack = Package(pack_id, pack_address, pack_city, pack_state, pack_zip,
                                 pack_deadline, pack_weight, pack_deliv_status)

            pack_hash_tbl.insertion(pack_id, wgups_pack)


# Calculates distance between delivery addresses
def dist_calculation(loc_x, loc_y):
    dist = WGUPS_Distances_CSV[loc_x][loc_y]
    if dist == '':
        dist = WGUPS_Distances_CSV[loc_y][loc_x]

    return float(dist)


# Gets address from CSV data file
def address_lookup(addr):
    for line in WGUPS_Addresses_CSV:
        if addr in line[2]:
            return int(line[0])


# Create Delivery Trucks
wgups_delivery_truck_1 = DeliveryTruck.DeliveryTruck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
                                                     0.0, "4001 South 700 East", datetime.timedelta(hours=8))

wgups_delivery_truck_2 = DeliveryTruck.DeliveryTruck(16, 18, None,
                                                     [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
                                                     0.0,
                                                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

wgups_delivery_truck_3 = DeliveryTruck.DeliveryTruck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0,
                                                     "4001 South 700 East",
                                                     datetime.timedelta(hours=9, minutes=5))

# Creates hash table and populates it with Packages from WGUPS_Packages.CSV
pack_hash_tbl = NewHashTbl()
wgups_load_pack_data("Data/WGUPS_Packages.csv", pack_hash_tbl)


# Arranges packages in delivery trucks based on closest delivery addresses
def out_for_delivery(delivery_truck):
    undelivered = []
    for pack_id in delivery_truck.packages:
        pack = pack_hash_tbl.item_lookup(pack_id)
        undelivered.append(pack)

    delivery_truck.packages.clear()

    while len(undelivered) > 0:
        addr_following = 2000
        pack_following = None
        for pack in undelivered:
            if dist_calculation(address_lookup(delivery_truck.location),
                                address_lookup(pack.deliv_address)) <= addr_following:
                addr_following = dist_calculation(address_lookup(delivery_truck.location),
                                                  address_lookup(pack.deliv_address))
                pack_following = pack

        delivery_truck.packages.append(pack_following.pack_id)

        undelivered.remove(pack_following)

        delivery_truck.mileage += addr_following

        delivery_truck.location = pack_following.deliv_address

        delivery_truck.time += datetime.timedelta(hours=addr_following / 18)

        pack_following.deliv_time = delivery_truck.time

        pack_following.depart_time = delivery_truck.departure

# Begin out_for_delivery. Also prevents the 3rd delivery truck from leaving until 1 and 2 have finished
out_for_delivery(wgups_delivery_truck_1)
out_for_delivery(wgups_delivery_truck_2)
wgups_delivery_truck_3.departure = min(wgups_delivery_truck_1.time, wgups_delivery_truck_2.time)
out_for_delivery(wgups_delivery_truck_3)


class Main:
    # Interface for program. Text below will show upon launch
    print("Welcome to the Western Governors University Parcel Service")
    print("Total mileage traveled for the programmed route is: ",
          wgups_delivery_truck_1.mileage + wgups_delivery_truck_2.mileage + wgups_delivery_truck_3.mileage)
    # Message asking the user to type 'enter' in order to use functional part of program
    user_enter_prog = input("To enter the program type 'enter' (Any other input will cause program to close) ")
    if user_enter_prog == "enter":
        try:
            # Message asking user to enter a specific check time
            user_time_input = input(
                "Enter a time in the format, HH:MM:SS, to check the status of a package or packages ")
            (hours, minutes, seconds) = user_time_input.split(":")
            time_convert = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            # Second message asks user if they want to view only one package or all of them
            all_or_one_confirm = input(
                "To view delivery status of all packages type 'all'. To view a single package type 'one' ")
            # If the user types one, they are then asked for the ID of a package
            if all_or_one_confirm == "one":
                try:
                    one_pack_selection = input("Enter ID of package to check delivery status ")
                    pack = pack_hash_tbl.item_lookup(int(one_pack_selection))
                    pack.pack_update(time_convert)
                    print(str(pack))
                except ValueError:
                    print("Improper input. Exiting program")
                    exit()
            # If the user types all, all packages will be listed
            elif all_or_one_confirm == "all":
                try:
                    for pack_id in range(1, 41):
                        pack = pack_hash_tbl.item_lookup(pack_id)
                        pack.pack_update(time_convert)
                        print(str(pack))
                except ValueError:
                    print("Improper input. Exiting program")
                    exit()

            else:
                exit()
        except ValueError:
            print("Improper input. Exiting program")
            exit()
    elif input != "enter":
        print("Improper input. Exiting program")
        exit()
