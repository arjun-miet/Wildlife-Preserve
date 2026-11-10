
# COM-501: Wildlife Conservation Field Log
# Milestone 3: OOP and Custom Exception

# Custom exception class
class InvalidSightingError(Exception):
    pass


# Wildlife sighting class
class WildlifeSighting:

    # Class variable
    project_name = "Wildlife Conservation Field Log"

    # Constructor
    def __init__(self, species, zone, count, distance_m):

        # Validate animal count
        if count <= 0:
            raise InvalidSightingError(
                "Count must be greater than zero."
            )

        # Validate zone
        if zone not in ["Z1", "Z2", "Z3"]:
            raise InvalidSightingError("Invalid zone.")

        self.species = species
        self.zone = zone
        self.count = count
        self.distance_m = distance_m

    # Calculate monitoring score
    def monitoring_score(self):
        return self.count * 10 + self.distance_m // 100

    # Display sighting details
    def display_record(self):
        print("Species:", self.species)
        print("Zone:", self.zone)
        print("Count:", self.count)
        print("Distance:", self.distance_m, "metres")
        print("Monitoring Score:", self.monitoring_score())

    # String representation
    def __str__(self):
        return (
            self.species + " - " + self.zone
            + " - Count: " + str(self.count)
        )
