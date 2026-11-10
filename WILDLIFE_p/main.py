
# COM-501: Wildlife Conservation Field Sighting and Patrol Log
# Final Application: Milestones 1 to 5

import os
import time

from wildlife import WildlifeSighting, InvalidSightingError

from wildlife_utils import (
    zone_summary,
    species_total,
    estimate_patrol_hours,
    average_count
)

# Species priority dictionary
priority = {
    "Snow Leopard": "HIGH",
    "Musk Deer": "HIGH",
    "Himalayan Monal": "MEDIUM",
    "Langur": "LOW"
}

records = []
unique_species = set()

# Create log directory
LOG_DIR = "field_logs"
LOG_FILE = os.path.join(LOG_DIR, "sightings.txt")

os.makedirs(LOG_DIR, exist_ok=True)

print("===== WILDLIFE CONSERVATION FIELD LOG =====")

# ---------------- MILESTONE 1 AND 2 ----------------

while True:

    observer = input("\nEnter observer name: ").strip().title()
    species = input("Enter species name (DONE to finish): ").strip().title()

    if species.upper() == "DONE":
        break

    zone = input("Enter zone (Z1/Z2/Z3): ").strip().upper()

    # Validate species
    if species not in priority:
        print("Rejected: Unknown species!")
        continue

    try:
        count = int(input("Enter animal count: "))
        duration = float(input("Enter duration (minutes): "))

        if duration <= 0:
            raise ValueError("Duration must be positive.")

        # ---------------- MILESTONE 3 ----------------

        distance = float(input("Enter distance (metres): "))

        sighting = WildlifeSighting(
            species, zone, count, distance
        )

        # Display data types
        print("Count type:", type(count))
        print("Distance type:", type(distance))

        # Calculate sightings per minute
        rate = count / duration

        # Convert distance to kilometres
        distance_km = distance / 1000

        # Generate four-character sighting code
        code = species[:2].upper() + zone[-2:].upper()

        print("Sightings per minute:", round(rate, 2))
        print("Distance in km:", distance_km)
        print("Sighting Code:", code)

        # Store record as dictionary
        record = {
            "observer": observer,
            "species": sighting.species,
            "zone": sighting.zone,
            "count": sighting.count,
            "duration": duration,
            "distance": sighting.distance_m,
            "priority": priority[species]
        }

        records.append(record)
        unique_species.add(species)

        print("Sighting recorded successfully!")

    except (ValueError, InvalidSightingError) as error:
        print("Rejected:", error)
        continue


# ---------------- MILESTONE 4 ----------------

start_time = time.time()

print("\n========== PATROL SUMMARY ==========")

print("Total Animals:",
      sum(r["count"] for r in records))

print("Unique Species:", len(unique_species))

# Zone-wise summary
summary = zone_summary(records)

print("\nZone-wise Sightings:")

for zone, total in summary.items():
    print(zone, ":", total)

# Species total
print("\nSnow Leopard Total:",
      species_total(records, "Snow Leopard"))

# Average animal count
counts = [r["count"] for r in records]

print("Average Animal Count:",
      round(average_count(*counts), 2))

# HIGH priority records
print("\nHIGH Priority Records:")

for record in records:
    if record["priority"] == "HIGH":
        print(record["species"], "-", record["count"])

# Patrol time calculation
total_distance = sum(r["distance"] for r in records) / 1000

print("\nTotal Patrol Distance:", total_distance, "km")

print("Estimated Patrol Hours:",
      estimate_patrol_hours(total_distance))

end_time = time.time()

print("Report Generation Time:",
      round(end_time - start_time, 4), "seconds")


# ---------------- MILESTONE 5 ----------------

# Append daily records to file
def save_field_logs():

    try:
        with open(LOG_FILE, "a") as file:

            for record in records:

                line = (
                    record["zone"] + "|" +
                    record["species"] + "|" +
                    str(record["count"]) + "|" +
                    str(record["distance"])
                )

                file.write(line + "\n")

        print("\nDaily records saved successfully.")

    except OSError as error:
        print("File writing error:", error)


# Read and validate saved records
def read_field_logs():

    print("\n========== SAVED FIELD LOGS ==========")

    try:
        with open(LOG_FILE, "r") as file:

            for line_number, line in enumerate(file, start=1):

                fields = line.strip().split("|")

                # Detect missing fields
                if len(fields) != 4 or any(
                    field.strip() == "" for field in fields
                ):
                    print("Line", line_number,
                          ": Missing fields. Record skipped.")
                    continue

                zone, species, count, distance = fields

                try:
                    count = int(count)
                    distance = float(distance)

                    if zone not in ["Z1", "Z2", "Z3"]:
                        raise ValueError("Invalid zone.")

                    if species not in priority:
                        raise ValueError("Unknown species.")

                    if count <= 0 or distance <= 0:
                        raise ValueError("Values must be positive.")

                    print(zone, "|", species, "|",
                          count, "|", distance)

                except ValueError as error:
                    print("Line", line_number,
                          ": Invalid record -", error)
                    continue

        # Display file metadata
        file_size = os.path.getsize(LOG_FILE)

        print("\nFile Size:", file_size, "bytes")

    except FileNotFoundError:
        print("Error: Field log file not found.")

    except OSError as error:
        print("File reading error:", error)


# Execute file operations
save_field_logs()
read_field_logs()

print("\n===== APPLICATION COMPLETED =====")
