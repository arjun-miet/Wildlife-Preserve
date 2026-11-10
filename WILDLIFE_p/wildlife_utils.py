
# COM-501: Wildlife Conservation Field Log
# Milestone 4: Utility Functions

import math

# Calculate zone-wise animal totals
def zone_summary(records):

    summary = {"Z1": 0, "Z2": 0, "Z3": 0}

    for record in records:
        zone = record["zone"]
        summary[zone] += record["count"]

    return summary


# Calculate total count of a species
def species_total(records, species):

    total = 0

    for record in records:
        if record["species"] == species:
            total += record["count"]

    return total


# Estimate patrol hours
def estimate_patrol_hours(distance_km, speed_kmph=4.0):

    hours = distance_km / speed_kmph

    return math.ceil(hours)


# Calculate average using variable arguments
def average_count(*counts):

    if len(counts) == 0:
        return 0

    return sum(counts) / len(counts)
