import json
import os

# Check if file exists to prevent path runtime errors
if not os.path.exists("students.json"):
    print("Error: students.json file not found!")
    exit(1)

with open("students.json", "r") as f:
    students = json.load(f)

# Data Analysis: Calculate metrics to print
topper = max(students, key=lambda x: x["marks"])
lowest = min(students, key=lambda x: x["marks"])
avg_marks = sum(s["marks"] for s in students) / len(students)

print("============== CIVICFLOW DATA INSIGHTS ==============")
print(f"Total Students Analysed : {len(students)}")
print(f"Top Performer           : {topper['name']} ({topper['marks']} Marks)")
print(f"Lowest Performer        : {lowest['name']} ({lowest['marks']} Marks)")
print(f"Class Average Metric    : {avg_marks:.2f}")
print("=====================================================")
